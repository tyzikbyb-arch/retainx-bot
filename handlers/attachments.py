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
    "grok": {   # Grok Imagine 1.5 — Start Frame only, mandatory. No End Frame
                # button at all for this tool. img_refs intentionally omitted:
                # it would let a user satisfy the attach screen via a plain
                # Image Reference while never providing the required Start
                # Frame, since exclusive_startend hides each alternative once
                # the other is chosen — a dead end the menu can't recover from.
        "start_frame": True, "end_frame": False,
        "start_frame_required": True,
        "hint": "Attach a Start Frame to continue — it's required for this model.",
    },

    # ── Premium video ─────────────────────────────────────────────────────────

    "veo31": {  # Veo 3.1 — Artlist's UI doesn't expose Image Reference for
                # this model (confirmed live by hand, order #373: button
                # rendered as disabled in the panel), so don't offer it.
        "start_frame": True, "end_frame": True,
        "exclusive_startend": True,
    },
    "veo31f": { # Veo 3.1 Fast
        "start_frame": True, "end_frame": True,
        "img_refs": 3,
        "exclusive_startend": True,
    },
    "veo31l": { # Veo 3.1 Lite
        "start_frame": True, "end_frame": True,
        "img_refs": 1,
        "exclusive_startend": True,
    },
    "veo31e": { # Veo 3.1 Extend — requires video
        "vid_refs": 1, "vid_ref_required": True,
        "prompt_label": "Upload a 2–30 second video and describe what happens next",
        "hint": "Works best with videos created using Veo models",
    },
    "sora2": {  # Sora 2 Pro — no End Frame button for this tool
        "start_frame": True, "end_frame": False,
        "hint": "Sora 2 Pro is highly unstable. Switch to another model if it fails.",
    },
    "ltx23": {  # LTX 2.3 Pro
        "start_frame": True, "end_frame": True,
        "img_refs": 1,
        "exclusive_startend": True,
    },

    # ── Kling ─────────────────────────────────────────────────────────────────

    "kl30": {   # Kling 3.0
        "start_frame": True, "end_frame": True,
        "img_refs": 1,
        "exclusive_startend": True,
    },
    "kl03": {   # Kling 0.3
        "start_frame": True, "end_frame": True,
        "img_refs": 1,
        "exclusive_startend": True,
    },
    "klmc": {   # Kling 3.0 Motion Control
        "img_refs": 1, "vid_refs": 1,
        "hint": "Upload an image reference and/or a motion reference video",
    },
    "klve": {   # Kling 3.0 Video Edit
        "img_refs": 4, "vid_refs": 1,
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
    "fab1": {   # Fabric 1.0 Avatar — requires image
        "img_refs": 1,
        "img_required": True,
        "hint": "Upload a character image to generate an avatar video",
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
    "Works best with videos created using Veo models":
        "Лучше всего работает с видео, созданными моделями Veo",
    "Sora 2 Pro is highly unstable. Switch to another model if it fails.":
        "Sora 2 Pro работает нестабильно. Если генерация не удалась, попробуйте другую модель.",
    "Upload an image reference and/or a motion reference video":
        "Загрузите референс-изображение и/или референс-видео движения",
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
    "Upload a character image to generate an avatar video":
        "Загрузите изображение персонажа, чтобы создать видео-аватар",
}

_PROMPT_LABEL_RU = {
    "Upload a 2–30 second video and describe what happens next":
        "Загрузите видео длительностью 2–30 секунд и опишите, что будет дальше",
    "Upload a 3–10 second video and describe the edits you want to make":
        "Загрузите видео длительностью 3–10 секунд и опишите, какие правки нужны",
    "Describe your character's expressions and gestures (optional)":
        "Опишите мимику и жесты персонажа (необязательно)",
}

_DEFAULT_HINT_RU = "Прикрепите референс-файлы (необязательно)\n  или сразу переходите к промпту."
_DEFAULT_PROMPT_LABEL_RU = "Введите промпт:"


def get_hint(tid: str, lang: str, default_en: str) -> str:
    en = get_attach_config(tid).get("hint", default_en)
    if lang == "ru":
        return _HINT_RU.get(en, _DEFAULT_HINT_RU if en == default_en else en)
    return en


def get_prompt_label(tid: str, lang: str, default_en: str) -> str:
    en = get_attach_config(tid).get("prompt_label", default_en)
    if lang == "ru":
        return _PROMPT_LABEL_RU.get(en, _DEFAULT_PROMPT_LABEL_RU if en == default_en else en)
    return en
