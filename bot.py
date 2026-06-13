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
from database import is_new_user, add_coins, get_coins, set_referred_by, get_user_orders
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

# ── Persistent bottom keyboard ────────────────────────────────
MAIN_REPLY_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⌂  Main Menu"), KeyboardButton(text="◈  Wallet")],
        [KeyboardButton(text="▸  Video"),      KeyboardButton(text="▸  Images"),   KeyboardButton(text="▸  Audio")],
        [KeyboardButton(text="≡  Orders"),      KeyboardButton(text="◌  Support")],
    ],
    resize_keyboard=True,
    persistent=True,
)

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

    await show_main_menu(msg, new)

async def show_main_menu(target, new_user: bool = False):
    uid = target.from_user.id
    coins = get_coins(uid)
    bonus_line = f"\n  Welcome bonus  <b>+{WELCOME_BONUS} coins</b> credited.\n" if new_user else ""
    bonus_text = f"\n  + {WELCOME_BONUS} coins credited\n" if new_user else ""
    text = (
        "<b>RetainX Studio</b>\n"
        "─────────────────────\n"
        f"{bonus_text}"
        f"  Balance  ·  <b>{coins} coins</b>\n\n"
        "  AI-powered generation\n"
        "  Video  ·  Images  ·  Audio"
    )
    keyboard = kb(
        [InlineKeyboardButton(text="Video Generation", callback_data="cat_video")],
        [InlineKeyboardButton(text="Image Generation", callback_data="cat_images")],
        [InlineKeyboardButton(text="Audio & Voice",    callback_data="cat_audio")],
        [InlineKeyboardButton(text=f"Wallet  ·  {coins} coins", callback_data="wallet")],
        [InlineKeyboardButton(text="Pricing",  callback_data="pricing_menu"),
         InlineKeyboardButton(text="◌  Support",  url="https://t.me/RetainXStudio")],
    )
    await target.answer(text, reply_markup=MAIN_REPLY_KB, parse_mode="HTML")
    await target.answer("Select a service:", reply_markup=keyboard, parse_mode="HTML")

