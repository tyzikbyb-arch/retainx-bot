from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID, BOT_TOKEN
from database import get_order, update_order_status, add_coins
from keyboards import kb, menu_btn
from aiogram.types import InlineKeyboardButton

router = Router()

class AdminStates(StatesGroup):
    sending_result = State()

@router.callback_query(F.data.startswith("delivered_"))
async def mark_delivered(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("delivered_", ""))
    await state.update_data(admin_oid=oid)
    await state.set_state(AdminStates.sending_result)
    await cb.message.answer(
        f"📤  Attach the file for Order #{oid}\n"
        f"(Send video, image, or document)"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order_admin(cb: CallbackQuery):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("cancel_order_", ""))
    order = get_order(oid)
    if not order:
        await cb.answer("Order not found")
        return
    # Refund coins
    add_coins(order["user_id"], order["coins"])
    update_order_status(oid, "cancelled")
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        order["user_id"],
        f"◌  <b>Order #{oid} Cancelled</b>\n\n"
        f"  <b>{order['coins']} coins</b> have been refunded to your wallet.\n"
        f"  We apologise for the inconvenience.",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✕  Order #{oid} cancelled — {order['coins']} coins refunded.")
    await cb.answer()

@router.callback_query(F.data.startswith("delivered_"))
async def mark_delivered_quick(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("delivered_", ""))
    await state.update_data(admin_oid=oid)
    await state.set_state(AdminStates.sending_result)
    await cb.message.answer(f"📤  Attach file for Order #{oid}")
    await cb.answer()

@router.message(AdminStates.sending_result, F.from_user.id == ADMIN_ID)
async def admin_deliver_file(msg: Message, state: FSMContext):
    if not (msg.video or msg.document or msg.photo or msg.animation):
        await msg.answer("Please attach a video, image, or document.")
        return
    data = await state.get_data()
    oid = data.get("admin_oid")
    target_uid = data.get("admin_target_uid")
    order = get_order(oid)

    # If order not in DB but we have target_uid from /deliver command
    if not order and not target_uid:
        await msg.answer(
            f"⚠️ Order #{oid} not found in database.\n\n"
            f"Use /deliver USER_ID to send directly:\n"
            f"Example: <code>/deliver 939285095</code>",
            parse_mode="HTML"
        )
        await state.clear()
        return

    uid = target_uid if target_uid else order["user_id"]
    tool = order["tool"] if order else "—"
    prompt = order["params"].get("prompt", "—") if order else "—"

    caption = (
        f"◈  <b>Your Order is Ready</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Order     #{oid}\n"
        f"  Model     {tool}\n\n"
        f"  Thank you for choosing RetainX Studio."
    )
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)

    try:
        if msg.video:
            await bot.send_video(uid, msg.video.file_id, caption=caption, parse_mode="HTML")
        elif msg.animation:
            await bot.send_animation(uid, msg.animation.file_id, caption=caption, parse_mode="HTML")
        elif msg.document:
            await bot.send_document(uid, msg.document.file_id, caption=caption, parse_mode="HTML")
        elif msg.photo:
            await bot.send_photo(uid, msg.photo[-1].file_id, caption=caption, parse_mode="HTML")

        if order:
            update_order_status(oid, "delivered")
        await msg.answer(f"✓  Delivered to user {uid}.")
    except Exception as e:
        await msg.answer(f"❌ Failed to deliver: {e}")
    await state.clear()
