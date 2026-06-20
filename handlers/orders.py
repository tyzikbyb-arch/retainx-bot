from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import get_user_orders, get_lang
from keyboards import kb, menu_btn, back_btn
from i18n import t
import time

router = Router()

STATUS_EMOJI = {
    "processing": "○",
    "delivered":  "✓",
    "cancelled":  "✕",
}

STATUS_KEY = {
    "processing": "order_status_processing",
    "delivered":  "order_status_delivered",
    "cancelled":  "order_status_cancelled",
}

@router.message(F.text == "📋  Orders")
async def orders_from_reply(msg: Message, state: FSMContext):
    await show_orders(msg, msg.from_user.id)

@router.callback_query(F.data == "my_orders")
async def orders_cb(cb: CallbackQuery):
    await show_orders(cb, cb.from_user.id, edit=True)

async def show_orders(target, uid: int, edit: bool = False):
    lang = get_lang(uid)
    orders = get_user_orders(uid)

    if not orders:
        text = (
            f"{t('order_history_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('order_history_empty', lang)}"
        )
        markup = kb([menu_btn(lang)])
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

    buttons.append([menu_btn(lang)])

    text = (
        f"{t('order_history_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_history_total', lang, total=total)}\n"
        f"{t('order_history_completed', lang, delivered=delivered)}\n"
        f"{t('order_history_spent', lang, spent=spent)}\n\n"
        f"{t('order_history_tap_to_view', lang)}"
    )

    if edit:
        await target.message.edit_text(text, reply_markup=kb(*buttons), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb(*buttons), parse_mode="HTML")

@router.callback_query(F.data.startswith("od_"))
async def order_detail(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    oid = int(cb.data.replace("od_", ""))
    orders = get_user_orders(cb.from_user.id)
    order = next((o for o in orders if int(o["id"]) == oid), None)

    if not order:
        await cb.answer(t("order_not_found", lang), show_alert=True)
        return

    status = order.get("status", "—")
    emoji = STATUS_EMOJI.get(status, "◌")
    status_label = t(STATUS_KEY[status], lang) if status in STATUS_KEY else status.capitalize()
    params = order.get("params", {})
    created = order.get("created", 0)
    date_str = time.strftime("%b %d, %Y  %H:%M", time.localtime(int(created))) if created else "—"

    lines = ""
    if params.get("resolution"):    lines += t("order_detail_resolution", lang, res=params['resolution']) + "\n"
    if params.get("aspect_ratio"):  lines += t("order_detail_aspect_ratio", lang, ar=params['aspect_ratio']) + "\n"
    if params.get("duration"):      lines += t("order_detail_duration", lang, dur=params['duration']) + "\n"
    if params.get("quality"):       lines += t("order_detail_quality", lang, quality=params['quality']) + "\n"
    if params.get("audio"):         lines += t("order_detail_audio", lang) + "\n"
    if params.get("language"):      lines += t("order_detail_language", lang, lang=params['language']) + "\n"

    prompt = params.get("prompt") or "—"
    if len(prompt) > 300:
        prompt = prompt[:300] + "…"

    coins = int(order["coins"])

    text = (
        f"{t('order_detail_title', lang, oid=oid)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_detail_status', lang, emoji=emoji, status=status_label)}\n"
        f"{t('order_detail_model', lang, tool=order['tool'])}\n"
        f"{t('order_detail_coins', lang, coins=coins)}\n"
        f"{t('order_detail_date', lang, date=date_str)}\n\n"
        f"{lines}\n"
        f"{t('order_detail_prompt_label', lang)}\n<code>{prompt}</code>"
    )

    keyboard = kb(
        [InlineKeyboardButton(text=t("order_btn_repeat", lang), callback_data=f"repeat_{oid}")],
        [InlineKeyboardButton(text=t("order_btn_back", lang), callback_data="my_orders")],
        [menu_btn(lang)],
    )

    # If delivered and has file — send file first, then details
    file_id = order.get("file_id")
    file_type = order.get("file_type")

    if file_id and status == "delivered":
        try:
            from aiogram import Bot
            from config import BOT_TOKEN
            bot = Bot(token=BOT_TOKEN)
            uid = cb.from_user.id
            result_caption = t("order_your_result", lang)
            if file_type == "photo":
                await bot.send_photo(uid, file_id, caption=result_caption)
            else:
                # video/animation/document (and legacy NULL from before this
                # field was always populated) are all re-sent as a document —
                # send_video/send_animation re-trigger Telegram's silent-MP4
                # auto-play "GIF" preview, the same bug already fixed for the
                # original delivery path.
                await bot.send_document(uid, file_id, caption=result_caption,
                                         disable_content_type_detection=True)
        except Exception:
            pass

    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("repeat_"))
async def repeat_order(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    oid = int(cb.data.replace("repeat_", ""))
    orders = get_user_orders(cb.from_user.id)
    order = next((o for o in orders if int(o["id"]) == oid), None)

    if not order:
        await cb.answer(t("order_not_found", lang), show_alert=True)
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

    lines = t("order_repeat_model", lang, tool=tool) + "\n"
    if params.get("resolution"):   lines += t("order_repeat_resolution", lang, res=params['resolution']) + "\n"
    if params.get("aspect_ratio"): lines += t("order_repeat_aspect", lang, ar=params['aspect_ratio']) + "\n"
    if params.get("duration"):     lines += t("order_repeat_duration", lang, dur=params['duration']) + "\n"
    lines += t("order_repeat_cost", lang, coins=coins) + "\n"

    await cb.message.edit_text(
        f"{t('order_repeat_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{lines}\n"
        f"{t('order_repeat_prev_prompt', lang)}\n<code>{prompt}</code>\n\n"
        f"{t('order_repeat_enter_prompt', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("order_btn_back", lang), callback_data=f"od_{oid}")],
            [menu_btn(lang)],
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
