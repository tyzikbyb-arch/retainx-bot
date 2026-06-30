"""
Catalog of Artlist Voice Catalog voices used to fulfil voiceover orders.

Sourced from a full export of toolkit.artlist.io's
`mediaCatalogRouter.getVoiceById` API (see data/artlist_voices.json) —
73 real voices, each with the TTS models it supports and, per model, the
languages it can speak together with a real preview-audio URL (signed,
long-lived CDN links straight from Artlist) so a customer can listen to a
voice before placing an order.

Only the four "pick-a-voice" text-to-speech models are exposed here.
Artlist's catalog also lists Cartesia Voice Changer (speech-to-speech) and
Minimax Voice Clone (voice cloning) under "Voice Over" — neither lets a
customer pick one of these 73 voices, so they're intentionally excluded.
"""

import json
import os

CATEGORIES = [
    "Social", "Tutorials", "Documentaries", "Trailers",
    "Explainers", "Characters", "Commercials", "Health & Wellness",
]

GENDERS = ["MALE", "FEMALE", "NEUTRAL"]

AGE_ORDER = ["CHILD", "TEEN", "YOUNG_ADULT", "ADULT", "MIDDLE_AGED", "SENIOR"]

# Model group id -> display info, in the order they should be offered.
MODELS = {
    206: {"name": "Eleven v3", "tags": ["Experimental", "Creative Control"]},
    311: {"name": "Eleven Multilingual v2", "tags": ["Stable", "Professional"]},
    6:   {"name": "MiniMax 02 HD", "tags": ["Consistent", "Cinematic"]},
    200: {"name": "Cartesia Sonic 2", "tags": ["Expressive", "Lifelike"]},
}
MODEL_ORDER = [206, 311, 6, 200]

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "artlist_voices.json")
with open(_DATA_PATH, encoding="utf-8") as _f:
    VOICE_CATALOG = json.load(_f)

_BY_ID = {v["id"]: v for v in VOICE_CATALOG}


def list_models() -> list[dict]:
    return [{"id": mid, **MODELS[mid]} for mid in MODEL_ORDER]


def get_model(model_id: int) -> dict | None:
    if model_id not in MODELS:
        return None
    return {"id": model_id, **MODELS[model_id]}


def get_voice(voice_id: int) -> dict | None:
    return _BY_ID.get(voice_id)


def _supports(voice: dict, model_id: int) -> bool:
    return str(model_id) in voice["models"]


def list_categories(model_id: int) -> list[str]:
    present = {c for v in VOICE_CATALOG if _supports(v, model_id) for c in v["categories"]}
    return [c for c in CATEGORIES if c in present]


def list_genders(model_id: int, category: str) -> list[str]:
    present = {
        v["gender"] for v in VOICE_CATALOG
        if _supports(v, model_id) and category in v["categories"]
    }
    return [g for g in GENDERS if g in present]


def list_ages(model_id: int, category: str, gender: str) -> list[str]:
    present = {
        v["age"] for v in VOICE_CATALOG
        if _supports(v, model_id) and category in v["categories"] and v["gender"] == gender
    }
    return [a for a in AGE_ORDER if a in present]


def list_voices(model_id: int, category: str, gender: str, age: str) -> list[dict]:
    return sorted(
        (v for v in VOICE_CATALOG
         if _supports(v, model_id) and category in v["categories"]
         and v["gender"] == gender and v["age"] == age),
        key=lambda v: v["name"],
    )


def list_languages(voice_id: int, model_id: int) -> list[dict]:
    voice = _BY_ID.get(voice_id)
    if not voice:
        return []
    model = voice["models"].get(str(model_id))
    if not model:
        return []
    return model["languages"]


def get_preview_url(voice_id: int, model_id: int, language_name: str | None = None) -> str | None:
    """Preview audio URL for (voice, model, language). Falls back to the
    model's default-language preview if the requested language has none."""
    langs = list_languages(voice_id, model_id)
    if not langs:
        return None
    if language_name:
        match = next((l for l in langs if l["name"] == language_name), None)
        if match and match["preview_url"]:
            return match["preview_url"]
    default = next((l for l in langs if l["is_default"]), None)
    return default["preview_url"] if default else None
