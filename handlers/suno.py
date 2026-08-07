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

DURATION_PRESETS = [20, 30, 60, 90, 120, 180, 240]
VOICE_OPTIONS    = ["auto", "male", "female"]


# ─── FSM states ──────────────────────────────────────────────────────────────

class SunoStates(StatesGroup):
    entering_music_prompt  = State()
    entering_style         = State()
    entering_title         = State()
    entering_custom_lyrics = State()
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
        suno_title="",
        suno_voice="auto",
        suno_duration=30,
        suno_custom_mode=False,
        suno_style_edit_mode=False,
    )
    await cb.message.edit_text(
        f"🎵  <b>{cfg['label']}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_select_mode', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_mode_normal", lang), callback_data="suno_mode_normal")],
            [InlineKeyboardButton(text=t("suno_btn_mode_custom", lang), callback_data="suno_mode_custom")],
            [back_btn("suno_gen_music", lang=lang), menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await cb.answer()


# ── Normal mode ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "suno_mode_normal")
async def suno_mode_normal(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    await state.update_data(suno_custom_mode=False)
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_normal_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_prompt', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_music_prompt)
    await cb.answer()


@router.message(SunoStates.entering_music_prompt)
async def suno_music_prompt_received(msg: Message, state: FSMContext):
    lang   = get_lang(msg.from_user.id)
    prompt = (msg.text or "").strip()
    if not prompt:
        await msg.answer(t("suno_enter_prompt", lang))
        return
    await state.update_data(suno_prompt=prompt)
    data = await state.get_data()
    await _show_music_confirm(msg, state, data, lang)


# ── Custom mode ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "suno_mode_custom")
async def suno_mode_custom(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    await state.update_data(suno_custom_mode=True)
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_title', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_skip", lang), callback_data="suno_skip_title")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_title)
    await cb.answer()


@router.message(SunoStates.entering_title)
async def suno_title_received(msg: Message, state: FSMContext):
    lang  = get_lang(msg.from_user.id)
    title = (msg.text or "").strip()
    await state.update_data(suno_title=title)
    data = await state.get_data()
    await msg.answer(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_style', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_skip", lang), callback_data="suno_skip_style")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_style)


@router.callback_query(F.data == "suno_skip_title")
async def suno_skip_title(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await state.update_data(suno_title="")
    data = await state.get_data()
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_style', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("suno_btn_skip", lang), callback_data="suno_skip_style")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_style)
    await cb.answer()


@router.callback_query(F.data == "suno_skip_style")
async def suno_skip_style(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await state.update_data(suno_style="")
    data = await state.get_data()
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_custom_lyrics', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_custom_lyrics)
    await cb.answer()


@router.message(SunoStates.entering_style)
async def suno_style_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    await state.update_data(suno_style=(msg.text or "").strip())
    data = await state.get_data()
    if data.get("suno_custom_mode") and not data.get("suno_style_edit_mode"):
        # Custom mode initial flow: proceed to lyrics input
        await msg.answer(
            f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_custom_lyrics', lang)}",
            reply_markup=kb([menu_btn(lang)]),
            parse_mode="HTML",
        )
        await state.set_state(SunoStates.entering_custom_lyrics)
    else:
        # Normal mode or editing style from confirm: return to confirm
        await state.update_data(suno_style_edit_mode=False)
        data = await state.get_data()
        await _show_music_confirm(msg, state, data, lang)


@router.message(SunoStates.entering_custom_lyrics)
async def suno_custom_lyrics_received(msg: Message, state: FSMContext):
    lang   = get_lang(msg.from_user.id)
    lyrics = (msg.text or "").strip()
    if not lyrics:
        await msg.answer(t("suno_enter_custom_lyrics", lang))
        return
    await state.update_data(suno_prompt=lyrics)
    data = await state.get_data()
    await _show_music_confirm(msg, state, data, lang)


# ── Shared confirm screen ─────────────────────────────────────────────────────

async def _show_music_confirm(msg_or_cb, state: FSMContext, data: dict, lang: str):
    model_label  = data.get("suno_model_label", "—")
    model        = data.get("suno_model", "")
    coins        = data.get("suno_coins", 0)
    prompt       = data.get("suno_prompt", "—")
    style        = data.get("suno_style", "")
    title        = data.get("suno_title", "")
    instrumental = data.get("suno_instrumental", False)
    custom_mode  = data.get("suno_custom_mode", False)
    voice        = data.get("suno_voice", "auto")
    duration     = data.get("suno_duration", 30)
    balance      = get_coins(msg_or_cb.from_user.id)
    coins_word   = t("coins_word", lang)

    mode_label  = t("suno_mode_custom_label", lang) if custom_mode else t("suno_mode_normal_label", lang)
    instr_label = t("suno_instrumental_on", lang) if instrumental else t("suno_instrumental_off", lang)

    voice_map = {
        "auto":   t("suno_voice_auto", lang),
        "male":   t("suno_voice_male", lang),
        "female": t("suno_voice_female", lang),
    }
    voice_label = voice_map.get(voice, voice_map["auto"])

    prompt_display = prompt[:200] + ("…" if len(prompt) > 200 else "")

    if custom_mode:
        title_line = f"  {t('suno_title_label', lang)}   <i>{title}</i>\n" if title else ""
        style_line = f"  {t('suno_style_label', lang)}   <i>{style}</i>\n" if style else ""
        content_block = (
            f"{title_line}"
            f"{style_line}"
            f"\n  {t('suno_lyrics_label', lang)}\n"
            f"  <i>{prompt_display}</i>\n\n"
        )
    else:
        style_line = f"  {t('suno_style_label', lang)}   <i>{style}</i>\n" if style else ""
        content_block = (
            f"{style_line}"
            f"\n  {t('suno_prompt_label', lang)}\n"
            f"  <i>{prompt_display}</i>\n\n"
        )

    text = (
        f"🎵  <b>{t('suno_order_summary', lang)}</b>  ·  {mode_label}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {t('suno_model_label', lang)}   <b>{model_label}</b>\n"
        f"  {t('suno_cost_label', lang)}   <b>{coins} {coins_word}</b>\n"
        f"  {t('suno_balance_label', lang)}   {balance} {coins_word}\n"
        f"{content_block}"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    rows = [
        [InlineKeyboardButton(text=t("suno_btn_confirm", lang, coins=coins), callback_data="suno_music_confirm")],
        [InlineKeyboardButton(text=f"{voice_label}  ↕", callback_data="suno_toggle_voice")],
        [InlineKeyboardButton(text=f"{instr_label}  ↕", callback_data="suno_toggle_instr")],
    ]
    if model == "V5_5":
        rows.append([InlineKeyboardButton(
            text=f"⏱  {duration} {t('suno_sec', lang)}  ↕",
            callback_data="suno_toggle_duration",
        )])

    if custom_mode:
        rows.append([
            InlineKeyboardButton(text=t("suno_btn_edit_lyrics", lang), callback_data="suno_edit_lyrics"),
            InlineKeyboardButton(text=t("suno_btn_edit_style", lang),  callback_data="suno_edit_style_custom"),
        ])
    else:
        style_btn = t("suno_btn_edit_style", lang) if style else t("suno_btn_add_style", lang)
        rows.append([
            InlineKeyboardButton(text=t("suno_btn_edit_prompt", lang), callback_data="suno_edit_prompt"),
            InlineKeyboardButton(text=style_btn,                       callback_data="suno_add_style"),
        ])

    rows.append([menu_btn(lang)])
    markup = kb(*rows)

    if isinstance(msg_or_cb, Message):
        await msg_or_cb.answer(text, reply_markup=markup, parse_mode="HTML")
    else:
        await msg_or_cb.message.edit_text(text, reply_markup=markup, parse_mode="HTML")


# ── Toggle handlers ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "suno_toggle_instr")
async def suno_toggle_instrumental(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(suno_instrumental=not data.get("suno_instrumental", False))
    data = await state.get_data()
    lang = get_lang(cb.from_user.id)
    await _show_music_confirm(cb, state, data, lang)
    await cb.answer()


@router.callback_query(F.data == "suno_toggle_voice")
async def suno_toggle_voice(cb: CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    voice = data.get("suno_voice", "auto")
    idx   = VOICE_OPTIONS.index(voice) if voice in VOICE_OPTIONS else 0
    await state.update_data(suno_voice=VOICE_OPTIONS[(idx + 1) % len(VOICE_OPTIONS)])
    data  = await state.get_data()
    lang  = get_lang(cb.from_user.id)
    await _show_music_confirm(cb, state, data, lang)
    await cb.answer()


@router.callback_query(F.data == "suno_toggle_duration")
async def suno_toggle_duration(cb: CallbackQuery, state: FSMContext):
    data     = await state.get_data()
    duration = data.get("suno_duration", 30)
    idx      = DURATION_PRESETS.index(duration) if duration in DURATION_PRESETS else 1
    await state.update_data(suno_duration=DURATION_PRESETS[(idx + 1) % len(DURATION_PRESETS)])
    data = await state.get_data()
    lang = get_lang(cb.from_user.id)
    await _show_music_confirm(cb, state, data, lang)
    await cb.answer()


# ── Edit handlers ─────────────────────────────────────────────────────────────

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


@router.callback_query(F.data == "suno_edit_lyrics")
async def suno_edit_lyrics(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    await cb.message.edit_text(
        f"🎵  <b>{data.get('suno_model_label', 'Suno')}</b>  ·  {t('suno_mode_custom_label', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_custom_lyrics', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_custom_lyrics)
    await cb.answer()


@router.callback_query(F.data == "suno_edit_style_custom")
async def suno_edit_style_custom(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await state.update_data(suno_style_edit_mode=True)
    await cb.message.edit_text(
        f"🎵  <b>Suno</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('suno_enter_style', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML",
    )
    await state.set_state(SunoStates.entering_style)
    await cb.answer()


# ── Confirm & submit ──────────────────────────────────────────────────────────

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
    title        = data.get("suno_title", "")
    instrumental = data.get("suno_instrumental", False)
    custom_mode  = data.get("suno_custom_mode", False)
    voice        = data.get("suno_voice", "auto")
    duration     = data.get("suno_duration", 30)

    if not prompt:
        await cb.answer(t("suno_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
        await cb.answer(t("suno_insufficient_coins", lang), show_alert=True)
        return

    params: dict = {
        "model":        model,
        "prompt":       prompt,
        "instrumental": instrumental,
        "custom_mode":  custom_mode,
    }
    if style:
        params["style"] = style
    if title:
        params["title"] = title
    if voice != "auto":
        params["vocal_gender"] = voice
    if model == "V5_5":
        params["duration"] = duration

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

    vtype       = data.get("suno_vocal_type", "separate_vocal")
    price_coins = data.get("suno_coins", 10)
    price_usd   = data.get("suno_usd", 0.50)
    file_id     = data.get("suno_audio_file_id")
    stem_name   = data.get("suno_stem_name", "")

    if not file_id:
        await cb.answer(t("suno_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
        await cb.answer(t("suno_insufficient_coins", lang), show_alert=True)
        return

    label_key = f"label_{lang}" if lang in ("ru", "ar") else "label_en"
    label = SUNO_VOCAL_TYPES[vtype].get(label_key) or SUNO_VOCAL_TYPES[vtype]["label_en"]
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
    lang  = get_lang(cb.from_user.id)
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
    lang   = get_lang(msg.from_user.id)
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
