import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = 5613493357
USDT_WALLET = "TGZu7K7kfqtNMTqCABfByLceuA49qRvLgo"
YOOMONEY_WALLET = "4100119559974790"
YOOMONEY_SECRET = os.environ.get("YOOMONEY_SECRET", "")
CARD_NUMBER = "5599002140486392"

COIN_TO_USD = 0.05        # 1 coin = $0.05
USD_TO_COINS = 20         # $1 = 20 coins
COIN_TO_RUB = 3.70        # 1 coin = 3.70 ₽
MIN_TOPUP_RUB = 185.0     # minimum 50 coins
WELCOME_BONUS = 5         # coins on first start
REFERRAL_JOIN_BONUS = 0   # extra coins for new user who joined via referral link
MIN_TOPUP_USD = 2.0       # minimum top-up
REFERRAL_PERCENT = 20     # 20% of referral top-up (legacy, tiers used instead)

# Tiered referral percentages based on number of referrals who made a purchase (buyers)
REFERRAL_TIERS = [
    {"min": 0,  "next": 6,  "first": 20, "repeat": 10, "name_en": "Starter", "name_ru": "Стартер"},
    {"min": 6,  "next": 16, "first": 22, "repeat": 12, "name_en": "Partner", "name_ru": "Партнёр"},
    {"min": 16, "next": None,"first": 25, "repeat": 15, "name_en": "Pro",     "name_ru": "Про"},
]

def usd_to_coins(usd: float) -> int:
    return round(usd / COIN_TO_USD)

def coins_to_usd(coins: int) -> float:
    return round(coins * COIN_TO_USD, 2)

# ─── IMAGE TOOLS ──────────────────────────────────────────────
IMAGE_TOOLS = {
    "Nano Banana Pro": {
        "emoji": "🍌",
        "max_refs": 14,
        "desc": "High-quality image generation with wide aspect ratio support",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"],
        "quality": ["1K","2K","4K"],
        "pricing": {"1K": 0.117, "2K": 0.117, "4K": 0.156},
        "coins_by_quality": {"1K": 3, "2K": 3, "4K": 4},
    },
    "Nano Banana 2": {
        "emoji": "🍌",
        "max_refs": 14,
        "desc": "Fast image generation with extended aspect ratio support",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9","1:4","4:1","1:8","8:1"],
        "quality": ["1K","2K","4K"],
        "pricing": {"1K": 0.052, "2K": 0.078, "4K": 0.117},
        "coins_by_quality": {"1K": 2, "2K": 2, "4K": 3},
    },
    "Seedream 5.0 Pro": {
        "emoji": "✦",
        "max_refs": 9,
        "desc": "Advanced AI image synthesis with cinematic quality",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"],
        "quality": ["1K","2K"],
        "pricing": {"1K": 0.0455, "2K": 0.091},
        "coins_by_quality": {"1K": 1, "2K": 2},
    },
    "GPT Image 2": {
        "emoji": "◈",
        "max_refs": 6,
        "desc": "OpenAI's latest image generation model",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9","21:9"],
        "quality": ["1K","2K","4K"],
        "pricing": {"1K": 0.039, "2K": 0.065, "4K": 0.104},
        "coins_by_quality": {"1K": 1, "2K": 2, "4K": 3},
    },
    "Wan 2.7 Pro": {
        "emoji": "◈",
        "max_refs": 9,
        "desc": "Professional image generation in 4K",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["4K"],
        "pricing": {"per_gen": 0.078},
        "coins": 2,
    },
    "Flux 2.0 Pro": {
        "emoji": "⚡",
        "max_refs": 10,
        "desc": "Premium photorealistic image generation",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["1K","2K"],
        "pricing": {"1K": 0.033, "2K": 0.046},
        "coins_by_quality": {"1K": 1, "2K": 1},
    },
    "Ideogram v3": {
        "emoji": "◎",
        "desc": "Creative AI with exceptional text rendering",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["TURBO","BALANCED","QUALITY"],
        "pricing": {"TURBO": 0.023, "BALANCED": 0.046, "QUALITY": 0.065},
        "coins_by_quality": {"TURBO": 1, "BALANCED": 1, "QUALITY": 2},
    },
    "Topaz Image Upscaler": {
        "emoji": "🔎",
        "max_refs": 1,
        "desc": "AI-powered image upscaling — 2K, 4K, and 8K output quality",
        "requires_ref": True,
        "quality": ["2K","4K","8K"],
        "pricing": {"2K": 0.065, "4K": 0.13, "8K": 0.26},
        "coins_by_quality": {"2K": 2, "4K": 3, "8K": 6},
    },
}

