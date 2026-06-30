import os
import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, BufferedInputFile, InputMediaDocument
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import coins_to_usd
from database import get_coins, spend_coins, create_order, get_lang
from keyboards import kb, back_btn, menu_btn, chunked
from i18n import t
import voice_catalog as vc

router = Router()

# Cover shown in place of Telegram's generic grey file icon on every voice
# preview document (mic + waveform, branded) — loaded once at import time.
_THUMB_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "audio_thumb.jpg")
with open(_THUMB_PATH, "rb") as _f:
    _AUDIO_THUMB_BYTES = _f.read()

def _audio_thumb() -> BufferedInputFile:
    return BufferedInputFile(_AUDIO_THUMB_BYTES, filename="thumb.jpg")

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

# Model names are intentionally NOT translated — they're product/brand names.
CATEGORY_LABELS_RU = {
    "Social": "Социальные сети",
    "Tutorials": "Обучение",
    "Documentaries": "Документалистика",
    "Trailers": "Трейлеры",
    "Explainers": "Объяснительные ролики",
    "Characters": "Персонажи",
    "Commercials": "Реклама",
    "Health & Wellness": "Здоровье и благополучие",
}

LANGUAGE_LABELS_RU = {
    "Afrikaans": "Африкаанс",
    "Arabic": "Арабский",
    "Armenian": "Армянский",
    "Assamese": "Ассамский",
    "Azerbaijani": "Азербайджанский",
    "Belarusian": "Белорусский",
    "Bengali": "Бенгальский",
    "Bosnian": "Боснийский",
    "Bulgarian": "Болгарский",
    "Cantonese": "Кантонский",
    "Catalan": "Каталанский",
    "Cebuano": "Себуанский",
    "Chichewa": "Чичева",
    "Croatian": "Хорватский",
    "Czech": "Чешский",
    "Danish": "Датский",
    "Dutch": "Голландский",
    "English": "Английский",
    "Estonian": "Эстонский",
    "Filipino": "Филиппинский",
    "Finnish": "Финский",
    "French": "Французский",
    "Galician": "Галисийский",
    "Georgian": "Грузинский",
    "German": "Немецкий",
    "Greek": "Греческий",
    "Gujarati": "Гуджарати",
    "Hausa": "Хауса",
    "Hebrew": "Иврит",
    "Hindi": "Хинди",
    "Hungarian": "Венгерский",
    "Icelandic": "Исландский",
    "Indonesian": "Индонезийский",
    "Irish": "Ирландский",
    "Italian": "Итальянский",
    "Japanese": "Японский",
    "Javanese": "Яванский",
    "Kannada": "Каннада",
    "Kazakh": "Казахский",
    "Kirghiz": "Киргизский",
    "Korean": "Корейский",
    "Latvian": "Латышский",
    "Lingala": "Лингала",
    "Lithuanian": "Литовский",
    "Luxembourgish": "Люксембургский",
    "Macedonian": "Македонский",
    "Malay": "Малайский",
    "Mandarin Chinese": "Китайский (мандарин)",
    "Marathi": "Маратхи",
    "Nepali": "Непальский",
    "Norwegian": "Норвежский",
    "Pashto": "Пушту",
    "Persian": "Персидский",
    "Polish": "Польский",
    "Portuguese": "Португальский",
    "Punjabi": "Панджаби",
    "Romanian": "Румынский",
    "Russian": "Русский",
    "Serbian": "Сербский",
    "Sindhi": "Синдхи",
    "Slovak": "Словацкий",
    "Slovenian": "Словенский",
    "Somali": "Сомалийский",
    "Spanish": "Испанский",
    "Swahili": "Суахили",
    "Swedish": "Шведский",
    "Tamil": "Тамильский",
    "Telugu": "Телугу",
    "Thai": "Тайский",
    "Turkish": "Турецкий",
    "Ukrainian": "Украинский",
    "Urdu": "Урду",
    "Vietnamese": "Вьетнамский",
    "Welsh": "Валлийский",
}

EFFECT_LABELS_RU = {
    "Announcer": "Диктор",
    "Cave": "Пещера",
    "Monster": "Монстр",
    "No Effect": "Без эффекта",
    "Phone Call": "Телефонный звонок",
    "Pro Studio": "Профессиональная студия",
    "Robotic Assistant": "Робот-ассистент",
    "Upstairs Neighbor": "Сосед сверху",
    "Vintage Radio": "Старое радио",
    "Walkie-Talkie": "Рация",
}

EMOTION_LABELS_RU = {
    "Angry": "Злость",
    "Best Fit": "Оптимально",
    "Disgusted": "Отвращение",
    "Monotone": "Монотонно",
    "Optimistic": "Оптимистично",
    "Sad": "Грусть",
    "Scared": "Испуг",
    "Surprised": "Удивление",
}

