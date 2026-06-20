import math
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import COIN_TO_USD, MIN_TOPUP_USD, USDT_WALLET, REFERRAL_PERCENT, BOT_TOKEN
from database import get_coins, add_coins, get_referred_by, get_lang
from keyboards import kb, back_btn, menu_btn
from i18n import t

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
    lang = get_lang(uid)
    coins = get_coins(uid)
    usd_val = round(coins * COIN_TO_USD, 2)
    text = (
        f"{t('wallet_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_balance', lang, coins=coins, usd=usd_val)}\n\n"
        f"{t('wallet_rate', lang)}\n"
        f"{t('wallet_min_topup', lang)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_add_coins", lang), callback_data="topup_start")],
        [InlineKeyboardButton(text=t("wallet_btn_referral", lang), callback_data="referral_info")],
        [menu_btn(lang)],
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
    lang = get_lang(cb.from_user.id)
    text = (
        f"{t('wallet_topup_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_topup_rate_line', lang)}\n"
        f"{t('wallet_topup_min_line', lang)}\n"
        f"{t('wallet_topup_5_line', lang)}\n"
        f"{t('wallet_topup_10_line', lang)}\n\n"
        f"{t('wallet_topup_select_or_custom', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_2", lang),  callback_data="topup_amount_2"),
         InlineKeyboardButton(text=t("wallet_btn_5", lang),  callback_data="topup_amount_5")],
        [InlineKeyboardButton(text=t("wallet_btn_10", lang), callback_data="topup_amount_10"),
         InlineKeyboardButton(text=t("wallet_btn_20", lang), callback_data="topup_amount_20")],
        [InlineKeyboardButton(text=t("wallet_btn_custom", lang), callback_data="topup_custom")],
        [back_btn("wallet", lang=lang), menu_btn(lang)],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("topup_amount_"))
async def topup_preset(cb: CallbackQuery, state: FSMContext):
    amount = float(cb.data.replace("topup_amount_", ""))
    await show_payment_options(cb, state, amount)

