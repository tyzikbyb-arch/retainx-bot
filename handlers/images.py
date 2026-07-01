from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import IMAGE_TOOLS, usd_to_coins
from database import get_coins, spend_coins, create_order, get_lang
from keyboards import kb, back_btn, menu_btn, chunked
from i18n import t
from handlers.attachments import file_too_large
from handlers import spinner as sp
import math

router = Router()

class ImageStates(StatesGroup):
    entering_prompt = State()
    collecting_refs = State()

# ── Category menu ─────────────────────────────────────────────
@router.callback_query(F.data == "cat_images")
async def images_menu(cb: CallbackQuery, state: FSMContext):
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
    name = cb.data.replace("img_", "", 1)
    lang = get_lang(cb.from_user.id)
    tool = IMAGE_TOOLS.get(name)
    if not tool:
        await cb.answer("Tool not found")
        return
    await state.update_data(img_tool=name)

    # Build aspect ratio buttons
    ars = tool.get("aspect_ratios", [])
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
    ar = cb.data.replace("img_ar_", "")
    lang = get_lang(cb.from_user.id)
    await state.update_data(img_ar=ar)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    qualities = tool.get("quality", [])

    if not qualities:
        # No quality step -- go to prompt
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
    quality = cb.data.replace("img_q_", "")
    await state.update_data(img_quality=quality)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    await ask_prompt(cb, state, name, tool)

