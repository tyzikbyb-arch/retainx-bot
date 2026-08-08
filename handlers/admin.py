import os
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramRetryAfter
from config import ADMIN_ID, BOT_TOKEN
from database import get_order, update_order_status, add_coins, save_delivery, get_lang, set_blogger, get_is_blogger, cancel_order_atomic, get_promo_code, create_promo_code, get_promo_code_by_uid
from keyboards import kb, menu_btn
from aiogram.types import InlineKeyboardButton
from i18n import t

router = Router()

# Same branded cover used for voice previews in handlers/voiceover.py, shown
# in place of Telegram's generic grey file icon when delivering an audio order.
_THUMB_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "audio_thumb.jpg")
_AUDIO_THUMB_BYTES = None

def _audio_thumb() -> BufferedInputFile | None:
    global _AUDIO_THUMB_BYTES
    if _AUDIO_THUMB_BYTES is None:
        try:
            with open(_THUMB_PATH, "rb") as f:
                _AUDIO_THUMB_BYTES = f.read()
        except FileNotFoundError:
            return None
    return BufferedInputFile(_AUDIO_THUMB_BYTES, filename="thumb.jpg")

class AdminStates(StatesGroup):
    sending_result = State()
    cancelling_order = State()

@router.callback_query(F.data.startswith("delivered_"))
async def mark_delivered(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_ID:
        return
    oid = int(cb.data.replace("delivered_", ""))
    # Clear admin_target_uid so a stale /deliver uid doesn't route this file to the wrong user
    await state.update_data(admin_oid=oid, admin_target_uid=None)
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

@router.message(AdminStates.cancelling_order, F.from_user.id == ADMIN_ID, F.text)
async def admin_cancel_with_reason(msg: Message, state: FSMContext):
    data = await state.get_data()
    oid = data.get("admin_cancel_oid")
    await state.clear()
    if not oid:
        await msg.answer("⚠️ No order ID in state.")
        return
    reason = msg.text.strip() if msg.text else ""
    if reason == "-":
        reason = ""
    from handlers import spinner as sp
    await sp.stop(oid)
    success, user_id, coins = cancel_order_atomic(oid)
    if not success:
        order = get_order(oid)
        if not order:
            await msg.answer(f"⚠️ Order #{oid} not found.")
        else:
            await msg.answer(
                f"⚠️ Order #{oid} is already <b>{order['status']}</b> — refund skipped.",
                parse_mode="HTML"
            )
        return
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    lang = get_lang(user_id)
    if reason:
        user_text = (
            f"◌  <b>Order #{oid} Cancelled</b>\n\n"
            f"  <b>{coins} coins</b> have been refunded to your wallet.\n\n"
            f"  Reason: {reason}"
        )
    else:
        user_text = (
            f"◌  <b>Order #{oid} Cancelled</b>\n\n"
            f"  <b>{coins} coins</b> have been refunded to your wallet.\n"
            f"  We apologise for the inconvenience."
        )
    try:
        await bot.send_message(
            user_id, user_text,
            parse_mode="HTML",
            reply_markup=kb([menu_btn(lang)])
        )
    except Exception:
        pass
    finally:
        await bot.session.close()
    admin_note = f"✕  Order #{oid} cancelled — {coins} coins refunded."
    if reason:
        admin_note += f"\n  Reason sent: {reason}"
    await msg.answer(admin_note)

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

    # Guard against double-delivery (admin re-clicks Deliver on an already-delivered order)
    if order and order.get("status") == "delivered":
        await msg.answer(f"⚠️ Order #{oid} is already delivered. Aborting to prevent duplicate.")
        await state.clear()
        return

    uid = target_uid if target_uid else order["user_id"]
    tool = order["tool"] if order else "—"

    lang = get_lang(uid)
    caption = t("order_ready_caption", lang, oid=oid, tool=tool)

    from aiogram import Bot
    from handlers import spinner as sp
    await sp.stop(oid)
    bot = Bot(token=BOT_TOKEN)

    file_id = None
    file_type = None
    if msg.video:
        file_id = msg.video.file_id;        file_type = "document"
    elif msg.animation:
        file_id = msg.animation.file_id;    file_type = "document"
    elif msg.document:
        file_id = msg.document.file_id;     file_type = "document"
    elif msg.photo:
        file_id = msg.photo[-1].file_id;    file_type = "photo"
    elif msg.audio or msg.voice:
        file_id = (msg.audio or msg.voice).file_id; file_type = "document"

    delivered = False
    for attempt in range(3):
        try:
            # Video/animation/document are always re-sent via send_document
            # (not send_video/send_animation), saved as file_type="document" so
            # any later re-send (handlers/orders.py "My Orders" detail view)
            # also goes through send_document instead of resurrecting the GIF
            # bug from a stale file_type. disable_content_type_detection stops
            # Telegram from still auto-detecting a silent MP4 and rendering it
            # as an auto-playing GIF-style preview even though it's sent as a
            # plain document — matching the automated worker delivery path in
            # playwright_worker.py.
            if file_type == "photo":
                await bot.send_photo(uid, file_id, caption=caption, parse_mode="HTML")
            elif file_type == "document" and (msg.audio or msg.voice):
                await bot.send_document(uid, file_id, thumbnail=_audio_thumb(),
                                        caption=caption, parse_mode="HTML",
                                        disable_content_type_detection=True)
            else:
                await bot.send_document(uid, file_id, caption=caption, parse_mode="HTML",
                                        disable_content_type_detection=True)
            delivered = True
            break
        except TelegramRetryAfter as e:
            wait = e.retry_after + 2
            await msg.answer(f"⏳ Telegram rate limit — ожидаю {wait}s и повторяю... (попытка {attempt + 1}/3)")
            await asyncio.sleep(wait)
        except Exception as e:
            await msg.answer(f"❌ Failed to deliver: {e}")
            await bot.session.close()
            await state.clear()
            return

    if delivered:
        if order and file_id:
            save_delivery(oid, file_id, file_type)
        elif order:
            update_order_status(oid, "delivered")
        await msg.answer(f"✓  Delivered to user {uid}.")
    else:
        await msg.answer("❌ Failed to deliver after 3 attempts — Telegram rate limit. Try again later.")

    await bot.session.close()
    await state.clear()

@router.message(Command("setblogger"))
async def cmd_set_blogger(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("Usage: /setblogger USER_ID")
        return
    try:
        uid = int(parts[1])
        already = get_is_blogger(uid)
        set_blogger(uid, True)
        status = "already was" if already else "✓ set"
        await msg.answer(f"Blogger {status}: user {uid}")
    except Exception as e:
        await msg.answer(f"❌ Error: {e}")

@router.message(Command("removeblogger"))
async def cmd_remove_blogger(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.answer("Usage: /removeblogger USER_ID")
        return
    try:
        uid = int(parts[1])
        set_blogger(uid, False)
        await msg.answer(f"✓ Blogger status removed: user {uid}")
    except Exception as e:
        await msg.answer(f"❌ Error: {e}")

@router.message(Command("setpromo"))
async def cmd_set_promo(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 3 or not parts[1].isdigit():
        await msg.answer("Usage: /setpromo USER_ID CODE\nExample: /setpromo 939285095 MYBLOG25")
        return
    try:
        uid = int(parts[1])
        code = parts[2].upper()
        existing_for_user = get_promo_code_by_uid(uid)
        if existing_for_user:
            await msg.answer(f"⚠️ User {uid} already has promo code: {existing_for_user['code']}")
            return
        if get_promo_code(code):
            await msg.answer(f"⚠️ Code {code} is already taken by another user.")
            return
        create_promo_code(uid, code)
        await msg.answer(f"✓ Promo code {code} assigned to user {uid}")
    except Exception as e:
        await msg.answer(f"❌ Error: {e}")