VOICE_NAME_LABELS_RU = {
    "All-Rounder": "Универсал",
    "Alpha": "Альфа",
    "Anchor": "Якорь",
    "Aspire": "Стремление",
    "Assistance": "Помощник",
    "Balance": "Баланс",
    "Boss": "Босс",
    "Bright": "Светлый",
    "Bulletin": "Бюллетень",
    "Candid": "Искренний",
    "Charmed": "Очарование",
    "Chipper": "Бодрячок",
    "Cupcake": "Кексик",
    "Curiosity": "Любопытство",
    "Deadpan": "Невозмутимый",
    "Edge": "Грань",
    "Essence": "Суть",
    "Esteem": "Уважение",
    "Everyday": "Обыденный",
    "Explore": "Исследователь",
    "Flair": "Изюминка",
    "Focus": "Фокус",
    "Gloom": "Мрак",
    "Gloss": "Глянец",
    "Grace": "Грация",
    "Gravity": "Серьёзность",
    "Grounded": "Приземлённый",
    "Guidance": "Наставник",
    "Horizon": "Горизонт",
    "Hushed": "Приглушённый",
    "Hype": "Хайп",
    "Initiative": "Инициатива",
    "Insight": "Проницательность",
    "Jackpot": "Джекпот",
    "Keen": "Увлечённый",
    "League": "Лига",
    "Mentor": "Наставник",
    "Mild": "Мягкий",
    "Mono": "Моно",
    "Neutral": "Нейтральный",
    "Nourish": "Забота",
    "Obsession": "Одержимость",
    "Paradigm": "Парадигма",
    "Path": "Путь",
    "Pep": "Энергия",
    "Persuasion": "Убеждение",
    "Pixel": "Пиксель",
    "Polished": "Отточенный",
    "Posh": "Шик",
    "Precision": "Точность",
    "Primetime": "Прайм-тайм",
    "Professor": "Профессор",
    "Quest": "Квест",
    "Resonance": "Резонанс",
    "Revelation": "Откровение",
    "Rural": "Деревенский",
    "Santa": "Санта",
    "Secrets": "Секреты",
    "Serenity": "Безмятежность",
    "Shadow": "Тень",
    "Showtime": "Время шоу",
    "Sleek": "Изящный",
    "Stride": "Уверенный шаг",
    "Suburb": "Пригород",
    "Sunny": "Солнечный",
    "Tattle": "Сплетник",
    "Trail": "Тропа",
    "Twinkle": "Искорка",
    "Unfiltered": "Без прикрас",
    "Vibes": "Вайб",
    "Views": "Взгляды",
    "Vision": "Видение",
    "Wit": "Остроумие",
}

