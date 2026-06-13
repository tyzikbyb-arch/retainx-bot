import math
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import COIN_TO_USD, MIN_TOPUP_USD, USDT_WALLET, REFERRAL_PERCENT, BOT_TOKEN
from database import get_coins, add_coins, get_referred_by
from keyboards import kb, back_btn, menu_btn

router = Router()

TRON_API = "https://apilist.tronscanapi.com/api/transaction-info"

class TopupStates(StatesGroup):
    entering_amount = State()
    entering_tx = State()

# ── Wallet ────────────────────────────────────────────────────
async def show_wallet(target, state: FSMContext = None):
    if state:
        await state.clear()
    uid = target.from_user.id if isinstance(target, (Message, CallbackQuery)) else target
    coins = get_coins(uid)
    usd_val = round(coins * COIN_TO_USD, 2)
    text = (
        "◈  <b>Your Wallet</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Balance     <b>{coins} coins</b>  (≈ ${usd_val})\n\n"
        "  Rate          1 coin  =  $0.05\n"
        "  Min top-up   $2.00  =  40 coins\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = kb(
        [InlineKeyboardButton(text="＋  Add Coins", callback_data="topup_start")],
        [InlineKeyboardButton(text="◈  Referral Program", callback_data="referral_info")],
        [menu_btn()],
    )
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data == "wallet")
async def wallet_cb(cb: CallbackQuery, state: FSMContext):
    await show_wallet(cb, state)

# ── Top-up start ──────────────────────────────────────────────
@router.callback_query(F.data == "topup_start")
async def topup_start(cb: CallbackQuery, state: FSMContext):
    text = (
        "＋  <b>Add Coins</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  1 coin  =  <b>$0.05</b>\n"
        "  $2.00   =  <b>40 coins</b>  ← minimum\n"
        "  $5.00   =  <b>100 coins</b>\n"
        "  $10.00  =  <b>200 coins</b>\n\n"
        "Select amount or enter custom:"
    )
    keyboard = kb(
        [InlineKeyboardButton(text="$2  →  40 coins",   callback_data="topup_amount_2"),
         InlineKeyboardButton(text="$5  →  100 coins",  callback_data="topup_amount_5")],
        [InlineKeyboardButton(text="$10  →  200 coins", callback_data="topup_amount_10"),
         InlineKeyboardButton(text="$20  →  400 coins", callback_data="topup_amount_20")],
        [InlineKeyboardButton(text="✎  Custom amount", callback_data="topup_custom")],
        [back_btn("wallet"), menu_btn()],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("topup_amount_"))
async def topup_preset(cb: CallbackQuery, state: FSMContext):
    amount = float(cb.data.replace("topup_amount_", ""))
    await show_payment_options(cb, state, amount)

@router.callback_query(F.data == "topup_custom")
async def topup_custom(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text(
        "✎  <b>Custom Amount</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Type the amount in USD (minimum $2.00):\n\n"
        "<i>Example: 7.5</i>",
        reply_markup=kb([back_btn("topup_start"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_amount)

@router.message(TopupStates.entering_amount)
async def receive_custom_amount(msg: Message, state: FSMContext):
    text = msg.text.strip()
    try:
        amount = float(text.replace(",", ".").replace("$", "").strip())
        if amount < MIN_TOPUP_USD:
            await msg.answer(f"Minimum deposit is ${MIN_TOPUP_USD}. Please enter a valid amount (e.g. 2, 5, 10).")
            return
        await state.clear()
        await show_payment_options_msg(msg, state, amount)
    except ValueError:
        await msg.answer("Please enter a number (e.g. 5 or 7.50).\n\nType /cancel to exit.")

async def show_payment_options(cb: CallbackQuery, state: FSMContext, amount: float):
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    text = (
        f"◈  <b>Confirm Top-up</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Amount      <b>${amount:.2f}</b>\n"
        f"  You receive  <b>{coins} coins</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Choose payment method:"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=f"⭐  Pay with Stars ({stars_amount} XTR)", callback_data=f"pay_stars_{amount}")],
        [InlineKeyboardButton(text="₮  Pay with USDT (TRC20)", callback_data=f"pay_usdt_{amount}")],
        [back_btn("topup_start"), menu_btn()],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=amount)

async def show_payment_options_msg(msg: Message, state: FSMContext, amount: float):
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    text = (
        f"◈  <b>Confirm Top-up</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Amount      <b>${amount:.2f}</b>\n"
        f"  You receive  <b>{coins} coins</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Choose payment method:"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=f"⭐  Pay with Stars ({stars_amount} XTR)", callback_data=f"pay_stars_{amount}")],
        [InlineKeyboardButton(text="₮  Pay with USDT (TRC20)", callback_data=f"pay_usdt_{amount}")],
        [back_btn("topup_start"), menu_btn()],
    )
    await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=amount)

