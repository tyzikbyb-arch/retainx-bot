import asyncio, logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.fsm.storage.memory import MemoryStorage
try:
    from aiogram.fsm.storage.redis import RedisStorage
    import os
    REDIS_URL = os.environ.get("REDIS_URL", "")
    if REDIS_URL:
        storage = RedisStorage.from_url(REDIS_URL)
        print("Using Redis storage")
    else:
        storage = MemoryStorage()
        print("Using Memory storage")
except Exception:
    storage = MemoryStorage()
    print("Redis unavailable, using Memory storage")

from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMIN_ID, WELCOME_BONUS
from database import is_new_user, add_coins, get_coins, set_referred_by
from keyboards import kb, menu_btn
from handlers import credits, images, video, admin as admin_handler, orders as orders_handler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(credits.router)
dp.include_router(images.router)
dp.include_router(video.router)
dp.include_router(admin_handler.router)
dp.include_router(orders_handler.router)

# ── Keyboards ─────────────────────────────────────────────────
CLIENT_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⌂  Main Menu"), KeyboardButton(text="◈  Wallet")],
        [KeyboardButton(text="▸  Video"),      KeyboardButton(text="▸  Images"),   KeyboardButton(text="▸  Audio")],
        [KeyboardButton(text="≡  Orders"),     KeyboardButton(text="◌  Support")],
    ],
    resize_keyboard=True,
    persistent=True,
)

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

def get_kb(uid: int):
    return ADMIN_KB if uid == ADMIN_ID else CLIENT_KB

# ── /start ────────────────────────────────────────────────────
@dp.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    uid = msg.from_user.id
    args = msg.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            ref_id = int(args[1].replace("ref_", ""))
            if ref_id != uid:
                set_referred_by(uid, ref_id)
        except ValueError:
            pass

    new = is_new_user(uid)
    if new:
        add_coins(uid, WELCOME_BONUS)

    coins = get_coins(uid)

    if new:
        # New user welcome
        welcome_text = (
            "◈  <b>Welcome to RetainX Studio</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  The fastest and most affordable way\n"
            "  to generate AI video, images & audio.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  Up to <b>3× cheaper</b> than any competitor.\n"
            "  Results delivered in <b>~2 minutes.</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"  🎁  <b>{WELCOME_BONUS} free coins</b> added to your account.\n"
            f"  Balance   <b>{coins} coins</b>"
        )
        keyboard = kb(
            [InlineKeyboardButton(text="▸  Start Generating", callback_data="cat_video")],
            [InlineKeyboardButton(text="◎  View Pricing",     callback_data="pricing_menu")],
            [InlineKeyboardButton(text="◌  Support",          url="https://t.me/RetainXStudio")],
        )
        await msg.answer(welcome_text, reply_markup=get_kb(uid), parse_mode="HTML")
        await msg.answer("What would you like to create?", reply_markup=keyboard, parse_mode="HTML")
    else:
        # Returning user
        text = (
            "◈  <b>RetainX Studio</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  Balance   <b>{coins} coins</b>\n\n"
            "  Generate AI video, images & audio\n"
            "  at the most competitive rates.\n\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        keyboard = kb(
            [InlineKeyboardButton(text="▸  Video Generation", callback_data="cat_video")],
            [InlineKeyboardButton(text="▸  Image Generation", callback_data="cat_images")],
            [InlineKeyboardButton(text="▸  Audio & Voice",    callback_data="cat_audio")],
            [InlineKeyboardButton(text="◈  Wallet  ·  " + str(coins) + " coins", callback_data="wallet")],
            [InlineKeyboardButton(text="◎  Pricing",          callback_data="pricing_menu")],
            [InlineKeyboardButton(text="◌  Support",          url="https://t.me/RetainXStudio")],
        )
        await msg.answer(text, reply_markup=get_kb(uid), parse_mode="HTML")
        await msg.answer("Choose an option:", reply_markup=keyboard, parse_mode="HTML")

# ── Panel button router ───────────────────────────────────────
PANEL_BUTTONS = {
    "⌂  Main Menu", "◈  Wallet", "▸  Video", "▸  Images",
    "▸  Audio", "≡  Orders", "◌  Support",
    "≡  All Orders", "✉  Msg User", "＋  Add Coins",
    "📤  Deliver", "✕  Cancel Order", "◌  Admin Help", "◈  Users", "◌  Commands",
}

