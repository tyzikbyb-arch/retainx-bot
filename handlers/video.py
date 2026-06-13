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

# ── Tool ID map (short keys to avoid FSM issues) ──────────────
TOOL_IDS = {
    "sd20":   "Seedance 2.0",
    "sd20f":  "Seedance 2.0 Fast",
    "hh10":   "Happy Horse 1.0",
    "wan27":  "Wan 2.7",
    "veo31":  "Veo 3.1",
    "veo31f": "Veo 3.1 Fast",
    "veo31l": "Veo 3.1 Lite",
    "veo31e": "Veo 3.1 Extend",
    "sora2":  "Sora 2 Pro",
    "ltx23":  "LTX 2.3 Pro",
    "kl30":   "Kling 3.0",
    "kl03":   "Kling 0.3",
    "klmc":   "Kling 3.0 Motion Control",
    "klve":   "Kling 3.0 Video Edit",
    "hga4":   "HeyGen Avatar 4",
    "hgtr":   "HeyGen Translate",
    "eldb":   "ElevenLabs Dubbing",
    "lips":   "Lipsync v2 Pro",
    "omni":   "OmniHuman 1.5",
    "fab1":   "Fabric 1.0 Avatar",
    "aur1":   "Aurora Avatar",
    "grok":   "Grok Imagine 1.5",
}
ID_TO_TOOL = {v: k for k, v in TOOL_IDS.items()}

TOOL_DESCS = {
    "Seedance 2.0":            "High-quality cinematic video generation up to 1080p with optional audio.",
    "Seedance 2.0 Fast":       "Faster variant of Seedance 2.0 — up to 720p, quicker turnaround.",
    "Happy Horse 1.0":         "Smooth motion video generation with natural movement, up to 1080p.",
    "Wan 2.7":                 "Versatile multi-ratio video model with wide format support.",
    "Veo 3.1":                 "Google's flagship video model — cinematic quality up to 4K with audio.",
    "Veo 3.1 Fast":            "Veo 3.1 express mode — same quality, faster render times.",
    "Veo 3.1 Lite":            "Lightweight Veo model for quick, cost-effective generation.",
    "Veo 3.1 Extend":          "Extend any existing video clip by 7 seconds using Veo.",
    "Sora 2 Pro":              "OpenAI's advanced video generation model with premium realism.",
    "LTX 2.3 Pro":             "High-framerate professional video — up to 4K at 50fps.",
    "Kling 3.0":               "One of the most powerful AI video models of 2026. Realistic motion, character consistency, built-in audio, image-to-video, up to 4K.",
    "Kling 0.3":               "Kling compact model — same visual quality, optimised for speed.",
    "Kling 3.0 Motion Control":"Precise scene-level motion control in 1080p, 30-second output.",
    "Kling 3.0 Video Edit":    "Edit and enhance existing video clips using Kling AI.",
    "HeyGen Avatar 4":         "Photorealistic talking avatar — sync any script to a lifelike presenter.",
    "HeyGen Translate":        "AI-powered video translation with accurate lip-sync.",
    "ElevenLabs Dubbing":      "Professional multilingual AI dubbing with voice cloning.",
    "Lipsync v2 Pro":          "Advanced lip-sync — align any audio track to any video.",
    "OmniHuman 1.5":           "Full-body human avatar animation from a single image.",
    "Fabric 1.0 Avatar":       "Premium avatar video generation with expressive motion.",
    "Aurora Avatar":           "Realistic avatar video from photo — natural expressions.",
    "Grok Imagine 1.5":        "Grok's creative video model — imaginative and stylised output.",
}

VIDEO_SUBCATS = {
    "Standard":  ["sd20","sd20f","hh10","wan27"],
    "Premium":   ["veo31","veo31f","veo31l","veo31e","sora2","ltx23"],
    "Kling":     ["kl30","kl03","klmc","klve"],
    "Avatar":    ["hga4","hgtr","eldb","lips","omni","fab1","aur1","grok"],
}
SUBCAT_LABELS = {
    "Standard": "▸  Standard Video",
    "Premium":  "▸  Premium Video",
    "Kling":    "▸  Kling Video",
    "Avatar":   "▸  Avatar & Dubbing",
}