DESCRIPTION_LABELS_RU = {
    "A dependable, friendly, and approachable everyman.": "Надёжный, дружелюбный и располагающий к себе образ простого человека.",
    "Deeply resonant with a soulful, textured tone": "Глубокий, проникновенный голос с насыщенным, душевным тембром",
    "Insightful and articulate with soulful depth": "Проницательный и красноречивый, с глубокой душевностью",
    "A singsong warmth that sparks curiosity with a young audience": "Напевная теплота, пробуждающая любопытство у юной аудитории",
    "Narrate with a friendly, welcoming voice": "Озвучивайте дружелюбным, располагающим голосом",
    "A charismatic voice to sell your product": "Харизматичный голос для продажи вашего продукта",
    "A steady voice to accompany every journey": "Уверенный голос — спутник в любом путешествии",
    "Speak clearly and directly to your audience": "Говорите чётко и прямо со своей аудиторией",
    "Engage and reassure your listeners": "Вовлекайте и успокаивайте своих слушателей",
    "A distinct grit-meets-artisanal edge with a touch of stoicism": "Особая твёрдость с налётом мастерства и стоицизма",
    "Communicate with clarity and optimism": "Общайтесь с ясностью и оптимизмом",
    "Deliver information at eye level": "Подавайте информацию на равных, без снисходительности",
    "Infuse your video with a young, clear and relatable voice.": "Наполните видео молодым, чётким и располагающим голосом.",
    "Engage your audience with a down-to-earth British accent": "Увлеките аудиторию приземлённым британским акцентом",
    "A bold and determined voice with a touch of empathy": "Смелый и решительный голос с ноткой эмпатии",
    "Craft a sense of trust and wisdom": "Создайте ощущение доверия и мудрости",
    "Spread your message with a trendy, friendly voice": "Донесите сообщение модным, дружелюбным голосом",
    "A sweet, high-spirited voice that radiates a bubbly, bright energy": "Милый, жизнерадостный голос, излучающий искрящуюся, яркую энергию",
    "A composed voice that reflects calm and sensibility": "Уравновешенный голос, отражающий спокойствие и здравомыслие",
    "Spark wonder and childlike adventure in your video": "Пробудите в видео ощущение чуда и детского приключения",
    "Relay facts with confident professionalism": "Излагайте факты с уверенным профессионализмом",
    "Tell your story with childlike wonder": "Расскажите свою историю с детским удивлением",
    "Excite your viewers with a young and energetic voice": "Воодушевите зрителей молодым, энергичным голосом",
    "Narrate with warmth and wisdom": "Озвучивайте с теплотой и мудростью",
    "Express empathy and raw emotion in your video": "Выразите в видео эмпатию и неприкрытые эмоции",
    "Transport your audience with a raspy Southern drawl": "Перенесите аудиторию хрипловатым южным говором",
    "Make complex ideas sound simple": "Сделайте сложные идеи простыми на слух",
    "Clarity and elegance in every word": "Ясность и элегантность в каждом слове",
    "A bold, sharp, and mischievous youthful British voice": "Дерзкий, острый и озорной юный британский голос",
    "An approachable voice for any video": "Располагающий голос для любого видео",
    "Educate and entertain with a voice that inspires curiosity": "Обучайте и развлекайте голосом, пробуждающим любопытство",
    "Add depth with raspy hoarse tones": "Добавьте глубины хрипловатыми, сиплыми нотками",
    "Soothe and calm your senses": "Успокойте и умиротворите чувства",
    "Establish trust, authority, and a clear vision of the future": "Создайте доверие, авторитет и ясное видение будущего",
    "Casual Gen Z style narration": "Непринуждённая озвучка в стиле поколения Z",
    "A touch of cheekiness paired with sarcasm": "Нотка дерзости в сочетании с сарказмом",
    "Bring a sense of enthusiasm to facts": "Привнесите воодушевление в подачу фактов",
    "Uplift your audience with the sweet, innocent voice of a child": "Поднимите настроение аудитории милым, невинным детским голосом",
    "A reassuring voice you can depend on": "Успокаивающий голос, на который можно положиться",
    "A futuristic voice for guiding and educating users": "Футуристичный голос для навигации и обучения пользователей",
    "Effortlessly delightful, with a fun and inviting energy": "Непринуждённо приятный, с весёлой и располагающей энергией",
    "Tell epic stories with a deep, cinematic voice": "Рассказывайте эпичные истории глубоким, кинематографичным голосом",
    "A bright and energetic tone to inspire your audience": "Яркий, энергичный тон, вдохновляющий аудиторию",
    "Convey information with warmth": "Передавайте информацию с теплотой",
    "Influence your audience with sassy confidence": "Влияйте на аудиторию дерзкой уверенностью",
    "Create genuine and relatable content": "Создавайте искренний, близкий зрителю контент",
    "Motivate and empower your audience": "Мотивируйте и вдохновляйте свою аудиторию",
    "Lighten things up with an cool, energetic, optimistic voice": "Разрядите обстановку классным, энергичным, оптимистичным голосом",
    "Street-wise, tough, with a threatening authority": "Уличная смекалка, жёсткость и угрожающий авторитет",
    "Sell anything with enthusiasm": "Продавайте что угодно с энтузиазмом",
    "A calm and understated voice to subtly inspire your audience.": "Спокойный, сдержанный голос, который тонко вдохновляет аудиторию.",
    "Stir up emotions with a bold young voice": "Всколыхните эмоции смелым молодым голосом",
    "Share your message with a raw voice": "Поделитесь своим посланием неприкрытым голосом",
    "A high dosage of friendly enthusiasm": "Большая доза дружелюбного энтузиазма",
    "Soft whispers to relax and unwind": "Тихий шёпот для расслабления и отдыха",
    "Invigorate your audience with a booming, charismatic voice": "Взбодрите аудиторию мощным, харизматичным голосом",
    "Give your video a refined touch with a young British accent": "Придайте видео изысканности молодым британским акцентом",
    "Infuse your video with energy and excitement": "Наполните видео энергией и азартом",
    "A grounded, confident voice to communicate with purpose": "Приземлённый, уверенный голос для целеустремлённого общения",
    "A dreamy, delicate voice that brings a sense of peace and wonder": "Мечтательный, нежный голос, дарящий ощущение покоя и чуда",
    "A composed voice with quiet strength and steady purpose": "Уравновешенный голос с тихой силой и устойчивой целеустремлённостью",
    "Inspire audiences with a voice of knowledge": "Вдохновляйте аудиторию голосом знания",
    "Raw and intimate authenticity": "Неприкрытая, интимная искренность",
    "Steady, strong and quietly adventurous": "Уверенный, сильный и тихо авантюрный",
    "Dive into an imaginative tale with wit and youthful curiosity": "Погрузитесь в фантазийную историю с остроумием и юным любопытством",
    "Soothe your audience with a voice of tranquility": "Успокойте аудиторию голосом безмятежности",
    "A cool, laidback voice with a touch of attitude": "Классный, непринуждённый голос с ноткой характера",
    "Deliver thrilling, high-stakes energy with a booming British voice": "Передайте захватывающую, напряжённую энергию мощным британским голосом",
    "A non-binary voice that's soft, calm and understated": "Небинарный голос — мягкий, спокойный и сдержанный",
    "A rich, resonant voice full of warmth, wonder and timeless cheer": "Богатый, звучный голос, полный теплоты, чуда и неизменного веселья",
    "An authentic, articulate voice that motivates viewers": "Искренний, чёткий голос, мотивирующий зрителей",
    "A smooth, confident voice that's always ready for the spotlight": "Плавный, уверенный голос, всегда готовый к свету софитов",
    "Graceful, composed and effortlessly confident": "Грациозный, уравновешенный и непринуждённо уверенный",
}

