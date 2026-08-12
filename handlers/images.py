import json
import math
import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import IMAGE_TOOLS, usd_to_coins
from database import get_coins, add_coins, spend_coins, create_order, get_lang, has_unlimited
from keyboards import kb, back_btn, menu_btn, chunked
from i18n import t
from handlers.attachments import file_too_large

# ── Redis-backed atomic ref storage ──────────────────────────────────────────
# Using RPUSH (atomic) instead of FSM read-modify-write to avoid race
# conditions when album photos arrive simultaneously.

_REFS_TTL = 3600  # 1 h


def _ref_key(uid: int) -> str:
    return f"retainx:img_refs:{uid}"


async def _refs_clear(uid: int) -> None:
    redis_url = os.environ.get("REDIS_URL", "")
    if not redis_url:
        return
    import redis.asyncio as aioredis
    r = await aioredis.from_url(redis_url, decode_responses=True)
    await r.delete(_ref_key(uid))
    await r.aclose()


async def _refs_push(uid: int, ref: dict) -> int:
    """Atomically append one ref; returns new list length."""
    redis_url = os.environ.get("REDIS_URL", "")
    if not redis_url:
        return 0
    import redis.asyncio as aioredis
    r = await aioredis.from_url(redis_url, decode_responses=True)
    key = _ref_key(uid)
    count = await r.rpush(key, json.dumps(ref))
    await r.expire(key, _REFS_TTL)
    await r.aclose()
    return count


async def _refs_get(uid: int) -> list:
    redis_url = os.environ.get("REDIS_URL", "")
    if not redis_url:
        return []
    import redis.asyncio as aioredis
    r = await aioredis.from_url(redis_url, decode_responses=True)
    raw = await r.lrange(_ref_key(uid), 0, -1)
    await r.aclose()
    return [json.loads(x) for x in raw]

router = Router()

class ImageStates(StatesGroup):
    entering_prompt = State()
    collecting_refs = State()