def get_price_table(tid: str):
    return {
        "sd20":  SEEDANCE_20_PRICES,
        "sd20f": SEEDANCE_20_FAST_PRICES,
        "hh10":  HAPPY_HORSE_PRICES,
        "wan27": WAN_27_PRICES,
        "veo31": VEO_31_PRICES,
        "veo31f":VEO_31_FAST_PRICES,
        "veo31l":VEO_31_LITE_PRICES,
        "sora2": SORA_2_PRO_PRICES,
        "ltx23": LTX_23_PRICES,
        "kl30":  KLING_30_VIDEO_PRICES,
        "kl03":  KLING_03_VIDEO_PRICES,
    }.get(tid, {})

def get_resolutions(tid: str):
    return {
        "sd20":  ["480p","720p","1080p"],
        "sd20f": ["480p","720p"],
        "hh10":  ["720p","1080p"],
        "wan27": ["720p","1080p"],
        "veo31": ["720p","1080p","4K"],
        "veo31f":["720p","1080p","4K"],
        "veo31l":["720p","1080p"],
        "sora2": ["720p","1080p"],
        "ltx23": ["1080p","2K","4K"],
        "kl30":  ["720p","1080p","4K"],
        "kl03":  ["720p","1080p","4K"],
    }.get(tid, ["720p","1080p"])

def get_aspect_ratios(tid: str):
    return {
        "sd20":  ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "sd20f": ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "hh10":  ["16:9","9:16","1:1","21:9","4:3","3:4"],
        "wan27": ["16:9","9:16","1:1","4:3","3:4"],
        "veo31": ["16:9","9:16"],
        "veo31f":["16:9","9:16"],
        "veo31l":["16:9","9:16"],
        "sora2": ["16:9","9:16"],
        "ltx23": ["16:9","9:16"],
        "kl30":  ["16:9","9:16","1:1"],
        "kl03":  ["16:9","9:16","1:1"],
    }.get(tid, ["16:9","9:16"])

def get_durations(tid: str):
    return {
        "sd20":  list(range(4,16)),
        "sd20f": list(range(4,16)),
        "hh10":  list(range(3,16)),
        "wan27": list(range(2,16)),
        "veo31": [4,6,8],
        "veo31f":[4,6,8],
        "veo31l":[4,6,8],
        "sora2": [4,8,12],
        "ltx23": [6,8,10],
        "kl30":  list(range(3,16)),
        "kl03":  list(range(3,16)),
    }.get(tid, [4,8,12])

HAS_AUDIO = {"sd20","sd20f","veo31","veo31f","veo31l","ltx23","sora2","kl30","kl03","hga4","hgtr","eldb","lips"}

# ── Video menu ────────────────────────────────────────────────
@router.callback_query(F.data == "cat_video")
async def video_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    buttons = [[InlineKeyboardButton(text=SUBCAT_LABELS[s], callback_data=f"vsub_{s}")] for s in VIDEO_SUBCATS]
    buttons.append([back_btn("main_menu", "⌂  Main Menu")])
    await cb.message.edit_text(
        "◈  <b>Video Generation</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a category:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vsub_"))
