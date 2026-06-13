from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import get_user_orders
from keyboards import kb, menu_btn
import time

router = Router()

# get_user_orders imported from database

STATUS_EMOJI = {
    "processing": "⏳",
    "delivered":  "✅",
    "cancelled":  "✕",
}

@router.message(F.text == "📋  Orders")
async def orders_from_reply(msg: Message, state: FSMContext):
    await show_orders(msg, msg.from_user.id)

@router.callback_query(F.data == "my_orders")
async def orders_cb(cb: CallbackQuery):
    await show_orders(cb, cb.from_user.id, edit=True)

@router.callback_query(F.data.startswith("order_detail_"))
async def order_detail(cb: CallbackQuery):
    oid = int(cb.data.replace("order_detail_", ""))
    data = _load_orders()
    order = data["orders"].get(str(oid))
    if not order:
        await cb.answer("Order not found")
        return

    status = order.get("status", "—")
    emoji = STATUS_EMOJI.get(status, "◌")
    params = order.get("params", {})
    created = order.get("created", 0)
    date_str = time.strftime("%b %d, %Y  %H:%M", time.localtime(created)) if created else "—"

    lines = ""
    if params.get("resolution"):   lines += f"  Resolution    {params['resolution']}\n"
    if params.get("aspect_ratio"): lines += f"  Aspect ratio  {params['aspect_ratio']}\n"
    if params.get("duration"):     lines += f"  Duration       {params['duration']} sec\n"
    if params.get("quality"):      lines += f"  Quality          {params['quality']}\n"
    if params.get("language"):     lines += f"  Language      {params['language']}\n"

    prompt = params.get("prompt") or "—"
    if len(prompt) > 200:
        prompt = prompt[:200] + "…"

    await cb.message.edit_text(
        f"◈  <b>Order #{oid}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Status    {emoji}  <b>{status.capitalize()}</b>\n"
        f"  Model     <b>{order['tool']}</b>\n"
        f"  Coins      {order['coins']}◈\n"
        f"  Date        {date_str}\n\n"
        f"{lines}\n"
        f"  Prompt:\n<i>{prompt}</i>",
        reply_markup=kb(
            [InlineKeyboardButton(text="← Back to Orders", callback_data="my_orders")],
            [menu_btn()],
        ),
        parse_mode="HTML"
    )

async def show_orders(target, uid: int, edit: bool = False):
    orders = get_user_orders(uid)

    if not orders:
        text = (
            "📋  <b>Order History</b>\n"
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

    # Sort newest first
    orders_sorted = sorted(orders, key=lambda o: o.get("created", 0), reverse=True)

    buttons = []
    for o in orders_sorted[:20]:  # Show last 20
        oid = o["id"]
        status = o.get("status", "—")
        emoji = STATUS_EMOJI.get(status, "◌")
        tool = o["tool"]
        if len(tool) > 18:
            tool = tool[:18] + "…"
        coins = o["coins"]
        buttons.append([InlineKeyboardButton(
            text=f"{emoji}  #{oid}  {tool}  ·  {coins}◈",
            callback_data=f"order_detail_{oid}"
        )])

    buttons.append([menu_btn()])

    total = len(orders)
    delivered = sum(1 for o in orders if o.get("status") == "delivered")
    spent = sum(o["coins"] for o in orders)

    text = (
        f"📋  <b>Order History</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Total orders    <b>{total}</b>\n"
        f"  Completed       <b>{delivered}</b>\n"
        f"  Coins spent     <b>{spent}◈</b>\n\n"
        f"  Tap any order for details:"
    )

    if edit:
        await target.message.edit_text(text, reply_markup=kb(*buttons), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb(*buttons), parse_mode="HTML")
