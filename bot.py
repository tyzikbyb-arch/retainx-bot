import asyncio, logging, os
from aiogram import Bot, Dispatcher, F
from aiohttp import web
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
try:
    from aiogram.fsm.storage.redis import RedisStorage
    import os
    REDIS_URL = os.environ.get("REDIS_URL", "")
    if REDIS_URL:
        storage = RedisStorage.from_url(REDIS_URL)
        events_isolation = storage.create_isolation()
        print("Using Redis storage")
    else:
        storage = MemoryStorage()
        events_isolation = SimpleEventIsolation()
        print("Using Memory storage")
except Exception:
    storage = MemoryStorage()
    events_isolation = SimpleEventIsolation()
    print("Redis unavailable, using Memory storage")

from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMIN_ID, WELCOME_BONUS, REFERRAL_JOIN_BONUS
from database import is_new_user, add_coins, get_coins, set_referred_by, get_lang, set_lang
from keyboards import kb, menu_btn, client_kb
from i18n import t, CLIENT_ACTION_BY_TEXT, CLIENT_TEXTS
from handlers import credits, images, video, admin as admin_handler, orders as orders_handler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage, events_isolation=events_isolation)

dp.include_router(credits.router)
dp.include_router(images.router)
dp.include_router(video.router)
dp.include_router(admin_handler.router)
dp.include_router(orders_handler.router)

# ── Keyboards ─────────────────────────────────────────────────
ADMIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="≡  All Orders"),  KeyboardButton(text="◈  Users")],
        [KeyboardButton(text="✉  Msg User"),    KeyboardButton(text="＋  Add Coins")],
        [KeyboardButton(text="📤  Deliver"),     KeyboardButton(text="✕  Cancel Order")],
        [KeyboardButton(text="◌  Commands")],
    ],
    resize_keyboard=True,
    persistent=True,
)

def get_kb(uid: int, lang: str = "en"):
    return ADMIN_KB if uid == ADMIN_ID else client_kb(lang)