@router.callback_query(F.data == "topup_custom")
async def topup_custom(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('wallet_custom_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_custom_desc', lang)}",
        reply_markup=kb([back_btn("topup_start", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_amount)

@router.message(TopupStates.entering_amount)
async def receive_custom_amount(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    text = msg.text.strip()
    try:
        amount = float(text.replace(",", ".").replace("$", "").strip())
        if amount < MIN_TOPUP_USD:
            await msg.answer(t("wallet_min_deposit_error", lang, min=MIN_TOPUP_USD))
            return
        await state.clear()
        await show_payment_options_msg(msg, state, amount)
    except ValueError:
        await msg.answer(t("wallet_enter_number_error", lang))

async def show_payment_options(cb: CallbackQuery, state: FSMContext, amount: float):
    lang = get_lang(cb.from_user.id)
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
        f"{t('wallet_confirm_receive', lang, coins=coins)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{amount}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{amount}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=amount)

async def show_payment_options_msg(msg: Message, state: FSMContext, amount: float):
    lang = get_lang(msg.from_user.id)
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
        f"{t('wallet_confirm_receive', lang, coins=coins)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{amount}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{amount}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=amount)

# ── USDT payment ──────────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_usdt_"))
async def pay_usdt(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    amount = float(cb.data.replace("pay_usdt_", ""))
    coins = math.floor(amount / COIN_TO_USD)
    await state.update_data(topup_amount=amount, topup_coins=coins)
    text = (
        f"{t('wallet_usdt_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_usdt_send_exactly', lang, amount=f'{amount:.2f}')}\n"
        f"{t('wallet_usdt_network', lang)}\n\n"
        f"{t('wallet_usdt_address_label', lang)}\n"
        f"<code>{USDT_WALLET}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_usdt_after_sending', lang)}"
    )
    await cb.message.edit_text(
        text,
        reply_markup=kb([back_btn("topup_start", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_tx)

# ── Auto-verify TX hash ───────────────────────────────────────
@router.message(TopupStates.entering_tx)
async def receive_tx_hash(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    tx_hash = msg.text.strip()
    data = await state.get_data()
    amount = float(data.get("topup_amount", 0))
    coins = int(data.get("topup_coins", math.floor(amount / COIN_TO_USD)))
    uid = msg.from_user.id

    await msg.answer(t("wallet_verifying", lang))

    try:
        verified, actual_amount = await verify_tron_tx(tx_hash, amount)

        if verified:
            # Auto-credit coins
            add_coins(uid, coins)
            await _handle_referral_bonus(uid, coins)
            await msg.answer(
                f"{t('wallet_verified_title', lang)}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{t('wallet_verified_confirmed', lang)}\n"
                f"{t('wallet_verified_amount', lang, amount=f'{actual_amount:.2f}')}\n"
                f"{t('wallet_verified_coins', lang, coins=coins)}\n"
                f"{t('wallet_verified_balance', lang, coins=get_coins(uid))}",
                reply_markup=kb([menu_btn(lang)]),
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
    lang = get_lang(uid)
    await msg.answer(
        f"{t('wallet_review_title', lang)}\n\n"
        f"{t('wallet_review_body', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )

# ── Stars payment ─────────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_stars_"))
async def pay_stars(cb: CallbackQuery, state: FSMContext):
    from aiogram import Bot
    lang = get_lang(cb.from_user.id)
    amount = float(cb.data.replace("pay_stars_", ""))
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    bot = Bot(token=BOT_TOKEN)
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title=t("wallet_stars_invoice_title", lang),
        description=t("wallet_stars_invoice_desc", lang, coins=coins),
        payload=f"topup_{coins}_{cb.from_user.id}",
        currency="XTR",
        prices=[LabeledPrice(label=t("wallet_stars_label", lang, coins=coins), amount=stars_amount)],
        provider_token="",
    )
    await cb.answer()

@router.message(F.successful_payment)
async def successful_stars_payment(msg: Message):
    lang = get_lang(msg.from_user.id)
    payload = msg.successful_payment.invoice_payload
    parts = payload.split("_")
    coins = int(parts[1])
    uid = msg.from_user.id
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
    await msg.answer(
        f"{t('wallet_stars_success_title', lang)}\n\n"
        f"{t('wallet_stars_success_body', lang, coins=coins, coins2=get_coins(uid))}",
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
    user_lang = get_lang(uid)
    await bot.send_message(
        uid,
        f"{t('wallet_topup_confirmed_title', user_lang)}\n\n"
        f"{t('wallet_topup_confirmed_body', user_lang, coins=coins, balance=get_coins(uid))}",
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
    user_lang = get_lang(uid)
    await bot.send_message(uid, t("wallet_topup_rejected", user_lang))
    await cb.message.edit_text(f"✕  Rejected — user {uid}")

async def _handle_referral_bonus(uid: int, coins_added: int):
    ref_uid = get_referred_by(uid)
    if ref_uid:
        bonus = round(coins_added * REFERRAL_PERCENT / 100)
        if bonus > 0:
            add_coins(ref_uid, bonus)
            from aiogram import Bot
            bot = Bot(token=BOT_TOKEN)
            ref_lang = get_lang(ref_uid)
            await bot.send_message(
                ref_uid,
                f"{t('wallet_referral_bonus_title', ref_lang)}\n\n"
                f"{t('wallet_referral_bonus_body', ref_lang, bonus=bonus)}",
                parse_mode="HTML"
            )

# ── Referral info ─────────────────────────────────────────────
@router.callback_query(F.data == "referral_info")
async def referral_info(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    bot_username = "RetainXStudio"
    link = f"https://t.me/{bot_username}?start=ref_{cb.from_user.id}"
    text = (
        f"{t('wallet_referral_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_referral_desc', lang)}\n\n"
        f"{t('wallet_referral_link_label', lang)}\n"
        f"<code>{link}</code>\n\n"
        f"{t('wallet_referral_share', lang)}"
    )
    await cb.message.edit_text(
        text,
        reply_markup=kb([back_btn("wallet", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