# ─── VIDEO TOOLS ──────────────────────────────────────────────
# Seedance 2.0 prices per resolution/duration
SEEDANCE_20_PRICES = {
    "480p": {4:0.49,5:0.62,6:0.74,7:0.86,8:0.99,9:1.11,10:1.24,11:1.36,12:1.48,13:1.61,14:1.73,15:1.85},
    "720p": {4:1.07,5:1.33,6:1.60,7:1.87,8:2.13,9:2.40,10:2.67,11:2.93,12:3.20,13:3.46,14:3.73,15:4.00},
    "1080p":{4:2.65,5:3.32,6:3.98,7:4.64,8:5.30,9:5.97,10:6.63,11:7.29,12:7.96,13:8.62,14:9.28,15:9.95},
    "4K":   {4:5.41,5:6.76,6:8.11,7:9.46,8:10.82,9:12.17,10:13.52,11:14.87,12:16.22,13:17.58,14:18.93,15:20.28},
}
SEEDANCE_20_FAST_PRICES = {
    "480p": {4:0.40,5:0.50,6:0.60,7:0.71,8:0.81,9:0.91,10:1.01,11:1.11,12:1.21,13:1.31,14:1.41,15:1.51},
    "720p": {4:0.86,5:1.07,6:1.29,7:1.50,8:1.72,9:1.93,10:2.15,11:2.36,12:2.57,13:2.79,14:3.00,15:3.22},
}

# kie.ai tokens-per-second WITH a reference video attached (×0.005 → USD, ×1.30 → our price)
VIDEO_REF_RATES = {
    "sd20":  {"4K": 128.0, "1080p": 62.0, "720p": 25.0, "480p": 11.5},
    "sd20f": {"720p": 20.0, "480p": 9.0},
}

def calc_video_ref_usd(tid: str, res: str, output_sec: int, ref_sec: int) -> float:
    """Return our price (USD) for sd20/sd20f when a reference video is attached."""
    rate = VIDEO_REF_RATES.get(tid, {}).get(res, 0.0)
    if rate == 0.0:
        return 0.0
    return (output_sec + ref_sec) * rate * 0.005 * 1.30
HAPPY_HORSE_PRICES = {
    "720p": {3:0.44,4:0.59,5:0.73,6:0.88,7:1.02,8:1.17,9:1.32,10:1.46,11:1.61,12:1.76,13:1.90,14:2.05,15:2.19},
    "1080p":{3:0.57,4:0.75,5:0.94,6:1.13,7:1.32,8:1.51,9:1.70,10:1.89,11:2.07,12:2.26,13:2.45,14:2.64,15:2.83},
}
VEO_31_PRICES = {
    "720p": {4:1.63,6:1.63,8:1.63},
    "1080p":{4:1.66,6:1.66,8:1.66},
    "4K":   {4:2.41,6:2.41,8:2.41},
}
VEO_31_FAST_PRICES = {
    "720p": {4:0.39,6:0.39,8:0.39},
    "1080p":{4:0.42,6:0.42,8:0.42},
    "4K":   {4:1.17,6:1.17,8:1.17},
}
VEO_31_LITE_PRICES = {
    "720p": {4:0.20,6:0.20,8:0.20},
    "1080p":{4:0.23,6:0.23,8:0.23},
}
KLING_30_VIDEO_PRICES = {
    "720p": {3:0.39,4:0.52,5:0.65,6:0.78,7:0.91,8:1.04,9:1.17,10:1.30,11:1.43,12:1.56,13:1.69,14:1.82,15:1.95},
    "1080p":{3:0.53,4:0.70,5:0.88,6:1.05,7:1.23,8:1.40,9:1.58,10:1.76,11:1.93,12:2.11,13:2.28,14:2.46,15:2.63},
    "4K":   {3:1.31,4:1.74,5:2.18,6:2.61,7:3.05,8:3.48,9:3.92,10:4.36,11:4.79,12:5.23,13:5.66,14:6.10,15:6.53},
}
KLING_03_VIDEO_PRICES = KLING_30_VIDEO_PRICES  # same pricing
KLING_30_MOTION_CONTROL_PRICES = KLING_30_VIDEO_PRICES  # same pricing, fixed at 1080p
WAN_27_PRICES = {
    "720p": {2:0.21,3:0.31,4:0.42,5:0.52,6:0.62,7:0.73,8:0.83,9:0.94,10:1.04,11:1.14,12:1.25,13:1.35,14:1.46,15:1.56},
    "1080p":{2:0.31,3:0.47,4:0.62,5:0.78,6:0.94,7:1.09,8:1.25,9:1.40,10:1.56,11:1.72,12:1.87,13:2.03,14:2.18,15:2.34},
}
SORA_2_PRO_PRICES = {
    "720p": {4:1.30,8:2.60,12:3.90},
    "1080p":{4:1.90,8:3.80,12:5.70},
}
LTX_23_PRICES = {
    "720p": {6:0.30,8:0.40,10:0.50},
    "1080p":{6:0.60,8:0.80,10:1.00},
    "2K":   {6:1.20,8:1.60,10:2.00},
    "4K":   {6:2.25,8:3.00,10:3.75},
}
GROK_IMAGINE_15_PRICES = {sec: round(sec*0.20,2) for sec in range(1,16)}
GROK_TV_PRICES = {sec: round(sec*0.20,2) for sec in [6,8,10,12,15,20,25,30]}
GROK_IV_PRICES = GROK_TV_PRICES
GROK_UPSCALE_PRICES = {"720p": 0.50, "1080p": 1.00}
GROK_EXTEND_PRICES = {6: 1.50, 10: 2.50}
HEYGEN_AVATAR_PRICES = {
    1: 3.00, 2: 6.00, 3: 9.00, 4: 12.00, 5: 15.00,
    6: 18.00, 7: 21.00, 8: 23.00, 9: 26.00, 10: 29.00,
    11: 32.00, 12: 35.00, 13: 38.00, 14: 41.00, 15: 44.00,
}
HEYGEN_TRANSLATE_PRICES = {i:round(i*0.20,2) for i in range(1,16)}
HEYGEN_TRANSLATE_PRECISION_PRICES = {
    1: 3.00, 2: 6.00, 3: 9.00, 4: 12.00, 5: 15.00,
    6: 18.00, 7: 21.00, 8: 23.00, 9: 26.00, 10: 29.00,
    11: 32.00, 12: 35.00, 13: 38.00, 14: 41.00, 15: 44.00,
}
HEYGEN_TRANSLATE_SPEED_PRICES = {
    1: 1.50, 2: 3.00, 3: 4.50, 4: 6.00, 5: 7.50,
    6: 9.00, 7: 10.50, 8: 12.00, 9: 13.50, 10: 15.00,
    11: 16.50, 12: 18.00, 13: 19.50, 14: 21.00, 15: 22.50,
}
HEYGEN_AVATAR_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]
HEYGEN_AVATAR_RESOLUTIONS = ["720p", "1080p"]
HEYGEN_AVATAR_TALKING_STYLES = ["Stable", "Expressive"]
ELEVENLABS_DUBBING_PRICES = {
    1: 3.00, 2: 6.00, 3: 9.00, 4: 12.00, 5: 15.00,
    6: 18.00, 7: 21.00, 8: 23.00, 9: 26.00, 10: 29.00,
    11: 32.00, 12: 35.00, 13: 38.00, 14: 41.00, 15: 44.00,
}
LIPSYNC_PRICES = {
    1: 3.00, 2: 6.00, 3: 9.00, 4: 12.00, 5: 15.00,
    6: 18.00, 7: 21.00, 8: 23.00, 9: 26.00, 10: 29.00,
    11: 32.00, 12: 35.00, 13: 38.00, 14: 41.00, 15: 44.00,
}