@dp.message(F.text.in_(PANEL_BUTTONS))
async def panel_router(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    text = msg.text

    # Client buttons
    if text == "⌂  Main Menu":
        await state.clear()
        coins = get_coins(uid)
        keyboard = kb(
            [InlineKeyboardButton(text="▸  Video Generation", callback_data="cat_video")],
            [InlineKeyboardButton(text="▸  Image Generation", callback_data="cat_images")],
            [InlineKeyboardButton(text="▸  Audio & Voice",    callback_data="cat_audio")],
            [InlineKeyboardButton(text="◈  Wallet  ·  " + str(coins) + " coins", callback_data="wallet")],
            [InlineKeyboardButton(text="◎  Pricing",          callback_data="pricing_menu")],
            [InlineKeyboardButton(text="◌  Support",          url="https://t.me/RetainXStudio")],
        )
        await msg.answer(
            f"◈  <b>RetainX Studio</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  Balance   <b>{coins} coins</b>\n\n"
            "  Generate AI video, images & audio\n"
            "  at the most competitive rates.",
            reply_markup=keyboard, parse_mode="HTML"
        )
    elif text == "◈  Wallet":
        from handlers.credits import show_wallet
        await show_wallet(msg, state)
    elif text == "▸  Video":
        await state.clear()
        buttons = [
            [InlineKeyboardButton(text="▸  Standard Video",   callback_data="vsub_Standard")],
            [InlineKeyboardButton(text="▸  Premium Video",    callback_data="vsub_Premium")],
            [InlineKeyboardButton(text="▸  Kling Video",      callback_data="vsub_Kling")],
            [InlineKeyboardButton(text="▸  Avatar & Dubbing", callback_data="vsub_Avatar")],
            [InlineKeyboardButton(text="⌂  Main Menu",        callback_data="main_menu")],
        ]
        await msg.answer(
            "◈  <b>Video Generation</b>\n━━━━━━━━━━━━━━━━━━━━\n\nSelect a category:",
            reply_markup=kb(*buttons), parse_mode="HTML"
        )
    elif text == "▸  Images":
        await state.clear()
        from config import IMAGE_TOOLS
        buttons = [[InlineKeyboardButton(text=f"{info['emoji']}  {name}", callback_data=f"img_{name}")] for name, info in IMAGE_TOOLS.items()]
        buttons.append([InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")])
        await msg.answer(
            "◈  <b>Image Generation</b>\n━━━━━━━━━━━━━━━━━━━━\n\nSelect a model:",
            reply_markup=kb(*buttons), parse_mode="HTML"
        )
    elif text == "▸  Audio":
        await msg.answer(
            "◌  <b>Audio & Voice</b>\n━━━━━━━━━━━━━━━━━━━━\n\n  Coming soon.\n\n  Stay tuned.",
            reply_markup=kb([InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")]),
            parse_mode="HTML"
        )
    elif text == "≡  Orders":
        from handlers.orders import show_orders
        await show_orders(msg, uid)
    elif text == "◌  Support":
        await msg.answer(
            "◌  <b>Support</b>\n━━━━━━━━━━━━━━━━━━━━\n\n  Contact us: @RetainXStudio",
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
    keyboard = kb(
        [InlineKeyboardButton(text="▸  Video Generation", callback_data="cat_video")],
        [InlineKeyboardButton(text="▸  Image Generation", callback_data="cat_images")],
        [InlineKeyboardButton(text="▸  Audio & Voice",    callback_data="cat_audio")],
        [InlineKeyboardButton(text="◈  Wallet  ·  " + str(coins) + " coins", callback_data="wallet")],
        [InlineKeyboardButton(text="◎  Pricing",          callback_data="pricing_menu")],
        [InlineKeyboardButton(text="◌  Support",          url="https://t.me/RetainXStudio")],
    )
    await cb.message.edit_text(
        f"◈  <b>RetainX Studio</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Balance   <b>{coins} coins</b>\n\n"
        "  Generate AI video, images & audio\n"
        "  at the most competitive rates.\n\n"
        "━━━━━━━━━━━━━━━━━━━━",
        reply_markup=keyboard, parse_mode="HTML"
    )

# ── Audio placeholder ─────────────────────────────────────────
@dp.callback_query(F.data == "cat_audio")
async def audio_coming_soon(cb: CallbackQuery):
    await cb.message.edit_text(
        "◌  <b>Audio & Voice</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Coming soon.\n\n"
        "  We are integrating voice synthesis\n"
        "  and music generation tools.\n\n"
        "  Stay tuned.",
        reply_markup=kb([InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")]),
        parse_mode="HTML"
    )

# ── Pricing ───────────────────────────────────────────────────
@dp.callback_query(F.data == "pricing_menu")
async def pricing_menu(cb: CallbackQuery):
    await cb.message.edit_text(
        "◎  <b>Pricing</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  1 coin  =  <b>$0.05</b>\n\n"
        "  Select a category to view rates:",
        reply_markup=kb(
            [InlineKeyboardButton(text="▸  Image Pricing", callback_data="price_images")],
            [InlineKeyboardButton(text="▸  Video Pricing", callback_data="price_video")],
            [InlineKeyboardButton(text="⌂  Main Menu",     callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "price_images")
async def price_images(cb: CallbackQuery):
    from config import IMAGE_TOOLS
    lines = "◎  <b>Image Pricing</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    for name, info in IMAGE_TOOLS.items():
        if "coins_by_quality" in info:
            coins_str = "  /  ".join(f"{q}: {c}◈" for q, c in info["coins_by_quality"].items())
        else:
            coins_str = f"{info.get('coins', 1)}◈"
        lines += f"  {info['emoji']}  <b>{name}</b>  —  {coins_str}\n"
    await cb.message.edit_text(
        lines,
        reply_markup=kb(
            [InlineKeyboardButton(text="▸  Video Pricing", callback_data="price_video")],
            [InlineKeyboardButton(text="⌂  Main Menu",     callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "price_video")
async def price_video(cb: CallbackQuery):
    await cb.message.edit_text(
        "◎  <b>Video Pricing</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Prices vary by model, resolution & duration.\n"
        "  Select a model in Video Generation\n"
        "  to see exact coin costs per option.\n\n"
        "  <b>Sample rates:</b>\n"
        "  Kling 3.0   720p  5s  —  6◈\n"
        "  Veo 3.1     4K    8s  —  58◈\n"
        "  Seedance   1080p 10s  —  60◈\n",
        reply_markup=kb(
            [InlineKeyboardButton(text="▸  Image Pricing", callback_data="price_images")],
            [InlineKeyboardButton(text="⌂  Main Menu",     callback_data="main_menu")],
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
        await bot.send_message(uid, f"◈  <b>{amount} coins</b> added to your wallet.\nBalance: <b>{new_balance} coins</b>", parse_mode="HTML")
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
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
