from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import kb, back_btn, menu_btn, chunked
from handlers.attachments import get_attach_config, has_attachments
from database import get_coins, spend_coins, create_order
from config import (
    usd_to_coins,
    SEEDANCE_20_PRICES, SEEDANCE_20_FAST_PRICES, HAPPY_HORSE_PRICES,
    VEO_31_PRICES, VEO_31_FAST_PRICES, VEO_31_LITE_PRICES,
    KLING_30_VIDEO_PRICES, KLING_03_VIDEO_PRICES,
    WAN_27_PRICES, SORA_2_PRO_PRICES, LTX_23_PRICES,
    GROK_IMAGINE_15_PRICES, HEYGEN_AVATAR_PRICES, HEYGEN_TRANSLATE_PRICES,
    HEYGEN_TRANSLATE_PRECISION_PRICES, HEYGEN_TRANSLATE_SPEED_PRICES,
    HEYGEN_AVATAR_ASPECT_RATIOS, HEYGEN_AVATAR_RESOLUTIONS, HEYGEN_AVATAR_TALKING_STYLES,
    OMNIHUMAN_PRICES, AURORA_AVATAR_PRICES,
    ELEVENLABS_DUBBING_PRICES, LIPSYNC_PRICES,
    HEYGEN_TRANSLATE_LANGUAGES, ELEVENLABS_DUBBING_LANGUAGES,
)
import math

router = Router()

class VideoStates(StatesGroup):
    entering_prompt = State()
    uploading_video = State()
    # Generic attachment states (used by all tools)
    attach_mode = State()
    collecting_start = State()
    collecting_end = State()
    collecting_imgs = State()
    collecting_vids = State()
    collecting_audio = State()
    # Legacy Seedance states (kept for compatibility)
    sd_attach_mode = State()
    sd_collecting_start = State()
    sd_collecting_end = State()
    sd_collecting_imgs = State()
    sd_collecting_vids = State()
    sd_collecting_audio = State()
    sd_entering_prompt = State()

# ── Tool ID map (short keys to avoid FSM issues) ──────────────
TOOL_IDS = {
    "sd20":   "Seedance 2.0",
    "sd20f":  "Seedance 2.0 Fast",
    "hh10":   "Happy Horse 1.0",
    "wan27":  "Wan 2.7",
    "veo31":  "Veo 3.1",
    "veo31f": "Veo 3.1 Fast",
    "veo31l": "Veo 3.1 Lite",
    "veo31e": "Veo 3.1 Extend Video",
    "sora2":  "Sora 2 Pro",
    "ltx23":  "LTX 2.3 Pro",
    "kl30":   "Kling 3.0",
    "kl03":   "Kling O3",
    "klmc":   "Kling 3.0 Motion Control",
    "klve":   "Kling O3 Video Edit",
    "hga4":   "HeyGen Avatar 4",
    "hgtr":   "HeyGen Translate",
    "eldb":   "ElevenLabs Dubbing",
    "lips":   "Lipsync v2 Pro",
    "omni":   "OmniHuman 1.5 Avatar",
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
    "Standard":  ["sd20","sd20f","hh10","wan27","grok"],
    "Premium":   ["veo31","veo31f","veo31l","veo31e","sora2","ltx23"],
    "Kling":     ["kl30","kl03","klmc","klve"],
    "Avatar":    ["hga4","hgtr","eldb","lips","omni","aur1","fab1"],
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

HAS_AUDIO = {"sd20","sd20f","veo31","veo31f","veo31l","ltx23","sora2","kl30","kl03","hgtr","eldb","lips"}

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
def _sd_attach_menu(coins: int = 0) -> str:
    return (
        "◈  <b>Seedance 2.0</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Attach reference files (optional)\n"
        "  or skip directly to your prompt.\n\n"
        "  ⚠️  Start/End Frame cannot be combined\n"
        "  with other attachment types."
    )

def _sd_attach_kb(data: dict) -> list:
    mode = data.get("sd_mode", "free")  # "startend" or "free"
    imgs = data.get("sd_imgs", [])
    vids = data.get("sd_vids", [])
    auds = data.get("sd_auds", [])
    start = data.get("sd_start")
    end = data.get("sd_end")

    buttons = []
    if mode != "free":
        # Start/End mode active
        s_label = f"✓ Start Frame" if start else "◈  Start Frame"
        e_label = f"✓ End Frame" if end else "◈  End Frame"
        buttons.append([InlineKeyboardButton(text=s_label, callback_data="sd_set_start")])
        buttons.append([InlineKeyboardButton(text=e_label, callback_data="sd_set_end")])
        buttons.append([InlineKeyboardButton(text="✕  Clear Start/End", callback_data="sd_clear_startend")])
    else:
        # Free mode
        img_label = f"◈  Image Ref  ({len(imgs)}/9)" if imgs else "◈  Image Reference"
        vid_label = f"◈  Video Ref  ({len(vids)}/3)" if vids else "◈  Video Reference"
        aud_label = f"◈  Audio File  ({len(auds)}/3)" if auds else "◈  Audio File"
        buttons.append([InlineKeyboardButton(text=img_label, callback_data="sd_add_imgs")])
        buttons.append([InlineKeyboardButton(text=vid_label, callback_data="sd_add_vids")])
        buttons.append([InlineKeyboardButton(text=aud_label, callback_data="sd_add_auds")])
        if not (imgs or vids or auds):
            buttons.append([InlineKeyboardButton(text="◈  Start & End Frame", callback_data="sd_startend_mode")])

    has_any = start or end or imgs or vids or auds
    prompt_label = f"✓  Write Prompt →" if has_any else "▸  Skip — Write Prompt"
    buttons.append([InlineKeyboardButton(text=prompt_label, callback_data="sd_to_prompt")])
    buttons.append([back_btn("vt_sd20"), menu_btn()])  # sd20/sd20f share same menu
    return buttons

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
        "fab1": ({"Type":"Avatar Video"}, 0.90),
        # omni, aur1 handled separately
    }
    if tid in fixed:
        params, usd = fixed[tid]
        coins = usd_to_coins(usd)
        await state.update_data(v_coins=coins, v_usd=usd)
        if has_attachments(tid):
            await state.update_data(att_mode="free", att_start=None, att_end=None,
                                    att_imgs=[], att_vids=[], att_auds=[])
            await _show_attach_menu(cb, state)
            await state.set_state(VideoStates.attach_mode)
        else:
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

    if tid == "hga4":
        await show_hga4_ar(cb, state)
        return
    if tid == "hgtr":
        await show_hgtr_quality(cb, state)
        return
    if tid == "omni":
        await show_omni_dur(cb, state)
        return
    if tid == "aur1":
        await aur1_start(cb, state)
        return
    if tid in ("eldb","lips"):
        await show_duration_tool(cb, state, tid)
        return

    # Tools with attachments — show attach menu first
    if has_attachments(tid):
        await state.update_data(
            att_mode="free", att_start=None, att_end=None,
            att_imgs=[], att_vids=[], att_auds=[],
            # legacy seedance fields reset
            sd_mode="free", sd_start=None, sd_end=None,
            sd_imgs=[], sd_vids=[], sd_auds=[],
        )
        await _show_attach_menu(cb, state)
        await state.set_state(VideoStates.attach_mode)
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
    rows.append([back_btn(f"vr_{res}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {res}  {ar}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("vd_"))
async def dur_selected(cb: CallbackQuery, state: FSMContext):
    dur = int(cb.data[3:])
    data = await state.get_data()
    tid  = data.get("v_tid","")
    res  = data.get("v_res","")
    name = data.get("v_tool","")
    ar   = data.get("v_ar","—")

    price_table = get_price_table(tid)
    usd   = price_table.get(res, {}).get(dur, 0)
    coins = usd_to_coins(usd) if usd > 0 else 1
    await state.update_data(v_dur=dur, v_coins=coins, v_usd=usd)

    if tid in HAS_AUDIO:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>  —  {res}  {dur}s\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  Cost   <b>{coins} coins</b>\n\n"
            "  Include audio in the video?",
            reply_markup=kb(
                [InlineKeyboardButton(text="🔊 With Audio", callback_data="vaud_yes"),
                 InlineKeyboardButton(text="🔇 No Audio",   callback_data="vaud_no")],
                [back_btn(f"va_{ar.replace(':','x')}"), menu_btn()],
            ), parse_mode="HTML"
        )
        return

    await _ask_prompt(cb, state, name, res, ar, dur, False, coins)

@router.callback_query(F.data.startswith("vaud_"))
async def audio_selected(cb: CallbackQuery, state: FSMContext):
    audio = cb.data == "vaud_yes"
    await state.update_data(v_audio=audio)
    data = await state.get_data()
    await _ask_prompt(
        cb, state,
        data.get("v_tool",""),
        data.get("v_res","—"),
        data.get("v_ar","—"),
        data.get("v_dur","—"),
        audio,
        data.get("v_coins", 0),
    )

async def _ask_prompt(cb, state, name, res, ar, dur, audio, coins):
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Resolution    {res}\n"
        f"  Aspect ratio  {ar}\n"
        f"  Duration       {dur} sec\n"
        f"  Audio            {'Yes' if audio else 'No'}\n"
        f"  Cost              <b>{coins} coins</b>\n\n"
        "Enter your prompt:",
        reply_markup=kb([back_btn(f"va_{str(ar).replace(':','x')}"), menu_btn()]),
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
    await state.update_data(v_tool="Veo 3.1 Extend", v_tid="veo31e", v_coins=coins, v_usd=usd, v_ext_mode=mode,
                            att_mode="free", att_start=None, att_end=None,
                            att_imgs=[], att_vids=[], att_auds=[])
    await _show_attach_menu(cb, state)
    await state.set_state(VideoStates.attach_mode)

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
        "hgtr": HEYGEN_TRANSLATE_PRICES,
        "eldb": ELEVENLABS_DUBBING_PRICES,
        "lips": LIPSYNC_PRICES,
    }.get(tid, {})
    if not prices:
        await cb.answer("Unknown tool")
        return
    btns = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"vdtool_{tid}_{m}"
        )
        for m, usd in prices.items()
    ]
    buttons = btns
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
        "hgtr": HEYGEN_TRANSLATE_PRICES,
        "eldb": ELEVENLABS_DUBBING_PRICES,
        "lips": LIPSYNC_PRICES,
    }.get(tid, {})
    usd = prices.get(minutes, 0)
    coins = usd_to_coins(usd)
    await state.update_data(v_tool=name, v_tid=tid, v_dur=minutes, v_coins=coins, v_usd=usd)

    if tid == "hgtr":
        await show_lang_select(cb, state, HEYGEN_TRANSLATE_LANGUAGES, "vlangh")
        return
    if tid == "eldb":
        await show_lang_select(cb, state, ELEVENLABS_DUBBING_LANGUAGES, "vlange")
        return
    # lips — go to attachment menu
    if tid == "lips":
        await state.update_data(
            att_mode="free", att_start=None, att_end=None,
            att_imgs=[], att_vids=[], att_auds=[],
        )
        await _show_attach_menu(cb, state)
        await state.set_state(VideoStates.attach_mode)
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
        "  Send your video file in any format\n"
        "  (MP4, MOV, AVI, MKV etc.)",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.uploading_video)

