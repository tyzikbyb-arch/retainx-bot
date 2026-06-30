from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID, BOT_TOKEN
from database import get_order, update_order_status, add_coins, save_delivery
from keyboards import kb, menu_btn
from aiogram.types import InlineKeyboardButton

router = Router()

class AdminStates(StatesGroup):
    sending_result = State()
    cancelling_order = State()

@router.callback_query(F.data.startswith("delivered_"))
async def mark_delivered(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("delivered_", ""))
    await state.update_data(admin_oid=oid)
    await state.set_state(AdminStates.sending_result)
    await cb.message.answer(
        f"▸  Attach the file for Order #{oid}\n"
        f"(Send video, image, audio, or document)"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order_admin(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("cancel_order_", ""))
    order = get_order(oid)
    if not order:
        await cb.answer("Order not found")
        return
    await state.update_data(admin_cancel_oid=oid)
    await state.set_state(AdminStates.cancelling_order)
    await cb.message.answer(
        f"✕  <b>Cancel Order #{oid}</b>\n\n"
        f"Send the reason for cancellation — it will be shown to the user.\n"
        f"Or send <code>-</code> to cancel without a reason.",
        parse_mode="HTML"
    )
    await cb.answer()

@router.message(AdminStates.cancelling_order, F.from_user.id == ADMIN_ID)
async def admin_cancel_with_reason(msg: Message, state: FSMContext):
    data = await state.get_data()
    oid = data.get("admin_cancel_oid")
    await state.clear()
    if not oid:
        await msg.answer("⚠️ No order ID in state.")
        return
    order = get_order(oid)
    if not order:
        await msg.answer(f"⚠️ Order #{oid} not found.")
        return
    reason = msg.text.strip() if msg.text else ""
    if reason == "-":
        reason = ""
    add_coins(order["user_id"], order["coins"])
    update_order_status(oid, "cancelled")
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    if reason:
        user_text = (
            f"◌  <b>Order #{oid} Cancelled</b>\n\n"
            f"  <b>{order['coins']} coins</b> have been refunded to your wallet.\n\n"
            f"  Reason: {reason}"
        )
    else:
        user_text = (
            f"◌  <b>Order #{oid} Cancelled</b>\n\n"
            f"  <b>{order['coins']} coins</b> have been refunded to your wallet.\n"
            f"  We apologise for the inconvenience."
        )
    await bot.send_message(order["user_id"], user_text, parse_mode="HTML")
    admin_note = f"✕  Order #{oid} cancelled — {order['coins']} coins refunded."
    if reason:
        admin_note += f"\n  Reason sent: {reason}"
    await msg.answer(admin_note)

@router.callback_query(F.data.startswith("delivered_"))
async def mark_delivered_quick(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("delivered_", ""))
    await state.update_data(admin_oid=oid)
    await state.set_state(AdminStates.sending_result)
    await cb.message.answer(f"▸  Attach file for Order #{oid}")
    await cb.answer()

@router.message(AdminStates.sending_result, F.from_user.id == ADMIN_ID)
async def admin_deliver_file(msg: Message, state: FSMContext):
    if not (msg.video or msg.document or msg.photo or msg.animation or msg.audio or msg.voice):
        await msg.answer("Please attach a video, image, audio, or document.")
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
        file_id = None
        file_type = None
        # Video/animation/document are always re-sent via send_document
        # (not send_video/send_animation), saved as file_type="document" so
        # any later re-send (handlers/orders.py "My Orders" detail view)
        # also goes through send_document instead of resurrecting the GIF
        # bug from a stale file_type. disable_content_type_detection stops
        # Telegram from still auto-detecting a silent MP4 and rendering it
        # as an auto-playing GIF-style preview even though it's sent as a
        # plain document — matching the automated worker delivery path in
        # playwright_worker.py.
        if msg.video:
            file_id = msg.video.file_id
            file_type = "document"
            await bot.send_document(uid, file_id, caption=caption, parse_mode="HTML",
                                     disable_content_type_detection=True)
        elif msg.animation:
            file_id = msg.animation.file_id
            file_type = "document"
            await bot.send_document(uid, file_id, caption=caption, parse_mode="HTML",
                                     disable_content_type_detection=True)
        elif msg.document:
            file_id = msg.document.file_id
            file_type = "document"
            await bot.send_document(uid, file_id, caption=caption, parse_mode="HTML",
                                     disable_content_type_detection=True)
        elif msg.photo:
            file_id = msg.photo[-1].file_id
            file_type = "photo"
            await bot.send_photo(uid, file_id, caption=caption, parse_mode="HTML")
        elif msg.audio or msg.voice:
            # Sent via send_document (not send_audio) so it doesn't join
            # Telegram's chat-wide continuous-playback queue, same fix
            # already applied to voiceover previews in handlers/voiceover.py.
            file_id = (msg.audio or msg.voice).file_id
            file_type = "document"
            await bot.send_document(uid, file_id, caption=caption, parse_mode="HTML",
                                     disable_content_type_detection=True)

        if order and file_id:
            save_delivery(oid, file_id, file_type)
        elif order:
            update_order_status(oid, "delivered")
        await msg.answer(f"✓  Delivered to user {uid}.")
    except Exception as e:
        await msg.answer(f"❌ Failed to deliver: {e}")
    await state.clear()