def _ru(value: str, table: dict, lang: str) -> str:
    return table.get(value, value) if lang == "ru" else value

def _category_label(category: str, lang: str) -> str:
    return _ru(category, CATEGORY_LABELS_RU, lang)

def _language_label(language: str, lang: str) -> str:
    return _ru(language, LANGUAGE_LABELS_RU, lang)

def _effect_label(effect: str, lang: str) -> str:
    return _ru(effect, EFFECT_LABELS_RU, lang)

def _emotion_label(emotion: str, lang: str) -> str:
    return _ru(emotion, EMOTION_LABELS_RU, lang)

def _voice_name_label(name: str, lang: str) -> str:
    return _ru(name, VOICE_NAME_LABELS_RU, lang)

def _description_label(description: str, lang: str) -> str:
    return _ru(description, DESCRIPTION_LABELS_RU, lang)

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
    # `language` here must stay canonical English for the catalog lookup below;
    # translation is applied only to the display strings further down.
    preview_url = vc.get_preview_url(voice_id, model_id, language)
    if not preview_url:
        return False
    audio_bytes = await _fetch_preview_bytes(preview_url)
    if not audio_bytes:
        return False
    display_name = _voice_name_label(voice_name, lang)
    display_language = _language_label(language, lang)
    # Sent as a document (not sendAudio) so Telegram doesn't add this preview
    # to its chat-wide continuous-playback queue, which auto-advances to
    # neighboring audio messages after one finishes.
    await message.answer_document(
        document=BufferedInputFile(audio_bytes, filename=f"{voice_name}.m4a"),
        thumbnail=_audio_thumb(),
        caption=t("vo_preview_caption", lang, voice=display_name, language=display_language, model=model_name),
    )
    return True

def _model_price_badge(model: dict) -> str:
    return f"◈ {model['coins']}"