HEYGEN_TRANSLATE_LANGUAGES = [
    "English","Spanish","French","Italian","German","Polish","Portuguese",
    "Chinese","Japanese","Korean","Arabic","Filipino","Indonesian","Russian",
    "Dutch","Swedish","Danish","Romanian","Ukrainian","Greek","Croatian",
    "Bulgarian","Slovak","Turkish","Hindi","Tamil",
]
ELEVENLABS_DUBBING_LANGUAGES = [
    "English","Chinese","Spanish","Hindi","Portuguese","French","German",
    "Japanese","Arabic","Russian","Korean","Indonesian","Italian","Dutch",
    "Turkish","Polish","Swedish","Filipino","Malay","Romanian","Ukrainian",
    "Greek","Czech","Danish","Finnish","Bulgarian","Croatian","Slovak","Tamil",
]
OMNIHUMAN_PRICES = {
    1: 3.00, 2: 6.00, 3: 9.00, 4: 12.00, 5: 15.00,
    6: 18.00, 7: 21.00, 8: 23.00, 9: 26.00, 10: 29.00,
    11: 32.00, 12: 35.00, 13: 38.00, 14: 41.00, 15: 44.00,
}

AURORA_AVATAR_PRICES = {
    1: 2.7, 2: 5.4, 3: 8.1, 4: 10.8, 5: 13.5,
    6: 16.2, 7: 18.9, 8: 20.7, 9: 23.4, 10: 26.1,
    11: 28.8, 12: 31.5, 13: 34.2, 14: 36.9, 15: 39.6,
}

