from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import IMAGE_TOOLS, usd_to_coins
from database import get_coins, spend_coins, create_order
from keyboards import kb, back_btn, menu_btn, chunked
import math

router = Router()

class ImageStates(StatesGroup):
    entering_prompt = State()
    collecting_refs = State()

# ── Category menu ─────────────────────────────────────────────
@router.callback_query(F.data == "cat_images")
async def images_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    buttons = []
    for name, info in IMAGE_TOOLS.items():
        buttons.append([InlineKeyboardButton(
            text=f"{info['emoji']}  {name}",
            callback_data=f"img_{name}"
        )])
    buttons.append([back_btn("main_menu", "⌂  Main Menu")])
    await cb.message.edit_text(
        "◈  <b>Image Generation</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a model to continue:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

# ── Tool selected ─────────────────────────────────────────────
@router.callback_query(F.data.startswith("img_") & ~F.data.startswith("img_ar_") & ~F.data.startswith("img_q_") & ~F.data.startswith("img_confirm") & ~F.data.startswith("img_add") & ~F.data.startswith("img_ref") & ~F.data.startswith("img_to_") & ~F.data.startswith("img_edit"))
async def image_tool_selected(cb: CallbackQuery, state: FSMContext):
    name = cb.data.replace("img_", "", 1)
    tool = IMAGE_TOOLS.get(name)
    if not tool:
        await cb.answer("Tool not found")
        return
    await state.update_data(img_tool=name)

    # Build aspect ratio buttons
    ars = tool.get("aspect_ratios", [])
    ar_buttons = [InlineKeyboardButton(text=ar, callback_data=f"img_ar_{ar}") for ar in ars]
    rows = list(chunked(ar_buttons, 4))

    # Pricing summary
    pricing = tool.get("pricing", {})
    if "per_gen" in pricing:
        coins = tool.get("coins", usd_to_coins(pricing["per_gen"]))
        price_line = f"  <b>{coins} coins</b>  per generation"
    elif "coins_by_quality" in tool:
        cbq = tool["coins_by_quality"]
        price_line = "  " + "  /  ".join(f"{q}: <b>{c} coins</b>" for q, c in cbq.items())
    else:
        price_line = ""

    text = (
        f"{tool['emoji']}  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {tool['desc']}\n\n"
        f"  Price   {price_line}\n\n"
        f"  Select aspect ratio:"
    )
    rows.append([back_btn("cat_images"), menu_btn()])
    await cb.message.edit_text(text, reply_markup=kb(*rows), parse_mode="HTML")

# ── Aspect ratio selected ─────────────────────────────────────
@router.callback_query(F.data.startswith("img_ar_"))
async def image_ar_selected(cb: CallbackQuery, state: FSMContext):
    ar = cb.data.replace("img_ar_", "")
    await state.update_data(img_ar=ar)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    qualities = tool.get("quality", [])

    if not qualities:
        # No quality step — go to prompt
        await state.update_data(img_quality=None)
        await ask_prompt(cb, state, name, tool)
        return

    q_buttons = [InlineKeyboardButton(text=q, callback_data=f"img_q_{q}") for q in qualities]
    rows = list(chunked(q_buttons, 3))
    rows.append([back_btn(f"img_{name}"), menu_btn()])
    await cb.message.edit_text(
        f"◈  <b>{name}</b>  —  {ar}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Select quality:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )

# ── Quality selected ──────────────────────────────────────────
@router.callback_query(F.data.startswith("img_q_"))
async def image_quality_selected(cb: CallbackQuery, state: FSMContext):
    quality = cb.data.replace("img_q_", "")
    await state.update_data(img_quality=quality)
    data = await state.get_data()
    name = data.get("img_tool")
    tool = IMAGE_TOOLS.get(name)
    await ask_prompt(cb, state, name, tool)

async def ask_prompt(cb: CallbackQuery, state: FSMContext, name: str, tool: dict):
    data = await state.get_data()
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    coins = _get_img_coins(tool, quality)
    user_coins = get_coins(cb.from_user.id)
    max_refs = tool.get("max_refs", 0)
    await state.update_data(img_coins=coins, img_refs=[])

    if max_refs > 0:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  Aspect ratio   {ar}\n"
            f"  Quality           {quality or '—'}\n"
            f"  Cost               <b>{coins} coins</b>\n"
            f"  Your balance   {user_coins} coins\n\n"
            f"  Attach reference images (optional)\n"
            f"  or skip to write your prompt.",
            reply_markup=kb(
                [InlineKeyboardButton(text=f"◈  Add Image Reference  (up to {max_refs})", callback_data="img_add_refs")],
                [InlineKeyboardButton(text="▸  Skip — Write Prompt", callback_data="img_to_prompt")],
                [back_btn(f"img_{name}"), menu_btn()],
            ),
            parse_mode="HTML"
        )
    else:
        await cb.message.edit_text(
            f"◈  <b>{name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  Aspect ratio   {ar}\n"
            f"  Quality           {quality or '—'}\n"
            f"  Cost               <b>{coins} coins</b>\n"
            f"  Your balance   {user_coins} coins\n\n"
            f"Enter your prompt:",
            reply_markup=kb([back_btn(f"img_{name}"), menu_btn()]),
            parse_mode="HTML"
        )
        await state.set_state(ImageStates.entering_prompt)

def _get_img_coins(tool: dict, quality: str) -> int:
    if "coins_by_quality" in tool and quality:
        return tool["coins_by_quality"].get(quality, tool.get("coins", 1))
    return tool.get("coins", usd_to_coins(tool.get("pricing", {}).get("per_gen", 0.05)))

# ── Prompt entered ────────────────────────────────────────────
@router.message(ImageStates.entering_prompt)
async def image_prompt_received(msg: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("img_tool")
    ar = data.get("img_ar")
    quality = data.get("img_quality")
    coins = data.get("img_coins", 1)
    prompt = msg.text

    await state.update_data(img_prompt=prompt)

    params_text = f"  Model           <b>{name}</b>\n  Aspect ratio   {ar}\n"
    if quality:
        params_text += f"  Quality           {quality}\n"
    params_text += f"  Cost               <b>{coins} coins</b>\n"

    await msg.answer(
        f"◈  <b>Order Summary</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{params_text}\n"
        f"  Prompt:\n<i>{prompt}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(text=f"◈  Confirm  ({coins} coins)", callback_data="img_confirm")],
            [InlineKeyboardButton(text="✎  Edit Prompt", callback_data=f"img_edit_prompt")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "img_edit_prompt")
async def img_edit_prompt(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "✎  Enter your new prompt:",
        reply_markup=kb([menu_btn()])
    )
    await state.set_state(ImageStates.entering_prompt)

# ── Confirm order ─────────────────────────────────────────────
@router.callback_query(F.data == "img_confirm")
async def image_confirm(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coins = data.get("img_coins", 1)
    uid = cb.from_user.id
    name = data.get("img_tool")
    prompt = data.get("img_prompt")

    # Validate state is intact
    if not name or not prompt or coins == 0:
        await cb.answer(
            "Session expired. Please start your order again.",
            show_alert=True
        )
        await state.clear()
        return

    if not spend_coins(uid, coins):
        await cb.answer("Insufficient coins. Please top up your wallet.", show_alert=True)
        return
    ar = data.get("img_ar")
    quality = data.get("img_quality")
    prompt = data.get("img_prompt")
    price_usd = round(coins * 0.05, 2)

    params = {"aspect_ratio": ar, "quality": quality, "prompt": prompt}
    oid = create_order(uid, cb.from_user.username or cb.from_user.first_name, name, params, coins, price_usd)

    await _notify_admin(cb, oid, name, params, coins, price_usd)

    await cb.message.edit_text(
        f"◌  <b>Order #{oid} Placed</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Model     <b>{name}</b>\n"
        f"  Coins      <b>{coins} deducted</b>\n\n"
        f"  Estimated time  ~2 minutes\n\n"
        f"  We will deliver your image here shortly.",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )
    await state.clear()

async def _notify_admin(cb: CallbackQuery, oid: int, name: str, params: dict, coins: int, price_usd: float):
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    bot = Bot(token=BOT_TOKEN)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Delivered", callback_data=f"delivered_{oid}"),
        InlineKeyboardButton(text="✕  Cancel", callback_data=f"cancel_order_{oid}"),
    ]])
    refs_line = f"\n  Refs      {len(params.get('refs') or [])} image(s)" if params.get("refs") else ""
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>New Image Order #{oid}</b>\n\n"
        f"  User     @{cb.from_user.username or '—'} (<code>{cb.from_user.id}</code>)\n"
        f"  Model   <b>{name}</b>\n"
        f"  AR         {params.get('aspect_ratio')}\n"
        f"  Quality   {params.get('quality') or '—'}{refs_line}\n"
        f"  Coins    <b>{coins}</b>  (${price_usd})",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await bot.send_message(
        ADMIN_ID,
        f"📋 <b>Prompt #{oid}:</b>\n\n<code>{params.get('prompt','—')}</code>",
        parse_mode="HTML"
    )
    # Send reference images
    for i, ref in enumerate(params.get("refs") or [], 1):
        try:
            if ref["type"] == "photo":
                await bot.send_photo(ADMIN_ID, ref["file_id"], caption=f"◈  Image Ref  @img{i}")
            else:
                await bot.send_document(ADMIN_ID, ref["file_id"], caption=f"◈  Image Ref  @img{i}")
        except Exception:
            pass

# ── Image Reference handlers ──────────────────────────────────
@router.callback_query(F.data == "img_add_refs")
async def img_add_refs(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    from config import IMAGE_TOOLS
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    await cb.message.edit_text(
        f"◈  <b>Image Reference</b>  ({len(refs)}/{max_refs})\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Send up to <b>{max_refs} images</b> as reference.\n\n"
        f"  Use <code>@img1</code>, <code>@img2</code> etc.\n"
        f"  in your prompt to refer to each image.\n\n"
        f"  Tap <b>Done</b> when finished.",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="img_refs_done")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.collecting_refs)

@router.message(ImageStates.collecting_refs, F.photo | F.document)
async def img_collect_ref(msg: Message, state: FSMContext):
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    from config import IMAGE_TOOLS
    tool = IMAGE_TOOLS.get(name, {})
    max_refs = tool.get("max_refs", 9)

    if len(refs) >= max_refs:
        await msg.answer(f"Maximum {max_refs} images reached. Tap Done to continue.")
        return

    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id
    ftype = "photo" if msg.photo else "document"
    refs.append({"file_id": file_id, "type": ftype, "ref": f"img{len(refs)+1}"})
    await state.update_data(img_refs=refs)
    await msg.answer(
        f"✓  Image @img{len(refs)} saved.  ({len(refs)}/{max_refs})\n"
        f"{'Send more or tap Done.' if len(refs) < max_refs else 'Maximum reached. Tap Done.'}",
        reply_markup=kb(
            [InlineKeyboardButton(text="✓  Done", callback_data="img_refs_done")],
            [menu_btn()],
        )
    )

@router.callback_query(F.data == "img_refs_done")
async def img_refs_done(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    refs = data.get("img_refs", [])
    name = data.get("img_tool", "")
    coins = data.get("img_coins", 1)
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")

    ref_line = f"\n  ◈  {len(refs)} image ref(s) attached\n" if refs else ""

    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Aspect ratio   {ar}\n"
        f"  Quality           {quality or '—'}\n"
        f"{ref_line}\n"
        f"  Cost               <b>{coins} coins</b>\n\n"
        f"Enter your prompt:",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)

@router.callback_query(F.data == "img_to_prompt")
async def img_to_prompt(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("img_tool", "")
    coins = data.get("img_coins", 1)
    ar = data.get("img_ar", "—")
    quality = data.get("img_quality", "—")
    await cb.message.edit_text(
        f"◈  <b>{name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Aspect ratio   {ar}\n"
        f"  Quality           {quality or '—'}\n"
        f"  Cost               <b>{coins} coins</b>\n\n"
        f"Enter your prompt:",
        reply_markup=kb([back_btn(f"img_{name}"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(ImageStates.entering_prompt)
