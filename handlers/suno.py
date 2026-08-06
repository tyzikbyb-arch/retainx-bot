import json
import logging
import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import (
    coins_to_usd, usd_to_coins,
    SUNO_MUSIC_MODELS, SUNO_VOCAL_TYPES, SUNO_LYRICS_PRICE,
)
from database import get_coins, add_coins, spend_coins, create_order, get_lang
from keyboards import kb, back_btn, menu_btn
from i18n import t
from handlers import spinner as sp

log = logging.getLogger(__name__)
router = Router()

# ─── FSM states ──────────────────────────────────────────────────────────────

class SunoStates(StatesGroup):
    entering_music_prompt  = State()
    entering_style         = State()
    entering_lyrics_prompt = State()
    waiting_for_audio      = State()
    entering_stem_name     = State()


# ─── Entry: Music category ────────────────────────────────────────────────────

@router.callback_query(F.data == "cat_music")
async def suno_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"🎵  <b>Suno Music</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_select_feature', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_generate_music",  lang), callback_data="suno_gen_music")],
            [InlineKeyboardButton(text=t("suno_btn_stem_separation", lang), callback_data="suno_stem_sep")],
            [InlineKeyboardButton(text=t("suno_btn_generate_lyrics", lang), callback_data="suno_gen_lyrics")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await cb.answer()


# ════════════════════════════════════════════════════════════════════════════
# Flow 1 — Generate Music
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "suno_gen_music")
async def suno_music_model_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    buttons = [
        InlineKeyboardButton(
            text=f"{cfg['emoji']}  {cfg['label']}   {cfg['coins']}◈",
            callback_data=f"suno_mm_{model}",
        )
        for model, cfg in SUNO_MUSIC_MODELS.items()
    ]
    rows = [[btn] for btn in buttons]
    rows.append([back_btn("cat_music", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"🎵  <b>Suno — {t('suno_btn_generate_music', lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_select_model', lang)}",
        reply_markup=kb(*rows),
        parse_mode="HTML",
    )
    await cb.answer()


@router.callback_query(F.data.startswith("suno_mm_"))
async def suno_music_model_selected(cb: CallbackQuery, state: FSMContext):
    model = cb.data.replace("suno_mm_", "", 1)
    if model not in SUNO_MUSIC_MODELS:
        await cb.answer("Unknown model")
        return
    lang = get_lang(cb.from_user.id)
    cfg  = SUNO_MUSIC_MODELS[model]
    await state.update_data(
        suno_model=model,
        suno_model_label=cfg["label"],
        suno_coins=cfg["coins"],
        suno_usd=cfg["usd"],
        suno_instrumental=False,
        suno_style="",
    )
    await cb.message.edit_text(
        f"🎵  <b>{cfg['label']}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_prompt', lang)}",
        reply_markup=kb(
            [back_btn("suno_gen_music", lang=lang), menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_music_prompt)
    await cb.answer()


@router.message(SunoStates.entering_music_prompt)
async def suno_music_prompt_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    prompt = (msg.text or "").strip()
    if not prompt:
        await msg.answer(t("suno_enter_prompt", lang))
        return
    await state.update_data(suno_prompt=prompt)
    data = await state.get_data()
    await _show_music_confirm(msg, state, data, lang)


async def _show_music_confirm(msg_or_cb, state: FSMContext, data: dict, lang: str):
    model_label  = data.get("suno_model_label", "—")
    coins        = data.get("suno_coins", 0)
    prompt       = data.get("suno_prompt", "—")
    style        = data.get("suno_style", "")
    instrumental = data.get("suno_instrumental", False)
    balance      = get_coins(msg_or_cb.from_user.id)
    coins_word   = t("coins_word", lang)

    style_line  = f"  {t('suno_style_label', lang)}   <i>{style}</i>\n" if style else ""
    instr_label = t("suno_instrumental_on", lang) if instrumental else t("suno_instrumental_off", lang)

    text = (
        f"🎵  <b>{t('suno_order_summary', lang)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_model_label', lang)}   <b>{model_label}</b>\n"
        f"{style_line}"
        f"  {t('suno_instrumental_label', lang)}   {instr_label}\n"
        f"  {t('suno_cost_label', lang)}   <b>{coins} {coins_word}</b>\n"
        f"  {t('suno_balance_label', lang)}   {balance} {coins_word}\n\n"
        f"  {t('suno_prompt_label', lang)}\n"
        f"  <i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    markup = kb(
        [InlineKeyboardButton(text=t("suno_btn_confirm", lang, coins=coins), callback_data="suno_music_confirm")],
        [InlineKeyboardButton(text=instr_label + "  ↕", callback_data="suno_toggle_instr")],
        [InlineKeyboardButton(text=t("suno_btn_add_style", lang), callback_data="suno_add_style")],
        [InlineKeyboardButton(text=t("suno_btn_edit_prompt", lang), callback_data="suno_edit_prompt")],
        [menu_btn(lang)],
    )
    if isinstance(msg_or_cb, Message):
        await msg_or_cb.answer(text, reply_markup=markup, parse_mode="HTML")
    else:
        await msg_or_cb.message.edit_text(text, reply_markup=markup, parse_mode="HTML")


@router.callback_query(F.data == "suno_toggle_instr")
async def suno_toggle_instrumental(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(suno_instrumental=not data.get("suno_instrumental", False))
    data = await state.get_data()
    lang = get_lang(cb.from_user.id)
    await _show_music_confirm(cb, state, data, lang)
    await cb.answer()


@router.callback_query(F.data == "suno_add_style")
async def suno_add_style(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"🎵  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_style', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_style)
    await cb.answer()


@router.message(SunoStates.entering_style)
async def suno_style_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    await state.update_data(suno_style=(msg.text or "").strip())
    data = await state.get_data()
    await _show_music_confirm(msg, state, data, lang)


@router.callback_query(F.data == "suno_edit_prompt")
async def suno_edit_prompt(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_prompt', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_music_prompt)
    await cb.answer()


@router.callback_query(F.data == "suno_music_confirm")
async def suno_music_confirm(cb: CallbackQuery, state: FSMContext):
    lang  = get_lang(cb.from_user.id)
    data  = await state.get_data()
    uid   = cb.from_user.id

    model        = data.get("suno_model", "V4")
    model_label  = data.get("suno_model_label", "Suno")
    price_coins  = data.get("suno_coins", 4)
    price_usd    = data.get("suno_usd", 0.20)
    prompt       = data.get("suno_prompt", "")
    style        = data.get("suno_style", "")
    instrumental = data.get("suno_instrumental", False)

    if not prompt:
        await cb.answer(t("suno_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
        await cb.answer(t("suno_insufficient_coins", lang), show_alert=True)
        return

    params = {
        "model":        model,
        "prompt":       prompt,
        "style":        style,
        "instrumental": instrumental,
        "custom_mode":  bool(style),
    }
    tool_name = f"Suno Music — {model_label}"
    try:
        oid = create_order(uid, cb.from_user.username or cb.from_user.first_name or "",
                           tool_name, params, price_coins, price_usd)
    except Exception:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    if not oid:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    wait_min = sp.wait_minutes(tool_name, "suno_music")
    base_text = (
        f"✓  <b>{t('suno_order_placed_music', lang, oid=oid)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_model_label', lang)}   <b>{model_label}</b>\n"
        f"  {t('suno_coins_deducted', lang, coins=price_coins)}\n\n"
        f"  {t('suno_estimated_delivery', lang, minutes=wait_min)}\n\n"
        f"  {t('suno_will_deliver_music', lang)}"
    )
    await cb.message.edit_text(base_text, reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
    sp.start(oid, cb.message.chat.id, cb.message.message_id, base_text, wait_min)
    await state.clear()
    await _push_order(oid, uid, "suno_music", tool_name, params, price_coins, price_usd,
                      username=cb.from_user.username or "")


# ════════════════════════════════════════════════════════════════════════════
# Flow 2 — Vocal Stem Separation
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "suno_stem_sep")
async def suno_stem_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(cb.from_user.id)
    buttons = []
    for vtype, cfg in SUNO_VOCAL_TYPES.items():
        label_key = f"label_{lang}" if lang in ("ru", "ar") else "label_en"
        label = cfg.get(label_key) or cfg["label_en"]
        buttons.append(InlineKeyboardButton(
            text=f"{label}   {cfg['coins']}◈",
            callback_data=f"suno_vt_{vtype}",
        ))
    rows = [[btn] for btn in buttons]
    rows.append([back_btn("cat_music", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"✂️  <b>{t('suno_btn_stem_separation', lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_select_vocal_type', lang)}",
        reply_markup=kb(*rows),
        parse_mode="HTML",
    )
    await cb.answer()


@router.callback_query(F.data.startswith("suno_vt_"))
async def suno_vocal_type_selected(cb: CallbackQuery, state: FSMContext):
    vtype = cb.data.replace("suno_vt_", "", 1)
    if vtype not in SUNO_VOCAL_TYPES:
        await cb.answer("Unknown type")
        return
    lang = get_lang(cb.from_user.id)
    cfg  = SUNO_VOCAL_TYPES[vtype]
    await state.update_data(
        suno_vocal_type=vtype,
        suno_coins=cfg["coins"],
        suno_usd=cfg["usd"],
        suno_stem_name="",
    )
    if vtype == "split_stem_advanced":
        await cb.message.edit_text(
            f"✂️  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_stem_name', lang)}",
            reply_markup=kb([back_btn("suno_stem_sep", lang=lang), menu_btn(lang)]),
            parse_mode="HTML",
        )
        await state.set_state(SunoStates.entering_stem_name)
    else:
        await cb.message.edit_text(
            f"✂️  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_upload_audio', lang)}",
            reply_markup=kb([back_btn("suno_stem_sep", lang=lang), menu_btn(lang)]),
            parse_mode="HTML",
        )
        await state.set_state(SunoStates.waiting_for_audio)
    await cb.answer()


@router.message(SunoStates.entering_stem_name)
async def suno_stem_name_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    await state.update_data(suno_stem_name=(msg.text or "").strip())
    await msg.answer(
        f"✂️  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_upload_audio', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.waiting_for_audio)


@router.message(SunoStates.waiting_for_audio)
async def suno_audio_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    uid  = msg.from_user.id

    audio = msg.audio or msg.document or msg.voice
    if not audio:
        await msg.answer(t("suno_send_audio_file", lang))
        return

    file_id = audio.file_id
    data    = await state.get_data()
    vtype   = data.get("suno_vocal_type", "separate_vocal")
    coins   = data.get("suno_coins", 10)
    usd     = data.get("suno_usd", 0.50)
    stem    = data.get("suno_stem_name", "")
    balance = get_coins(uid)
    coins_word = t("coins_word", lang)

    label_key = f"label_{lang}" if lang in ("ru", "ar") else "label_en"
    label = SUNO_VOCAL_TYPES[vtype].get(label_key) or SUNO_VOCAL_TYPES[vtype]["label_en"]
    stem_line = f"  {t('suno_stem_label', lang)}   <i>{stem}</i>\n" if stem else ""
    text = (
        f"✂️  <b>{t('suno_order_summary', lang)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_type_label', lang)}   <b>{label}</b>\n"
        f"{stem_line}"
        f"  {t('suno_cost_label', lang)}   <b>{coins} {coins_word}</b>\n"
        f"  {t('suno_balance_label', lang)}   {balance} {coins_word}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    await state.update_data(suno_audio_file_id=file_id)
    await msg.answer(
        text,
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_confirm", lang, coins=coins), callback_data="suno_vocal_confirm")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "suno_vocal_confirm")
async def suno_vocal_confirm(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    uid  = cb.from_user.id

    vtype      = data.get("suno_vocal_type", "separate_vocal")
    price_coins = data.get("suno_coins", 10)
    price_usd   = data.get("suno_usd", 0.50)
    file_id    = data.get("suno_audio_file_id")
    stem_name  = data.get("suno_stem_name", "")

    if not file_id:
        await cb.answer(t("suno_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
        await cb.answer(t("suno_insufficient_coins", lang), show_alert=True)
        return

    label_key = f"label_{lang}" if lang in ("ru", "ar") else "label_en"
    label = SUNO_VOCAL_TYPES[vtype].get(label_key) or SUNO_VOCAL_TYPES[vtype]["label_en"]
    # Pass file_id; worker will upload it to kie.ai CDN via _upload_tg_file_to_kie
    params = {"type": vtype, "file_id": file_id}
    if stem_name:
        params["stem_name"] = stem_name

    tool_name = f"Suno Stem — {label}"
    try:
        oid = create_order(uid, cb.from_user.username or cb.from_user.first_name or "",
                           tool_name, params, price_coins, price_usd)
    except Exception:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    if not oid:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    wait_min  = sp.wait_minutes(tool_name, "suno_vocal")
    base_text = (
        f"✓  <b>{t('suno_order_placed_vocal', lang, oid=oid)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_type_label', lang)}   <b>{label}</b>\n"
        f"  {t('suno_coins_deducted', lang, coins=price_coins)}\n\n"
        f"  {t('suno_estimated_delivery', lang, minutes=wait_min)}\n\n"
        f"  {t('suno_will_deliver_vocal', lang)}"
    )
    await cb.message.edit_text(base_text, reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
    sp.start(oid, cb.message.chat.id, cb.message.message_id, base_text, wait_min)
    await state.clear()
    await _push_order(oid, uid, "suno_vocal", tool_name, params, price_coins, price_usd,
                      username=cb.from_user.username or "")


# ════════════════════════════════════════════════════════════════════════════
# Flow 3 — Generate Lyrics
# ════════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "suno_gen_lyrics")
async def suno_lyrics_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(cb.from_user.id)
    coins = SUNO_LYRICS_PRICE["coins"]
    await cb.message.edit_text(
        f"📝  <b>{t('suno_btn_generate_lyrics', lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_lyrics_prompt', lang, coins=coins)}",
        reply_markup=kb([back_btn("cat_music", lang=lang), menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_lyrics_prompt)
    await cb.answer()


@router.message(SunoStates.entering_lyrics_prompt)
async def suno_lyrics_prompt_received(msg: Message, state: FSMContext):
    lang  = get_lang(msg.from_user.id)
    prompt = (msg.text or "").strip()
    if not prompt:
        await msg.answer(t("suno_enter_lyrics_prompt", lang, coins=SUNO_LYRICS_PRICE["coins"]))
        return

    await state.update_data(suno_lyrics_prompt=prompt)
    price_coins = SUNO_LYRICS_PRICE["coins"]
    balance     = get_coins(msg.from_user.id)
    coins_word  = t("coins_word", lang)

    await msg.answer(
        f"📝  <b>{t('suno_order_summary', lang)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_cost_label', lang)}   <b>{price_coins} {coins_word}</b>\n"
        f"  {t('suno_balance_label', lang)}   {balance} {coins_word}\n\n"
        f"  {t('suno_prompt_label', lang)}\n"
        f"  <i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_confirm", lang, coins=price_coins), callback_data="suno_lyrics_confirm")],
            [InlineKeyboardButton(text=t("suno_btn_edit_prompt", lang), callback_data="suno_edit_lyrics_prompt")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "suno_edit_lyrics_prompt")
async def suno_edit_lyrics_prompt(cb: CallbackQuery, state: FSMContext):
    lang  = get_lang(cb.from_user.id)
    coins = SUNO_LYRICS_PRICE["coins"]
    await cb.message.edit_text(
        f"📝  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_lyrics_prompt', lang, coins=coins)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_lyrics_prompt)
    await cb.answer()


@router.callback_query(F.data == "suno_lyrics_confirm")
async def suno_lyrics_confirm(cb: CallbackQuery, state: FSMContext):
    lang  = get_lang(cb.from_user.id)
    data  = await state.get_data()
    uid   = cb.from_user.id

    prompt      = data.get("suno_lyrics_prompt", "")
    price_coins = SUNO_LYRICS_PRICE["coins"]
    price_usd   = SUNO_LYRICS_PRICE["usd"]

    if not prompt:
        await cb.answer(t("suno_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
        await cb.answer(t("suno_insufficient_coins", lang), show_alert=True)
        return

    params    = {"prompt": prompt}
    tool_name = "Suno Lyrics"
    try:
        oid = create_order(uid, cb.from_user.username or cb.from_user.first_name or "",
                           tool_name, params, price_coins, price_usd)
    except Exception:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    if not oid:
        add_coins(uid, price_coins)
        await state.clear()
        await cb.message.edit_text(t("vid_order_error", lang), reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
        return

    wait_min  = sp.wait_minutes(tool_name, "suno_lyrics")
    base_text = (
        f"✓  <b>{t('suno_order_placed_lyrics', lang, oid=oid)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_coins_deducted', lang, coins=price_coins)}\n\n"
        f"  {t('suno_estimated_delivery', lang, minutes=wait_min)}\n\n"
        f"  {t('suno_will_deliver_lyrics', lang)}"
    )
    await cb.message.edit_text(base_text, reply_markup=kb([menu_btn(lang)]), parse_mode="HTML")
    sp.start(oid, cb.message.chat.id, cb.message.message_id, base_text, wait_min)
    await state.clear()
    await _push_order(oid, uid, "suno_lyrics", tool_name, params, price_coins, price_usd,
                      username=cb.from_user.username or "")


# ─── Queue helper ─────────────────────────────────────────────────────────────

async def _push_order(oid, uid, tool_id, tool_name, params, coins, usd, username=""):
    try:
        import redis.asyncio as aioredis
        redis_url = os.environ.get("REDIS_URL", "")
        if not redis_url:
            return
        r = await aioredis.from_url(redis_url, decode_responses=True)
        order_data = {
            "order_id":  oid,
            "user_id":   uid,
            "tool_id":   tool_id,
            "tool_name": tool_name,
            "type":      tool_id,
            "params":    params,
            "coins":     coins,
            "usd":       usd,
            "username":  username,
        }
        await r.rpush("retainx:orders", json.dumps(order_data))
        log.info(f"[QUEUE] Suno order #{oid} ({tool_id}) pushed")
        from worker_monitor import check_workers_alive, send_no_workers_alert
        if not await check_workers_alive(redis_url):
            await send_no_workers_alert(
                order_id=oid, user_id=uid, username=username,
                tool=tool_name, params=params, coins=coins, redis_url=redis_url,
            )
        await r.aclose()
    except Exception as e:
        log.error(f"[QUEUE] Failed to push suno order #{oid}: {e}")
