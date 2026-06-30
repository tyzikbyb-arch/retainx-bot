import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import VOICEOVER_PRICE_COINS, VOICEOVER_PRICE_USD
from database import get_coins, spend_coins, create_order, get_lang
from keyboards import kb, back_btn, menu_btn, chunked
from i18n import t
import voice_catalog as vc

router = Router()

class VoiceoverStates(StatesGroup):
    entering_text = State()

GENDER_LABELS = {
    "en": {"MALE": "Male", "FEMALE": "Female", "NEUTRAL": "Neutral"},
    "ru": {"MALE": "Мужской", "FEMALE": "Женский", "NEUTRAL": "Нейтральный"},
}
AGE_LABELS = {
    "en": {
        "CHILD": "Child", "TEEN": "Teen", "YOUNG_ADULT": "Young Adult",
        "ADULT": "Adult", "MIDDLE_AGED": "Middle-aged", "SENIOR": "Senior",
    },
    "ru": {
        "CHILD": "Ребёнок", "TEEN": "Подросток", "YOUNG_ADULT": "Молодой взрослый",
        "ADULT": "Взрослый", "MIDDLE_AGED": "Средних лет", "SENIOR": "Пожилой",
    },
}

def _gender_label(gender: str, lang: str) -> str:
    return GENDER_LABELS.get(lang, GENDER_LABELS["en"]).get(gender, gender)

def _age_label(age: str, lang: str) -> str:
    return AGE_LABELS.get(lang, AGE_LABELS["en"]).get(age, age)

def _default_language(voice_id: int, model_id: int) -> str:
    langs = vc.list_languages(voice_id, model_id)
    default = next((l for l in langs if l["is_default"]), None)
    return default["name"] if default else (langs[0]["name"] if langs else "English")