# ── Shared main-menu builders ────────────────────────────────
def build_main_menu_text(coins: int, lang: str) -> str:
    return (
        f"{t('main_menu_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('main_menu_balance', lang, coins=coins)}\n\n"
        f"{t('main_menu_desc', lang)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

def build_main_menu_kb(coins: int, lang: str) -> InlineKeyboardMarkup:
    return kb(
        [InlineKeyboardButton(text=t("btn_video_generation", lang), callback_data="cat_video")],
        [InlineKeyboardButton(text=t("btn_image_generation", lang), callback_data="cat_images")],
        [InlineKeyboardButton(text=t("btn_audio_voice", lang),      callback_data="cat_audio")],
        [InlineKeyboardButton(text=t("btn_wallet_coins", lang, coins=coins), callback_data="wallet")],
        [InlineKeyboardButton(text=t("btn_pricing", lang),  callback_data="pricing_menu")],
        [InlineKeyboardButton(text=t("btn_language", lang), callback_data="lang_menu")],
        [InlineKeyboardButton(text=t("btn_support", lang),  url="https://t.me/RetainXStudio")],
    )

# ── /start ────────────────────────────────────────────────────
@dp.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    uid = msg.from_user.id
    args = msg.text.split()

    new = is_new_user(uid)

    # Process referral link BEFORE add_coins so we know the total bonus upfront
    ref_id_val = None
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            rid = int(args[1].replace("ref_", ""))
            if rid != uid:
                ref_id_val = rid
                set_referred_by(uid, rid)
        except ValueError:
            pass

    if new:
        bonus = WELCOME_BONUS + (REFERRAL_JOIN_BONUS if ref_id_val else 0)
        add_coins(uid, bonus)
        # Notify referrer that their friend just joined
        if ref_id_val:
            async def _notify_referrer():
                try:
                    ref_lang = get_lang(ref_id_val)
                    uname = f"@{msg.from_user.username}" if msg.from_user.username else f"ID {uid}"
                    await bot.send_message(
                        ref_id_val,
                        t("referral_friend_joined", ref_lang, username=uname),
                        parse_mode="HTML"
                    )
                except Exception:
                    pass
            asyncio.create_task(_notify_referrer())

    coins = get_coins(uid)
    lang = get_lang(uid)

    if new:
        total_bonus = WELCOME_BONUS + (REFERRAL_JOIN_BONUS if ref_id_val else 0)
        # New user welcome
        welcome_text = (
            f"{t('welcome_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('welcome_body', lang)}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"{t('welcome_bonus', lang, bonus=total_bonus, coins=coins)}"
        )
        keyboard = kb(
            [InlineKeyboardButton(text=t("btn_start_generating", lang), callback_data="cat_video")],
            [InlineKeyboardButton(text=t("btn_view_pricing", lang),     callback_data="pricing_menu")],
            [InlineKeyboardButton(text=t("btn_language", lang),         callback_data="lang_menu")],
            [InlineKeyboardButton(text=t("btn_support", lang),          url="https://t.me/RetainXStudio")],
        )
        await msg.answer(welcome_text, reply_markup=get_kb(uid, lang), parse_mode="HTML")
        await msg.answer(t("what_create", lang), reply_markup=keyboard, parse_mode="HTML")
    else:
        # Returning user
        text = build_main_menu_text(coins, lang)
        keyboard = build_main_menu_kb(coins, lang)
        await msg.answer(text, reply_markup=get_kb(uid, lang), parse_mode="HTML")
        await msg.answer(t("choose_option", lang), reply_markup=keyboard, parse_mode="HTML")

# ── Panel button router ───────────────────────────────────────
ADMIN_PANEL_BUTTONS = {
    "≡  All Orders", "✉  Msg User", "＋  Add Coins",
    "📤  Deliver", "✕  Cancel Order", "◌  Admin Help", "◈  Users", "◌  Commands",
}
PANEL_BUTTONS = CLIENT_TEXTS | ADMIN_PANEL_BUTTONS

@dp.message(F.text.in_(PANEL_BUTTONS))
async def panel_router(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    text = msg.text
    action = CLIENT_ACTION_BY_TEXT.get(text)
    lang = get_lang(uid) if action else "en"

    # Client buttons
    if action == "main_menu":
        await state.clear()
        coins = get_coins(uid)
        await msg.answer(
            build_main_menu_text(coins, lang),
            reply_markup=build_main_menu_kb(coins, lang), parse_mode="HTML"
        )
    elif action == "wallet":
        from handlers.credits import show_wallet
        await show_wallet(msg, state)
    elif action == "video":
        await state.clear()
        buttons = [[InlineKeyboardButton(text=video.subcat_label(s, lang), callback_data=f"vsub_{s}")] for s in video.VIDEO_SUBCATS]
        buttons.append([InlineKeyboardButton(text=t("btn_back", lang),   callback_data="main_menu")])
        await msg.answer(
            f"{t('video_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('select_category', lang)}",
            reply_markup=kb(*buttons), parse_mode="HTML"
        )
    elif action == "images":
        await state.clear()
        from config import IMAGE_TOOLS
        buttons = [[InlineKeyboardButton(text=f"{info['emoji']}  {name}", callback_data=f"img_{name}")] for name, info in IMAGE_TOOLS.items()]
        buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")])
        await msg.answer(
            f"{t('images_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('select_model', lang)}",
            reply_markup=kb(*buttons), parse_mode="HTML"
        )
    elif action == "audio":
        await msg.answer(
            f"{t('audio_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('audio_body', lang)}",
            reply_markup=kb([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")]),
            parse_mode="HTML"
        )
    elif action == "orders":
        from handlers.orders import show_orders
        await show_orders(msg, uid)
    elif action == "support":
        await msg.answer(
            f"{t('support_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('support_body', lang)}",
            parse_mode="HTML"
        )

    # Admin buttons
    elif text == "≡  All Orders" and uid == ADMIN_ID:
        from database import _load_orders_all
        orders = _load_orders_all()
        if not orders:
            await msg.answer("No orders yet.")
            return
        text_out = "◈  <b>Recent Orders</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for o in orders[:15]:
            s = "✓" if o["status"] == "delivered" else ("✕" if o["status"] == "cancelled" else "○")
            text_out += f"  {s}  #{o['id']}  <b>{o['tool']}</b>  ·  @{o['username']}  ·  {o['coins']}◈\n"
        await msg.answer(text_out, parse_mode="HTML")

    elif text == "✉  Msg User" and uid == ADMIN_ID:
        await msg.answer(
            "◈  <b>Send Message</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "<code>/msg USER_ID Your text</code>\n\n"
            "Example:\n<code>/msg 939285095 Your order is ready!</code>",
            parse_mode="HTML"
        )
    elif text == "＋  Add Coins" and uid == ADMIN_ID:
        await msg.answer(
            "◈  <b>Add Coins</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "<code>/addcoins USER_ID AMOUNT</code>\n\n"
            "Example:\n<code>/addcoins 939285095 100</code>",
            parse_mode="HTML"
        )
    elif text == "📤  Deliver" and uid == ADMIN_ID:
        await msg.answer(
            "◈  <b>Deliver File</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "<code>/deliver USER_ID ORDER_ID</code>\n\n"
            "Example:\n<code>/deliver 939285095 8</code>\n\nThen attach the file.",
            parse_mode="HTML"
        )
    elif text == "✕  Cancel Order" and uid == ADMIN_ID:
        await msg.answer(
            "◈  <b>Cancel Order</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "<code>/cancelorder ORDER_ID</code>\n\n"
            "Example:\n<code>/cancelorder 8</code>",
            parse_mode="HTML"
        )
    elif text == "◈  Users" and uid == ADMIN_ID:
        from database import get_all_users
        users = get_all_users()
        if not users:
            await msg.answer("No users yet.")
            return
        text_out = f"◈  <b>All Users ({len(users)})</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for u in users[:30]:
            import time
            date = time.strftime("%b %d", time.localtime(int(u["joined"]))) if u["joined"] else "—"
            orders = u["order_count"] or 0
            coins = u["coins"] or 0
            uid_str = u["uid"]
            text_out += f"  <code>{uid_str}</code>  ·  {coins}◈  ·  {orders} orders  ·  {date}\n"
        text_out += "\n  <i>Use /msg USER_ID to contact any user</i>"
        await msg.answer(text_out, parse_mode="HTML")

    elif text in ("◌  Admin Help", "◌  Commands") and uid == ADMIN_ID:
        await msg.answer(
            "◈  <b>Admin Panel</b>\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            "<b>Panel Buttons:</b>\n"
            "  ≡  All Orders — last 15 orders\n"
            "  ◈  Users — all users list\n"
            "  ✉  Msg User — send message to user\n"
            "  ＋  Add Coins — add coins to user\n"
            "  📤  Deliver — deliver file to user\n"
            "  ✕  Cancel Order — cancel & refund\n\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            "<b>Commands:</b>\n"
            "  /msg <code>USER_ID TEXT</code>\n"
            "  → Send message to user from bot\n\n"
            "  /addcoins <code>USER_ID AMOUNT</code>\n"
            "  → Add coins to user wallet\n\n"
            "  /deliver <code>USER_ID ORDER_ID</code>\n"
            "  → Attach file to deliver to user\n\n"
            "  /cancelorder <code>ORDER_ID</code>\n"
            "  → Cancel order and refund coins\n\n"
            "  /balance\n"
            "  → Check your coin balance\n\n"
            "  /cancel\n"
            "  → Reset your FSM state\n\n"
            "  /addaccount <code>EMAIL PASSWORD [label]</code>\n"
            "  → Add an Artlist account to the pool\n\n"
            "  /accounts\n"
            "  → List Artlist account pool status\n\n"
            "  /accstatus <code>ID active|exhausted|banned|disabled</code>\n"
            "  → Change an account's status\n\n"
            "  /delaccount <code>ID</code>\n"
            "  → Remove an account from the pool\n\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            parse_mode="HTML"
        )

# ── Main menu callback ────────────────────────────────────────
@dp.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    uid = cb.from_user.id
    coins = get_coins(uid)
    lang = get_lang(uid)
    await cb.message.edit_text(
        build_main_menu_text(coins, lang),
        reply_markup=build_main_menu_kb(coins, lang), parse_mode="HTML"
    )

# ── Language switch ───────────────────────────────────────────
@dp.callback_query(F.data == "lang_menu")
async def lang_menu_cb(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    await cb.message.edit_text(
        f"{t('lang_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('lang_desc', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=("✓  " if lang == "en" else "○  ") + "English",  callback_data="lang_set_en")],
            [InlineKeyboardButton(text=("✓  " if lang == "ru" else "○  ") + "Русский",  callback_data="lang_set_ru")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.in_({"lang_set_en", "lang_set_ru"}))
async def lang_set_cb(cb: CallbackQuery):
    uid = cb.from_user.id
    new_lang = "en" if cb.data == "lang_set_en" else "ru"
    set_lang(uid, new_lang)
    coins = get_coins(uid)
    await cb.message.edit_text(
        build_main_menu_text(coins, new_lang),
        reply_markup=build_main_menu_kb(coins, new_lang), parse_mode="HTML"
    )
    await cb.message.answer(t("lang_changed", new_lang), reply_markup=get_kb(uid, new_lang))
    await cb.answer()

# ── Audio placeholder ─────────────────────────────────────────
@dp.callback_query(F.data == "cat_audio")
async def audio_coming_soon(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('audio_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('audio_body', lang)}",
        reply_markup=kb([InlineKeyboardButton(text=t("btn_back", lang), callback_data="main_menu")]),
        parse_mode="HTML"
    )

# ── Pricing ───────────────────────────────────────────────────
@dp.callback_query(F.data == "pricing_menu")
async def pricing_menu(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('pricing_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('pricing_body', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_image_pricing", lang), callback_data="price_images")],
            [InlineKeyboardButton(text=t("btn_video_pricing", lang), callback_data="price_video")],
            [InlineKeyboardButton(text=t("btn_back", lang),          callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "price_images")
async def price_images(cb: CallbackQuery):
    from config import IMAGE_TOOLS
    lang = get_lang(cb.from_user.id)
    lines = f"{t('price_images_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
    for name, info in IMAGE_TOOLS.items():
        if "coins_by_quality" in info:
            coins_str = "  /  ".join(f"{q}: {c}◈" for q, c in info["coins_by_quality"].items())
        else:
            coins_str = f"{info.get('coins', 1)}◈"
        lines += f"  {info['emoji']}  <b>{name}</b>  —  {coins_str}\n"
    await cb.message.edit_text(
        lines,
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_video_pricing", lang), callback_data="price_video")],
            [InlineKeyboardButton(text=t("menu_main_menu", lang),    callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "price_video")
async def price_video(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('price_video_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('price_video_body', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(text=t("btn_image_pricing", lang), callback_data="price_images")],
            [InlineKeyboardButton(text=t("menu_main_menu", lang),    callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

# ── Admin commands ────────────────────────────────────────────
@dp.message(Command("msg"))
async def msg_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split(None, 2)
    if len(parts) < 3:
        await msg.answer("Usage: <code>/msg USER_ID Text</code>", parse_mode="HTML")
        return
    try:
        uid = int(parts[1])
        text = parts[2]
        await bot.send_message(
            uid,
            f"◈  <b>Message from RetainX Studio</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n{text}",
            parse_mode="HTML"
        )
        await msg.answer(f"✓  Message sent to user {uid}.")
    except Exception as e:
        await msg.answer(f"❌ Failed: {e}")

@dp.message(Command("addcoins"))
async def add_coins_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) != 3:
        await msg.answer("Usage: <code>/addcoins USER_ID AMOUNT</code>", parse_mode="HTML")
        return
    try:
        uid = int(parts[1])
        amount = int(parts[2])
        add_coins(uid, amount)
        new_balance = get_coins(uid)
        await msg.answer(f"✓  Added <b>{amount} coins</b> to user <code>{uid}</code>\nBalance: <b>{new_balance} coins</b>", parse_mode="HTML")
        try:
            await bot.send_message(uid, f"◈  <b>{amount} coins</b> added to your wallet.\nBalance: <b>{new_balance} coins</b>", parse_mode="HTML")
        except Exception:
            await msg.answer("⚠️  Coins credited, but user hasn't started the bot yet — notification not sent.")
    except Exception as e:
        await msg.answer(f"Error: {e}")

@dp.message(Command("deliver"))
async def deliver_cmd(msg: Message, state: FSMContext):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 2:
        await msg.answer("Usage: <code>/deliver USER_ID [ORDER_ID]</code>", parse_mode="HTML")
        return
    try:
        uid = int(parts[1])
        oid = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        await msg.answer("Invalid format.")
        return
    from handlers.admin import AdminStates
    await state.update_data(admin_oid=oid, admin_target_uid=uid)
    await state.set_state(AdminStates.sending_result)
    await msg.answer(f"📤  Attach file for user <code>{uid}</code>", parse_mode="HTML")

@dp.message(Command("cancelorder"))
async def cancelorder_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 2:
        await msg.answer("Usage: <code>/cancelorder ORDER_ID</code>", parse_mode="HTML")
        return
    try:
        oid = int(parts[1])
        from database import get_order, update_order_status
        order = get_order(oid)
        if not order:
            await msg.answer("Order not found.")
            return
        add_coins(order["user_id"], order["coins"])
        update_order_status(oid, "cancelled")
        await bot.send_message(order["user_id"], f"◌  <b>Order #{oid} Cancelled</b>\n\n  <b>{order['coins']} coins</b> refunded.", parse_mode="HTML")
        await msg.answer(f"✓  Order #{oid} cancelled. {order['coins']} coins refunded.")
    except Exception as e:
        await msg.answer(f"Error: {e}")

@dp.message(Command("cancel"))
async def cancel_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("◌  State cleared. Use the menu below to continue.")

# ── Artlist account pool admin commands ────────────────────────
@dp.message(Command("addaccount"))
async def add_account_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split(None, 3)
    if len(parts) < 3:
        await msg.answer(
            "Usage: <code>/addaccount EMAIL PASSWORD [label]</code>",
            parse_mode="HTML"
        )
        return
    email, password = parts[1], parts[2]
    label = parts[3] if len(parts) > 3 else None
    from database import add_artlist_account
    aid = add_artlist_account(email, password, label)
    await msg.answer(f"✓  Artlist account #{aid} added ({email}).")

@dp.message(Command("accounts"))
async def list_accounts_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    from database import list_artlist_accounts
    accounts = list_artlist_accounts()
    if not accounts:
        await msg.answer("No Artlist accounts in the pool yet. Use /addaccount to add one.")
        return
    status_emoji = {"active": "✓", "exhausted": "○", "banned": "✕", "disabled": "—"}
    lines = "◈  <b>Artlist Account Pool</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    for a in accounts:
        e = status_emoji.get(a["status"], "?")
        label = a["label"] or a["email"]
        worker = f"  · {a['assigned_worker']}" if a["assigned_worker"] else ""
        lines += f"  {e}  #{a['id']}  <b>{label}</b>  ({a['status']}){worker}\n"
    lines += "\n  /accstatus ID active|exhausted|banned|disabled\n  /delaccount ID"
    await msg.answer(lines, parse_mode="HTML")

@dp.message(Command("accstatus"))
async def account_status_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) != 3 or parts[2] not in ("active", "exhausted", "banned", "disabled"):
        await msg.answer(
            "Usage: <code>/accstatus ID active|exhausted|banned|disabled</code>",
            parse_mode="HTML"
        )
        return
    try:
        aid = int(parts[1])
    except ValueError:
        await msg.answer("Invalid account ID.")
        return
    from database import set_artlist_account_status
    set_artlist_account_status(aid, parts[2])
    await msg.answer(f"✓  Account #{aid} set to '{parts[2]}'.")

@dp.message(Command("delaccount"))
async def del_account_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) != 2:
        await msg.answer("Usage: <code>/delaccount ID</code>", parse_mode="HTML")
        return
    try:
        aid = int(parts[1])
    except ValueError:
        await msg.answer("Invalid account ID.")
        return
    from database import remove_artlist_account
    remove_artlist_account(aid)
    await msg.answer(f"✓  Account #{aid} removed.")

@dp.message(Command("balance"))
async def balance_cmd(msg: Message):
    coins = get_coins(msg.from_user.id)
    await msg.answer(f"◈  Your balance: <b>{coins} coins</b>", parse_mode="HTML")

@dp.message(F.text.regexp(r"^/send_\d+$"))
async def send_result_cmd(msg: Message, state: FSMContext):
    if msg.from_user.id != ADMIN_ID:
        return
    oid = int(msg.text.replace("/send_", ""))
    from database import get_order
    order = get_order(oid)
    if not order:
        await msg.answer("Order not found.")
        return
    from handlers.admin import AdminStates
    await state.update_data(admin_oid=oid)
    await state.set_state(AdminStates.sending_result)
    await msg.answer(f"📤  Attach file for Order #{oid}")

async def main():
    print("RetainX Studio — started ◈")
    await bot.delete_webhook(drop_pending_updates=True)

    from handlers.yoomoney import yoomoney_webhook
    app = web.Application()
    app.router.add_post("/yoomoney/webhook", yoomoney_webhook)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"YooMoney webhook server on :{port}")

    import os as _os
    from worker_monitor import stale_order_monitor
    _redis_url = _os.environ.get("REDIS_URL", "")
    if _redis_url:
        asyncio.create_task(stale_order_monitor(bot, _redis_url))

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