# ── Category menu ─────────────────────────────────────────────
@router.callback_query(F.data == "cat_images")
async def images_menu(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.clear()
    lang = get_lang(cb.from_user.id)
    buttons = []
    for name, info in IMAGE_TOOLS.items():
        buttons.append([InlineKeyboardButton(
            text=f"{info['emoji']}  {name}",
            callback_data=f"img_{name}"
        )])
    buttons.append([menu_btn(lang)])
    await cb.message.edit_text(
        f"{t('img_menu_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('img_menu_select', lang)}",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

# ── Tool selected ─────────────────────────────────────────────
@router.callback_query(F.data.startswith("img_") & ~F.data.startswith("img_ar_") & ~F.data.startswith("img_q_") & ~F.data.startswith("img_confirm") & ~F.data.startswith("img_add") & ~F.data.startswith("img_ref") & ~F.data.startswith("img_to_") & ~F.data.startswith("img_edit"))
async def image_tool_selected(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    name = cb.data.replace("img_", "", 1)
    lang = get_lang(cb.from_user.id)
    tool = IMAGE_TOOLS.get(name)
    if not tool:
        await cb.answer("Tool not found")
        return
    await state.update_data(img_tool=name)

    # Build aspect ratio buttons
    ars = tool.get("aspect_ratios", [])
    if not ars:
        qualities = tool.get("quality", [])
        if qualities:
            # No AR but has quality tiers — show quality picker with pricing
            await state.update_data(img_ar="—")
            cbq = tool.get("coins_by_quality", {})
            coins_word = t("coins_word", lang)
            if cbq:
                price_line = "  " + "  /  ".join(f"{q}: <b>{c} {coins_word}</b>" for q, c in cbq.items())
            else:
                coins = tool.get("coins", 1)
                price_line = f"  <b>{coins} {coins_word}</b>  {t('img_per_gen', lang)}"
            q_buttons = [InlineKeyboardButton(text=q, callback_data=f"img_q_{q}") for q in qualities]
            rows = list(chunked(q_buttons, 3))
            rows.append([back_btn("cat_images", lang=lang), menu_btn(lang)])
            await cb.message.edit_text(
                f"{tool['emoji']}  <b>{name}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"  {tool['desc']}\n\n"
                f"  {t('img_price_label', lang)}   {price_line}\n\n"
                f"  {t('img_select_quality', lang)}",
                reply_markup=kb(*rows),
                parse_mode="HTML"
            )
            return
        # No AR and no quality — go straight to prompt/refs
        await state.update_data(img_ar="—", img_quality=None)
        await ask_prompt(cb, state, name, tool)
        return
    ar_buttons = [InlineKeyboardButton(text=ar, callback_data=f"img_ar_{ar}") for ar in ars]
    rows = list(chunked(ar_buttons, 4))

    # Pricing summary
    pricing = tool.get("pricing", {})
    coins_word = t("coins_word", lang)
    if "per_gen" in pricing:
        coins = tool.get("coins", usd_to_coins(pricing["per_gen"]))
        price_line = f"  <b>{coins} {coins_word}</b>  {t('img_per_gen', lang)}"
    elif "coins_by_quality" in tool:
        cbq = tool["coins_by_quality"]
        price_line = "  " + "  /  ".join(f"{q}: <b>{c} {coins_word}</b>" for q, c in cbq.items())
    else:
        price_line = ""

    text = (
        f"{tool['emoji']}  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {tool['desc']}\n\n"
        f"  {t('img_price_label', lang)}   {price_line}\n\n"
        f"  {t('img_select_ar', lang)}"
    )
    rows.append([back_btn("cat_images", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(text, reply_markup=kb(*rows), parse_mode="HTML")

# ── Aspect ratio selected ─────────────────────────────────────
@router.callback_query(F.data.startswith("img_ar_"))
async def image_ar_selected(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    ar = cb.data.replace("img_ar_", "")
    lang = get_lang(cb.from_user.id)
    await state.update_data(img_ar=ar)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    qualities = tool.get("quality", [])

    if not qualities:
        # No quality step — go to prompt
        await state.update_data(img_quality=None)
        await ask_prompt(cb, state, name, tool)
        return

    q_buttons = [InlineKeyboardButton(text=q, callback_data=f"img_q_{q}") for q in qualities]
    rows = list(chunked(q_buttons, 3))
    rows.append([back_btn(f"img_{name}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {ar}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('img_select_quality', lang)}",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

# ── Quality selected ──────────────────────────────────────────
@router.callback_query(F.data.startswith("img_q_"))
async def image_quality_selected(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    quality = cb.data.replace("img_q_", "")
    await state.update_data(img_quality=quality)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    await ask_prompt(cb, state, name, tool)

async def ask_prompt(cb: CallbackQuery, state: FSMContext, name: str, tool: dict):
    uid = cb.from_user.id
    lang = get_lang(uid)
    data = await state.get_data()
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    coins = _get_img_coins(tool, quality)
    user_coins = get_coins(uid)
    max_refs = tool.get("max_refs", 0)
    coins_word = t("coins_word", lang)
    unlimited = has_unlimited(uid)
    await state.update_data(img_coins=coins, img_refs=[])

    cost_lines = (
        f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n"
        f"  {t('img_balance_label', lang)}   {user_coins} {coins_word}\n"
    ) if not unlimited else ""

    requires_ref = tool.get("requires_ref", False)
    if max_refs > 0:
        ref_btn_text = t("img_btn_add_ref", lang, max=max_refs)
        ref_rows = [[InlineKeyboardButton(text=ref_btn_text, callback_data="img_add_refs")]]
        if not requires_ref:
            ref_rows.append([InlineKeyboardButton(text=t("img_btn_skip_prompt", lang), callback_data="img_to_prompt")])
        ref_rows.append([back_btn(f"img_{name}", lang=lang), menu_btn(lang)])
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
            f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
            f"{cost_lines}\n"
            f"{t('img_attach_optional', lang)}",
            reply_markup=kb(*ref_rows),
            parse_mode="HTML"
        )
    else:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
            f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
            f"{cost_lines}\n"
            f"{t('img_enter_prompt', lang)}",
            reply_markup=kb([back_btn(f"img_{name}", lang=lang), menu_btn(lang)]),
            parse_mode="HTML"
        )
        await state.set_state(ImageStates.entering_prompt)

def _get_img_coins(tool: dict, quality: str) -> int:
    if "coins_by_quality" in tool and quality:
        return tool["coins_by_quality"].get(quality, tool.get("coins", 1))
    return tool.get("coins", usd_to_coins(tool.get("pricing", {}).get("per_gen", 0.05)))

# ── Prompt entered ────────────────────────────────────────────
@router.message(ImageStates.entering_prompt)
async def image_prompt_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    uid  = msg.from_user.id
    data = await state.get_data()
    name = data.get("img_tool")
    ar = data.get("img_ar")
    quality = data.get("img_quality")
    coins = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)

    # Support captioned photos: user sends image(s) with text as caption
    prompt = msg.text or msg.caption

    if not prompt:
        # Photo with no caption — tell them to send text
        await msg.answer(
            t("img_enter_prompt", lang),
            reply_markup=kb(
                [InlineKeyboardButton(text=t("btn_done", lang), callback_data="img_refs_done")],
                [menu_btn(lang)],
            )
        )
        return

    # If photos are attached, save them into img_refs (append to any already collected)
    if msg.photo or msg.document:
        tool = IMAGE_TOOLS.get(name, {})
        max_refs = tool.get("max_refs", 0)
        if max_refs > 0:
            existing_refs = data.get("img_refs") or []
            file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
            ftype   = "photo" if msg.photo else "document"
            if len(existing_refs) < max_refs:
                existing_refs = list(existing_refs)
                idx = len(existing_refs) + 1
                existing_refs.append({"file_id": file_id, "type": ftype, "ref": f"img{idx}"})
                await state.update_data(img_refs=existing_refs)

    await state.update_data(img_prompt=prompt)

    unlimited = has_unlimited(uid)
    params_text = f"  {t('img_model_label', lang)}           <b>{name}</b>\n  {t('img_aspect_ratio_label', lang)}   {ar}\n"
    if quality:
        params_text += f"  {t('img_quality_label', lang)}           {quality}\n"
    if not unlimited:
        params_text += f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n"

    refs_line = ""
    all_refs = (await state.get_data()).get("img_refs") or []
    if all_refs:
        refs_line = f"\n{t('img_refs_attached', lang, count=len(all_refs))}"

    confirm_btn = t("img_btn_confirm_free", lang) if unlimited else t("img_btn_confirm", lang, coins=coins)
    await msg.answer(
        f"{t('img_order_summary_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{params_text}{refs_line}\n"
        f"  {t('img_prompt_label', lang)}\n<i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=confirm_btn, callback_data="img_confirm")],
            [InlineKeyboardButton(text=t("img_btn_edit_prompt", lang), callback_data=f"img_edit_prompt")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "img_edit_prompt")
async def img_edit_prompt(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        t("img_edit_prompt_prompt", lang),
        reply_markup=kb([menu_btn(lang)])
    )
    await state.set_state(ImageStates.entering_prompt)

# ── Confirm order ─────────────────────────────────────────────
@router.callback_query(F.data == "img_confirm")
async def image_confirm(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    coins = data.get("img_coins", 1)
    uid = cb.from_user.id
    name = data.get("img_tool")
    tid  = data.get("img_tid", name or "img")
    prompt = data.get("img_prompt")

    # Validate state is intact
    if not name or not prompt or coins == 0:
        await cb.answer(
            t("img_session_expired", lang),
            show_alert=True
        )
        await state.clear()
        return

    unlimited = has_unlimited(uid)
    if not unlimited:
        if not spend_coins(uid, coins):
            await cb.answer(t("img_insufficient_coins", lang), show_alert=True)
            return

    ar = data.get("img_ar")
    quality = data.get("img_quality")
    prompt = data.get("img_prompt")
    refs = data.get("img_refs", [])
    price_usd = round(coins * 0.05, 2)

    params = {"aspect_ratio": ar, "quality": quality, "prompt": prompt, "refs": refs if refs else None}
    try:
        oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, name, params, coins, price_usd)
    except Exception:
        if not unlimited:
            add_coins(uid, coins)
        await cb.answer(t("img_order_error", lang), show_alert=True)
        return

    await cb.answer()
    # Push to Redis queue for auto-generation
    await _push_to_queue(oid, uid, cb.from_user.username or "", tid, name, params, coins, price_usd)

    from handlers import spinner as sp
    displayed_coins = 0 if unlimited else coins
    base_text = (
        f"{t('img_order_placed_title', lang, oid=oid)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('img_model_row', lang, name=name)}\n"
        f"{t('img_coins_deducted', lang, coins=displayed_coins)}\n\n"
        f"{t('img_estimated_time', lang, minutes=2)}\n\n"
        f"{t('img_will_deliver', lang)}"
    )
    await cb.message.edit_text(base_text, reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
    sp.start(oid, cb.message.chat.id, cb.message.message_id, base_text, 2)
    await state.clear()
    try:
        await _notify_admin(cb, oid, name, params, coins, price_usd)
    except Exception:
        pass

async def _push_to_queue(oid: int, uid: int, username: str, tid: str, tool: str, params: dict, coins: int, usd: float):
    import logging, os, json
    log = logging.getLogger(__name__)
    try:
        import redis.asyncio as aioredis
        redis_url = os.environ.get("REDIS_URL", "")
        if not redis_url:
            log.error(f"[QUEUE] REDIS_URL not set — image order #{oid} dropped!")
            return
        r = await aioredis.from_url(redis_url, decode_responses=True)
        order_data = {
            "order_id": oid,
            "user_id": uid,
            "username": username,
            "tool_id": tid,
            "tool_name": tool,
            "params": params,
            "coins": coins,
            "usd": usd,
            "type": "image",
        }
        await r.rpush("retainx:orders", json.dumps(order_data))
        await r.aclose()
        log.info(f"[QUEUE] Image order #{oid} pushed (tool={tid})")
    except Exception as e:
        log.error(f"[QUEUE] Failed to push image order #{oid}: {e}")

async def _notify_admin(cb: CallbackQuery, oid: int, name: str, params: dict, coins: int, price_usd: float):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✓  Delivered", callback_data=f"delivered_{oid}"),
            InlineKeyboardButton(text="✕  Cancel", callback_data=f"cancel_order_{oid}"),
        ]])
        refs_line = f"\n  Refs        {len(params.get('refs') or [])} image(s)" if params.get("refs") else ""
        await bot.send_message(
            ADMIN_ID,
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"◈  <b>New Image Order #{oid}</b>\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            f"  User     @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
            f"  Model   <b>{name}</b>\n"
            f"  AR         {params.get('aspect_ratio')}\n"
            f"  Quality   {params.get('quality') or '—'}{refs_line}\n"
            f"  Coins    <b>{coins}◈</b>  (${price_usd})",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await bot.send_message(
            ADMIN_ID,
            f"📋 <b>Prompt #{oid}:</b>\n\n<code>{params.get('prompt','—')}</code>",
            parse_mode="HTML"
        )
        # Send reference images
        for i, ref in enumerate(params.get("refs") or [], 1):
            try:
                if ref["type"] == "photo":
                    await bot.send_photo(ADMIN_ID, ref["file_id"], caption=f"◈  Image Ref  @img{i}")
                else:
                    await bot.send_document(ADMIN_ID, ref["file_id"], caption=f"◈  Image Ref  @img{i}")
            except Exception:
                pass
    finally:
        await bot.session.close()

# ── Image Reference handlers ──────────────────────────────────
@router.callback_query(F.data == "img_add_refs")
async def img_add_refs(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    uid  = cb.from_user.id
    lang = get_lang(uid)
    data = await state.get_data()
    name = data.get("img_tool", "")
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    await _refs_clear(uid)  # reset for fresh collection
    await cb.message.edit_text(
        f"{t('img_ref_title', lang, count=0, max=max_refs)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('img_ref_instructions', lang, max=max_refs)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_done", lang), callback_data="img_refs_done")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.collecting_refs)

@router.message(ImageStates.collecting_refs, F.photo | F.document)
async def img_collect_ref(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    uid  = msg.from_user.id

    if file_too_large(msg):
        await msg.answer(t("err_file_too_large", lang))
        return

    data     = await state.get_data()
    name     = data.get("img_tool", "")
    tool     = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    # Check current count before pushing (slight race ok — capped hard at Done)
    current = await _refs_get(uid)
    if len(current) >= max_refs:
        await msg.answer(t("img_ref_max_alert", lang, max=max_refs))
        return

    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype   = "photo" if msg.photo else "document"

    # RPUSH is atomic — no race condition even with simultaneous album photos
    count = await _refs_push(uid, {"file_id": file_id, "type": ftype})

    follow_up = t("img_ref_send_more", lang) if count < max_refs else t("img_ref_max_reached", lang)
    await msg.answer(
        f"{t('img_ref_saved', lang, n=count, count=count, max=max_refs)}\n"
        f"{follow_up}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_done", lang), callback_data="img_refs_done")],
            [menu_btn(lang)],
        )
    )

@router.callback_query(F.data == "img_refs_done")
async def img_refs_done(cb: CallbackQuery, state: FSMContext):
    uid  = cb.from_user.id
    lang = get_lang(uid)
    data = await state.get_data()
    name = data.get("img_tool", "")
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    # Pull refs from Redis (atomic store), cap at max, save to FSM for the order
    refs = (await _refs_get(uid))[:max_refs]
    # Attach ref labels now that we know the final order
    for i, ref in enumerate(refs):
        ref["ref"] = f"img{i+1}"
    await _refs_clear(uid)
    await state.update_data(img_refs=refs)

    if tool.get("requires_ref") and not refs:
        await cb.answer(t("img_ref_required_alert", lang), show_alert=True)
        return
    await cb.answer()

    coins      = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)
    ar         = data.get("img_ar", "—")
    quality    = data.get("img_quality", "—")
    unlimited  = has_unlimited(uid)

    ref_line  = f"\n{t('img_refs_attached', lang, count=len(refs))}" if refs else ""
    cost_line = f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n\n" if not unlimited else "\n"

    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
        f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
        f"{ref_line}\n"
        f"{cost_line}"
        f"{t('img_enter_prompt', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)

@router.callback_query(F.data == "img_to_prompt")
async def img_to_prompt(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    name = data.get("img_tool", "")
    coins = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    unlimited = has_unlimited(cb.from_user.id)
    cost_line = f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n\n" if not unlimited else "\n"
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
        f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
        f"{cost_line}"
        f"{t('img_enter_prompt', lang)}",
        reply_markup=kb([back_btn(f"img_{name}", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)