# ─── SUNO MUSIC ────────────────────────────────────────────────
SUNO_MUSIC_MODELS = {
    "V4":       {"coins": 4,  "usd": 0.20, "label": "Suno V4",        "emoji": "◈"},
    "V4_5":     {"coins": 8,  "usd": 0.40, "label": "Suno V4.5",      "emoji": "◈"},
    "V4_5PLUS": {"coins": 12, "usd": 0.60, "label": "Suno V4.5 Plus", "emoji": "✦"},
    "V5":       {"coins": 10, "usd": 0.50, "label": "Suno V5",        "emoji": "✦"},
    "V5_5":     {"coins": 15, "usd": 0.75, "label": "Suno V5.5",      "emoji": "♛"},
}
SUNO_VOCAL_TYPES = {
    "separate_vocal":      {"coins": 10, "usd": 0.50,
                            "label_en": "2-Stem (Vocal + Instrumental)",
                            "label_ru": "2 трека (Голос + Инструментал)",
                            "label_ar": "مسارَين (صوت + موسيقى)"},
    "split_stem":          {"coins": 50, "usd": 2.50,
                            "label_en": "12-Stem Full Breakdown",
                            "label_ru": "12 треков (полное разделение)",
                            "label_ar": "12 مساراً (تقسيم كامل)"},
    "split_stem_advanced": {"coins": 20, "usd": 1.00,
                            "label_en": "Single Stem Extraction",
                            "label_ru": "Извлечь один трек",
                            "label_ar": "استخراج مسار واحد"},
}
SUNO_LYRICS_PRICE = {"coins": 2, "usd": 0.10}

# ─── RUNWAY ────────────────────────────────────────────────────
# kie.ai cost × 1.30 markup: 720p/5s=$0.06, 720p/10s=$0.15, 1080p/5s=$0.15, 1080p/10s=$0.15
RUNWAY_ALEPH_PRICE: float = 0.72   # kie.ai $0.55 × 1.30
RUNWAY_PRICES = {
    "720p":  {5: 0.08, 10: 0.20},
    "1080p": {5: 0.20, 10: 0.20},
}

# ─── MINIMAX H3 ────────────────────────────────────────────────
# kie.ai rates: 768P=$0.1125/sec, 2K=$0.1825/sec — × 1.30 markup
MINIMAX_H3_PRICES = {
    "768P": {4:0.59,5:0.73,6:0.88,7:1.02,8:1.17,9:1.32,10:1.46,11:1.61,12:1.76,13:1.90,14:2.05,15:2.19},
    "2K":   {4:0.95,5:1.19,6:1.42,7:1.66,8:1.90,9:2.14,10:2.37,11:2.61,12:2.85,13:3.08,14:3.32,15:3.56},
}
# Additional charge when a video reference is attached (kie.ai charges same per-sec rate for input)
MINIMAX_H3_VIDEO_REF_RATES = {"768P": 0.14625, "2K": 0.23725}

# ─── TOPAZ VIDEO UPSCALE ──────────────────────────────────────
# kie.ai rates: 1x/2x=$0.04/sec, 4x=$0.07/sec — × 1.30 markup
TOPAZ_VIDEO_UPSCALE_RATES = {"2": 0.052, "4": 0.091}

# ─── UNLIMITED PASS ───────────────────────────────────────────
RESOLUTION_ORDER = ["480p", "720p", "1080p", "2K", "4K"]

UNLIMITED_TIER_CONFIG = {
    "standard": {
        "name_ru": "Стандарт",
        "name_en": "Standard",
        "emoji": "⚡",
        "subcats": ["Standard", "Kling"],
        "subcat_overrides": {
            "Standard": ["sd20f", "wan27", "veo31l", "grokimag"],
        },
        "max_resolution": "720p",
        "voiceover": False,
    },
    "pro": {
        "name_ru": "Про",
        "name_en": "Pro",
        "emoji": "⚡⚡",
        "subcats": ["Standard", "Kling", "Premium"],
        "max_resolution": "1080p",
        "voiceover": True,
    },
    "vip": {
        "name_ru": "VIP",
        "name_en": "VIP",
        "emoji": "♛",
        "subcats": ["Standard", "Kling", "Premium"],
        "max_resolution": "4K",
        "voiceover": True,
    },
}

# Coin prices per tier × duration (hours)
# Standard: 990₽/hr · Pro: 2450₽/hr · VIP: 5990₽/hr (1 coin = 3.70₽)
# 2hr = 10% cheaper per hour · 3hr = 20% cheaper per hour
UNLIMITED_PLANS = {
    "standard": {1: 268, 2: 482, 3: 642},
    "pro":      {1: 662, 2: 1192, 3: 1589},
    "vip":      {1: 1619, 2: 2914, 3: 3886},
}

def filter_resolutions(resolutions: list, max_res: str) -> list:
    """Filter resolution list to only include options up to max_res."""
    if max_res not in RESOLUTION_ORDER:
        return resolutions
    max_idx = RESOLUTION_ORDER.index(max_res)
    result = []
    for r in resolutions:
        if r not in RESOLUTION_ORDER:
            result.append(r)
        elif RESOLUTION_ORDER.index(r) <= max_idx:
            result.append(r)
    return result