async def _fetch_preview_bytes(url: str) -> bytes | None:
    """Artlist's CDN serves preview files with a wrong Content-Type
    (application/x-www-form-urlencoded instead of audio/*), which makes
    Telegram's own URL-fetch hang forever. Download the bytes ourselves
    and upload them with an explicit .m4a filename instead."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return None
                return await resp.read()
    except Exception:
        return None

async def _send_preview(message, voice_name: str, voice_id: int, model_id: int, model_name: str, language: str, lang: str) -> bool:
    preview_url = vc.get_preview_url(voice_id, model_id, language)
    if not preview_url:
        return False
    audio_bytes = await _fetch_preview_bytes(preview_url)
    if not audio_bytes:
        return False
    await message.answer_audio(
        audio=BufferedInputFile(audio_bytes, filename=f"{voice_name}.m4a"),
        title=voice_name,
        caption=t("vo_preview_caption", lang, voice=voice_name, language=language, model=model_name),
    )
    return True

# ── Model menu (entry point) ────────────────────────────────────
@router.callback_query(F.data == "cat_audio")
async def voiceover_model_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(cb.from_user.id)
    buttons = [InlineKeyboardButton(text=m["name"], callback_data=f"vo_model_{m['id']}") for m in vc.list_models()]
    rows = list(chunked(buttons, 1))
    rows.append([menu_btn(lang)])
    await cb.message.edit_text(
        f"{t('audio_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_model', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Model selected → category menu ──────────────────────────────
@router.callback_query(F.data.startswith("vo_model_"))
async def voiceover_model_selected(cb: CallbackQuery, state: FSMContext):
    model_id = int(cb.data.replace("vo_model_", "", 1))
    lang = get_lang(cb.from_user.id)
    model = vc.get_model(model_id)
    if not model:
        await cb.answer("Model not found")
        return
    await state.update_data(vo_model=model_id, vo_model_name=model["name"])
    buttons = [InlineKeyboardButton(text=cat, callback_data=f"vo_cat_{cat}") for cat in vc.list_categories(model_id)]
    rows = list(chunked(buttons, 2))
    rows.append([back_btn("cat_audio", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{model['name']}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_category', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Category selected → gender menu ─────────────────────────────
@router.callback_query(F.data.startswith("vo_cat_"))
async def voiceover_category_selected(cb: CallbackQuery, state: FSMContext):
    category = cb.data.replace("vo_cat_", "", 1)
    lang = get_lang(cb.from_user.id)
    await state.update_data(vo_cat=category)
    data = await state.get_data()
    model_id = data.get("vo_model")
    genders = vc.list_genders(model_id, category)
    buttons = [InlineKeyboardButton(text=_gender_label(g, lang), callback_data=f"vo_gender_{g}") for g in genders]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vo_model_{model_id}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{category}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_gender', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Gender selected → age menu ──────────────────────────────────
@router.callback_query(F.data.startswith("vo_gender_"))
async def voiceover_gender_selected(cb: CallbackQuery, state: FSMContext):
    gender = cb.data.replace("vo_gender_", "", 1)
    lang = get_lang(cb.from_user.id)
    await state.update_data(vo_gender=gender)
    data = await state.get_data()
    model_id = data.get("vo_model")
    category = data.get("vo_cat")
    ages = vc.list_ages(model_id, category, gender)
    buttons = [InlineKeyboardButton(text=_age_label(a, lang), callback_data=f"vo_age_{a}") for a in ages]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vo_cat_{category}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{category}</b>  —  {_gender_label(gender, lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_age', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Age selected → voice list ───────────────────────────────────
@router.callback_query(F.data.startswith("vo_age_"))
async def voiceover_age_selected(cb: CallbackQuery, state: FSMContext):
    age = cb.data.replace("vo_age_", "", 1)
    lang = get_lang(cb.from_user.id)
    await state.update_data(vo_age=age)
    data = await state.get_data()
    model_id = data.get("vo_model")
    category = data.get("vo_cat")
    gender = data.get("vo_gender")
    voices = vc.list_voices(model_id, category, gender, age)
    buttons = [InlineKeyboardButton(text=v["name"], callback_data=f"vo_voice_{v['id']}") for v in voices]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vo_gender_{gender}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{category}</b>  —  {_gender_label(gender, lang)}  —  {_age_label(age, lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_voice', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

def _voice_card_text(voice: dict, model_name: str, language: str, lang: str) -> str:
    return (
        f"◈  <b>{voice['name']}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {voice['description']}\n\n"
        f"{t('vo_voice_model_label', lang, model=model_name)}\n"
        f"{t('vo_voice_gender_label', lang, gender=_gender_label(voice['gender'], lang))}\n"
        f"{t('vo_voice_age_label', lang, age=_age_label(voice['age'], lang))}\n"
        f"{t('vo_voice_language_label', lang, language=language)}"
    )

def _voice_card_kb(voice_id: int, age: str, language: str, lang: str):
    return kb(
        [InlineKeyboardButton(text=t("vo_btn_listen", lang), callback_data="vo_listen")],
        [InlineKeyboardButton(text=t("vo_btn_change_language", lang, language=language), callback_data="vo_lang_menu")],
        [InlineKeyboardButton(text=t("vo_btn_choose_voice", lang), callback_data="vo_pick")],
        [back_btn(f"vo_age_{age}", lang=lang), menu_btn(lang)],
    )

# ── Voice selected → voice card + preview sample ────────────────
@router.callback_query(F.data.startswith("vo_voice_"))
async def voiceover_voice_selected(cb: CallbackQuery, state: FSMContext):
    voice_id = int(cb.data.replace("vo_voice_", "", 1))
    lang = get_lang(cb.from_user.id)
    voice = vc.get_voice(voice_id)
    if not voice:
        await cb.answer("Voice not found")
        return
    data = await state.get_data()
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name", "—")
    age = data.get("vo_age")
    language = _default_language(voice_id, model_id)
    await state.update_data(vo_voice_id=voice_id, vo_voice_name=voice["name"], vo_lang=language)

    await cb.message.edit_text(
        _voice_card_text(voice, model_name, language, lang),
        reply_markup=_voice_card_kb(voice_id, age, language, lang),
        parse_mode="HTML"
    )
    await _send_preview(cb.message, voice["name"], voice_id, model_id, model_name, language, lang)

# ── Listen again ─────────────────────────────────────────────────
@router.callback_query(F.data == "vo_listen")
async def voiceover_listen(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_id = data.get("vo_voice_id")
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name", "—")
    voice_name = data.get("vo_voice_name", "—")
    language = data.get("vo_lang", "English")
    sent = await _send_preview(cb.message, voice_name, voice_id, model_id, model_name, language, lang)
    if not sent:
        await cb.answer(t("vo_select_language", lang), show_alert=True)
        return
    await cb.answer()

# ── Change language → language list ──────────────────────────────
@router.callback_query(F.data == "vo_lang_menu")
async def voiceover_language_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_id = data.get("vo_voice_id")
    model_id = data.get("vo_model")
    voice_name = data.get("vo_voice_name", "—")
    languages = vc.list_languages(voice_id, model_id)
    buttons = [InlineKeyboardButton(text=l["name"], callback_data=f"vo_lang_{l['name'][:24]}") for l in languages]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vo_voice_{voice_id}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_language', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Language selected → back to voice card + new preview ─────────
@router.callback_query(F.data.startswith("vo_lang_"))
async def voiceover_language_selected(cb: CallbackQuery, state: FSMContext):
    language = cb.data.replace("vo_lang_", "", 1)
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_id = data.get("vo_voice_id")
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name", "—")
    age = data.get("vo_age")
    voice = vc.get_voice(voice_id)
    if not voice:
        await cb.answer("Voice not found")
        return

    languages = vc.list_languages(voice_id, model_id)
    match = next((l for l in languages if l["name"].startswith(language)), None)
    full_language = match["name"] if match else language
    await state.update_data(vo_lang=full_language)

    await cb.message.edit_text(
        _voice_card_text(voice, model_name, full_language, lang),
        reply_markup=_voice_card_kb(voice_id, age, full_language, lang),
        parse_mode="HTML"
    )
    sent = await _send_preview(cb.message, voice["name"], voice_id, model_id, model_name, full_language, lang)
    if not sent:
        await cb.answer()

# ── Voice picked → ask for text ───────────────────────────────
@router.callback_query(F.data == "vo_pick")
async def voiceover_pick(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = data.get("vo_voice_name", "—")
    voice_id = data.get("vo_voice_id")
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_enter_text', lang)}",
        reply_markup=kb([back_btn(f"vo_voice_{voice_id}", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(VoiceoverStates.entering_text)

# ── Text entered → order summary ──────────────────────────────
@router.message(VoiceoverStates.entering_text)
async def voiceover_text_received(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    await state.update_data(vo_text=msg.text)
    data = await state.get_data()
    voice_name = data.get("vo_voice_name", "—")
    model_name = data.get("vo_model_name", "—")
    language = data.get("vo_lang", "—")
    coins_word = t("coins_word", lang)
    user_coins = get_coins(msg.from_user.id)

    await msg.answer(
        f"{t('vo_order_summary_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_voice_label', lang, name=voice_name)}\n"
        f"{t('vo_model_label', lang, model=model_name)}\n"
        f"{t('vo_language_label', lang, language=language)}\n"
        f"{t('vo_cost_label', lang)}<b>{VOICEOVER_PRICE_COINS} {coins_word}</b>\n"
        f"{t('vo_balance_label', lang)}{user_coins} {coins_word}\n\n"
        f"{t('vo_text_label', lang)}\n<i>{msg.text}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("vo_btn_confirm", lang, coins=VOICEOVER_PRICE_COINS), callback_data="vo_confirm")],
            [InlineKeyboardButton(text=t("vo_btn_edit_text", lang), callback_data="vo_edit_text")],
            [menu_btn(lang)],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "vo_edit_text")
async def voiceover_edit_text(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        t("vo_edit_text_prompt", lang),
        reply_markup=kb([menu_btn(lang)])
    )
    await state.set_state(VoiceoverStates.entering_text)

# ── Confirm order ─────────────────────────────────────────────
@router.callback_query(F.data == "vo_confirm")
async def voiceover_confirm(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    uid = cb.from_user.id
    voice_id = data.get("vo_voice_id")
    voice_name = data.get("vo_voice_name")
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name")
    language = data.get("vo_lang")
    text = data.get("vo_text")

    if not voice_id or not text:
        await cb.answer(t("vo_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, VOICEOVER_PRICE_COINS):
        await cb.answer(t("vo_insufficient_coins", lang), show_alert=True)
        return

    params = {
        "voice_id": voice_id,
        "voice_name": voice_name,
        "model_id": model_id,
        "model_name": model_name,
        "language": language,
        "category": data.get("vo_cat"),
        "gender": data.get("vo_gender"),
        "age": data.get("vo_age"),
        "text": text,
    }
    tool_name = f"Voiceover — {voice_name} ({model_name})"
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool_name, params, VOICEOVER_PRICE_COINS, VOICEOVER_PRICE_USD)

    await _push_to_queue(oid, uid, voice_id, tool_name, params, VOICEOVER_PRICE_COINS, VOICEOVER_PRICE_USD, username=cb.from_user.username or cb.from_user.first_name or "")
    await _notify_admin(cb, oid, tool_name, params, VOICEOVER_PRICE_COINS, VOICEOVER_PRICE_USD)

    await cb.message.edit_text(
        f"{t('vo_order_placed_title', lang, oid=oid)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_voice_row', lang, name=voice_name)}\n"
        f"{t('vo_coins_deducted', lang, coins=VOICEOVER_PRICE_COINS)}\n\n"
        f"{t('vo_estimated_delivery', lang)}\n\n"
        f"{t('vo_will_deliver', lang)}",
        reply_markup=kb([menu_btn(lang)]), parse_mode="HTML"
    )
    await state.clear()

async def _push_to_queue(oid: int, uid: int, voice_id: int, tool: str, params: dict, coins: int, usd: float, username: str = ""):
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
            "tool_id": str(voice_id),
            "tool_name": tool,
            "type": "voiceover",
            "params": params,
            "coins": coins,
            "usd": usd,
        }
        await r.rpush("retainx:orders", json.dumps(order_data))
        log.info(f"[QUEUE] Voiceover order #{oid} pushed to queue")
        from worker_monitor import check_workers_alive, send_no_workers_alert
        if not await check_workers_alive(redis_url):
            log.warning(f"[QUEUE] No live workers -- sending manual alert for voiceover order #{oid}")
            await send_no_workers_alert(
                order_id=oid, user_id=uid, username=username,
                tool=tool, params=params, coins=coins, redis_url=redis_url,
            )
        await r.aclose()
    except Exception as e:
        log.error(f"[QUEUE] Failed to push voiceover order #{oid}: {e}")

async def _notify_admin(cb: CallbackQuery, oid: int, tool: str, params: dict, coins: int, price_usd: float):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Delivered", callback_data=f"delivered_{oid}"),
        InlineKeyboardButton(text="✕  Cancel", callback_data=f"cancel_order_{oid}"),
    ]])
    await bot.send_message(
        ADMIN_ID,
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"◈  <b>New Voiceover Order #{oid}</b>\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"  User       @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
        f"  Voice      <b>{params.get('voice_name')}</b>  (id {params.get('voice_id')})\n"
        f"  Model      {params.get('model_name')}\n"
        f"  Language   {params.get('language')}\n"
        f"  Category   {params.get('category')}\n"
        f"  Gender     {params.get('gender')}\n"
        f"  Age        {params.get('age')}\n"
        f"  Coins      <b>{coins}◈</b>  (${price_usd})",
        reply_markup=keyboard, parse_mode="HTML"
    )
    await bot.send_message(
        ADMIN_ID,
        f"📋 <b>Text #{oid}:</b>\n\n<code>{params.get('text','—')}</code>",
        parse_mode="HTML"
    )