# ── Model menu (entry point) ────────────────────────────────────
@router.callback_query(F.data == "cat_audio")
async def voiceover_model_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(cb.from_user.id)
    buttons = [
        InlineKeyboardButton(text=f"{m['name']}   {_model_price_badge(m)}", callback_data=f"vo_model_{m['id']}")
        for m in vc.list_models()
    ]
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
    await state.update_data(vo_model=model_id, vo_model_name=model["name"], vo_price_coins=model["coins"])
    buttons = [InlineKeyboardButton(text=_category_label(cat, lang), callback_data=f"vo_cat_{cat}") for cat in vc.list_categories(model_id)]
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
        f"◈  <b>{_category_label(category, lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_gender', lang)}",
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
        f"◈  <b>{_category_label(category, lang)}</b>  —  {_gender_label(gender, lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_age', lang)}",
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
    await state.update_data(vo_voice_ids=[v["id"] for v in voices])
    buttons = [InlineKeyboardButton(text=_voice_name_label(v["name"], lang), callback_data=f"vo_voice_{v['id']}") for v in voices]
    rows = list(chunked(buttons, 3))
    if voices:
        rows.insert(0, [InlineKeyboardButton(text=t("vo_btn_listen_all", lang, count=len(voices)), callback_data="vo_listen_all")])
    rows.append([back_btn(f"vo_gender_{gender}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{_category_label(category, lang)}</b>  —  {_gender_label(gender, lang)}  —  {_age_label(age, lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_voice', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

# ── Listen to all voices in the current filter ──────────────────
@router.callback_query(F.data == "vo_listen_all")
async def voiceover_listen_all(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    model_id = data.get("vo_model")
    voice_ids = data.get("vo_voice_ids", [])
    if not voice_ids:
        await cb.answer()
        return
    await cb.answer(t("vo_listen_all_sending", lang))
    for batch in chunked(voice_ids, 10):
        media = []
        for vid in batch:
            voice = vc.get_voice(vid)
            if not voice:
                continue
            language = _default_language(vid, model_id)
            preview_url = vc.get_preview_url(vid, model_id, language)
            if not preview_url:
                continue
            audio_bytes = await _fetch_preview_bytes(preview_url)
            if not audio_bytes:
                continue
            display_name = _voice_name_label(voice["name"], lang)
            # InputMediaDocument (not Audio) so these previews don't join
            # Telegram's chat-wide continuous-playback queue.
            media.append(InputMediaDocument(
                media=BufferedInputFile(audio_bytes, filename=f"{voice['name']}.m4a"),
                thumbnail=_audio_thumb(),
                caption=display_name,
            ))
        if media:
            await cb.message.answer_media_group(media=media)

def _voice_card_text(voice: dict, model_name: str, language: str, lang: str, stability: int | None = None, effect: str | None = None, emotion: str | None = None, speed: float | None = None) -> str:
    text = (
        f"◈  <b>{_voice_name_label(voice['name'], lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {_description_label(voice['description'], lang)}\n\n"
        f"{t('vo_voice_model_label', lang, model=model_name)}\n"
        f"{t('vo_voice_gender_label', lang, gender=_gender_label(voice['gender'], lang))}\n"
        f"{t('vo_voice_age_label', lang, age=_age_label(voice['age'], lang))}\n"
        f"{t('vo_voice_language_label', lang, language=_language_label(language, lang))}"
    )
    if stability is not None:
        text += f"\n{t('vo_voice_stability_label', lang, pct=stability)}"
    if effect:
        text += f"\n{t('vo_voice_effect_label', lang, effect=_effect_label(effect, lang))}"
    if emotion:
        text += f"\n{t('vo_voice_emotion_label', lang, emotion=_emotion_label(emotion, lang))}"
    if speed is not None:
        text += f"\n{t('vo_voice_speed_label', lang, speed=speed)}"
    return text

def _voice_card_kb(voice_id: int, model_id: int, age: str, language: str, stability: int | None, effect: str | None, lang: str, emotion: str | None = None, speed: float | None = None, voice_ids: list[int] | None = None):
    voice_ids = voice_ids or []
    idx = voice_ids.index(voice_id) if voice_id in voice_ids else -1
    nav_row = []
    if idx > 0:
        nav_row.append(InlineKeyboardButton(text="◀", callback_data="vo_navprev"))
    nav_row.append(InlineKeyboardButton(text=t("vo_btn_listen", lang), callback_data="vo_listen"))
    if 0 <= idx < len(voice_ids) - 1:
        nav_row.append(InlineKeyboardButton(text="▶", callback_data="vo_navnext"))
    rows = [
        nav_row,
        [InlineKeyboardButton(text=t("vo_btn_change_language", lang, language=_language_label(language, lang)), callback_data="vo_lang_menu")],
    ]
    if model_id in vc.STABILITY_MODELS:
        rows.append([InlineKeyboardButton(text=t("vo_btn_stability", lang, pct=stability), callback_data="vo_stabmenu")])
    if vc.list_effects(model_id):
        rows.append([InlineKeyboardButton(text=t("vo_btn_effect", lang, effect=_effect_label(effect, lang)), callback_data="vo_fxmenu")])
    if vc.list_emotions(model_id):
        rows.append([InlineKeyboardButton(text=t("vo_btn_emotion", lang, emotion=_emotion_label(emotion, lang)), callback_data="vo_emomenu")])
    if model_id in vc.SPEED_MODELS:
        rows.append([InlineKeyboardButton(text=t("vo_btn_speed", lang, speed=speed), callback_data="vo_spdmenu")])
    rows.append([InlineKeyboardButton(text=t("vo_btn_choose_voice", lang), callback_data="vo_pick")])
    rows.append([back_btn(f"vo_age_{age}", lang=lang), menu_btn(lang)])
    return kb(*rows)

def _stability_bar(pct: int) -> str:
    filled = pct // 10
    return "🟦" * filled + "⬜" * (10 - filled) + f"   {pct}%"

def _speed_bar(speed: float) -> str:
    filled = round((speed - 0.5) / 0.1)
    return "🟦" * filled + "⬜" * (10 - filled) + f"   {speed}x"

async def _select_voice(cb: CallbackQuery, state: FSMContext, voice_id: int):
    lang = get_lang(cb.from_user.id)
    voice = vc.get_voice(voice_id)
    if not voice:
        await cb.answer("Voice not found")
        return
    data = await state.get_data()
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name", "—")
    age = data.get("vo_age")
    voice_ids = data.get("vo_voice_ids", [])
    language = _default_language(voice_id, model_id)
    stability = vc.STABILITY_DEFAULT if model_id in vc.STABILITY_MODELS else None
    effect = "No Effect" if vc.list_effects(model_id) else None
    emotions = vc.list_emotions(model_id)
    emotion = next((e["name"] for e in emotions if e["is_default"]), emotions[0]["name"] if emotions else None)
    speed = vc.SPEED_DEFAULT if model_id in vc.SPEED_MODELS else None
    await state.update_data(
        vo_voice_id=voice_id, vo_voice_name=voice["name"], vo_lang=language,
        vo_stability=stability, vo_effect=effect, vo_emotion=emotion, vo_speed=speed,
    )

    await cb.message.edit_text(
        _voice_card_text(voice, model_name, language, lang, stability, effect, emotion, speed),
        reply_markup=_voice_card_kb(voice_id, model_id, age, language, stability, effect, lang, emotion, speed, voice_ids),
        parse_mode="HTML"
    )
    await _send_preview(cb.message, voice["name"], voice_id, model_id, model_name, language, lang)

# ── Voice selected → voice card + preview sample ────────────────
@router.callback_query(F.data.startswith("vo_voice_"))
async def voiceover_voice_selected(cb: CallbackQuery, state: FSMContext):
    voice_id = int(cb.data.replace("vo_voice_", "", 1))
    await _select_voice(cb, state, voice_id)

# ── Prev / Next voice in the current filtered list ────────────────
@router.callback_query(F.data.in_(["vo_navprev", "vo_navnext"]))
async def voiceover_voice_nav(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    voice_ids = data.get("vo_voice_ids", [])
    current_id = data.get("vo_voice_id")
    if not voice_ids or current_id not in voice_ids:
        await cb.answer()
        return
    idx = voice_ids.index(current_id)
    new_idx = idx - 1 if cb.data == "vo_navprev" else idx + 1
    if new_idx < 0 or new_idx >= len(voice_ids):
        await cb.answer()
        return
    await _select_voice(cb, state, voice_ids[new_idx])
    await cb.answer()

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
    buttons = [InlineKeyboardButton(text=_language_label(l["name"], lang), callback_data=f"vo_lang_{l['name'][:24]}") for l in languages]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vo_voice_{voice_id}", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"◈  <b>{_voice_name_label(voice_name, lang)}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_language', lang)}",
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
    voice_ids = data.get("vo_voice_ids", [])
    voice = vc.get_voice(voice_id)
    if not voice:
        await cb.answer("Voice not found")
        return

    languages = vc.list_languages(voice_id, model_id)
    match = next((l for l in languages if l["name"].startswith(language)), None)
    full_language = match["name"] if match else language
    await state.update_data(vo_lang=full_language)
    stability = data.get("vo_stability")
    effect = data.get("vo_effect")
    emotion = data.get("vo_emotion")
    speed = data.get("vo_speed")

    await cb.message.edit_text(
        _voice_card_text(voice, model_name, full_language, lang, stability, effect, emotion, speed),
        reply_markup=_voice_card_kb(voice_id, model_id, age, full_language, stability, effect, lang, emotion, speed, voice_ids),
        parse_mode="HTML"
    )
    sent = await _send_preview(cb.message, voice["name"], voice_id, model_id, model_name, full_language, lang)
    if not sent:
        await cb.answer()

# ── Stability slider (Eleven v3 only) ─────────────────────────────
@router.callback_query(F.data == "vo_stabmenu")
async def voiceover_stability_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    stability = data.get("vo_stability", vc.STABILITY_DEFAULT)
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_select_stability', lang)}\n\n{_stability_bar(stability)}",
        reply_markup=kb(
            [InlineKeyboardButton(text="➖", callback_data="vo_stabdown"),
             InlineKeyboardButton(text="➕", callback_data="vo_stabup")],
            [InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_stabdone")],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data.in_(["vo_stabup", "vo_stabdown"]))
async def voiceover_stability_adjust(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    stability = data.get("vo_stability", vc.STABILITY_DEFAULT)
    step = 10 if cb.data == "vo_stabup" else -10
    stability = max(min(stability + step, 100), 10)
    await state.update_data(vo_stability=stability)
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_select_stability', lang)}\n\n{_stability_bar(stability)}",
        reply_markup=kb(
            [InlineKeyboardButton(text="➖", callback_data="vo_stabdown"),
             InlineKeyboardButton(text="➕", callback_data="vo_stabup")],
            [InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_stabdone")],
        ),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data == "vo_stabdone")
async def voiceover_stability_done(cb: CallbackQuery, state: FSMContext):
    await _render_voice_card(cb, state)

# ── Voice effects ──────────────────────────────────────────────────
@router.callback_query(F.data == "vo_fxmenu")
async def voiceover_effect_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    model_id = data.get("vo_model")
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    current_effect = data.get("vo_effect", "No Effect")
    effects = vc.list_effects(model_id)
    buttons = [
        InlineKeyboardButton(
            text=("✓ " if e["name"] == current_effect else "") + _effect_label(e["name"], lang),
            callback_data=f"vo_fx_{i}",
        )
        for i, e in enumerate(effects)
    ]
    rows = list(chunked(buttons, 2))
    rows.append([InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_fxdone")])
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_effect', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vo_fx_"))
async def voiceover_effect_selected(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.replace("vo_fx_", "", 1))
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    model_id = data.get("vo_model")
    effects = vc.list_effects(model_id)
    if idx < 0 or idx >= len(effects):
        await cb.answer("Effect not found")
        return
    effect = effects[idx]
    await state.update_data(vo_effect=effect["name"])

    if effect["preview_url"]:
        audio_bytes = await _fetch_preview_bytes(effect["preview_url"])
        if audio_bytes:
            display_effect = _effect_label(effect["name"], lang)
            # Document (not Audio) so this preview doesn't join Telegram's
            # chat-wide continuous-playback queue.
            await cb.message.answer_document(
                document=BufferedInputFile(audio_bytes, filename=f"{effect['name']}.m4a"),
                thumbnail=_audio_thumb(),
                caption=t("vo_effect_preview_caption", lang, effect=display_effect),
            )
    await voiceover_effect_menu(cb, state)
    await cb.answer()

@router.callback_query(F.data == "vo_fxdone")
async def voiceover_effect_done(cb: CallbackQuery, state: FSMContext):
    await _render_voice_card(cb, state)

# ── Voice emotion (MiniMax 02 HD, Cartesia Sonic 2 only) ───────────
@router.callback_query(F.data == "vo_emomenu")
async def voiceover_emotion_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    model_id = data.get("vo_model")
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    current_emotion = data.get("vo_emotion")
    emotions = vc.list_emotions(model_id)
    buttons = [
        InlineKeyboardButton(
            text=("✓ " if e["name"] == current_emotion else "") + _emotion_label(e["name"], lang),
            callback_data=f"vo_emo_{i}",
        )
        for i, e in enumerate(emotions)
    ]
    rows = list(chunked(buttons, 2))
    rows.append([InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_emodone")])
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n{t('vo_select_emotion', lang)}",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vo_emo_"))
async def voiceover_emotion_selected(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.replace("vo_emo_", "", 1))
    data = await state.get_data()
    model_id = data.get("vo_model")
    emotions = vc.list_emotions(model_id)
    if idx < 0 or idx >= len(emotions):
        await cb.answer("Emotion not found")
        return
    await state.update_data(vo_emotion=emotions[idx]["name"])
    await voiceover_emotion_menu(cb, state)
    await cb.answer()

@router.callback_query(F.data == "vo_emodone")
async def voiceover_emotion_done(cb: CallbackQuery, state: FSMContext):
    await _render_voice_card(cb, state)

# ── Voice speed (all models) ────────────────────────────────────────
@router.callback_query(F.data == "vo_spdmenu")
async def voiceover_speed_menu(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    speed = data.get("vo_speed", vc.SPEED_DEFAULT)
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_select_speed', lang)}\n\n{_speed_bar(speed)}",
        reply_markup=kb(
            [InlineKeyboardButton(text="➖", callback_data="vo_spddown"),
             InlineKeyboardButton(text="➕", callback_data="vo_spdup")],
            [InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_spddone")],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data.in_(["vo_spdup", "vo_spddown"]))
async def voiceover_speed_adjust(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    speed = data.get("vo_speed", vc.SPEED_DEFAULT)
    step = 0.1 if cb.data == "vo_spdup" else -0.1
    speed = round(max(min(speed + step, 1.5), 0.5), 1)
    await state.update_data(vo_speed=speed)
    await cb.message.edit_text(
        f"◈  <b>{voice_name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_select_speed', lang)}\n\n{_speed_bar(speed)}",
        reply_markup=kb(
            [InlineKeyboardButton(text="➖", callback_data="vo_spddown"),
             InlineKeyboardButton(text="➕", callback_data="vo_spdup")],
            [InlineKeyboardButton(text=t("vo_btn_done", lang), callback_data="vo_spddone")],
        ),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data == "vo_spddone")
async def voiceover_speed_done(cb: CallbackQuery, state: FSMContext):
    await _render_voice_card(cb, state)

async def _render_voice_card(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_id = data.get("vo_voice_id")
    model_id = data.get("vo_model")
    model_name = data.get("vo_model_name", "—")
    age = data.get("vo_age")
    language = data.get("vo_lang", "—")
    stability = data.get("vo_stability")
    effect = data.get("vo_effect")
    emotion = data.get("vo_emotion")
    speed = data.get("vo_speed")
    voice_ids = data.get("vo_voice_ids", [])
    voice = vc.get_voice(voice_id)
    if not voice:
        await cb.answer("Voice not found")
        return
    await cb.message.edit_text(
        _voice_card_text(voice, model_name, language, lang, stability, effect, emotion, speed),
        reply_markup=_voice_card_kb(voice_id, model_id, age, language, stability, effect, lang, emotion, speed, voice_ids),
        parse_mode="HTML"
    )

# ── Voice picked → ask for text ───────────────────────────────
@router.callback_query(F.data == "vo_pick")
async def voiceover_pick(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
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
    voice_name = _voice_name_label(data.get("vo_voice_name", "—"), lang)
    model_name = data.get("vo_model_name", "—")
    language = _language_label(data.get("vo_lang", "—"), lang)
    stability = data.get("vo_stability")
    effect = data.get("vo_effect")
    emotion = data.get("vo_emotion")
    speed = data.get("vo_speed")
    price_coins = data.get("vo_price_coins", 5)
    coins_word = t("coins_word", lang)
    user_coins = get_coins(msg.from_user.id)

    extra_lines = ""
    if stability is not None:
        extra_lines += f"{t('vo_stability_label', lang, pct=stability)}\n"
    if effect:
        extra_lines += f"{t('vo_effect_label', lang, effect=_effect_label(effect, lang))}\n"
    if emotion:
        extra_lines += f"{t('vo_emotion_label', lang, emotion=_emotion_label(emotion, lang))}\n"
    if speed is not None:
        extra_lines += f"{t('vo_speed_label', lang, speed=speed)}\n"

    await msg.answer(
        f"{t('vo_order_summary_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_voice_label', lang, name=voice_name)}\n"
        f"{t('vo_model_label', lang, model=model_name)}\n"
        f"{t('vo_language_label', lang, language=language)}\n"
        f"{extra_lines}"
        f"{t('vo_cost_label', lang)}<b>{price_coins} {coins_word}</b>\n"
        f"{t('vo_balance_label', lang)}{user_coins} {coins_word}\n\n"
        f"{t('vo_text_label', lang)}\n<i>{msg.text}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("vo_btn_confirm", lang, coins=price_coins), callback_data="vo_confirm")],
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
    price_coins = data.get("vo_price_coins", 5)
    price_usd = coins_to_usd(price_coins)

    if not voice_id or not text:
        await cb.answer(t("vo_session_expired", lang), show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, price_coins):
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
        "stability": data.get("vo_stability"),
        "effect": data.get("vo_effect"),
        "emotion": data.get("vo_emotion"),
        "speed": data.get("vo_speed"),
        "text": text,
    }
    tool_name = f"Voiceover — {voice_name} ({model_name})"
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool_name, params, price_coins, price_usd)

    await _push_to_queue(oid, uid, voice_id, tool_name, params, price_coins, price_usd, username=cb.from_user.username or cb.from_user.first_name or "")
    await _notify_admin(cb, oid, tool_name, params, price_coins, price_usd)

    display_voice_name = _voice_name_label(voice_name, lang)
    await cb.message.edit_text(
        f"{t('vo_order_placed_title', lang, oid=oid)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('vo_voice_row', lang, name=display_voice_name)}\n"
        f"{t('vo_coins_deducted', lang, coins=price_coins)}\n\n"
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
    extra = ""
    if params.get("stability") is not None:
        extra += f"  Stability  {params['stability']}%\n"
    if params.get("effect"):
        extra += f"  Effect     {params['effect']}\n"
    if params.get("emotion"):
        extra += f"  Emotion    {params['emotion']}\n"
    if params.get("speed") is not None:
        extra += f"  Speed      {params['speed']}x\n"
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
        f"{extra}"
        f"  Coins      <b>{coins}◈</b>  (${price_usd})",
        reply_markup=keyboard, parse_mode="HTML"
    )
    await bot.send_message(
        ADMIN_ID,
        f"📋 <b>Text #{oid}:</b>\n\n<code>{params.get('text','—')}</code>",
        parse_mode="HTML"
    )
