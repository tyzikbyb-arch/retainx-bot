"""
Attachment configuration for each video tool.
Defines what files each tool accepts and custom UI text.
"""

# Attachment config per tool ID
# Keys:
#   start_frame: bool - single start image
#   end_frame: bool - end image (only with start_frame)
#   img_refs: int - max image references (0 = none)
#   vid_refs: int - max video references (0 = none)
#   aud_refs: int - max audio files (0 = none)
#   prompt_label: str - custom prompt label (None = "Enter your prompt")
#   no_prompt: bool - skip prompt entirely
#   hint: str - custom hint text (replaces default warning)
#   vid_ref_required: bool - video reference is mandatory
#   img_required: bool - image reference is mandatory
#   aud_required: bool - audio is mandatory
#   start_frame_required: bool - start frame is mandatory
#   exclusive_startend: bool - start/end frame are mutually exclusive with img_refs

TOOL_ATTACHMENTS = {

    # ── Standard video ────────────────────────────────────────────────────────

    "sd20": {   # Seedance 2.0
        "start_frame": True, "end_frame": True,
        "img_refs": 9, "vid_refs": 3, "aud_refs": 3,
        "exclusive_startend": True,
    },
    "sd20f": {  # Seedance 2.0 Fast
        "start_frame": True, "end_frame": True,
        "img_refs": 9, "vid_refs": 3, "aud_refs": 3,
        "exclusive_startend": True,
    },
    "hh10": {   # Happy Horse 1.1 — no End Frame button for this tool
        "start_frame": True, "end_frame": False,
        "img_refs": 1,
        "exclusive_startend": True,
    },
    "wan27": {  # Wan 2.7 — Artlist's UI doesn't expose Image Reference for
                # this model (confirmed live, order #368: button rendered
                # as disabled and never becomes selectable), so the bot
                # offers Audio File instead of img_refs.
        "start_frame": True, "end_frame": True,
        "aud_refs": 1,
        "exclusive_startend": True,
    },
    "groki": {  # Grok Image-to-Video — requires a character photo; the model
                # animates movement inspired by that photo (not pixel-exact).
        "start_frame": True, "end_frame": False,
        "start_frame_required": True,
        "start_frame_label_key": "vid_btn_char_photo",
        "start_frame_title_key": "vid_char_photo_title",
        "start_frame_desc_key":  "vid_char_photo_desc",
        "hint": "Attach a photo of your character — the model will animate it.",
    },
    "grok": {
        "start_frame": True, "end_frame": False,
        "start_frame_label_key": "vid_btn_char_photo",
        "start_frame_title_key": "vid_char_photo_title",
        "start_frame_desc_key":  "vid_char_photo_desc",
        "hint": "Optional: attach a photo as a style reference.",
    },

    # ── Premium video ─────────────────────────────────────────────────────────

    "veo31": {  # Veo 3.1 — Artlist's UI doesn't expose Image Reference for
                # this model (confirmed live by hand, order #373: button
                # rendered as disabled in the panel), so don't offer it.
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "veo31f": { # Veo 3.1 Fast — no Image Reference tab in Artlist's UI
                # (confirmed live by hand, same as veo31/#373).
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "veo31l": { # Veo 3.1 Lite — no Image Reference tab in Artlist's UI
                # (confirmed live by hand, same as veo31/#373).
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "sora2": {  # Sora 2 Pro — no End Frame button for this tool
        "start_frame": True, "end_frame": False,
        "hint": "Sora 2 Pro is highly unstable. Switch to another model if it fails.",
    },
    "ltx23": {  # LTX 2.3 Pro — Artlist's UI shows Image Reference as disabled
                # for this model (confirmed live, order #398), so don't offer it.
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },

    # ── Kling ─────────────────────────────────────────────────────────────────

    "kl30": {   # Kling 3.0
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "kl03": {   # Kling 0.3 — Artlist's UI shows Image Reference as disabled
                # for this model (confirmed live, order #401), so don't offer it.
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "klmc": {   # Kling 3.0 Motion Control — input_urls (character image) is
                # required by kie.ai; video_urls is optional motion reference
        "start_frame": True, "end_frame": False,
        "start_frame_required": True,
        "vid_refs": 1,
    },
    "klve": {   # Kling O3 Video Edit — video reference is mandatory
                # (confirmed live, order #521: Artlist shows red warning and
                # never starts generation without it; times out after 20 min)
        "vid_refs": 1,
        "vid_ref_required": True,
        "max_vid_duration": 10,
        "prompt_label": "Upload a 3–10 second video and describe the edits you want to make",
    },

    # ── Avatar ────────────────────────────────────────────────────────────────

    "hga4": {   # HeyGen Avatar 4
        "img_refs": 1, "aud_refs": 1,
        "no_prompt": True,
        "img_required": True,
        "aud_required": True,
        "hint": "Upload a character image and a voice recording to make your avatar talk",
    },
    "hgtr": {   # HeyGen Translate — requires video
        "vid_refs": 1, "vid_ref_required": True,
        "no_prompt": True,
        "hint": "Upload a video to translate it with AI lip-sync",
    },
    "eldb": {   # ElevenLabs Dubbing — requires video
        "vid_refs": 1, "vid_ref_required": True,
        "no_prompt": True,
        "hint": "Upload a video to dub it into another language",
    },
    "lips": {   # Lipsync v2 Pro — requires video + audio
        "vid_refs": 1, "aud_refs": 1,
        "no_prompt": True,
        "vid_ref_required": True,
        "aud_required": True,
        "hint": "Upload a video of a character and a voice recording to sync lips",
    },
    "omni": {   # OmniHuman 1.5 — requires image + audio
        "img_refs": 1, "aud_refs": 1,
        "no_prompt": True,
        "img_required": True,
        "aud_required": True,
        "hint": "Upload a character image and a voice recording to animate your avatar",
    },
    "aur1": {   # Aurora Avatar — requires image + audio
        "img_refs": 1, "aud_refs": 1,
        "img_required": True,
        "aud_required": True,
        "prompt_label": "Describe your character's expressions and gestures (optional)",
        "hint": "Upload a character image and a voice recording to make your avatar talk",
    },
}


def get_attach_config(tid: str) -> dict:
    return TOOL_ATTACHMENTS.get(tid, {})


def has_attachments(tid: str) -> bool:
    cfg = get_attach_config(tid)
    return bool(
        cfg.get("start_frame") or cfg.get("img_refs") or
        cfg.get("vid_refs") or cfg.get("aud_refs")
    )


# Telegram's Bot API hard-caps file downloads via getFile() at 20MB,
# regardless of our code — the worker later calls getFile() to fetch the
# file by file_id before uploading it to Artlist, and that call fails
# outright for anything bigger (order #299: video ref upload accepted
# here, queued, then failed in the worker 30+s later with "file is too
# big"). Checking file_size up front lets us reject it immediately with a
# clear reason instead of silently queueing a doomed order.
TELEGRAM_MAX_DOWNLOAD_BYTES = 20 * 1024 * 1024


def file_too_large(msg) -> bool:
    for media in (msg.video, msg.document, msg.audio, msg.voice, msg.animation):
        if media is not None:
            return bool(media.file_size) and media.file_size > TELEGRAM_MAX_DOWNLOAD_BYTES
    if msg.photo:
        largest = msg.photo[-1]
        return bool(largest.file_size) and largest.file_size > TELEGRAM_MAX_DOWNLOAD_BYTES
    return False


# Russian translations for per-tool hint / prompt_label text (English lives
# inline in TOOL_ATTACHMENTS above and is used as the lookup key / default).
_HINT_RU = {
    "Attach a Start Frame to continue — it's required for this model.":
        "Прикрепите Start Frame, чтобы продолжить — для этой модели это обязательно.",
    "Sora 2 Pro is highly unstable. Switch to another model if it fails.":
        "Sora 2 Pro работает нестабильно. Если генерация не удалась, попробуйте другую модель.",
    "Attach a photo of your character — the model will animate it.":
        "Прикрепите фото персонажа — модель создаст его анимацию.",
    "Optional: attach a photo as a style reference.":
        "Необязательно: прикрепите фото как стилевой референс.",
    "Upload a character image and a voice recording to make your avatar talk":
        "Загрузите изображение персонажа и аудиозапись голоса, чтобы аватар заговорил",
    "Upload a video to translate it with AI lip-sync":
        "Загрузите видео, чтобы перевести его с AI липсинком",
    "Upload a video to dub it into another language":
        "Загрузите видео, чтобы озвучить его на другом языке",
    "Upload a video of a character and a voice recording to sync lips":
        "Загрузите видео персонажа и аудиозапись голоса для синхронизации губ",
    "Upload a character image and a voice recording to animate your avatar":
        "Загрузите изображение персонажа и аудиозапись голоса, чтобы анимировать аватар",
}

_PROMPT_LABEL_RU = {
    "Upload a 3–10 second video and describe the edits you want to make":
        "Загрузите видео длительностью 3–10 секунд и опишите, какие правки нужны",
    "Describe your character's expressions and gestures (optional)":
        "Опишите мимику и жесты персонажа (необязательно)",
}

_DEFAULT_HINT_RU = "Прикрепите референс-файлы (необязательно)\n  или сразу переходите к промпту.\n\n  Максимальный размер файла: 20 МБ."
_DEFAULT_HINT_AR = "أرفق ملفات مرجعية (اختياري)\n  أو انتقل مباشرة إلى البروم بت.\n\n  الحد الأقصى لحجم الملف: 20 ميغابايت."
_DEFAULT_PROMPT_LABEL_RU = "Введите промпт:"

_HINT_AR = {
    "Attach a Start Frame to continue — it's required for this model.":
        "أرفق إطار البداية للمتابعة — وهو مطلوب لهذا النموذج.",
    "Sora 2 Pro is highly unstable. Switch to another model if it fails.":
        "Sora 2 Pro غير مستقرة للغاية. انتقل إلى نموذج آخر إذا فشلت.",
    "Attach a photo of your character — the model will animate it.":
        "أرفق صورة شخصيتك — سيقوم النموذج بتحريكها.",
    "Optional: attach a photo as a style reference.":
        "اختياري: أرفق صورة كمرجع أسلوبي.",
    "Upload a character image and a voice recording to make your avatar talk":
        "ارفع صورة الشخصية وتسجيلاً صوتياً لجعل الأفاتار يتحدث",
    "Upload a video to translate it with AI lip-sync":
        "ارفع فيديو لترجمته مع مزامنة الشفاه بالذكاء الاصطناعي",
    "Upload a video to dub it into another language":
        "ارفع فيديو لدبلجته إلى لغة أخرى",
    "Upload a video of a character and a voice recording to sync lips":
        "ارفع فيديو الشخصية وتسجيلاً صوتياً لمزامنة الشفاه",
    "Upload a character image and a voice recording to animate your avatar":
        "ارفع صورة الشخصية وتسجيلاً صوتياً لتحريك الأفاتار",
}


def get_hint(tid: str, lang: str, default_en: str) -> str:
    en = get_attach_config(tid).get("hint", default_en)
    if lang == "ru":
        return _HINT_RU.get(en, _DEFAULT_HINT_RU if en == default_en else en)
    if lang == "ar":
        return _HINT_AR.get(en, _DEFAULT_HINT_AR if en == default_en else en)
    return en


def get_prompt_label(tid: str, lang: str, default_en: str) -> str:
    en = get_attach_config(tid).get("prompt_label", default_en)
    if lang == "ru":
        return _PROMPT_LABEL_RU.get(en, _DEFAULT_PROMPT_LABEL_RU if en == default_en else en)
    return en
