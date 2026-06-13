from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import get_user_orders
from keyboards import kb, menu_btn
import time

router = Router()

STATUS_EMOJI = {
    "processing": "○",
    "delivered":  "✓",
    "cancelled":  "✕",
}

@router.message(F.text == "📋  Orders")
async def orders_from_reply(msg: Message, state: FSMContext):
    await show_orders(msg, msg.from_user.id)

@router.callback_query(F.data == "my_orders")
async def orders_cb(cb: CallbackQuery):
    await show_orders(cb, cb.from_user.id, edit=True)

async def show_orders(target, uid: int, edit: bool = False):
    orders = get_user_orders(uid)

    if not orders:
        text = (
            "◈  <b>Order History</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  You have no orders yet.\n\n"
            "  Start generating to see your history here."
        )
        markup = kb([menu_btn()])
        if edit:
            await target.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
        else:
            await target.answer(text, reply_markup=markup, parse_mode="HTML")
        return

    orders_sorted = sorted(orders, key=lambda o: o.get("created", 0), reverse=True)

    total = len(orders)
    delivered = sum(1 for o in orders if o.get("status") == "delivered")
    spent = sum(int(o["coins"]) for o in orders)

    buttons = []
    for o in orders_sorted[:20]:
        oid = int(o["id"])
        status = o.get("status", "—")
        emoji = STATUS_EMOJI.get(status, "◌")
        tool = str(o["tool"])
        if len(tool) > 20:
            tool = tool[:20] + "…"
        coins = int(o["coins"])
        buttons.append([InlineKeyboardButton(
            text=f"{emoji}  #{oid}  {tool}  ·  {coins}◈",
            callback_data=f"od_{oid}"
        )])

    buttons.append([menu_btn()])

    text = (
        f"◈  <b>Order History</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Total orders    <b>{total}</b>\n"
        f"  Completed       <b>{delivered}</b>\n"
        f"  Coins spent     <b>{spent}◈</b>\n\n"
        f"  Tap any order to view details:"
    )

    if edit:
        await target.message.edit_text(text, reply_markup=kb(*buttons), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb(*buttons), parse_mode="HTML")

@router.callback_query(F.data.startswith("od_"))
async def order_detail(cb: CallbackQuery):
    oid = int(cb.data.replace("od_", ""))
    orders = get_user_orders(cb.from_user.id)
    order = next((o for o in orders if int(o["id"]) == oid), None)

    if not order:
        await cb.answer("Order not found", show_alert=True)
        return

    status = order.get("status", "—")
    emoji = STATUS_EMOJI.get(status, "◌")
    params = order.get("params", {})
    created = order.get("created", 0)
    date_str = time.strftime("%b %d, %Y  %H:%M", time.localtime(int(created))) if created else "—"

    lines = ""
    if params.get("resolution"):    lines += f"  Resolution    {params['resolution']}\n"
    if params.get("aspect_ratio"):  lines += f"  Aspect ratio  {params['aspect_ratio']}\n"
    if params.get("duration"):      lines += f"  Duration       {params['duration']} sec\n"
    if params.get("quality"):       lines += f"  Quality          {params['quality']}\n"
    if params.get("audio"):         lines += f"  Audio            Yes\n"
    if params.get("language"):      lines += f"  Language      {params['language']}\n"

    prompt = params.get("prompt") or "—"
    if len(prompt) > 300:
        prompt = prompt[:300] + "…"

    coins = int(order["coins"])

    text = (
        f"◈  <b>Order #{oid}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Status    {emoji}  <b>{status.capitalize()}</b>\n"
        f"  Model     <b>{order['tool']}</b>\n"
        f"  Coins      {coins}◈\n"
        f"  Date        {date_str}\n\n"
        f"{lines}\n"
        f"  Prompt:\n<code>{prompt}</code>"
    )

    await cb.message.edit_text(
        text,
        reply_markup=kb(
            [InlineKeyboardButton(text="↺  Repeat this order", callback_data=f"repeat_{oid}")],
            [InlineKeyboardButton(text="← Back", callback_data="my_orders")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("repeat_"))
async def repeat_order(cb: CallbackQuery, state: FSMContext):
    oid = int(cb.data.replace("repeat_", ""))
    orders = get_user_orders(cb.from_user.id)
    order = next((o for o in orders if int(o["id"]) == oid), None)

    if not order:
        await cb.answer("Order not found", show_alert=True)
        return

    params = order.get("params", {})
    tool = order["tool"]
    coins = int(order["coins"])
    prompt = params.get("prompt", "—")

    # Pre-fill state with previous order data
    await state.update_data(
        v_tool=tool,
        v_coins=coins,
        v_res=params.get("resolution"),
        v_ar=params.get("aspect_ratio"),
        v_dur=params.get("duration"),
        v_audio=params.get("audio", False),
        v_lang=params.get("language"),
        v_usd=order.get("price_usd", 0),
        img_tool=tool,
        img_coins=coins,
        img_ar=params.get("aspect_ratio"),
        img_quality=params.get("quality"),
    )

    lines = f"  Model     <b>{tool}</b>\n"
    if params.get("resolution"):   lines += f"  Resolution   {params['resolution']}\n"
    if params.get("aspect_ratio"): lines += f"  Aspect        {params['aspect_ratio']}\n"
    if params.get("duration"):     lines += f"  Duration      {params['duration']} sec\n"
    lines += f"  Cost           <b>{coins} coins</b>\n"

    await cb.message.edit_text(
        f"◈  <b>Repeat Order</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{lines}\n"
        f"  Previous prompt:\n<code>{prompt}</code>\n\n"
        f"  Enter your prompt (or send same as above):",
        reply_markup=kb(
            [InlineKeyboardButton(text="← Back", callback_data=f"od_{oid}")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )

    # Set appropriate state
    from handlers.video import VideoStates
    from handlers.images import ImageStates
    # Determine if video or image
    from config import IMAGE_TOOLS
    if tool in IMAGE_TOOLS:
        await state.set_state(ImageStates.entering_prompt)
    else:
        await state.set_state(VideoStates.entering_prompt)
