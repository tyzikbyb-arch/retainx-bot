from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import kb, back_btn, menu_btn, chunked
from database import get_coins, spend_coins, create_order
from config import (
    usd_to_coins,
    SEEDANCE_20_PRICES, SEEDANCE_20_FAST_PRICES, HAPPY_HORSE_PRICES,
    VEO_31_PRICES, VEO_31_FAST_PRICES, VEO_31_LITE_PRICES,
    KLING_30_VIDEO_PRICES, KLING_03_VIDEO_PRICES,
    WAN_27_PRICES, SORA_2_PRO_PRICES, LTX_23_PRICES,
    GROK_IMAGINE_15_PRICES, HEYGEN_AVATAR_PRICES, HEYGEN_TRANSLATE_PRICES,
    ELEVENLABS_DUBBING_PRICES, LIPSYNC_PRICES,
    HEYGEN_TRANSLATE_LANGUAGES, ELEVENLABS_DUBBING_LANGUAGES,
)
import math

router = Router()

class VideoStates(StatesGroup):
    entering_prompt = State()
    heygen_translate_lang = State()
    elevenlabs_lang = State()

# ── Video subcategories ───────────────────────────────────────
VIDEO_SUBCATS = {
    "Standard Video": ["Seedance 2.0","Seedance 2.0 Fast","Happy Horse 1.0","Wan 2.7"],
    "Premium Video":  ["Veo 3.1","Veo 3.1 Fast","Veo 3.1 Lite","Veo 3.1 Extend","Sora 2 Pro","LTX 2.3 Pro"],
    "Kling Video":    ["Kling 3.0","Kling 0.3","Kling 3.0 Motion Control","Kling 3.0 Video Edit"],
    "Avatar & Dub":   ["HeyGen Avatar 4","HeyGen Translate","ElevenLabs Dubbing","Lipsync v2 Pro","OmniHuman 1.5","Fabric 1.0 Avatar","Aurora Avatar","Grok Imagine 1.5"],
}

TOOL_DESCS = {
    "Seedance 2.0": "Cinematic video generation up to 1080p with audio",
    "Seedance 2.0 Fast": "Faster variant of Seedance 2.0 up to 720p",
    "Happy Horse 1.0": "Smooth motion video generation up to 1080p",
    "Wan 2.7": "Versatile video model with wide aspect ratio support",
    "Veo 3.1": "Google's flagship video model up to 4K",
    "Veo 3.1 Fast": "Veo 3.1 express mode — faster renders",
    "Veo 3.1 Lite": "Lightweight Veo model for quick generation",
    "Veo 3.1 Extend": "Extend existing video clips with Veo",
    "Sora 2 Pro": "OpenAI's advanced video generation model",
    "LTX 2.3 Pro": "High-framerate professional video generation",
    "Kling 3.0": "Kling's latest cinematic video model",
    "Kling 0.3": "Kling compact model — same quality, lighter",
    "Kling 3.0 Motion Control": "Precise motion control in 1080p, 30 sec",
    "Kling 3.0 Video Edit": "Edit and enhance existing video clips",
    "HeyGen Avatar 4": "Photorealistic talking avatar generation",
    "HeyGen Translate": "AI video translation with lip-sync",
    "ElevenLabs Dubbing": "Professional multilingual AI dubbing",
    "Lipsync v2 Pro": "Advanced lip-sync for any video",
    "OmniHuman 1.5": "Full-body human avatar animation",
    "Fabric 1.0 Avatar": "Premium avatar generation",
    "Aurora Avatar": "Realistic avatar video generation",
    "Grok Imagine 1.5": "Grok's video generation model",
}

@router.callback_query(F.data == "cat_video")
async def video_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    buttons = [[InlineKeyboardButton(text=f"▸  {sub}", callback_data=f"vsub_{sub}")] for sub in VIDEO_SUBCATS]
    buttons.append([back_btn("main_menu", "⌂  Main Menu")])
    await cb.message.edit_text(
        "◈  <b>Video Generation</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a category:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vsub_"))