@router.callback_query(F.data.startswith("vlange_"))
async def eleven_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data[7:]
    await state.update_data(v_lang=lang)
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    await cb.message.edit_text(
        f"◈  <b>ElevenLabs Dubbing</b>  —  {lang}\n\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        "  Send your video file in any format\n"
        "  (MP4, MOV, AVI, MKV etc.)",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.set_state(VideoStates.uploading_video)

# ── Video upload (HeyGen/ElevenLabs) ─────────────────────────
@router.message(VideoStates.uploading_video)
async def video_uploaded(msg: Message, state: FSMContext):
    if not (msg.video or msg.document or msg.animation):
        await msg.answer(
            "Please send a video file (MP4, MOV, AVI, MKV etc.)\n\nType /cancel to exit."
        )
        return

    if msg.video:
        file_id = msg.video.file_id
        ftype = "video"
    elif msg.animation:
        file_id = msg.animation.file_id
        ftype = "animation"
    else:
        file_id = msg.document.file_id
        ftype = "document"

    await state.update_data(v_upload_file_id=file_id, v_upload_file_type=ftype)
    data = await state.get_data()
    tool = data.get("v_tool", "—")
    lang = data.get("v_lang", "—")
    coins = data.get("v_coins", 0)

    await msg.answer(
        f"✓  Video received\n\n"
        f"◈  <b>{tool}</b>  —  {lang}\n"
        f"  Cost   <b>{coins} coins</b>\n\n"
        f"  Add any additional notes (optional)\n"
        f"  or skip to confirm order:",
        reply_markup=kb(
            [InlineKeyboardButton(text=f"◈  Confirm  ({coins} coins)", callback_data="vid_confirm")],
            [InlineKeyboardButton(text="✎  Add Notes", callback_data="vid_add_notes")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )
    await state.update_data(v_prompt="—")  # default empty prompt

@router.callback_query(F.data == "vid_add_notes")
async def vid_add_notes(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "✎  Add notes or instructions (optional):",
        reply_markup=kb([menu_btn()])
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Prompt ────────────────────────────────────────────────────
@router.message(VideoStates.entering_prompt)
async def prompt_received(msg: Message, state: FSMContext):
    data = await state.get_data()
    tool  = data.get("v_tool", "—")
    tid   = data.get("v_tid", "")
    coins = data.get("v_coins", 0)
    res   = data.get("v_res", "—")
    ar    = data.get("v_ar", "—")
    dur   = data.get("v_dur", "—")
    audio = data.get("v_audio", False)
    lang  = data.get("v_lang")
    prompt = msg.text
    await state.update_data(v_prompt=prompt)

    # Attachment summary
    attach_summary = ""
    att_imgs = data.get("att_imgs", []) or data.get("sd_imgs", [])
    att_vids = data.get("att_vids", []) or data.get("sd_vids", [])
    att_auds = data.get("att_auds", []) or data.get("sd_auds", [])
    att_start = data.get("att_start") or data.get("sd_start")
    att_end = data.get("att_end") or data.get("sd_end")
    if att_start: attach_summary += "  ◈  Start frame\n"
    if att_end:   attach_summary += "  ◈  End frame\n"
    if att_imgs:  attach_summary += f"  ◈  {len(att_imgs)} image ref(s)\n"
    if att_vids:  attach_summary += f"  ◈  {len(att_vids)} video ref(s)\n"
    if att_auds:  attach_summary += f"  ◈  {len(att_auds)} audio file(s)\n"
    if tool == "Seedance 2.0":
        pass  # already handled above

    # Tools that don't show resolution/aspect/audio in summary
    no_res_tools = {"aur1", "omni", "hga4", "lips"}
    lines = f"  Model          <b>{tool}</b>\n"
    if res != "—" and tid not in no_res_tools:   lines += f"  Resolution    {res}\n"
    if ar  != "—" and tid not in no_res_tools:   lines += f"  Aspect ratio  {ar}\n"
    if dur != "—":   lines += f"  Duration       {dur} sec\n"
    if lang:          lines += f"  Language      {lang}\n"
    if tid not in no_res_tools: lines += f"  Audio            {'Yes' if audio else 'No'}\n"
    if attach_summary: lines += f"\n  Attachments:\n{attach_summary}"
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
    await _do_confirm(cb, state)
    return

async def _vid_confirm_legacy(cb: CallbackQuery, state: FSMContext):
    """Legacy confirm kept for reference."""
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    tool  = data.get("v_tool", "—")
    prompt = data.get("v_prompt", "—")
    uid = cb.from_user.id

    if not tool or tool == "—" or coins == 0:
        await cb.answer("Session expired. Please start your order again.", show_alert=True)
        await state.clear()
        return

    if not spend_coins(uid, coins):
        await cb.answer("Insufficient coins. Please top up your wallet.", show_alert=True)
        return
    # Build attachments for Seedance 2.0
    attachments = {}
    if tool == "Seedance 2.0":
        if data.get("sd_start"): attachments["start"] = data["sd_start"]
        if data.get("sd_end"):   attachments["end"]   = data["sd_end"]
        if data.get("sd_imgs"):  attachments["imgs"]  = data["sd_imgs"]
        if data.get("sd_vids"):  attachments["vids"]  = data["sd_vids"]
        if data.get("sd_auds"):  attachments["auds"]  = data["sd_auds"]

    params = {
        "resolution":    data.get("v_res"),
        "aspect_ratio":  data.get("v_ar"),
        "duration":      data.get("v_dur"),
        "audio":         data.get("v_audio"),
        "language":      data.get("v_lang"),
        "prompt":        prompt,
        "attachments":   attachments if attachments else None,
        "upload_file_id":   data.get("v_upload_file_id"),
        "upload_file_type": data.get("v_upload_file_type"),
    }
    usd = data.get("v_usd", 0)
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool, params, coins, usd)

    # Push to Redis queue for auto-generation
    await _push_to_queue(oid, uid, tid, tool, params, coins, usd)

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
    # Build compact order card
    lines = ""
    if p.get("resolution"):   lines += f"  Resolution   {p['resolution']}\n"
    if p.get("aspect_ratio"): lines += f"  Aspect          {p['aspect_ratio']}\n"
    if p.get("duration"):     lines += f"  Duration        {p['duration']} {'min' if tool in ('HeyGen Avatar 4','OmniHuman 1.5','Aurora Avatar','Lipsync v2 Pro','HeyGen Translate','ElevenLabs Dubbing') else 'sec'}\n"
    if p.get("language"):     lines += f"  Language       {p['language']}\n"
    if p.get("audio"):        lines += f"  Audio             Yes\n"

    await bot.send_message(
        ADMIN_ID,
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"◈  <b>New Video Order #{oid}</b>\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"  User     @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
        f"  Model   <b>{tool}</b>\n"
        f"{lines}"
        f"  Coins    <b>{coins}◈</b>  (${usd})",
        reply_markup=keyboard, parse_mode="HTML"
    )
    # Send prompt as separate copyable message
    prompt_text = p.get('prompt','—')
    if prompt_text and prompt_text != "—":
        await bot.send_message(
            ADMIN_ID,
            f"📋 <b>Prompt #{oid}:</b>\n\n<code>{prompt_text}</code>",
            parse_mode="HTML"
        )
    # Send uploaded video (HeyGen/ElevenLabs)
    upload_fid = p.get("upload_file_id")
    upload_ftype = p.get("upload_file_type")
    if upload_fid:
        try:
            caption = f"◈  Source video for Order #{oid}"
            if upload_ftype == "video":
                await bot.send_video(ADMIN_ID, upload_fid, caption=caption)
            elif upload_ftype == "animation":
                await bot.send_animation(ADMIN_ID, upload_fid, caption=caption)
            else:
                await bot.send_document(ADMIN_ID, upload_fid, caption=caption)
        except Exception as e:
            await bot.send_message(ADMIN_ID, f"⚠️  Error sending source video: {e}")
    # Send attachments
    attachments = p.get("attachments") or {}
    if attachments:
        async def _send_file(fid, ftype, caption):
            try:
                if ftype == "photo":
                    await bot.send_photo(ADMIN_ID, fid, caption=caption)
                elif ftype == "video":
                    await bot.send_video(ADMIN_ID, fid, caption=caption)
                elif ftype == "animation":
                    await bot.send_animation(ADMIN_ID, fid, caption=caption)
                elif ftype == "audio":
                    await bot.send_audio(ADMIN_ID, fid, caption=caption)
                elif ftype == "voice":
                    await bot.send_voice(ADMIN_ID, fid, caption=caption)
                else:
                    await bot.send_document(ADMIN_ID, fid, caption=caption)
            except Exception as e:
                await bot.send_message(ADMIN_ID, f"⚠️  Could not send {caption}: {e}")

        start = attachments.get("start")
        end   = attachments.get("end")
        imgs  = attachments.get("imgs", [])
        vids  = attachments.get("vids", [])
        auds  = attachments.get("auds", [])

        if start: await _send_file(start["file_id"], start["type"], "◈  Start Frame  (@start)")
        if end:   await _send_file(end["file_id"],   end["type"],   "◈  End Frame  (@end)")
        for i, f in enumerate(imgs, 1):
            await _send_file(f["file_id"], f["type"], f"◈  Image Ref  @img{i}")
        for i, f in enumerate(vids, 1):
            await _send_file(f["file_id"], f["type"], f"◈  Video Ref  @vid{i}")
        for i, f in enumerate(auds, 1):
            await _send_file(f["file_id"], f["type"], f"◈  Audio  @aud{i}")

# ═══════════════════════════════════════════════════════════
# SEEDANCE 2.0 — ATTACHMENT HANDLERS
# ═══════════════════════════════════════════════════════════

async def _refresh_attach_menu(cb: CallbackQuery, state: FSMContext, coins: int = None):
    data = await state.get_data()
    c = coins or data.get("v_coins", usd_to_coins(0.60))
    await cb.message.edit_text(
        _sd_attach_menu(c),
        reply_markup=kb(*_sd_attach_kb(data)),
        parse_mode="HTML"
    )

# ── Mode selection ────────────────────────────────────────
@router.callback_query(F.data == "sd_startend_mode")
async def sd_startend_mode(cb: CallbackQuery, state: FSMContext):
    await state.update_data(sd_mode="startend", sd_imgs=[], sd_vids=[], sd_auds=[])
    await _refresh_attach_menu(cb, state)

@router.callback_query(F.data == "sd_clear_startend")
async def sd_clear_startend(cb: CallbackQuery, state: FSMContext):
    await state.update_data(sd_mode="free", sd_start=None, sd_end=None)
    await _refresh_attach_menu(cb, state)

# ── Start frame ───────────────────────────────────────────
@router.callback_query(F.data == "sd_set_start")
async def sd_set_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "◈  <b>Start Frame</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send the image for the <b>first frame</b> of your video.\n\n"
        "  Reference it in your prompt as <code>@start</code>",
        reply_markup=kb([back_btn("sd_back_attach"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.sd_collecting_start)

@router.message(VideoStates.sd_collecting_start)
async def sd_collect_start(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    await state.update_data(sd_start={"file_id": file_id, "type": ftype})
    await state.set_state(VideoStates.sd_attach_mode)
    data = await state.get_data()
    await msg.answer(
        "✓  Start frame saved.\n\nNow set the End Frame or write your prompt.",
        reply_markup=kb(*_sd_attach_kb(data))
    )

# ── End frame ─────────────────────────────────────────────
@router.callback_query(F.data == "sd_set_end")
async def sd_set_end(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "◈  <b>End Frame</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send the image for the <b>last frame</b> of your video.\n\n"
        "  Reference it in your prompt as <code>@end</code>",
        reply_markup=kb([back_btn("sd_back_attach"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.sd_collecting_end)

@router.message(VideoStates.sd_collecting_end)
async def sd_collect_end(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    await state.update_data(sd_end={"file_id": file_id, "type": ftype})
    await state.set_state(VideoStates.sd_attach_mode)
    data = await state.get_data()
    await msg.answer(
        "✓  End frame saved.\n\nWrite your prompt when ready.",
        reply_markup=kb(*_sd_attach_kb(data))
    )

# ── Image references ──────────────────────────────────────
@router.callback_query(F.data == "sd_add_imgs")
async def sd_add_imgs(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    imgs = data.get("sd_imgs", [])
    count = len(imgs)
    await cb.message.edit_text(
        f"◈  <b>Image Reference</b>  ({count}/9)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send up to <b>9 images</b> as reference.\n\n"
        "  <code>@img1</code>, <code>@img2</code> etc. are just labels\n"
        "  for you — the AI doesn't read them. Describe each image\n"
        "  in words in your prompt instead (e.g. \"the woman in photo 1\").\n\n"
        "  Send images one by one or as album.\n"
        "  Tap <b>Done</b> when finished.",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        ),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.sd_collecting_imgs)

@router.message(VideoStates.sd_collecting_imgs)
async def sd_collect_img(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    data = await state.get_data()
    imgs = data.get("sd_imgs", [])
    if len(imgs) >= 9:
        await msg.answer("Maximum 9 images reached. Tap Done to continue.")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    imgs.append({"file_id": file_id, "type": ftype, "ref": f"img{len(imgs)+1}"})
    await state.update_data(sd_imgs=imgs)
    await msg.answer(
        f"✓  Image @img{len(imgs)} saved.  ({len(imgs)}/9)\n"
        f"{'Send more or tap Done.' if len(imgs) < 9 else 'Maximum reached. Tap Done.'}",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        )
    )

# ── Video references ──────────────────────────────────────
@router.callback_query(F.data == "sd_add_vids")
async def sd_add_vids(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    vids = data.get("sd_vids", [])
    await cb.message.edit_text(
        f"◈  <b>Video Reference</b>  ({len(vids)}/3)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send up to <b>3 videos</b> as reference.\n\n"
        "  <code>@vid1</code>, <code>@vid2</code> etc. are just labels\n"
        "  for you — the AI doesn't read them. Describe each video\n"
        "  in words in your prompt instead.\n\n"
        "  Tap <b>Done</b> when finished.",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        ),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.sd_collecting_vids)

@router.message(VideoStates.sd_collecting_vids)
async def sd_collect_vid(msg: Message, state: FSMContext):
    if not (msg.video or msg.animation or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("video/"))):
        await msg.answer("◈  Please send a video file (MP4, MOV, AVI etc.)")
        return
    data = await state.get_data()
    vids = data.get("sd_vids", [])
    if len(vids) >= 3:
        await msg.answer("Maximum 3 videos reached. Tap Done to continue.")
        return
    file_id = msg.video.file_id if msg.video else msg.document.file_id
    ftype = "video" if msg.video else "document"
    vids.append({"file_id": file_id, "type": ftype, "ref": f"vid{len(vids)+1}"})
    await state.update_data(sd_vids=vids)
    await msg.answer(
        f"✓  Video @vid{len(vids)} saved.  ({len(vids)}/3)\n"
        f"{'Send more or tap Done.' if len(vids) < 3 else 'Maximum reached. Tap Done.'}",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        )
    )

# ── Audio files ───────────────────────────────────────────
@router.callback_query(F.data == "sd_add_auds")
async def sd_add_auds(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    auds = data.get("sd_auds", [])
    await cb.message.edit_text(
        f"◈  <b>Audio File</b>  ({len(auds)}/3)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send up to <b>3 audio files</b>.\n\n"
        "  <code>@aud1</code>, <code>@aud2</code> etc. are just labels\n"
        "  for you — the AI doesn't read them. Describe each audio\n"
        "  file in words in your prompt instead.\n\n"
        "  Tap <b>Done</b> when finished.",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        ),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.sd_collecting_audio)

@router.message(VideoStates.sd_collecting_audio)
async def sd_collect_aud(msg: Message, state: FSMContext):
    if not (msg.audio or msg.voice or (msg.document and msg.document.mime_type and (msg.document.mime_type.startswith("audio/") or msg.document.mime_type == "application/ogg"))):
        await msg.answer("◈  Please send an audio file (MP3, OGG, WAV, M4A etc.)")
        return
    data = await state.get_data()
    auds = data.get("sd_auds", [])
    if len(auds) >= 3:
        await msg.answer("Maximum 3 audio files reached. Tap Done to continue.")
        return
    if msg.audio:
        file_id = msg.audio.file_id
        ftype = "audio"
    elif msg.voice:
        file_id = msg.voice.file_id
        ftype = "voice"
    else:
        file_id = msg.document.file_id
        ftype = "document"
    auds.append({"file_id": file_id, "type": ftype, "ref": f"aud{len(auds)+1}"})
    await state.update_data(sd_auds=auds)
    await msg.answer(
        f"✓  Audio @aud{len(auds)} saved.  ({len(auds)}/3)\n"
        f"{'Send more or tap Done.' if len(auds) < 3 else 'Maximum reached. Tap Done.'}",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="sd_back_attach")],
            [menu_btn()]
        )
    )

# ── Back to attach menu ───────────────────────────────────
@router.callback_query(F.data == "sd_back_attach")
async def sd_back_attach(cb: CallbackQuery, state: FSMContext):
    await state.set_state(VideoStates.sd_attach_mode)
    await _refresh_attach_menu(cb, state)

# ── Proceed to resolution/prompt ──────────────────────────
@router.callback_query(F.data == "sd_to_prompt")
async def sd_to_prompt(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    imgs = data.get("sd_imgs", [])
    vids = data.get("sd_vids", [])
    auds = data.get("sd_auds", [])
    start = data.get("sd_start")
    end = data.get("sd_end")

    # Build attachment summary
    attach_lines = ""
    if start:
        attach_lines += "  ◈  Start frame attached\n"
    if end:
        attach_lines += "  ◈  End frame attached\n"
    if imgs:
        attach_lines += f"  ◈  {len(imgs)} image(s) → @img1"
        if len(imgs) > 1:
            attach_lines += f"–@img{len(imgs)}"
        attach_lines += "\n"
    if vids:
        attach_lines += f"  ◈  {len(vids)} video(s) → @vid1"
        if len(vids) > 1:
            attach_lines += f"–@vid{len(vids)}"
        attach_lines += "\n"
    if auds:
        attach_lines += f"  ◈  {len(auds)} audio(s) → @aud1"
        if len(auds) > 1:
            attach_lines += f"–@aud{len(auds)}"
        attach_lines += "\n"

    hint = ""
    if attach_lines:
        hint = (
            f"\n  <b>Attached files:</b>\n{attach_lines}\n"
            "  Note: these labels are just for your own reference —\n"
            "  the AI doesn't read them. Describe each file in words\n"
            "  in your prompt.\n"
        )

    await cb.message.edit_text(
        f"◈  <b>Seedance 2.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{hint}\n"
        "  Now select resolution:",
        reply_markup=kb(
            [InlineKeyboardButton(text="480p", callback_data="vr_480p")],
            [InlineKeyboardButton(text="720p", callback_data="vr_720p")],
            [InlineKeyboardButton(text="1080p", callback_data="vr_1080p")],
            [back_btn("vt_sd20"), menu_btn()],
        ),
        parse_mode="HTML"
    )

# ═══════════════════════════════════════════════════════════
# UNIVERSAL ATTACHMENT SYSTEM (all tools except Seedance)
# ═══════════════════════════════════════════════════════════

def _build_attach_menu_text(tid: str, data: dict) -> str:
    cfg = get_attach_config(tid)
    name = data.get("v_tool", "")
    hint = cfg.get("hint", "Attach reference files (optional)\n  or skip directly to your prompt.")
    return (
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {hint}"
    )

def _build_attach_buttons(tid: str, data: dict) -> list:
    cfg = get_attach_config(tid)
    buttons = []
    mode = data.get("att_mode", "free")

    start_frame = cfg.get("start_frame", False)
    end_frame = cfg.get("end_frame", False)
    max_imgs = cfg.get("img_refs", 0)
    max_vids = cfg.get("vid_refs", 0)
    max_auds = cfg.get("aud_refs", 0)
    exclusive = cfg.get("exclusive_startend", False)
    vid_required = cfg.get("vid_ref_required", False)
    no_prompt = cfg.get("no_prompt", False)

    start = data.get("att_start")
    end_ = data.get("att_end")
    imgs = data.get("att_imgs", [])
    vids = data.get("att_vids", [])
    auds = data.get("att_auds", [])

    # Start/End frame section
    if start_frame and (mode == "startend" or not exclusive):
        s_label = "✓  Start Frame" if start else "◈  Start Frame"
        buttons.append([InlineKeyboardButton(text=s_label, callback_data="att_set_start")])
        if end_frame:
            e_label = "✓  End Frame" if end_ else "◈  End Frame"
            buttons.append([InlineKeyboardButton(text=e_label, callback_data="att_set_end")])
        if exclusive and (start or end_):
            buttons.append([InlineKeyboardButton(text="✕  Clear", callback_data="att_clear_startend")])

    # For exclusive tools, show img/vid/aud only if not in startend mode
    if exclusive and mode == "startend":
        pass  # hide other options
    else:
        if max_imgs > 0 and not (exclusive and (start or end_)):
            img_label = f"✓  Image Ref  ({len(imgs)}/{max_imgs})" if imgs else f"◈  Image Reference  (up to {max_imgs})"
            buttons.append([InlineKeyboardButton(text=img_label, callback_data="att_add_imgs")])
        if max_vids > 0:
            req = " *required" if vid_required and not vids else ""
            vid_label = f"✓  Video Ref  ({len(vids)}/{max_vids})" if vids else f"◈  Video Reference  (up to {max_vids}){req}"
            buttons.append([InlineKeyboardButton(text=vid_label, callback_data="att_add_vids")])
        if max_auds > 0:
            aud_label = f"✓  Audio File  ({len(auds)}/{max_auds})" if auds else f"◈  Audio File  (up to {max_auds})"
            buttons.append([InlineKeyboardButton(text=aud_label, callback_data="att_add_auds")])

        # Show startend option only if nothing else attached
        if start_frame and exclusive and not (imgs or vids or auds):
            se_label = "✓  Start & End Frame" if (start or end_) else "◈  Start & End Frame"
            buttons.append([InlineKeyboardButton(text=se_label, callback_data="att_startend_mode")])

    # Proceed button
    has_any = start or end_ or imgs or vids or auds
    img_required = cfg.get("img_required", False)
    aud_required = cfg.get("aud_required", False)

    # Check all required files
    missing = []
    if vid_required and not vids: missing.append("video")
    if img_required and not imgs: missing.append("image")
    if aud_required and not auds: missing.append("audio")

    if missing:
        label = "⚠️  Upload " + " & ".join(missing) + " to continue"
        buttons.append([InlineKeyboardButton(text=label, callback_data="att_required_alert")])
        buttons.append([back_btn(f"vt_{tid}"), menu_btn()])
        return buttons

    if no_prompt:
        proceed_label = "◈  Confirm Order"
        proceed_cb = "att_confirm_no_prompt"
    else:
        proceed_label = "✓  Write Prompt →" if has_any else "▸  Skip — Write Prompt"
        proceed_cb = "att_to_prompt"

    buttons.append([InlineKeyboardButton(text=proceed_label, callback_data=proceed_cb)])
    buttons.append([back_btn(f"vt_{tid}"), menu_btn()])
    return buttons

async def _show_attach_menu(target, state: FSMContext, edit: bool = True):
    from aiogram.exceptions import TelegramBadRequest
    data = await state.get_data()
    tid = data.get("v_tid", "")
    text = _build_attach_menu_text(tid, data)
    markup = kb(*_build_attach_buttons(tid, data))
    try:
        if edit and isinstance(target, CallbackQuery):
            await target.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
        elif isinstance(target, Message):
            await target.answer(text, reply_markup=markup, parse_mode="HTML")
        else:
            await target.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    except TelegramBadRequest:
        pass  # Message not modified — ignore

# ── Intercept tool_selected for tools with attachments ────────
# This is handled inside tool_selected by checking has_attachments(tid)

# ── Start/End mode ────────────────────────────────────────────
@router.callback_query(F.data == "att_startend_mode")
async def att_startend_mode(cb: CallbackQuery, state: FSMContext):
    await state.update_data(att_mode="startend")
    await _show_attach_menu(cb, state)

@router.callback_query(F.data == "att_clear_startend")
async def att_clear_startend(cb: CallbackQuery, state: FSMContext):
    await state.update_data(att_mode="free", att_start=None, att_end=None)
    await _show_attach_menu(cb, state)

# ── Start frame ───────────────────────────────────────────────
@router.callback_query(F.data == "att_set_start")
async def att_set_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "◈  <b>Start Frame</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send the image for the <b>first frame</b>.\n\n"
        "  Reference it in your prompt as <code>@start</code>",
        reply_markup=kb([back_btn("att_back"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.collecting_start)

@router.message(VideoStates.collecting_start)
async def att_collect_start(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    await state.update_data(att_start={"file_id": file_id, "type": ftype})
    await state.set_state(VideoStates.attach_mode)
    await _show_attach_menu(msg, state, edit=False)

# ── End frame ─────────────────────────────────────────────────
@router.callback_query(F.data == "att_set_end")
async def att_set_end(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "◈  <b>End Frame</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Send the image for the <b>last frame</b>.\n\n"
        "  Reference it in your prompt as <code>@end</code>",
        reply_markup=kb([back_btn("att_back"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.collecting_end)

@router.message(VideoStates.collecting_end)
async def att_collect_end(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    await state.update_data(att_end={"file_id": file_id, "type": ftype})
    await state.set_state(VideoStates.attach_mode)
    await _show_attach_menu(msg, state, edit=False)

# ── Image refs ────────────────────────────────────────────────
@router.callback_query(F.data == "att_add_imgs")
async def att_add_imgs(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_imgs = cfg.get("img_refs", 9)
    imgs = data.get("att_imgs", [])
    await cb.message.edit_text(
        f"◈  <b>Image Reference</b>  ({len(imgs)}/{max_imgs})\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Send up to <b>{max_imgs} image(s)</b>.\n"
        f"  <code>@img1</code> etc. are just labels for you — the AI\n"
        f"  doesn't read them. Describe each image in words instead.\n\n"
        f"  Tap Done when finished.",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.collecting_imgs)

@router.message(VideoStates.collecting_imgs)
async def att_collect_img(msg: Message, state: FSMContext):
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"))):
        await msg.answer("◈  Please send an image file (JPG, PNG, WEBP etc.)")
        return
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_imgs = cfg.get("img_refs", 9)
    imgs = data.get("att_imgs", [])
    if len(imgs) >= max_imgs:
        await msg.answer(f"Maximum {max_imgs} image(s) reached. Tap Done.")
        return
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    imgs.append({"file_id": file_id, "type": ftype, "ref": f"img{len(imgs)+1}"})
    await state.update_data(att_imgs=imgs)
    await msg.answer(
        f"✓  @img{len(imgs)} saved  ({len(imgs)}/{max_imgs})",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()])
    )

# ── Video refs ────────────────────────────────────────────────
@router.callback_query(F.data == "att_add_vids")
async def att_add_vids(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_vids = cfg.get("vid_refs", 3)
    vids = data.get("att_vids", [])
    await cb.message.edit_text(
        f"◈  <b>Video Reference</b>  ({len(vids)}/{max_vids})\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Send up to <b>{max_vids} video(s)</b> in any format.\n"
        f"  <code>@vid1</code> etc. are just labels for you — the AI\n"
        f"  doesn't read them. Describe each video in words instead.\n\n"
        f"  Tap Done when finished.",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.collecting_vids)

@router.message(VideoStates.collecting_vids)
async def att_collect_vid(msg: Message, state: FSMContext):
    if not (msg.video or msg.animation or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("video/"))):
        await msg.answer("◈  Please send a video file (MP4, MOV, AVI etc.)")
        return
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_vids = cfg.get("vid_refs", 3)
    vids = data.get("att_vids", [])
    if len(vids) >= max_vids:
        await msg.answer(f"Maximum {max_vids} video(s) reached. Tap Done.")
        return
    if msg.video:
        file_id, ftype = msg.video.file_id, "video"
    elif msg.animation:
        file_id, ftype = msg.animation.file_id, "animation"
    else:
        file_id, ftype = msg.document.file_id, "document"
    vids.append({"file_id": file_id, "type": ftype, "ref": f"vid{len(vids)+1}"})
    await state.update_data(att_vids=vids)
    await msg.answer(
        f"✓  @vid{len(vids)} saved  ({len(vids)}/{max_vids})",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()])
    )

# ── Audio refs ────────────────────────────────────────────────
@router.callback_query(F.data == "att_add_auds")
async def att_add_auds(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_auds = cfg.get("aud_refs", 3)
    auds = data.get("att_auds", [])
    await cb.message.edit_text(
        f"◈  <b>Audio File</b>  ({len(auds)}/{max_auds})\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Send up to <b>{max_auds} audio file(s)</b>.\n"
        f"  <code>@aud1</code> etc. are just labels for you — the AI\n"
        f"  doesn't read them. Describe each audio file in words instead.\n\n"
        f"  Tap Done when finished.",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.collecting_audio)

@router.message(VideoStates.collecting_audio)
async def att_collect_aud(msg: Message, state: FSMContext):
    if not (msg.audio or msg.voice or (msg.document and msg.document.mime_type and (msg.document.mime_type.startswith("audio/") or msg.document.mime_type == "application/ogg"))):
        await msg.answer("◈  Please send an audio file (MP3, OGG, WAV, M4A etc.)")
        return
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    max_auds = cfg.get("aud_refs", 3)
    auds = data.get("att_auds", [])
    if len(auds) >= max_auds:
        await msg.answer(f"Maximum {max_auds} audio file(s) reached. Tap Done.")
        return
    if msg.audio:
        file_id, ftype = msg.audio.file_id, "audio"
    elif msg.voice:
        file_id, ftype = msg.voice.file_id, "voice"
    else:
        file_id, ftype = msg.document.file_id, "document"
    auds.append({"file_id": file_id, "type": ftype, "ref": f"aud{len(auds)+1}"})
    await state.update_data(att_auds=auds)
    await msg.answer(
        f"✓  @aud{len(auds)} saved  ({len(auds)}/{max_auds})",
        reply_markup=kb([InlineKeyboardButton(text="✓  Done", callback_data="att_back")], [menu_btn()])
    )

@router.callback_query(F.data.in_({"att_vid_required_alert", "att_required_alert"}))
async def att_required_alert(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Please upload the required files first.", show_alert=True)

# ── Back to attach menu ───────────────────────────────────────
@router.callback_query(F.data == "att_back")
async def att_back(cb: CallbackQuery, state: FSMContext):
    await state.set_state(VideoStates.attach_mode)
    await _show_attach_menu(cb, state)

# ── Proceed to prompt ─────────────────────────────────────────
# Tools that need resolution/duration selection after attachments
NEEDS_RESOLUTION = {"sd20", "sd20f", "hh10", "veo31", "veo31f", "veo31l",
                    "kl30", "kl03", "ltx23", "wan27", "sora2", "hail23"}

@router.callback_query(F.data == "att_to_prompt")
async def att_to_prompt(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)
    tool = data.get("v_tool", "")
    coins = data.get("v_coins", 0)

    if tid in NEEDS_RESOLUTION:
        # Go to resolution selection first
        resolutions = get_resolutions(tid)
        name = tool
        buttons = [[InlineKeyboardButton(text=r, callback_data=f"vr_{r}")] for r in resolutions]
        buttons.append([back_btn("att_back"), menu_btn()])
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Select resolution:",
            reply_markup=kb(*buttons), parse_mode="HTML"
        )
        return

    # Fixed price tools — go directly to prompt
    prompt_label = cfg.get("prompt_label", "Enter your prompt:")
    lines = ""
    if data.get("att_start"): lines += "  ◈  Start frame\n"
    if data.get("att_end"):   lines += "  ◈  End frame\n"
    imgs = data.get("att_imgs", [])
    vids = data.get("att_vids", [])
    auds = data.get("att_auds", [])
    if imgs: lines += f"  ◈  {len(imgs)} image ref(s)\n"
    if vids: lines += f"  ◈  {len(vids)} video ref(s)\n"
    if auds: lines += f"  ◈  {len(auds)} audio file(s)\n"

    attach_block = f"\n{lines}" if lines else ""
    await cb.message.edit_text(
        f"◈  <b>{tool}</b>\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{attach_block}\n"
        f"  {prompt_label}",
        reply_markup=kb([back_btn("att_back"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(VideoStates.entering_prompt)

# ── Confirm without prompt (no_prompt tools) ──────────────────
@router.callback_query(F.data == "att_confirm_no_prompt")
async def att_confirm_no_prompt(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tid = data.get("v_tid", "")
    cfg = get_attach_config(tid)

    imgs = data.get("att_imgs", [])
    vids = data.get("att_vids", [])
    auds = data.get("att_auds", [])

    missing = []
    if cfg.get("vid_ref_required") and not vids: missing.append("video")
    if cfg.get("img_required") and not imgs: missing.append("image")
    if cfg.get("aud_required") and not auds: missing.append("audio")

    if missing:
        await cb.answer(
            "Please upload required files: " + ", ".join(missing),
            show_alert=True
        )
        return

    await state.update_data(v_prompt="—")
    await _do_confirm(cb, state)

async def _push_to_queue(oid: int, uid: int, tid: str, tool: str, params: dict, coins: int, usd: float):
    """Push order to Redis queue for auto-generation worker."""
    import logging
    log = logging.getLogger(__name__)
    try:
        import redis.asyncio as aioredis
        import os, json
        redis_url = os.environ.get("REDIS_URL", "")
        log.info(f"[QUEUE] Pushing order #{oid} to Redis, URL present: {bool(redis_url)}")
        if not redis_url:
            log.warning("[QUEUE] REDIS_URL not set, skipping queue push")
            return
        r = await aioredis.from_url(redis_url, decode_responses=True)
        order_data = {
            "order_id": oid,
            "user_id": uid,
            "tool_id": tid,
            "tool_name": tool,
            "type": "video",
            "params": params,
            "coins": coins,
            "usd": usd,
        }
        await r.rpush("retainx:orders", json.dumps(order_data))
        await r.aclose()
        log.info(f"[QUEUE] Order #{oid} pushed successfully to retainx:orders")
    except Exception as e:
        log.error(f"[QUEUE] Failed to push order #{oid} to Redis: {e}")

async def _do_confirm(cb: CallbackQuery, state: FSMContext):
    """Shared confirmation logic."""
    data = await state.get_data()
    coins = data.get("v_coins", 0)
    uid = cb.from_user.id
    tool = data.get("v_tool", "—")
    tid = data.get("v_tid", "")
    prompt = data.get("v_prompt", "—")

    if not tool or tool == "—" or coins == 0:
        await cb.answer("Session expired. Please start again.", show_alert=True)
        await state.clear()
        return

    from database import spend_coins, create_order
    if not spend_coins(uid, coins):
        await cb.answer("Insufficient coins.", show_alert=True)
        return

    # Build unified attachments
    attachments = {}
    # Generic att_ fields
    if data.get("att_start"):  attachments["start"] = data["att_start"]
    if data.get("att_end"):    attachments["end"]   = data["att_end"]
    if data.get("att_imgs"):   attachments["imgs"]  = data["att_imgs"]
    if data.get("att_vids"):   attachments["vids"]  = data["att_vids"]
    if data.get("att_auds"):   attachments["auds"]  = data["att_auds"]
    # Legacy sd_ fields (Seedance)
    if data.get("sd_start"):   attachments["start"] = data["sd_start"]
    if data.get("sd_end"):     attachments["end"]   = data["sd_end"]
    if data.get("sd_imgs"):    attachments["imgs"]  = data["sd_imgs"]
    if data.get("sd_vids"):    attachments["vids"]  = data["sd_vids"]
    if data.get("sd_auds"):    attachments["auds"]  = data["sd_auds"]

    params = {
        "resolution":    data.get("v_res"),
        "aspect_ratio":  data.get("v_ar"),
        "duration":      data.get("v_dur"),
        "audio":         data.get("v_audio"),
        "language":      data.get("v_lang"),
        "prompt":        prompt,
        "attachments":   attachments if attachments else None,
        "upload_file_id":   data.get("v_upload_file_id"),
        "upload_file_type": data.get("v_upload_file_type"),
    }
    usd = data.get("v_usd", 0)
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, tool, params, coins, usd)

    # Push to Redis queue for auto-generation
    await _push_to_queue(oid, uid, tid, tool, params, coins, usd)

    await notify_admin(cb, oid, tool, params, coins, usd)

    await cb.message.edit_text(
        f"◌  <b>Order #{oid} Placed</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Model     <b>{tool}</b>\n"
        f"  Coins      <b>{coins} deducted</b>\n\n"
        f"  Estimated delivery  ~2 minutes\n\n"
        f"  Your result will be sent here.",
        reply_markup=kb([menu_btn()]), parse_mode="HTML"
    )
    await state.clear()

# ═══════════════════════════════════════════════════════════
# HEYGEN AVATAR 4 — Full flow
# AR → Resolution → Talking Style → Duration → Attachments
# ═══════════════════════════════════════════════════════════

async def show_hga4_ar(cb, state):
    buttons = [[InlineKeyboardButton(text=ar, callback_data=f"hga4_ar_{ar}")] for ar in HEYGEN_AVATAR_ASPECT_RATIOS]
    buttons.append([back_btn("vsub_Avatar"), menu_btn()])
    await cb.message.edit_text(
        "◈  <b>HeyGen Avatar 4</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select aspect ratio:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hga4_ar_"))
async def hga4_ar(cb: CallbackQuery, state: FSMContext):
    ar = cb.data[8:]
    await state.update_data(v_ar=ar)
    buttons = [[InlineKeyboardButton(text=r, callback_data=f"hga4_res_{r}")] for r in HEYGEN_AVATAR_RESOLUTIONS]
    buttons.append([back_btn("vt_hga4"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>HeyGen Avatar 4</b>  —  {ar}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select resolution:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hga4_res_"))
async def hga4_res(cb: CallbackQuery, state: FSMContext):
    res = cb.data[9:]
    await state.update_data(v_res=res)
    buttons = [[InlineKeyboardButton(text=s, callback_data=f"hga4_style_{s}")] for s in HEYGEN_AVATAR_TALKING_STYLES]
    data = await state.get_data()
    ar = data.get("v_ar", "—")
    buttons.append([back_btn(f"hga4_ar_{ar}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>HeyGen Avatar 4</b>  —  {ar}  {res}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select talking style:",
        reply_markup=kb(*buttons), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hga4_style_"))
async def hga4_style(cb: CallbackQuery, state: FSMContext):
    style = cb.data[11:]
    await state.update_data(v_style=style)
    data = await state.get_data()
    ar = data.get("v_ar", "—")
    res = data.get("v_res", "—")
    buttons_hga4 = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"hga4_dur_{m}"
        )
        for m, usd in HEYGEN_AVATAR_PRICES.items()
    ]
    # 3 per row for 1-9, 2 per row for 10-15
    rows = list(chunked(buttons_hga4[:9], 3)) + list(chunked(buttons_hga4[9:], 2))
    rows.append([back_btn(f"hga4_res_{res}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>HeyGen Avatar 4</b>  —  {ar}  {res}  {style}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hga4_dur_"))
async def hga4_dur(cb: CallbackQuery, state: FSMContext):
    minutes = int(cb.data[9:])
    usd = HEYGEN_AVATAR_PRICES[minutes]
    coins = usd_to_coins(usd)
    await state.update_data(
        v_tool="HeyGen Avatar 4", v_tid="hga4",
        v_dur=minutes, v_coins=coins, v_usd=usd,
        att_mode="free", att_start=None, att_end=None,
        att_imgs=[], att_vids=[], att_auds=[],
    )
    await _show_attach_menu(cb, state)
    await state.set_state(VideoStates.attach_mode)

# ═══════════════════════════════════════════════════════════
# HEYGEN TRANSLATE — Quality → Duration → Language → Video
# ═══════════════════════════════════════════════════════════

async def show_hgtr_quality(cb, state):
    await cb.message.edit_text(
        "◈  <b>HeyGen Translate</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select quality mode:\n\n"
        "  <b>Precision</b>  —  highest accuracy, slower\n"
        "  <b>Speed</b>  —  faster processing, lower cost",
        reply_markup=kb(
            [InlineKeyboardButton(text="◈  Precision", callback_data="hgtr_q_Precision")],
            [InlineKeyboardButton(text="◈  Speed",     callback_data="hgtr_q_Speed")],
            [back_btn("vsub_Avatar"), menu_btn()],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hgtr_q_"))
async def hgtr_quality(cb: CallbackQuery, state: FSMContext):
    quality = cb.data[7:]
    await state.update_data(v_quality=quality)
    prices = HEYGEN_TRANSLATE_PRECISION_PRICES if quality == "Precision" else HEYGEN_TRANSLATE_SPEED_PRICES
    buttons_hgtr = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"hgtr_dur_{m}"
        )
        for m, usd in prices.items()
    ]
    rows = list(chunked(buttons_hgtr[:9], 3)) + list(chunked(buttons_hgtr[9:], 2))
    rows.append([back_btn("vt_hgtr"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>HeyGen Translate</b>  —  {quality}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("hgtr_dur_"))
async def hgtr_dur(cb: CallbackQuery, state: FSMContext):
    minutes = int(cb.data[9:])
    data = await state.get_data()
    quality = data.get("v_quality", "Precision")
    prices = HEYGEN_TRANSLATE_PRECISION_PRICES if quality == "Precision" else HEYGEN_TRANSLATE_SPEED_PRICES
    usd = prices[minutes]
    coins = usd_to_coins(usd)
    await state.update_data(v_tool="HeyGen Translate", v_tid="hgtr", v_dur=minutes, v_coins=coins, v_usd=usd)
    await show_lang_select(cb, state, HEYGEN_TRANSLATE_LANGUAGES, "vlangh")

# ═══════════════════════════════════════════════════════════
# OMNIHUMAN 1.5 — Duration → Attachments
# ═══════════════════════════════════════════════════════════

async def show_omni_dur(cb, state):
    btns = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"omni_dur_{m}"
        )
        for m, usd in OMNIHUMAN_PRICES.items()
    ]
    rows = list(chunked(btns[:9], 3)) + list(chunked(btns[9:], 2))
    rows.append([back_btn("vsub_Avatar"), menu_btn()])
    await cb.message.edit_text(
        "◈  <b>OmniHuman 1.5</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Animate any portrait with voice.\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("omni_dur_"))
async def omni_dur(cb: CallbackQuery, state: FSMContext):
    minutes = int(cb.data[9:])
    usd = OMNIHUMAN_PRICES.get(minutes, 3.00)
    coins = usd_to_coins(usd)
    await state.update_data(
        v_tool="OmniHuman 1.5", v_tid="omni",
        v_dur=minutes, v_coins=coins, v_usd=usd,
        att_mode="free", att_start=None, att_end=None,
        att_imgs=[], att_vids=[], att_auds=[],
    )
    await _show_attach_menu(cb, state)
    await state.set_state(VideoStates.attach_mode)

# ═══════════════════════════════════════════════════════════
# AURORA AVATAR — AR → Resolution → Duration → Attachments
# ═══════════════════════════════════════════════════════════

@router.callback_query(F.data == "vt_aur1")
async def aur1_start(cb: CallbackQuery, state: FSMContext):
    await state.update_data(v_tool="Aurora Avatar", v_tid="aur1")
    btns = [
        InlineKeyboardButton(
            text=f"{m} min — {usd_to_coins(usd)}◈",
            callback_data=f"aur1_dur_{m}"
        )
        for m, usd in AURORA_AVATAR_PRICES.items()
    ]
    rows = list(chunked(btns[:9], 3)) + list(chunked(btns[9:], 2))
    rows.append([back_btn("vsub_Avatar"), menu_btn()])
    await cb.message.edit_text(
        "◈  <b>Aurora Avatar</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Select duration:",
        reply_markup=kb(*rows), parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("aur1_dur_"))
async def aur1_dur(cb: CallbackQuery, state: FSMContext):
    minutes = int(cb.data[9:])
    usd = AURORA_AVATAR_PRICES[minutes]
    coins = usd_to_coins(usd)
    await state.update_data(
        v_tool="Aurora Avatar", v_tid="aur1",
        v_dur=minutes, v_coins=coins, v_usd=usd,
        att_mode="free", att_start=None, att_end=None,
        att_imgs=[], att_vids=[], att_auds=[],
    )
    await _show_attach_menu(cb, state)
    await state.set_state(VideoStates.attach_mode)