async def ask_prompt(cb: CallbackQuery, state: FSMContext, name: str, tool: dict):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    coins = _get_img_coins(tool, quality)
    user_coins = get_coins(cb.from_user.id)
    max_refs = tool.get("max_refs", 0)
    coins_word = t("coins_word", lang)
    await state.update_data(img_coins=coins, img_refs=[])

    if max_refs > 0:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
            f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
            f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n"
            f"  {t('img_balance_label', lang)}   {user_coins} {coins_word}\n\n"
            f"{t('img_attach_optional', lang)}",
            reply_markup=kb(
                [InlineKeyboardButton(text=t("img_btn_add_ref", lang, max=max_refs), callback_data="img_add_refs")],
                [InlineKeyboardButton(text=t("img_btn_skip_prompt", lang), callback_data="img_to_prompt")],
                [back_btn(f"img_{name}", lang=lang), menu_btn(lang)],
            ),
            parse_mode="HTML"
        )
    else:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
            f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
            f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n"
            f"  {t('img_balance_label', lang)}   {user_coins} {coins_word}\n\n"
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
    data = await state.get_data()
    name = data.get("img_tool")
    ar = data.get("img_ar")
    quality = data.get("img_quality")
    coins = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)
    prompt = msg.text

    await state.update_data(img_prompt=prompt)

    params_text = f"  {t('img_model_label', lang)}           <b>{name}</b>\n  {t('img_aspect_ratio_label', lang)}   {ar}\n"
    if quality:
        params_text += f"  {t('img_quality_label', lang)}           {quality}\n"
    params_text += f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n"

    await msg.answer(
        f"{t('img_order_summary_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{params_text}\n"
        f"  {t('img_prompt_label', lang)}\n<i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("img_btn_confirm", lang, coins=coins), callback_data="img_confirm")],
            [InlineKeyboardButton(text=t("img_btn_edit_prompt", lang), callback_data=f"img_edit_prompt")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "img_edit_prompt")
async def img_edit_prompt(cb: CallbackQuery, state: FSMContext):
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

    if not spend_coins(uid, coins):
        await cb.answer(t("img_insufficient_coins", lang), show_alert=True)
        return
    ar = data.get("img_ar")
    quality = data.get("img_quality")
    prompt = data.get("img_prompt")
    refs = data.get("img_refs", [])
    price_usd = round(coins * 0.05, 2)

    params = {"aspect_ratio": ar, "quality": quality, "prompt": prompt, "refs": refs if refs else None}
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, name, params, coins, price_usd)

    # Push to Redis queue for auto-generation
    await _push_to_queue(oid, uid, tid, name, params, coins, price_usd, username=cb.from_user.username or cb.from_user.first_name or "")

    await _notify_admin(cb, oid, name, params, coins, price_usd)

    wait_min = sp.wait_minutes(name, "image")
    base_text = (
        f"{t('img_order_placed_title', lang, oid=oid)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('img_model_row', lang, name=name)}\n"
        f"{t('img_coins_deducted', lang, coins=coins)}\n\n"
        f"{t('img_estimated_time', lang, minutes=wait_min)}\n\n"
        f"{t('img_will_deliver', lang)}"
    )
    await cb.message.edit_text(base_text, reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
    sp.start(oid, cb.message.chat.id, cb.message.message_id, base_text, wait_min)
    await state.clear()

async def _push_to_queue(oid: int, uid: int, tid: str, tool: str, params: dict, coins: int, usd: float, username: str = ""):
    import logging, os, json
    log = logging.getLogger(__name__)
    try:
        import redis.asyncio as aioredis
        redis_url = os.environ.get("REDIS_URL", "")
        if not redis_url:
            return
        r = await aioredis.from_url(redis_url, decode_responses=True)
        order_data = {
            "order_id": oid,
            "user_id": uid,
            "tool_id": tid,
            "tool_name": tool,
            "params": params,
            "coins": coins,
            "usd": usd,
            "type": "image",
        }
        await r.rpush("retainx:orders", json.dumps(order_data))
        log.info(f"[QUEUE] Image order #{oid} pushed to queue")
        from worker_monitor import check_workers_alive, send_no_workers_alert
        if not await check_workers_alive(redis_url):
            log.warning(f"[QUEUE] No live workers -- sending manual alert for image order #{oid}")
            await send_no_workers_alert(
                order_id=oid, user_id=uid, username=username,
                tool=tool, params=params, coins=coins, redis_url=redis_url,
            )
        await r.aclose()
    except Exception as e:
        log.error(f"[QUEUE] Failed to push image order #{oid}: {e}")

async def _notify_admin(cb: CallbackQuery, oid: int, name: str, params: dict, coins: int, price_usd: float):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
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

# ── Image Reference handlers ──────────────────────────────────
@router.callback_query(F.data == "img_add_refs")
async def img_add_refs(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    from config import IMAGE_TOOLS
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    await cb.message.edit_text(
        f"{t('img_ref_title', lang, count=len(refs), max=max_refs)}\n"
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
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    from config import IMAGE_TOOLS
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    if len(refs) >= max_refs:
        await msg.answer(t("img_ref_max_alert", lang, max=max_refs))
        return
    if file_too_large(msg):
        await msg.answer(t("err_file_too_large", lang))
        return

    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    refs.append({"file_id": file_id, "type": ftype, "ref": f"img{len(refs)+1}"})
    await state.update_data(img_refs=refs)
    follow_up = t("img_ref_send_more", lang) if len(refs) < max_refs else t("img_ref_max_reached", lang)
    await msg.answer(
        f"{t('img_ref_saved', lang, n=len(refs), count=len(refs), max=max_refs)}\n"
        f"{follow_up}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_done", lang), callback_data="img_refs_done")],
            [menu_btn(lang)],
        )
    )

@router.callback_query(F.data == "img_refs_done")
async def img_refs_done(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    coins = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")

    ref_line = f"\n{t('img_refs_attached', lang, count=len(refs))}" if refs else ""

    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
        f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
        f"{ref_line}\n"
        f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n\n"
        f"{t('img_enter_prompt', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)

@router.callback_query(F.data == "img_to_prompt")
async def img_to_prompt(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    name = data.get("img_tool", "")
    coins = data.get("img_coins", 1)
    coins_word = t("coins_word", lang)
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('img_aspect_ratio_label', lang)}   {ar}\n"
        f"  {t('img_quality_label', lang)}           {quality or '—'}\n"
        f"  {t('img_cost_label', lang)}               <b>{coins} {coins_word}</b>\n\n"
        f"{t('img_enter_prompt', lang)}",
        reply_markup=kb([back_btn(f"img_{name}", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)