async def video_subcat(cb: CallbackQuery, state: FSMContext):
    subcat = cb.data.replace("vsub_", "")
    tools = VIDEO_SUBCATS.get(subcat, [])
    buttons = [[InlineKeyboardButton(text=t, callback_data=f"vtool_{t}")] for t in tools]
    buttons.append([back_btn("cat_video"), menu_btn()])
    await cb.message.edit_text(
        f"▸  <b>{subcat}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a model:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )
    await state.update_data(v_subcat=subcat)

@router.callback_query(F.data.startswith("vtool_"))
async def video_tool_selected(cb: CallbackQuery, state: FSMContext):
    tool = cb.data.replace("vtool_", "")
    await state.update_data(v_tool=tool)
    subcat = (await state.get_data()).get("v_subcat", "cat_video")
    await _show_tool_options(cb, state, tool, subcat)

async def _show_tool_options(cb: CallbackQuery, state: FSMContext, tool: str, subcat: str):
    desc = TOOL_DESCS.get(tool, "")

    # Fixed-price tools
    if tool == "Kling 3.0 Motion Control":
        await _confirm_fixed(cb, state, tool, {"resolution": "1080p", "duration": "30 sec"}, usd_to_coins(1.00), 1.00)
        return
    if tool == "Kling 3.0 Video Edit":
        await _confirm_fixed(cb, state, tool, {"resolution": "1080p", "duration": "10 sec"}, usd_to_coins(0.25), 0.25)
        return
    if tool == "OmniHuman 1.5":
        await _confirm_fixed(cb, state, tool, {"resolution": "1080p", "duration": "30 sec"}, usd_to_coins(2.99), 2.99)
        return
    if tool == "Fabric 1.0 Avatar":
        await _confirm_fixed(cb, state, tool, {"resolution": "720p", "duration": "1 min"}, usd_to_coins(0.99), 0.99)
        return
    if tool == "Aurora Avatar":
        await _confirm_fixed(cb, state, tool, {"resolution": "720p", "duration": "1 min"}, usd_to_coins(0.80), 0.80)
        return
    if tool == "Veo 3.1 Extend":
        await _show_veo_extend(cb, state)
        return
    if tool in ("HeyGen Avatar 4", "HeyGen Translate", "ElevenLabs Dubbing", "Lipsync v2 Pro"):
        await _show_duration_tool(cb, state, tool)
        return
    if tool == "Grok Imagine 1.5":
        await _show_grok(cb, state)
        return

    # Resolution selection
    res_map = {
        "Seedance 2.0": ["480p","720p","1080p"],
        "Seedance 2.0 Fast": ["480p","720p"],
        "Happy Horse 1.0": ["720p","1080p"],
        "Wan 2.7": ["720p","1080p"],
        "Veo 3.1": ["720p","1080p","4K"],
        "Veo 3.1 Fast": ["720p","1080p","4K"],
        "Veo 3.1 Lite": ["720p","1080p"],
        "Sora 2 Pro": ["720p","1080p"],
        "LTX 2.3 Pro": ["1080p","2K","4K"],
        "Kling 3.0": ["720p","1080p","4K"],
        "Kling 0.3": ["720p","1080p","4K"],
    }
    resolutions = res_map.get(tool, ["720p","1080p"])
    buttons = [[InlineKeyboardButton(text=r, callback_data=f"vres_{r}")] for r in resolutions]
    buttons.append([back_btn(f"vsub_{subcat}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {desc}\n\n"
        f"  Select resolution:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vres_"))
async def video_res_selected(cb: CallbackQuery, state: FSMContext):
    res = cb.data.replace("vres_", "")
    await state.update_data(v_res=res)
    data = await state.get_data()
    tool = data.get("v_tool")
    await _show_ar_or_dur(cb, state, tool, res)

async def _show_ar_or_dur(cb: CallbackQuery, state: FSMContext, tool: str, res: str):
    ar_map = {
        "Seedance 2.0": ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "Seedance 2.0 Fast": ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "Happy Horse 1.0": ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "Wan 2.7": ["16:9","9:16","1:1","4:3","3:4"],
        "Veo 3.1": ["16:9","9:16"],
        "Veo 3.1 Fast": ["16:9","9:16"],
        "Veo 3.1 Lite": ["16:9","9:16"],
        "Sora 2 Pro": ["16:9","9:16"],
        "LTX 2.3 Pro": ["16:9","9:16"],
        "Kling 3.0": ["16:9","9:16","1:1"],
        "Kling 0.3": ["16:9","9:16","1:1"],
    }
    ars = ar_map.get(tool, ["16:9","9:16"])
    buttons = [InlineKeyboardButton(text=ar, callback_data=f"var_{ar}") for ar in ars]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vtool_{tool}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>  —  {res}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Select aspect ratio:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("var_"))
async def video_ar_selected(cb: CallbackQuery, state: FSMContext):
    ar = cb.data.replace("var_", "")
    await state.update_data(v_ar=ar)
    data = await state.get_data()
    tool = data.get("v_tool")
    res = data.get("v_res")
    await _show_duration(cb, state, tool, res, ar)

async def _show_duration(cb: CallbackQuery, state: FSMContext, tool: str, res: str, ar: str):
    dur_map = {
        "Seedance 2.0": list(range(4,16)),
        "Seedance 2.0 Fast": list(range(4,16)),
        "Happy Horse 1.0": list(range(3,16)),
        "Wan 2.7": list(range(2,16)),
        "Veo 3.1": [4,6,8],
        "Veo 3.1 Fast": [4,6,8],
        "Veo 3.1 Lite": [4,6,8],
        "Sora 2 Pro": [4,8,12],
        "LTX 2.3 Pro": [6,8,10],
        "Kling 3.0": list(range(3,16)),
        "Kling 0.3": list(range(3,16)),
    }
    durations = dur_map.get(tool, [4,8,12])
    prices_table = _get_price_table(tool)
    buttons = []
    for d in durations:
        usd = prices_table.get(res, {}).get(d, 0)
        coins = usd_to_coins(usd)
        buttons.append(InlineKeyboardButton(text=f"{d}s — {coins}◈", callback_data=f"vdur_{d}"))
    rows = list(chunked(buttons, 3))

    # Audio option tools
    audio_tools = ["Seedance 2.0","Seedance 2.0 Fast","Veo 3.1","Veo 3.1 Fast","Veo 3.1 Lite","Kling 3.0","Kling 0.3","LTX 2.3 Pro","Sora 2 Pro"]
    if tool in audio_tools:
        rows.append([
            InlineKeyboardButton(text="🔊 With Audio", callback_data="vaudio_yes"),
            InlineKeyboardButton(text="🔇 No Audio", callback_data="vaudio_no"),
        ])

    rows.append([back_btn(f"vres_{res}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>  —  {res}  {ar}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Select duration:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

def _get_price_table(tool: str):
    return {
        "Seedance 2.0": SEEDANCE_20_PRICES,
        "Seedance 2.0 Fast": SEEDANCE_20_FAST_PRICES,
        "Happy Horse 1.0": HAPPY_HORSE_PRICES,
        "Wan 2.7": WAN_27_PRICES,
        "Veo 3.1": VEO_31_PRICES,
        "Veo 3.1 Fast": VEO_31_FAST_PRICES,
        "Veo 3.1 Lite": VEO_31_LITE_PRICES,
        "Sora 2 Pro": SORA_2_PRO_PRICES,
        "LTX 2.3 Pro": LTX_23_PRICES,
        "Kling 3.0": KLING_30_VIDEO_PRICES,
        "Kling 0.3": KLING_03_VIDEO_PRICES,
    }.get(tool, {})

@router.callback_query(F.data.startswith("vaudio_"))
async def video_audio(cb: CallbackQuery, state: FSMContext):
    audio = cb.data.replace("vaudio_", "") == "yes"
    await state.update_data(v_audio=audio)
    await cb.answer("Audio preference saved.")

@router.callback_query(F.data.startswith("vdur_"))
async def video_dur_selected(cb: CallbackQuery, state: FSMContext):
    dur = int(cb.data.replace("vdur_", ""))
    await state.update_data(v_dur=dur)
    data = await state.get_data()
    tool = data.get("v_tool")
    res = data.get("v_res")
    ar = data.get("v_ar")
    audio = data.get("v_audio", False)

    price_table = _get_price_table(tool)
    usd = price_table.get(res, {}).get(dur, 0)
    coins = usd_to_coins(usd)
    await state.update_data(v_coins=coins, v_usd=usd)

    await cb.message.edit_text(
        f"◈  <b>{tool}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Resolution   {res}\n"
        f"  Aspect ratio  {ar}\n"
        f"  Duration       {dur} sec\n"
        f"  Audio            {'Yes' if audio else 'No'}\n"
        f"  Cost               <b>{coins} coins</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Enter your prompt:",
        reply_markup=kb([back_btn(f"vtool_{tool}"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Veo Extend ────────────────────────────────────────────────
async def _show_veo_extend(cb: CallbackQuery, state: FSMContext):
    buttons = [
        [InlineKeyboardButton(text="Fast  —  14◈  (7 sec)", callback_data="vext_Fast")],
        [InlineKeyboardButton(text="Premium  —  30◈  (7 sec)", callback_data="vext_Premium")],
        [back_btn("vsub_Premium Video"), menu_btn()],
    ]
    await cb.message.edit_text(
        "◈  <b>Veo 3.1 Extend Video</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Extend your existing video by 7 seconds.\n\n"
        "  Select mode:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vext_"))
async def veo_extend_selected(cb: CallbackQuery, state: FSMContext):
    mode = cb.data.replace("vext_", "")
    usd = 0.70 if mode == "Fast" else 1.50
    coins = usd_to_coins(usd)
    await state.update_data(v_tool="Veo 3.1 Extend", v_ext_mode=mode, v_coins=coins, v_usd=usd)
    await cb.message.edit_text(
        f"◈  <b>Veo 3.1 Extend  —  {mode}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Duration   7 sec\n"
        f"  Cost          <b>{coins} coins</b>\n\n"
        f"Enter your prompt or describe the extension:",
        reply_markup=kb([back_btn("vtool_Veo 3.1 Extend"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Grok Imagine 1.5 ─────────────────────────────────────────
async def _show_grok(cb: CallbackQuery, state: FSMContext):
    buttons = []
    for sec, usd in GROK_IMAGINE_15_PRICES.items():
        coins = usd_to_coins(usd)
        buttons.append(InlineKeyboardButton(text=f"{sec}s — {coins}◈", callback_data=f"vgrok_{sec}"))
    rows = list(chunked(buttons, 3))
    rows.append([back_btn("vsub_Avatar & Dub"), menu_btn()])
    await cb.message.edit_text(
        "◈  <b>Grok Imagine 1.5</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Resolution: 720p\n\n"
        "  Select duration:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vgrok_"))
async def grok_dur(cb: CallbackQuery, state: FSMContext):
    sec = int(cb.data.replace("vgrok_", ""))
    usd = GROK_IMAGINE_15_PRICES[sec]
    coins = usd_to_coins(usd)
    await state.update_data(v_tool="Grok Imagine 1.5", v_dur=sec, v_coins=coins, v_usd=usd)
    await cb.message.edit_text(
        f"◈  <b>Grok Imagine 1.5</b>  —  {sec} sec\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn("vtool_Grok Imagine 1.5"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Duration-based tools (HeyGen, ElevenLabs, Lipsync) ───────
async def _show_duration_tool(cb: CallbackQuery, state: FSMContext, tool: str):
    if tool == "HeyGen Avatar 4":
        prices = HEYGEN_AVATAR_PRICES
        label = "minutes"
        max_min = 3
    elif tool == "HeyGen Translate":
        prices = HEYGEN_TRANSLATE_PRICES
        label = "minutes"
        max_min = 15
    elif tool == "ElevenLabs Dubbing":
        prices = ELEVENLABS_DUBBING_PRICES
        label = "minutes"
        max_min = 15
    else:  # Lipsync
        prices = LIPSYNC_PRICES
        label = "minutes"
        max_min = 5

    buttons = []
    for m, usd in prices.items():
        coins = usd_to_coins(usd)
        buttons.append(InlineKeyboardButton(text=f"{m} min — {coins}◈", callback_data=f"vdur_tool_{tool}_{m}"))
    rows = list(chunked(buttons, 3))
    rows.append([back_btn("vsub_Avatar & Dub"), menu_btn()])

    desc = TOOL_DESCS.get(tool, "")
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {desc}\n\n"
        f"  Select duration:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vdur_tool_"))
async def dur_tool_selected(cb: CallbackQuery, state: FSMContext):
    parts = cb.data.replace("vdur_tool_", "").rsplit("_", 1)
    tool = parts[0]
    minutes = int(parts[1])

    if tool == "HeyGen Avatar 4":
        usd = HEYGEN_AVATAR_PRICES[minutes]
    elif tool == "HeyGen Translate":
        usd = HEYGEN_TRANSLATE_PRICES[minutes]
    elif tool == "ElevenLabs Dubbing":
        usd = ELEVENLABS_DUBBING_PRICES[minutes]
    else:
        usd = LIPSYNC_PRICES[minutes]

    coins = usd_to_coins(usd)
    await state.update_data(v_tool=tool, v_dur=minutes, v_coins=coins, v_usd=usd)

    # Language tools
    if tool == "HeyGen Translate":
        await _show_language_select(cb, state, HEYGEN_TRANSLATE_LANGUAGES, "heygen_lang")
        return
    if tool == "ElevenLabs Dubbing":
        await _show_language_select(cb, state, ELEVENLABS_DUBBING_LANGUAGES, "elevenlabs_lang")
        return

    await cb.message.edit_text(
        f"◈  <b>{tool}</b>  —  {minutes} min\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn(f"vtool_{tool}"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

async def _show_language_select(cb: CallbackQuery, state: FSMContext, langs: list, prefix: str):
    buttons = [InlineKeyboardButton(text=l, callback_data=f"{prefix}_{l}") for l in langs]
    rows = list(chunked(buttons, 3))
    data = await state.get_data()
    tool = data.get("v_tool")
    rows.append([back_btn(f"vtool_{tool}"), menu_btn()])
    await cb.message.edit_text(
        "◈  Select target language:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("heygen_lang_"))
async def heygen_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data.replace("heygen_lang_", "")
    await state.update_data(v_lang=lang)
    data = await state.get_data()
    await cb.message.edit_text(
        f"◈  <b>HeyGen Translate</b>  —  {lang}\n\n"
        "Enter your prompt or describe the video:",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

@router.callback_query(F.data.startswith("elevenlabs_lang_"))
async def elevenlabs_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data.replace("elevenlabs_lang_", "")
    await state.update_data(v_lang=lang)
    data = await state.get_data()
    await cb.message.edit_text(
        f"◈  <b>ElevenLabs Dubbing</b>  —  {lang}\n\n"
        "Enter your prompt or describe the content:",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Fixed price confirm ───────────────────────────────────────
async def _confirm_fixed(cb: CallbackQuery, state: FSMContext, tool: str, params: dict, coins: int, usd: float):
    await state.update_data(v_tool=tool, v_coins=coins, v_usd=usd)
    params_text = "\n".join(f"  {k.title():<12} {v}" for k, v in params.items())
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{params_text}\n"
        f"  Cost           <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn("cat_video"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Prompt received ───────────────────────────────────────────
@router.message(VideoStates.entering_prompt)
async def video_prompt_received(msg: Message, state: FSMContext):
    data = await state.get_data()
    tool = data.get("v_tool", "—")
    coins = data.get("v_coins", 0)
    res = data.get("v_res", "—")
    ar = data.get("v_ar", "—")
    dur = data.get("v_dur", "—")
    audio = data.get("v_audio", False)
    prompt = msg.text

    await state.update_data(v_prompt=prompt)

    lines = f"  Model        <b>{tool}</b>\n"
    if res != "—": lines += f"  Resolution  {res}\n"
    if ar != "—":  lines += f"  Aspect       {ar}\n"
    if dur != "—": lines += f"  Duration     {dur} sec\n"
    if data.get("v_lang"): lines += f"  Language    {data['v_lang']}\n"
    lines += f"  Audio          {'Yes' if audio else 'No'}\n"
    lines += f"  Cost           <b>{coins} coins</b>\n"

    await msg.answer(
        f"◈  <b>Order Summary</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{lines}\n"
        f"  Prompt:\n<i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=f"◈  Confirm  ({coins} coins)", callback_data="vid_confirm")],
            [InlineKeyboardButton(text="✎  Edit Prompt", callback_data="vid_edit")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "vid_edit")
async def vid_edit(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text("✎  Enter your new prompt:", reply_markup=kb([menu_btn()]))
    await state.set_state(VideoStates.entering_prompt)

@router.callback_query(F.data == "vid_confirm")
async def video_confirm(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    uid = cb.from_user.id

    if not spend_coins(uid, coins):
        await cb.answer("Insufficient coins. Please top up your wallet.", show_alert=True)
        return

    tool = data.get("v_tool")
    params = {
        "resolution": data.get("v_res"),
        "aspect_ratio": data.get("v_ar"),
        "duration": data.get("v_dur"),
        "audio": data.get("v_audio"),
        "language": data.get("v_lang"),
        "prompt": data.get("v_prompt"),
    }
    usd = data.get("v_usd", 0)
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool, params, coins, usd)
    await _notify_admin_video(cb, oid, tool, params, coins, usd)

    await cb.message.edit_text(
        f"◌  <b>Order #{oid} Placed</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Model     <b>{tool}</b>\n"
        f"  Coins      <b>{coins} deducted</b>\n\n"
        f"  Estimated delivery  ~2 minutes\n\n"
        f"  Your video will be delivered here.",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )
    await state.clear()

async def _notify_admin_video(cb, oid, tool, params, coins, usd):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
    p = params
    details = (
        f"  Resolution   {p.get('resolution') or '—'}\n"
        f"  Aspect         {p.get('aspect_ratio') or '—'}\n"
        f"  Duration       {p.get('duration') or '—'}\n"
        f"  Audio            {p.get('audio') or 'No'}\n"
        f"  Language      {p.get('language') or '—'}\n"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Delivered", callback_data=f"delivered_{oid}"),
        InlineKeyboardButton(text="✕  Cancel", callback_data=f"cancel_order_{oid}"),
    ]])
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>New Video Order #{oid}</b>\n\n"
        f"  User     @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
        f"  Model   <b>{tool}</b>\n"
        f"{details}"
        f"  Coins    <b>{coins}</b>  (${usd})\n\n"
        f"  Prompt:\n<i>{p.get('prompt')}</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