# ── Reply keyboard handlers ───────────────────────────────────
@dp.message(F.text.in_({"⌂  Main Menu", "Main Menu"}))
async def reply_main_menu(msg: Message, state: FSMContext):
    await state.clear()
    uid = msg.from_user.id
    coins = get_coins(uid)
    keyboard = kb(
        [InlineKeyboardButton(text="Video Generation", callback_data="cat_video")],
        [InlineKeyboardButton(text="Image Generation", callback_data="cat_images")],
        [InlineKeyboardButton(text="Audio & Voice",    callback_data="cat_audio")],
        [InlineKeyboardButton(text=f"Wallet  ·  {coins} coins", callback_data="wallet")],
        [InlineKeyboardButton(text="Pricing", callback_data="pricing_menu"),
         InlineKeyboardButton(text="◌  Support", url="https://t.me/RetainXStudio")],
    )
    await msg.answer(
        f"<b>RetainX Studio</b>\n"
        f"─────────────────────\n"
        f"  Balance  ·  <b>{coins} coins</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(F.text.in_({"◈  Wallet", "Wallet"}))
async def reply_wallet(msg: Message, state: FSMContext):
    from handlers.credits import show_wallet
    await show_wallet(msg, state)

@dp.message(F.text.in_({"▸  Video", "Video"}))
async def reply_video(msg: Message, state: FSMContext):
    buttons = [
        [InlineKeyboardButton(text="▸  Standard Video", callback_data="vsub_Standard")],
        [InlineKeyboardButton(text="▸  Premium Video",  callback_data="vsub_Premium")],
        [InlineKeyboardButton(text="▸  Kling Video",    callback_data="vsub_Kling")],
        [InlineKeyboardButton(text="▸  Avatar & Dubbing", callback_data="vsub_Avatar")],
        [InlineKeyboardButton(text="⌂  Main Menu",      callback_data="main_menu")],
    ]
    await msg.answer(
        "◈  <b>Video Generation</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a category:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

@dp.message(F.text.in_({"▸  Images", "Images"}))
async def reply_images(msg: Message, state: FSMContext):
    from config import IMAGE_TOOLS
    buttons = [[InlineKeyboardButton(text=f"{info['emoji']}  {name}", callback_data=f"img_{name}")] for name, info in IMAGE_TOOLS.items()]
    buttons.append([InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")])
    await msg.answer(
        "◈  <b>Image Generation</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select a model:",
        reply_markup=kb(*buttons),
        parse_mode="HTML"
    )

# ── Main menu callback ────────────────────────────────────────
@dp.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    uid = cb.from_user.id
    coins = get_coins(uid)
    keyboard = kb(
        [InlineKeyboardButton(text="Video Generation", callback_data="cat_video")],
        [InlineKeyboardButton(text="Image Generation", callback_data="cat_images")],
        [InlineKeyboardButton(text="Audio & Voice",    callback_data="cat_audio")],
        [InlineKeyboardButton(text=f"Wallet  ·  {coins} coins", callback_data="wallet")],
        [InlineKeyboardButton(text="Pricing", callback_data="pricing_menu"),
         InlineKeyboardButton(text="◌  Support", url="https://t.me/RetainXStudio")],
    )
    await cb.message.edit_text(
        f"<b>RetainX Studio</b>\n"
        f"─────────────────────\n"
        f"  Balance  ·  <b>{coins} coins</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# ── Audio placeholder ─────────────────────────────────────────
@dp.callback_query(F.data == "cat_audio")
async def audio_coming_soon(cb: CallbackQuery):
    await cb.message.edit_text(
        "◌  <b>Audio & Voice</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
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
        "◎  <b>Pricing</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
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
        "◎  <b>Video Pricing</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Prices vary by model, resolution & duration.\n"
        "  Select a model in Video Generation\n"
        "  to see exact coin costs per option.\n\n"
        "  <b>Sample rates:</b>\n"
        "  Kling 3.0   720p  5s  —  6◈\n"
        "  Veo 3.1     4K    8s  —  58◈\n"
        "  Seedance   1080p 10s  —  60◈\n"
        "  Wan 2.7     720p  5s  —  10◈\n",
        reply_markup=kb(
            [InlineKeyboardButton(text="▸  Image Pricing", callback_data="price_images")],
            [InlineKeyboardButton(text="⌂  Main Menu",     callback_data="main_menu")],
        ),
        parse_mode="HTML"
    )

# ── Admin send result ─────────────────────────────────────────
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
    await state.update_data(admin_oid=oid)
    from handlers.admin import AdminStates
    await state.set_state(AdminStates.sending_result)
    await msg.answer(f"▸  Attach the file for Order #{oid}")

@dp.message(Command("deliver"))
async def deliver_cmd(msg: Message, state: FSMContext):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) < 2:
        await msg.answer(
            "Usage: <code>/deliver USER_ID [ORDER_ID]</code>\n"
            "Example: <code>/deliver 939285095 1</code>\n\n"
            "Then attach the file.",
            parse_mode="HTML"
        )
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
    await msg.answer(
        f"📤  Ready to deliver to user <code>{uid}</code>\n"
        f"Attach the file now:",
        parse_mode="HTML"
    )

@dp.message(Command("addcoins"))
async def add_coins_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    # Usage: /addcoins USER_ID AMOUNT
    parts = msg.text.strip().split()
    if len(parts) != 3:
        await msg.answer(
            "Usage: <code>/addcoins USER_ID AMOUNT</code>\n"
            "Example: <code>/addcoins 939285095 100</code>",
            parse_mode="HTML"
        )
        return
    try:
        uid = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await msg.answer("Invalid format. Use: /addcoins USER_ID AMOUNT")
        return
    add_coins(uid, amount)
    new_balance = get_coins(uid)
    # Notify admin
    await msg.answer(
        f"✓  Added <b>{amount} coins</b> to user <code>{uid}</code>\n"
        f"New balance: <b>{new_balance} coins</b>",
        parse_mode="HTML"
    )
    # Notify user
    try:
        await bot.send_message(
            uid,
            f"◈  <b>Coins Added</b>\n\n"
            f"  <b>{amount} coins</b> have been added to your wallet.\n"
            f"  New balance: <b>{new_balance} coins</b>",
            parse_mode="HTML"
        )
    except Exception:
        await msg.answer("! Could not notify user (they may have blocked the bot).")

@dp.message(Command("cancel"))
async def cancel_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "◌  State cleared. Use the menu below to continue.",
        reply_markup=MAIN_REPLY_KB
    )

@dp.message(Command("balance"))
async def balance_cmd(msg: Message):
    coins = get_coins(msg.from_user.id)
    await msg.answer(f"◈  Your balance: <b>{coins} coins</b>", parse_mode="HTML")

async def main():
    print("RetainX Studio — started ◈")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

@dp.message(F.text.in_({"◌  Support", "Support"}))
async def reply_support(msg: Message):
    await msg.answer(
        "◌  <b>Support</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  For any questions or issues,\n"
        "  contact us directly:\n\n"
        "  @RetainXStudio",
        parse_mode="HTML"
    )

@dp.message(F.text.in_({"▸  Audio", "Audio"}))
async def reply_audio(msg: Message):
    await msg.answer(
        "◌  <b>Audio & Voice</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Coming soon.\n\n"
        "  We are integrating voice synthesis\n"
        "  and music generation tools.\n\n"
        "  Stay tuned.",
        reply_markup=kb([InlineKeyboardButton(text="⌂  Main Menu", callback_data="main_menu")]),
        parse_mode="HTML"
    )