# ── USDT payment ──────────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_usdt_"))
async def pay_usdt(cb: CallbackQuery, state: FSMContext):
    amount = float(cb.data.replace("pay_usdt_", ""))
    coins = math.floor(amount / COIN_TO_USD)
    await state.update_data(topup_amount=amount, topup_coins=coins)
    text = (
        f"₮  <b>USDT Payment</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Send exactly  <b>${amount:.2f} USDT</b>\n"
        f"  Network          <b>TRC20 (Tron)</b>\n\n"
        f"  Wallet address:\n"
        f"<code>{USDT_WALLET}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"After sending, paste your <b>transaction hash</b> below.\n"
        f"<i>The system will verify it automatically.</i>"
    )
    await cb.message.edit_text(
        text,
        reply_markup=kb([back_btn("topup_start"), menu_btn()]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_tx)

# ── Auto-verify TX hash ───────────────────────────────────────
@router.message(TopupStates.entering_tx)
async def receive_tx_hash(msg: Message, state: FSMContext):
    tx_hash = msg.text.strip()
    data = await state.get_data()
    amount = float(data.get("topup_amount", 0))
    coins = int(data.get("topup_coins", math.floor(amount / COIN_TO_USD)))
    uid = msg.from_user.id

    await msg.answer("⏳  Verifying transaction...")

    try:
        verified, actual_amount = await verify_tron_tx(tx_hash, amount)

        if verified:
            # Auto-credit coins
            add_coins(uid, coins)
            await _handle_referral_bonus(uid, coins)
            await msg.answer(
                f"✓  <b>Payment Verified</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"  Transaction confirmed\n"
                f"  Amount received   <b>${actual_amount:.2f} USDT</b>\n"
                f"  Coins credited     <b>{coins} coins</b>\n"
                f"  New balance        <b>{get_coins(uid)} coins</b>",
                reply_markup=kb([menu_btn()]),
                parse_mode="HTML"
            )
            await state.clear()
        else:
            # Manual review fallback
            await _send_for_manual_review(msg, tx_hash, amount, coins, uid)
            await state.clear()

    except Exception as e:
        # Network error — send for manual review
        await _send_for_manual_review(msg, tx_hash, amount, coins, uid)
        await state.clear()

async def verify_tron_tx(tx_hash: str, expected_amount: float) -> tuple[bool, float]:
    """Verify USDT TRC20 transaction on TronScan."""
    url = f"{TRON_API}?hash={tx_hash}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()

    # Check transaction exists and is confirmed
    if not data or data.get("contractRet") != "SUCCESS":
        return False, 0

    # Check it's a TRC20 USDT transfer
    trc20_transfers = data.get("trc20TransferInfo", [])
    for transfer in trc20_transfers:
        # USDT TRC20 contract address
        if transfer.get("contract_address") == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
            to_address = transfer.get("to_address", "")
            amount_raw = int(transfer.get("amount_str", "0"))
            actual_usd = amount_raw / 1_000_000  # USDT has 6 decimals

            # Check destination is our wallet
            if to_address == USDT_WALLET:
                # Allow 1% tolerance
                if actual_usd >= expected_amount * 0.99:
                    return True, actual_usd

    return False, 0

async def _send_for_manual_review(msg: Message, tx_hash: str, amount: float, coins: int, uid: int):
    """Fallback to manual review if auto-verify fails."""
    from config import ADMIN_ID
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Confirm", callback_data=f"confirm_topup_{uid}_{coins}"),
        InlineKeyboardButton(text="✕  Reject",  callback_data=f"reject_topup_{uid}"),
    ]])
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>Manual Review Required</b>\n\n"
        f"  User    @{msg.from_user.username or '—'} (<code>{uid}</code>)\n"
        f"  Amount  <b>${amount:.2f}</b>  →  <b>{coins} coins</b>\n\n"
        f"  TX Hash:\n<code>{tx_hash}</code>\n\n"
        f"  <i>Auto-verify could not confirm. Please check manually.</i>",
        reply_markup=keyboard, parse_mode="HTML"
    )
    await msg.answer(
        "◌  <b>Under Review</b>\n\n"
        "  We could not verify your transaction automatically.\n"
        "  Our team will review it manually within 15 minutes.\n\n"
        "  Coins will be credited after confirmation.",
        reply_markup=kb([menu_btn()]),
        parse_mode="HTML"
    )

