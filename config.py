import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = 5613493357
USDT_WALLET = "TGZu7K7kfqtNMTqCABfByLceuA49qRvLgo"

COIN_TO_USD = 0.05        # 1 coin = $0.05
USD_TO_COINS = 20         # $1 = 20 coins
WELCOME_BONUS = 20        # coins on first start
MIN_TOPUP_USD = 2.0       # minimum top-up
REFERRAL_PERCENT = 20     # 20% of referral top-up

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
        "pricing": {"per_gen": 0.09},  # $0.09 = 2 coins (rounded up to 2)
        "coins": 2,
    },
    "Nano Banana": {
        "emoji": "🍌",
        "max_refs": 14,
        "desc": "Fast image generation with extended aspect ratio support",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9","1:4","4:1","1:8","8:1"],
        "quality": ["1K","2K","4K"],
        "pricing": {"per_gen": 0.05},
        "coins": 1,
    },
    "Seedream 5.0": {
        "emoji": "✦",
        "max_refs": 9,
        "desc": "Advanced AI image synthesis with cinematic quality",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"],
        "quality": ["1K","2K","4K"],
        "pricing": {"per_gen": 0.05},
        "coins": 1,
    },
    "GPT Image 2": {
        "emoji": "◈",
        "max_refs": 6,
        "desc": "OpenAI's latest image generation model",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9","21:9"],
        "quality": ["Medium","High"],
        "pricing": {"Medium": 0.05, "High": 0.29},
        "coins_by_quality": {"Medium": 1, "High": 6},
    },
    "Kling Image 3.0": {
        "emoji": "◉",
        "max_refs": 1,
        "desc": "Kling's powerful image generation engine",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"],
        "quality": ["1K","2K"],
        "pricing": {"per_gen": 0.05},
        "coins": 1,
    },
    "Kling Image 0.3": {
        "emoji": "◉",
        "max_refs": 10,
        "desc": "Kling's ultra-quality image model with 4K support",
        "aspect_ratios": ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"],
        "quality": ["1K","2K","4K"],
        "pricing": {"2K": 0.05, "4K": 0.09},
        "coins_by_quality": {"1K": 1, "2K": 1, "4K": 2},
    },
    "Wan 2.7 Pro Image": {
        "emoji": "◈",
        "max_refs": 9,
        "desc": "Professional image generation in 4K",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["4K"],
        "pricing": {"per_gen": 0.09},
        "coins": 2,
    },
    "Flux 2.0 Pro": {
        "emoji": "⚡",
        "max_refs": 10,
        "desc": "Premium photorealistic image generation",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["1K","2K"],
        "pricing": {"per_gen": 0.09},
        "coins": 2,
    },
    "Ideogram v3": {
        "emoji": "◎",
        "desc": "Creative AI with exceptional text rendering",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "pricing": {"per_gen": 0.09},
        "coins": 2,
    },

    "Hunyuan V3": {
        "emoji": "◉",
        "desc": "Tencent's advanced image generation system",
        "aspect_ratios": ["1:1","3:4","4:3","9:16","16:9"],
        "quality": ["1K"],
        "pricing": {"per_gen": 0.09},
        "coins": 2,
    },
}

# ─── VIDEO TOOLS ──────────────────────────────────────────────
# Seedance 2.0 prices per resolution/duration
SEEDANCE_20_PRICES = {
    "480p": {4:0.40,5:0.50,6:0.60,7:0.70,8:0.80,9:0.90,10:1.00,11:1.10,12:1.20,13:1.30,14:1.40,15:1.50},
    "720p": {4:0.60,5:0.75,6:0.90,7:1.05,8:1.20,9:1.35,10:1.50,11:1.65,12:1.80,13:1.95,14:2.10,15:2.25},
    "1080p":{4:1.20,5:1.50,6:1.80,7:2.10,8:2.40,9:2.70,10:3.00,11:3.30,12:3.60,13:3.90,14:4.20,15:4.50},
}
SEEDANCE_20_FAST_PRICES = {
    "480p": {4:0.25,5:0.30,6:0.35,7:0.40,8:0.45,9:0.50,10:0.55,11:0.60,12:0.65,13:0.70,14:0.75,15:0.80},
    "720p": {4:0.60,5:0.75,6:0.90,7:1.05,8:1.20,9:1.35,10:1.50,11:1.65,12:1.80,13:1.95,14:2.10,15:2.25},
}
HAPPY_HORSE_PRICES = {
    "720p": {3:0.50,4:0.80,5:1.00,6:1.20,7:1.40,8:1.60,9:1.80,10:2.00,11:2.20,12:2.40,13:2.60,14:2.80,15:3.00},
    "1080p":{3:0.90,4:1.20,5:1.50,6:1.80,7:2.10,8:2.40,9:2.70,10:3.00,11:3.30,12:3.60,13:3.90,14:4.20,15:4.50},
}
VEO_31_PRICES = {
    "720p": {4:0.75,6:1.20,8:1.60},
    "1080p":{4:0.75,6:1.20,8:1.60},
    "4K":   {4:1.50,6:2.20,8:2.90},
}
VEO_31_FAST_PRICES = {
    "720p": {4:0.40,6:0.60,8:0.80},
    "1080p":{4:0.40,6:0.60,8:0.80},
    "4K":   {4:1.00,6:1.50,8:2.00},
}
VEO_31_LITE_PRICES = {
    "720p": {4:0.15,6:0.20,8:0.25},
    "1080p":{4:0.20,6:0.30,8:0.40},
}
KLING_30_VIDEO_PRICES = {
    "720p": {3:0.20,4:0.25,5:0.30,6:0.35,7:0.40,8:0.45,9:0.50,10:0.55,11:0.60,12:0.65,13:0.70,14:0.75,15:0.80},
    "1080p":{3:0.25,4:0.30,5:0.40,6:0.45,7:0.50,8:0.60,9:0.65,10:0.75,11:0.85,12:0.90,13:1.00,14:1.05,15:1.10},
    "4K":   {3:0.75,4:1.00,5:1.25,6:1.50,7:1.75,8:2.00,9:2.25,10:2.50,11:2.75,12:3.00,13:3.25,14:3.50,15:3.75},
}
KLING_03_VIDEO_PRICES = KLING_30_VIDEO_PRICES  # same pricing
WAN_27_PRICES = {
    "720p": {2:0.20,3:0.30,4:0.40,5:0.50,6:0.60,7:0.70,8:0.80,9:0.90,10:1.00,11:1.10,12:1.20,13:1.30,14:1.40,15:1.50},
    "1080p":{2:0.30,3:0.45,4:0.60,5:0.75,6:0.90,7:1.05,8:1.20,9:1.35,10:1.50,11:1.65,12:1.80,13:1.95,14:2.10,15:2.25},
}
SORA_2_PRO_PRICES = {
    "720p": {4:1.30,8:2.60,12:3.90},
    "1080p":{4:1.90,8:3.80,12:5.70},
}
LTX_23_PRICES = {
    "1080p":{6:0.60,8:0.80,10:1.00},
    "2K":   {6:1.20,8:1.60,10:2.00},
    "4K":   {6:2.25,8:3.00,10:3.75},
}
GROK_IMAGINE_15_PRICES = {sec: round(sec*0.20,2) for sec in range(1,16)}
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
ELEVENLABS_DUBBING_PRICES = {i:round(i*0.20,2) for i in range(1,16)}
LIPSYNC_PRICES = {1:2.99,2:5.99,3:8.99,4:11.99,5:14.99}

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