async def video_subcat(cb: CallbackQuery, state: FSMContext):
    sub = cb.data[5:]
    tids = VIDEO_SUBCATS.get(sub, [])
    buttons = [[InlineKeyboardButton(text=TOOL_IDS[t], callback_data=f"vt_{t}")] for t in tids]
    buttons.append([back_btn("cat_video"), menu_btn()])
    await cb.message.edit_text(
        f"▸  <b>{SUBCAT_LABELS.get(sub, sub)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a model:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )
    await state.update_data(v_sub=sub)

# ── Tool selected ─────────────────────────────────────────────
@router.callback_query(F.data.startswith("vt_"))
async def tool_selected(cb: CallbackQuery, state: FSMContext):
    tid = cb.data[3:]
    if tid not in TOOL_IDS:
        await cb.answer("Unknown tool")
        return
    name = TOOL_IDS[tid]
    await state.update_data(v_tid=tid, v_tool=name)

    # Fixed price tools
    fixed = {
        "klmc": ({"Resolution":"1080p","Duration":"30 sec"}, 1.00),
        "klve": ({"Resolution":"1080p","Duration":"10 sec"}, 0.25),
        "omni": ({"Resolution":"1080p","Duration":"30 sec"}, 2.99),
        "fab1": ({"Resolution":"720p","Duration":"1 min"}, 0.99),
        "aur1": ({"Resolution":"720p","Duration":"1 min"}, 0.80),
    }
    if tid in fixed:
        params, usd = fixed[tid]
        coins = usd_to_coins(usd)
        await state.update_data(v_coins=coins, v_usd=usd)
        lines = "\n".join(f"  {k:<14}{v}" for k,v in params.items())
        sub = (await state.get_data()).get("v_sub","cat_video")
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  {TOOL_DESCS.get(name,'')}\n\n"
            f"{lines}\n"
            f"  Cost           <b>{coins} coins</b>\n\n"
            "Enter your prompt:",
            reply_markup=kb([back_btn(f"vsub_{sub}"), menu_btn()]), parse_mode="HTML"
        )
        await state.set_state(VideoStates.entering_prompt)
        return

    if tid == "veo31e":
        await show_veo_extend(cb, state)
        return

    if tid == "grok":
        await show_grok(cb, state)
        return

    if tid in ("hga4","hgtr","eldb","lips"):
        await show_duration_tool(cb, state, tid)
        return

    # Resolution step
    resolutions = get_resolutions(tid)
    sub = (await state.get_data()).get("v_sub","cat_video")
    buttons = [[InlineKeyboardButton(text=r, callback_data=f"vr_{r}")] for r in resolutions]
    buttons.append([back_btn(f"vsub_{sub}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {TOOL_DESCS.get(name,'')}\n\n"
        "  Select resolution:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vr_"))
async def res_selected(cb: CallbackQuery, state: FSMContext):
    res = cb.data[3:]
    await state.update_data(v_res=res)
    data = await state.get_data()
    tid = data.get("v_tid","")
    name = data.get("v_tool","")
    ars = get_aspect_ratios(tid)
    buttons = [InlineKeyboardButton(text=ar, callback_data=f"va_{ar.replace(':','x')}") for ar in ars]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn(f"vt_{tid}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {res}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select aspect ratio:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("va_"))
async def ar_selected(cb: CallbackQuery, state: FSMContext):
    ar = cb.data[3:].replace("x",":")
    await state.update_data(v_ar=ar)
    data = await state.get_data()
    tid = data.get("v_tid","")
    res = data.get("v_res","")
    name = data.get("v_tool","")
    await show_duration(cb, state, tid, res, ar, name)

async def show_duration(cb, state, tid, res, ar, name):
    price_table = get_price_table(tid)
    durations = get_durations(tid)
    buttons = []
    for d in durations:
        usd = price_table.get(res, {}).get(d, 0)
        coins = usd_to_coins(usd) if usd > 0 else 0
        buttons.append(InlineKeyboardButton(
            text=f"{d}s — {coins}◈",
            callback_data=f"vd_{d}"
        ))
    rows = list(chunked(buttons, 3))

    if tid in HAS_AUDIO:
        rows.append([
            InlineKeyboardButton(text="🔊 With Audio", callback_data="vaud_yes"),
            InlineKeyboardButton(text="🔇 No Audio", callback_data="vaud_no"),
        ])

    rows.append([back_btn(f"vr_{res}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {res}  {ar}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vaud_"))
async def audio_selected(cb: CallbackQuery, state: FSMContext):
    audio = cb.data == "vaud_yes"
    await state.update_data(v_audio=audio)
    await cb.answer(f"Audio: {'On' if audio else 'Off'}")

@router.callback_query(F.data.startswith("vd_"))
async def dur_selected(cb: CallbackQuery, state: FSMContext):
    dur = int(cb.data[3:])
    data = await state.get_data()
    tid = data.get("v_tid","")
    res = data.get("v_res","")
    name = data.get("v_tool","")
    ar = data.get("v_ar","—")
    audio = data.get("v_audio", False)

    price_table = get_price_table(tid)
    usd = price_table.get(res, {}).get(dur, 0)
    coins = usd_to_coins(usd) if usd > 0 else 1
    await state.update_data(v_dur=dur, v_coins=coins, v_usd=usd)

    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Resolution    {res}\n"
        f"  Aspect ratio  {ar}\n"
        f"  Duration       {dur} sec\n"
        f"  Audio            {'Yes' if audio else 'No'}\n"
        f"  Cost              <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn(f"va_{ar.replace(':','x')}"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Veo Extend ────────────────────────────────────────────────
async def show_veo_extend(cb, state):
    await cb.message.edit_text(
        "◈  <b>Veo 3.1 Extend Video</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Extend any video clip by 7 seconds.\n\n"
        "  Select mode:",
        reply_markup=kb(
            [InlineKeyboardButton(text="Fast  —  14◈  (7 sec)", callback_data="vext_Fast")],
            [InlineKeyboardButton(text="Premium  —  30◈  (7 sec)", callback_data="vext_Premium")],
            [back_btn("vsub_Premium"), menu_btn()],
        ), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vext_"))
async def veo_extend(cb: CallbackQuery, state: FSMContext):
    mode = cb.data[5:]
    usd = 0.70 if mode == "Fast" else 1.50
    coins = usd_to_coins(usd)
    await state.update_data(v_tool="Veo 3.1 Extend", v_tid="veo31e", v_coins=coins, v_usd=usd, v_ext_mode=mode)
    await cb.message.edit_text(
        f"◈  <b>Veo 3.1 Extend  —  {mode}</b>\n\n"
        f"  Duration   7 sec  |  Cost  <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn("vt_veo31e"), menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Grok ─────────────────────────────────────────────────────
async def show_grok(cb, state):
    buttons = [
        InlineKeyboardButton(
            text=f"{s}s — {usd_to_coins(usd)}◈",
            callback_data=f"vgrok_{s}"
        )
        for s, usd in GROK_IMAGINE_15_PRICES.items()
    ]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn("vsub_Avatar"), menu_btn()])
    await cb.message.edit_text(
        "◈  <b>Grok Imagine 1.5</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Resolution: 720p\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vgrok_"))
async def grok_dur(cb: CallbackQuery, state: FSMContext):
    sec = int(cb.data[6:])
    usd = GROK_IMAGINE_15_PRICES[sec]
    coins = usd_to_coins(usd)
    await state.update_data(v_tool="Grok Imagine 1.5", v_tid="grok", v_dur=sec, v_coins=coins, v_usd=usd)
    await cb.message.edit_text(
        f"◈  <b>Grok Imagine 1.5</b>  —  {sec} sec\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn("vt_grok"), menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Duration tools ────────────────────────────────────────────
async def show_duration_tool(cb, state, tid):
    name = TOOL_IDS[tid]
    prices = {
        "hga4": HEYGEN_AVATAR_PRICES,
        "hgtr": HEYGEN_TRANSLATE_PRICES,
        "eldb": ELEVENLABS_DUBBING_PRICES,
        "lips": LIPSYNC_PRICES,
    }[tid]
    buttons = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"vdtool_{tid}_{m}"
        )
        for m, usd in prices.items()
    ]
    rows = list(chunked(buttons, 3))
    rows.append([back_btn("vsub_Avatar"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {TOOL_DESCS.get(name,'')}\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vdtool_"))
async def dur_tool_selected(cb: CallbackQuery, state: FSMContext):
    parts = cb.data[7:].rsplit("_", 1)
    tid = parts[0]
    minutes = int(parts[1])
    name = TOOL_IDS.get(tid, tid)
    prices = {
        "hga4": HEYGEN_AVATAR_PRICES,
        "hgtr": HEYGEN_TRANSLATE_PRICES,
        "eldb": ELEVENLABS_DUBBING_PRICES,
        "lips": LIPSYNC_PRICES,
    }[tid]
    usd = prices[minutes]
    coins = usd_to_coins(usd)
    await state.update_data(v_tool=name, v_tid=tid, v_dur=minutes, v_coins=coins, v_usd=usd)

    if tid == "hgtr":
        await show_lang_select(cb, state, HEYGEN_TRANSLATE_LANGUAGES, "vlangh")
        return
    if tid == "eldb":
        await show_lang_select(cb, state, ELEVENLABS_DUBBING_LANGUAGES, "vlange")
        return

    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {minutes} min\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn(f"vt_{tid}"), menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

async def show_lang_select(cb, state, langs, prefix):
    buttons = [InlineKeyboardButton(text=l, callback_data=f"{prefix}_{l[:20]}") for l in langs]
    rows = list(chunked(buttons, 3))
    data = await state.get_data()
    tid = data.get("v_tid","")
    rows.append([back_btn(f"vt_{tid}"), menu_btn()])
    await cb.message.edit_text(
        "◈  Select target language:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vlangh_"))
async def heygen_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data[7:]
    await state.update_data(v_lang=lang)
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    await cb.message.edit_text(
        f"◈  <b>HeyGen Translate</b>  —  {lang}\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

@router.callback_query(F.data.startswith("vlange_"))
async def eleven_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data[7:]
    await state.update_data(v_lang=lang)
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    await cb.message.edit_text(
        f"◈  <b>ElevenLabs Dubbing</b>  —  {lang}\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Prompt ────────────────────────────────────────────────────
@router.message(VideoStates.entering_prompt)
async def prompt_received(msg: Message, state: FSMContext):
    data = await state.get_data()
    tool  = data.get("v_tool", "—")
    coins = data.get("v_coins", 0)
    res   = data.get("v_res", "—")
    ar    = data.get("v_ar", "—")
    dur   = data.get("v_dur", "—")
    audio = data.get("v_audio", False)
    lang  = data.get("v_lang")
    prompt = msg.text
    await state.update_data(v_prompt=prompt)

    lines = f"  Model          <b>{tool}</b>\n"
    if res != "—":   lines += f"  Resolution    {res}\n"
    if ar  != "—":   lines += f"  Aspect ratio  {ar}\n"
    if dur != "—":   lines += f"  Duration       {dur} sec\n"
    if lang:          lines += f"  Language      {lang}\n"
    lines += f"  Audio            {'Yes' if audio else 'No'}\n"
    lines += f"  Cost              <b>{coins} coins</b>\n"

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
        ), parse_mode="HTML"
    )

@router.callback_query(F.data == "vid_edit")
async def vid_edit(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text("✎  Enter your new prompt:", reply_markup=kb([menu_btn()]))
    await state.set_state(VideoStates.entering_prompt)

@router.callback_query(F.data == "vid_confirm")
async def vid_confirm(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    uid = cb.from_user.id

    if not spend_coins(uid, coins):
        await cb.answer("Insufficient coins. Please top up your wallet.", show_alert=True)
        return

    tool   = data.get("v_tool", "—")
    prompt = data.get("v_prompt", "—")
    params = {
        "resolution":   data.get("v_res"),
        "aspect_ratio": data.get("v_ar"),
        "duration":     data.get("v_dur"),
        "audio":        data.get("v_audio"),
        "language":     data.get("v_lang"),
        "prompt":       prompt,
    }
    usd = data.get("v_usd", 0)
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool, params, coins, usd)
    await notify_admin(cb, oid, tool, params, coins, usd)

    await cb.message.edit_text(
        f"◌  <b>Order #{oid} Placed</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Model     <b>{tool}</b>\n"
        f"  Coins      <b>{coins} deducted</b>\n\n"
        f"  Estimated delivery  ~2 minutes\n\n"
        f"  Your result will be sent here.",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.clear()

async def notify_admin(cb, oid, tool, params, coins, usd):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
    p = params
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Delivered", callback_data=f"delivered_{oid}"),
        InlineKeyboardButton(text="✕  Cancel",    callback_data=f"cancel_order_{oid}"),
    ]])
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>New Video Order #{oid}</b>\n\n"
        f"  User        @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
        f"  Model      <b>{tool}</b>\n"
        f"  Resolution {p.get('resolution') or '—'}\n"
        f"  Aspect      {p.get('aspect_ratio') or '—'}\n"
        f"  Duration    {p.get('duration') or '—'}\n"
        f"  Audio        {p.get('audio') or 'No'}\n"
        f"  Language   {p.get('language') or '—'}\n"
        f"  Coins       <b>{coins}</b>  (${usd})\n\n"
        f"  Prompt:\n<i>{p.get('prompt','—')}</i>",
        reply_markup=keyboard, parse_mode="HTML"
    )