# ── Stars payment ─────────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_stars_"))
async def pay_stars(cb: CallbackQuery, state: FSMContext):
    from aiogram import Bot
    amount = float(cb.data.replace("pay_stars_", ""))
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    bot = Bot(token=BOT_TOKEN)
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title="RetainX Studio — Coins",
        description=f"Top up {coins} coins to your RetainX account",
        payload=f"topup_{coins}_{cb.from_user.id}",
        currency="XTR",
        prices=[LabeledPrice(label=f"{coins} Coins", amount=stars_amount)],
        provider_token="",
    )
    await cb.answer()

@router.message(F.successful_payment)
async def successful_stars_payment(msg: Message):
    payload = msg.successful_payment.invoice_payload
    parts = payload.split("_")
    coins = int(parts[1])
    uid = msg.from_user.id
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
    await msg.answer(
        f"⭐  <b>Payment Successful</b>\n\n"
        f"  {coins} coins added to your wallet.\n"
        f"  New balance: <b>{get_coins(uid)} coins</b>",
        parse_mode="HTML"
    )

# ── Admin confirm/reject ──────────────────────────────────────
@router.callback_query(F.data.startswith("confirm_topup_"))
async def admin_confirm_topup(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    _, _, uid_str, coins_str = cb.data.split("_", 3)
    uid = int(uid_str)
    coins = int(coins_str)
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        uid,
        f"✓  <b>Top-up Confirmed</b>\n\n"
        f"  <b>{coins} coins</b> added to your wallet.\n"
        f"  Balance: <b>{get_coins(uid)} coins</b>",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✓  Confirmed — {coins} coins → user {uid}", parse_mode="HTML")

@router.callback_query(F.data.startswith("reject_topup_"))
async def admin_reject_topup(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    uid = int(cb.data.split("_")[-1])
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(uid, "✕  Your top-up was not confirmed. Please contact support.")
    await cb.message.edit_text(f"✕  Rejected — user {uid}")

async def _handle_referral_bonus(uid: int, coins_added: int):
    ref_uid = get_referred_by(uid)
    if ref_uid:
        bonus = round(coins_added * REFERRAL_PERCENT / 100)
        if bonus > 0:
            add_coins(ref_uid, bonus)
            from aiogram import Bot
            bot = Bot(token=BOT_TOKEN)
            await bot.send_message(
                ref_uid,
                f"◈  <b>Referral Bonus</b>\n\n"
                f"  Your referral topped up their wallet.\n"
                f"  You received <b>{bonus} coins</b> (20%).",
                parse_mode="HTML"
            )

# ── Referral info ─────────────────────────────────────────────
@router.callback_query(F.data == "referral_info")
async def referral_info(cb: CallbackQuery):
    bot_username = "RetainXStudio"
    link = f"https://t.me/{bot_username}?start=ref_{cb.from_user.id}"
    text = (
        "◈  <b>Referral Program</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Earn <b>20% in coins</b> every time your referral tops up.\n\n"
        "  Your referral link:\n"
        f"<code>{link}</code>\n\n"
        "  Share it and earn passively."
    )
    await cb.message.edit_text(
        text,
        reply_markup=kb([back_btn("wallet"), menu_btn()]),
        parse_mode="HTML"
    )
