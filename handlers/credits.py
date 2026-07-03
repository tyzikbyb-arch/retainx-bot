import math
import time
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import COIN_TO_USD, MIN_TOPUP_USD, USDT_WALLET, REFERRAL_PERCENT, BOT_TOKEN, YOOMONEY_WALLET, COIN_TO_RUB, MIN_TOPUP_RUB, REFERRAL_TIERS, REFERRAL_JOIN_BONUS, CARD_NUMBER
from database import (get_coins, add_coins, get_referred_by, get_lang,
                       add_referral_balance, add_referral_earning, increment_topup_count,
                       get_referral_stats, get_referral_list, create_withdrawal_request, process_withdrawal,
                       get_promo_code, get_my_promo_code, create_promo_code,
                       has_used_promo, has_topped_up, use_promo_code,
                       set_pending_yoomoney_promo, clear_pending_yoomoney_promo,
                       get_is_blogger)
from keyboards import kb, back_btn, menu_btn
from i18n import t

router = Router()

TRON_API = "https://apilist.tronscanapi.com/api/transaction-info"

class TopupStates(StatesGroup):
    entering_amount = State()
    entering_tx = State()
    entering_rub_amount = State()
    entering_promo = State()
    entering_card_amount = State()
    entering_card_proof = State()

class WithdrawalStates(StatesGroup):
    entering_requisites = State()

MIN_WITHDRAWAL_RUB = 300.0

# ── Wallet ────────────────────────────────────────────
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

# ── Top-up start ──────────────────────────────────────────
async def _show_topup_start(target, state: FSMContext, lang: str):
    """Shared helper used by callback and after promo entry/cancellation."""
    data = await state.get_data()
    promo_code = data.get("promo_code")
    promo_pct  = data.get("promo_discount", 0)
    text = (
        f"{t('wallet_topup_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_topup_rate_line', lang)}\n"
        f"{t('wallet_topup_min_line', lang)}\n"
        f"{t('wallet_topup_5_line', lang)}\n"
        f"{t('wallet_topup_10_line', lang)}\n\n"
        f"{t('wallet_topup_select_or_custom', lang)}"
    )
    promo_row = (
        [InlineKeyboardButton(
            text=t("promo_active_btn", lang, code=promo_code, pct=promo_pct),
            callback_data="promo_cancel"
        )]
        if promo_code else
        [InlineKeyboardButton(text=t("promo_btn", lang), callback_data="promo_enter")]
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_2", lang),  callback_data="topup_amount_2"),
         InlineKeyboardButton(text=t("wallet_btn_5", lang),  callback_data="topup_amount_5")],
        [InlineKeyboardButton(text=t("wallet_btn_10", lang), callback_data="topup_amount_10"),
         InlineKeyboardButton(text=t("wallet_btn_20", lang), callback_data="topup_amount_20")],
        [InlineKeyboardButton(text=t("wallet_btn_custom", lang), callback_data="topup_custom")],
        [InlineKeyboardButton(text=t("wallet_btn_yoomoney", lang), callback_data="topup_yoomoney")],
        [InlineKeyboardButton(text=t("wallet_btn_card", lang), callback_data="topup_card")],
        promo_row,
        [back_btn("wallet", lang=lang), menu_btn(lang)],
    )
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data == "topup_start")
async def topup_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    lang = get_lang(cb.from_user.id)
    await _show_topup_start(cb, state, lang)

# ── Promo code entry ──────────────────────────────────────
@router.callback_query(F.data == "promo_enter")
async def promo_enter_cb(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('promo_enter_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('promo_enter_desc', lang)}",
        reply_markup=kb([back_btn("topup_start", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_promo)

@router.message(TopupStates.entering_promo)
async def receive_promo_code(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    lang = get_lang(uid)
    code = msg.text.strip().upper() if msg.text else ""
    promo = get_promo_code(code)
    if not promo:
        await msg.answer(t("promo_invalid", lang))
        return
    if promo["owner_uid"] == uid:
        await msg.answer(t("promo_own_code", lang))
        return
    if has_used_promo(uid):
        await msg.answer(t("promo_already_used", lang))
        return
    if has_topped_up(uid):
        await msg.answer(t("promo_not_first", lang))
        return
    pct = promo["discount_pct"]
    await state.update_data(promo_code=code, promo_discount=pct)
    await msg.answer(t("promo_applied", lang, code=code, pct=pct), parse_mode="HTML")
    await _show_topup_start(msg, state, lang)

@router.callback_query(F.data == "promo_cancel")
async def promo_cancel_cb(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await state.update_data(promo_code=None, promo_discount=0)
    await cb.answer(t("promo_cancelled", lang))
    await _show_topup_start(cb, state, lang)

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
        # Only clear the FSM state (entering_amount), not state data —
        # state.clear() would erase the promo code stored earlier
        await state.set_state(None)
        await show_payment_options_msg(msg, state, amount)
    except ValueError:
        await msg.answer(t("wallet_enter_number_error", lang))

async def show_payment_options(cb: CallbackQuery, state: FSMContext, amount: float):
    lang = get_lang(cb.from_user.id)
    data = await state.get_data()
    promo_code = data.get("promo_code")
    promo_pct  = int(data.get("promo_discount") or 0)
    coins = math.floor(amount / COIN_TO_USD)
    if promo_code and promo_pct:
        pay_amount = round(amount * (1 - promo_pct / 100), 2)
        stars_amount = int(pay_amount * 100)
        promo_lines = (
            f"\n{t('wallet_confirm_original', lang, amount=f'${amount:.2f}')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'${pay_amount:.2f}', pct=promo_pct)}"
        )
    else:
        pay_amount = amount
        stars_amount = int(amount * 100)
        promo_lines = ""
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
        f"{t('wallet_confirm_receive', lang, coins=coins)}"
        f"{promo_lines}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{pay_amount}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{pay_amount}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=pay_amount, topup_coins=coins)

async def show_payment_options_msg(msg: Message, state: FSMContext, amount: float):
    lang = get_lang(msg.from_user.id)
    data = await state.get_data()
    promo_code = data.get("promo_code")
    promo_pct  = int(data.get("promo_discount") or 0)
    coins = math.floor(amount / COIN_TO_USD)
    if promo_code and promo_pct:
        pay_amount = round(amount * (1 - promo_pct / 100), 2)
        stars_amount = int(pay_amount * 100)
        promo_lines = (
            f"\n{t('wallet_confirm_original', lang, amount=f'${amount:.2f}')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'${pay_amount:.2f}', pct=promo_pct)}"
        )
    else:
        pay_amount = amount
        stars_amount = int(amount * 100)
        promo_lines = ""
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
        f"{t('wallet_confirm_receive', lang, coins=coins)}"
        f"{promo_lines}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{pay_amount}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{pay_amount}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=pay_amount, topup_coins=coins)

# ── USDT payment ──────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_usdt_"))
async def pay_usdt(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    amount = float(cb.data.replace("pay_usdt_", ""))
    data = await state.get_data()
    # coins come from state (set before discount applied) — do NOT recalculate
    # from pay_amount or the promo discount would shrink the coin credit too
    coins = data.get("topup_coins") or math.floor(amount / COIN_TO_USD)
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

# ── Auto-verify TX hash ────────────────────────────────────────
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
            add_coins(uid, coins)
            await _handle_referral_bonus(uid, coins, payment_type="usdt")
            promo_code = data.get("promo_code")
            if promo_code:
                use_promo_code(promo_code, uid)
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
            promo_code = data.get("promo_code")
            await _send_for_manual_review(msg, tx_hash, amount, coins, uid, promo_code)
            await state.clear()

    except Exception as e:
        # Network error — send for manual review
        promo_code = data.get("promo_code")
        await _send_for_manual_review(msg, tx_hash, amount, coins, uid, promo_code)
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

async def _send_for_manual_review(msg: Message, tx_hash: str, amount: float, coins: int, uid: int, promo_code: str = None):
    """Fallback to manual review if auto-verify fails."""
    from config import ADMIN_ID
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    promo_part = promo_code or "none"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Confirm", callback_data=f"confirm_topup_{uid}_{coins}_{promo_part}"),
        InlineKeyboardButton(text="✕  Reject",  callback_data=f"reject_topup_{uid}"),
    ]])
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>Manual Review Required</b>\n\n"
        f"  User    @{msg.from_user.username or '—'} (<code>{uid}</code>)\n"
        f"  Amount  <b>${amount:.2f}</b>  →  <b>{coins} coins</b>\n"
        + (f"  Promo   <code>{promo_code}</code>\n" if promo_code else "")
        + f"\n  TX Hash:\n<code>{tx_hash}</code>\n\n"
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

# ── Stars payment ─────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_stars_"))
async def pay_stars(cb: CallbackQuery, state: FSMContext):
    from aiogram import Bot
    lang = get_lang(cb.from_user.id)
    pay_amount = float(cb.data.replace("pay_stars_", ""))
    stars_amount = int(pay_amount * 100)
    # Coins come from state (set in show_payment_options to the original pre-discount amount)
    data = await state.get_data()
    coins = data.get("topup_coins") or math.floor(pay_amount / COIN_TO_USD)
    promo_code = data.get("promo_code")
    bot = Bot(token=BOT_TOKEN)
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title=t("wallet_stars_invoice_title", lang),
        description=t("wallet_stars_invoice_desc", lang, coins=coins),
        payload=f"topup_{coins}_{cb.from_user.id}_{promo_code or ''}",
        currency="XTR",
        prices=[LabeledPrice(label=t("wallet_stars_label", lang, coins=coins), amount=stars_amount)],
        provider_token="",
    )
    await cb.answer()

@router.message(F.successful_payment)
async def successful_stars_payment(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    payload = msg.successful_payment.invoice_payload
    parts = payload.split("_")
    coins = int(parts[1])
    uid = msg.from_user.id
    promo_code = parts[3] if len(parts) > 3 and parts[3] else None
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins, payment_type="stars")
    if promo_code:
        use_promo_code(promo_code, uid)
        await state.update_data(promo_code=None, promo_discount=0)
    await msg.answer(
        f"{t('wallet_stars_success_title', lang)}\n\n"
        f"{t('wallet_stars_success_body', lang, coins=coins, coins2=get_coins(uid))}",
        parse_mode="HTML"
    )

# ── YooMoney (RUB) flow ─────────────────────────────────────
@router.callback_query(F.data == "topup_yoomoney")
async def topup_yoomoney_start(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('wallet_yoomoney_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_yoomoney_rate_line', lang)}\n"
        f"{t('wallet_yoomoney_min_line', lang)}\n\n"
        f"{t('wallet_yoomoney_prompt', lang)}",
        reply_markup=kb([back_btn("topup_start", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_rub_amount)

@router.message(TopupStates.entering_rub_amount)
async def receive_rub_amount(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    text = msg.text.strip().replace(",", ".").replace("₽", "").replace(" ", "")
    try:
        amount_rub = float(text)
    except ValueError:
        await msg.answer(t("wallet_enter_number_error", lang))
        return

    if amount_rub < MIN_TOPUP_RUB:
        await msg.answer(t("wallet_yoomoney_min_error", lang, min=int(MIN_TOPUP_RUB)))
        return

    uid = msg.from_user.id
    coins = math.floor(amount_rub / COIN_TO_RUB)
    data = await state.get_data()
    promo_code = data.get("promo_code")
    promo_pct  = int(data.get("promo_discount") or 0)

    if promo_code and promo_pct:
        pay_rub = round(amount_rub * (1 - promo_pct / 100), 2)
        set_pending_yoomoney_promo(uid, coins, promo_code)
        promo_lines = (
            f"\n{t('wallet_confirm_original', lang, amount=f'{amount_rub:.2f} ₽')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'{pay_rub:.2f} ₽', pct=promo_pct)}"
        )
    else:
        pay_rub = amount_rub
        clear_pending_yoomoney_promo(uid)
        promo_lines = ""

    pay_url = (
        f"https://yoomoney.ru/quickpay/confirm.xml"
        f"?receiver={YOOMONEY_WALLET}"
        f"&quickpay-form=shop"
        f"&sum={pay_rub:.2f}"
        f"&label={uid}"
        f"&targets=RetainX+пополнение"
    )
    await state.clear()
    await msg.answer(
        f"{t('wallet_yoomoney_confirm_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_yoomoney_confirm_amount', lang, amount=f'{amount_rub:.2f}')}\n"
        f"{t('wallet_yoomoney_confirm_coins', lang, coins=coins)}"
        f"{promo_lines}\n\n"
        f"{t('wallet_yoomoney_confirm_note', lang)}",
        reply_markup=kb(
            [InlineKeyboardButton(
                text=t("wallet_btn_pay_yoomoney", lang, amount=f"{pay_rub:.0f}"),
                url=pay_url,
            )],
            [menu_btn(lang)],
        ),
        parse_mode="HTML"
    )

# ── Card payment (RF Mastercard) ──────────────────────────────
@router.callback_query(F.data == "topup_card")
async def topup_card_start(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('wallet_card_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_card_rate_line', lang)}\n"
        f"{t('wallet_card_min_line', lang)}\n\n"
        f"{t('wallet_card_prompt', lang)}",
        reply_markup=kb([back_btn("topup_start", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(TopupStates.entering_card_amount)

@router.message(TopupStates.entering_card_amount)
async def receive_card_amount(msg: Message, state: FSMContext):
    lang = get_lang(msg.from_user.id)
    text = msg.text.strip().replace(",", ".").replace("₽", "").replace(" ", "") if msg.text else ""
    try:
        amount_rub = float(text)
    except ValueError:
        await msg.answer(t("wallet_enter_number_error", lang))
        return

    if amount_rub < MIN_TOPUP_RUB:
        await msg.answer(t("wallet_card_min_error", lang, min=int(MIN_TOPUP_RUB)))
        return

    uid = msg.from_user.id
    coins = math.floor(amount_rub / COIN_TO_RUB)
    data = await state.get_data()
    promo_code = data.get("promo_code")
    promo_pct  = int(data.get("promo_discount") or 0)

    if promo_code and promo_pct:
        pay_rub = round(amount_rub * (1 - promo_pct / 100), 2)
        promo_lines = (
            f"\n{t('wallet_confirm_original', lang, amount=f'{amount_rub:.2f} ₽')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'{pay_rub:.2f} ₽', pct=promo_pct)}"
        )
    else:
        pay_rub = amount_rub
        promo_lines = ""

    await state.update_data(card_coins=coins, card_pay_rub=pay_rub, card_promo=promo_code)
    await state.set_state(TopupStates.entering_card_proof)

    await msg.answer(
        f"{t('wallet_card_confirm_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_card_confirm_amount', lang, amount=f'{pay_rub:.2f}')}\n"
        f"{t('wallet_card_confirm_coins', lang, coins=coins)}"
        f"{promo_lines}\n\n"
        f"{t('wallet_card_number_label', lang)}\n"
        f"<code>{CARD_NUMBER}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_card_note', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )

@router.message(TopupStates.entering_card_proof)
async def receive_card_proof(msg: Message, state: FSMContext):
    if not (msg.photo or msg.document or msg.text):
        return

    uid = msg.from_user.id
    lang = get_lang(uid)
    data = await state.get_data()
    coins = int(data.get("card_coins", 0))
    pay_rub = float(data.get("card_pay_rub", 0))
    promo_code = data.get("card_promo") or ""
    await state.clear()

    from config import ADMIN_ID
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)

    caption = (
        f"💳  <b>Card Payment Proof</b>\n\n"
        f"  User    @{msg.from_user.username or '—'} (<code>{uid}</code>)\n"
        f"  Amount  <b>{pay_rub:.2f} ₽</b>  →  <b>{coins} coins</b>\n"
        + (f"  Promo   <code>{promo_code}</code>\n" if promo_code else "")
    )
    promo_part = promo_code or "none"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✓  Confirm", callback_data=f"confirm_card_{uid}_{coins}_{promo_part}"),
        InlineKeyboardButton(text="✕  Reject",  callback_data=f"reject_card_{uid}"),
    ]])

    if msg.photo:
        await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=caption, reply_markup=keyboard, parse_mode="HTML")
    elif msg.document:
        await bot.send_document(ADMIN_ID, msg.document.file_id, caption=caption, reply_markup=keyboard, parse_mode="HTML")
    else:
        await bot.send_message(
            ADMIN_ID,
            caption + f"\n\n  Proof text:\n<code>{msg.text}</code>",
            reply_markup=keyboard, parse_mode="HTML"
        )

    await msg.answer(
        f"{t('wallet_card_submitted_title', lang)}\n\n"
        f"{t('wallet_card_submitted_body', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("confirm_card_"))
async def admin_confirm_card(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    # format: confirm_card_{uid}_{coins}_{promo_or_none}
    parts = cb.data.split("_")
    uid = int(parts[2])
    coins = int(parts[3])
    promo_code = parts[4] if len(parts) > 4 and parts[4] != "none" else None

    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins, payment_type="card")
    if promo_code:
        use_promo_code(promo_code, uid)

    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    user_lang = get_lang(uid)
    balance = get_coins(uid)
    await bot.send_message(
        uid,
        f"{t('wallet_card_success_title', user_lang)}\n\n"
        f"{t('wallet_card_success_body', user_lang, coins=coins, balance=balance)}",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✓  Card confirmed — {coins} coins → user {uid}", parse_mode="HTML")

@router.callback_query(F.data.startswith("reject_card_"))
async def admin_reject_card(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    uid = int(cb.data.split("_")[-1])
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    user_lang = get_lang(uid)
    await bot.send_message(
        uid,
        f"{t('wallet_card_rejected_title', user_lang)}\n\n"
        f"{t('wallet_card_rejected_body', user_lang)}",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✕  Card rejected — user {uid}")

# ── Admin confirm/reject ───────────────────────────────────────
@router.callback_query(F.data.startswith("confirm_topup_"))
async def admin_confirm_topup(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    # format: confirm_topup_{uid}_{coins}_{promo_or_none}
    parts = cb.data.split("_", 4)
    uid = int(parts[2])
    coins = int(parts[3])
    promo_code = parts[4] if len(parts) > 4 and parts[4] != "none" else None
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins, payment_type="usdt")
    if promo_code:
        use_promo_code(promo_code, uid)
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

def _get_tier(referral_count: int) -> dict:
    for tier in reversed(REFERRAL_TIERS):
        if referral_count >= tier["min"]:
            return tier
    return REFERRAL_TIERS[0]

def _tier_progress_bar(referral_count: int) -> tuple[dict, str, str]:
    tier = _get_tier(referral_count)
    if tier["next"] is None:
        bar = "████████████"
        label = "MAX"
    else:
        width = 12
        progress = referral_count - tier["min"]
        total = tier["next"] - tier["min"]
        filled = min(width, round(progress / total * width))
        bar = "█" * filled + "░" * (width - filled)
        label = f"{referral_count} / {tier['next']}"
    return tier, bar, label

async def _handle_referral_bonus(uid: int, coins_added: int, payment_type: str = "unknown"):
    topup_index = increment_topup_count(uid)  # 0 = first topup, 1+ = subsequent
    ref_uid = get_referred_by(uid)
    if ref_uid:
        # Determine referrer's tier by their total referral count
        ref_stats = get_referral_stats(ref_uid)
        tier = _get_tier(ref_stats.get("referral_count", 0))
        percentage = tier["first"] if topup_index == 0 else tier["repeat"]
        bonus_rub = round(coins_added * COIN_TO_RUB * percentage / 100, 2)
        if bonus_rub > 0:
            add_referral_balance(ref_uid, bonus_rub)
            add_referral_earning(ref_uid, uid, bonus_rub, percentage, payment_type)
            from aiogram import Bot
            bot = Bot(token=BOT_TOKEN)
            ref_lang = get_lang(ref_uid)
            await bot.send_message(
                ref_uid,
                f"{t('wallet_referral_bonus_title', ref_lang)}\n\n"
                f"{t('wallet_referral_bonus_body', ref_lang, bonus=f'{bonus_rub:.2f}', percentage=percentage)}",
                parse_mode="HTML"
            )

# ── Referral info ─────────────────────────────────────────
@router.callback_query(F.data == "referral_info")
async def referral_info(cb: CallbackQuery):
    import urllib.parse
    uid = cb.from_user.id
    lang = get_lang(uid)
    bot_username = "RetainXStudioBot"
    link = f"https://t.me/{bot_username}?start=ref_{uid}"
    stats = get_referral_stats(uid)
    balance = stats["balance"]
    total_earned = stats["total_earned"]
    pending = stats["pending_withdrawals"]
    referral_count = stats.get("referral_count", 0)
    buyers_count = stats.get("buyers_count", 0)

    tier, bar, bar_label = _tier_progress_bar(referral_count)
    tier_name = tier["name_ru"] if lang == "ru" else tier["name_en"]
    next_tier = None
    for i, t_ in enumerate(REFERRAL_TIERS):
        if t_["min"] == tier["min"] and i + 1 < len(REFERRAL_TIERS):
            next_tier = REFERRAL_TIERS[i + 1]
            break

    # Tier header line
    if tier["next"] is None:
        tier_header = t("wallet_referral_tier_max", lang, name=tier_name)
    elif next_tier:
        next_name = next_tier["name_ru"] if lang == "ru" else next_tier["name_en"]
        tier_header = t("wallet_referral_tier_line", lang, name=tier_name, next=next_name)
    else:
        tier_header = tier_name

    # Format numbers with spaces for thousands
    def fmt(n): return f"{n:,.2f}".replace(",", " ")

    text = (
        f"{t('wallet_referral_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  {tier_header}\n"
        f"  {bar}  {bar_label}\n\n"
        f"  {t('wallet_referral_rate', lang, first=tier['first'], repeat=tier['repeat'])}\n\n"
        "  ─────────────────────\n"
        f"  {t('wallet_referral_stat_invited', lang)}   <b>{referral_count}</b>\n"
        f"  {t('wallet_referral_stat_buyers', lang)}   <b>{buyers_count}</b>\n"
        f"  {t('wallet_referral_stat_balance', lang)}   <b>{fmt(balance)} ₽</b>\n"
        f"  {t('wallet_referral_stat_total', lang)}   <b>{fmt(total_earned)} ₽</b>\n"
        "  ─────────────────────\n\n"
        f"  {t('wallet_referral_join_bonus_note', lang, bonus=REFERRAL_JOIN_BONUS)}\n\n"
        f"  {t('wallet_referral_link_label', lang)}\n"
        f"  <code>{link}</code>"
    )

    share_text = urllib.parse.quote(t("wallet_referral_share_text", lang, link=link))
    share_url = f"https://t.me/share/url?url={urllib.parse.quote(link)}&text={share_text}"

    buttons = []
    buttons.append([InlineKeyboardButton(
        text=t("wallet_referral_share_btn", lang),
        url=share_url
    )])
    buttons.append([InlineKeyboardButton(
        text=t("wallet_referral_my_list_btn", lang, count=referral_count),
        callback_data="referral_list"
    )])
    if balance >= MIN_WITHDRAWAL_RUB and pending == 0:
        buttons.append([InlineKeyboardButton(
            text=t("wallet_referral_withdraw_btn", lang, amount=f"{balance:.2f}"),
            callback_data="referral_withdraw"
        )])
    elif balance > 0 and balance < MIN_WITHDRAWAL_RUB:
        buttons.append([InlineKeyboardButton(
            text=t("wallet_referral_withdraw_unavailable", lang, min=int(MIN_WITHDRAWAL_RUB)),
            callback_data="referral_withdraw_low"
        )])
    elif pending > 0:
        buttons.append([InlineKeyboardButton(
            text=t("wallet_referral_withdraw_pending", lang),
            callback_data="referral_withdraw_low"
        )])
    if get_is_blogger(uid):
        buttons.append([InlineKeyboardButton(
            text=t("wallet_referral_promo_btn", lang),
            callback_data="referral_my_promo"
        )])
    buttons.append([back_btn("wallet", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(text, reply_markup=kb(*buttons), parse_mode="HTML")


@router.callback_query(F.data == "referral_my_promo")
async def referral_my_promo(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    promo = get_my_promo_code(uid)
    if not promo:
        text = (
            f"{t('my_promo_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('my_promo_none', lang)}"
        )
        keyboard = kb(
            [InlineKeyboardButton(text=t("my_promo_create_btn", lang), callback_data="referral_create_promo")],
            [back_btn("referral_info", lang=lang), menu_btn(lang)],
        )
    else:
        text = (
            f"{t('my_promo_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('my_promo_code_label', lang, code=promo['code'])}\n"
            f"{t('my_promo_discount_label', lang, pct=promo['discount_pct'])}\n"
            f"{t('my_promo_uses_label', lang, uses=promo['uses_count'])}\n\n"
            f"  {t('my_promo_share_hint', lang)}"
        )
        keyboard = kb(
            [back_btn("referral_info", lang=lang), menu_btn(lang)],
        )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "referral_create_promo")
async def referral_create_promo(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    if get_my_promo_code(uid):
        await cb.answer()
        return
    username = cb.from_user.username or str(uid)
    try:
        code = create_promo_code(uid, username)
    except RuntimeError:
        await cb.answer("Could not generate code. Please try again.", show_alert=True)
        return
    text = (
        f"{t('my_promo_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('my_promo_code_label', lang, code=code)}\n"
        f"{t('my_promo_discount_label', lang, pct=30)}\n"
        f"{t('my_promo_uses_label', lang, uses=0)}\n\n"
        f"  {t('my_promo_share_hint', lang)}"
    )
    keyboard = kb(
        [back_btn("referral_info", lang=lang), menu_btn(lang)],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "referral_list")
async def referral_list_handler(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    referrals = get_referral_list(uid)

    if not referrals:
        text = (
            f"{t('wallet_referral_list_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('wallet_referral_list_empty', lang)}"
        )
    else:
        buyers = sum(1 for r in referrals if (r.get("topup_count") or 0) > 0)
        total_sub = sum(r.get("sub_count") or 0 for r in referrals)
        total_sub_buyers = sum(r.get("sub_buyers") or 0 for r in referrals)
        lines = []
        for r in referrals[:30]:
            username = f"@{r['username']}" if r.get("username") else f"ID {r['uid']}"
            icon = "✅" if (r.get("topup_count") or 0) > 0 else "◌"
            sub_count = r.get("sub_count") or 0
            sub_buyers = r.get("sub_buyers") or 0
            if sub_count > 0:
                lines.append(
                    f"  {icon}  {username}  ·  "
                    f"{t('wallet_referral_sub_followers', lang, n=sub_count)}  ·  "
                    f"{t('wallet_referral_sub_buyers', lang, n=sub_buyers)}"
                )
            else:
                joined_ts = r.get("joined") or 0
                joined_date = time.strftime("%d.%m.%Y", time.localtime(joined_ts)) if joined_ts else "—"
                lines.append(f"  {icon}  {username}  ·  {joined_date}")
        header = t("wallet_referral_list_header", lang, count=len(referrals), buyers=buyers)
        blogger_line = (
            f"\n{t('wallet_referral_blogger_totals', lang, sub=total_sub, sub_buyers=total_sub_buyers)}"
            if total_sub > 0 else ""
        )
        text = (
            f"{t('wallet_referral_list_title', lang)}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{header}{blogger_line}\n\n"
            + "\n".join(lines)
        )

    await cb.message.edit_text(
        text,
        reply_markup=kb([back_btn("referral_info", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "referral_withdraw_low")
async def referral_withdraw_low(cb: CallbackQuery):
    await cb.answer()


@router.callback_query(F.data == "referral_withdraw")
async def referral_withdraw_start(cb: CallbackQuery, state: FSMContext):
    uid = cb.from_user.id
    lang = get_lang(uid)
    stats = get_referral_stats(uid)
    balance = stats["balance"]
    if balance < MIN_WITHDRAWAL_RUB:
        await cb.answer(t("wallet_referral_withdraw_low_alert", lang, min=int(MIN_WITHDRAWAL_RUB)), show_alert=True)
        return
    await cb.message.edit_text(
        f"{t('wallet_referral_withdraw_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_referral_withdraw_amount', lang, amount=f'{balance:.2f}')}\n\n"
        f"{t('wallet_referral_enter_requisites', lang)}",
        reply_markup=kb([back_btn("referral_info", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await state.set_state(WithdrawalStates.entering_requisites)
    await state.update_data(withdrawal_amount=balance)


@router.message(WithdrawalStates.entering_requisites)
async def receive_requisites(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    lang = get_lang(uid)
    requisites = msg.text.strip() if msg.text else ""
    if not requisites or len(requisites) < 5:
        await msg.answer(t("wallet_referral_requisites_invalid", lang))
        return
    data = await state.get_data()
    amount = float(data.get("withdrawal_amount", 0))
    req_id = create_withdrawal_request(uid, amount, requisites)
    await state.clear()
    from config import ADMIN_ID
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        ADMIN_ID,
        f"◈  <b>Withdrawal Request #{req_id}</b>\n\n"
        f"  User: <code>{uid}</code>\n"
        f"  Amount: <b>{amount:.2f} ₽</b>\n\n"
        f"  Requisites:\n{requisites}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✓  Paid", callback_data=f"withdrawal_paid_{req_id}"),
            InlineKeyboardButton(text="✕  Reject", callback_data=f"withdrawal_reject_{req_id}_{uid}"),
        ]]),
        parse_mode="HTML"
    )
    await msg.answer(
        f"{t('wallet_referral_withdraw_submitted_title', lang)}\n\n"
        f"{t('wallet_referral_withdraw_submitted_body', lang, amount=f'{amount:.2f}')}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("withdrawal_paid_"))
async def withdrawal_paid(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    req_id = int(cb.data.replace("withdrawal_paid_", ""))
    req = process_withdrawal(req_id, "paid")
    if not req:
        await cb.answer("Not found")
        return
    uid = req["user_id"]
    amount = req["amount_rub"]
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    user_lang = get_lang(uid)
    await bot.send_message(
        uid,
        f"{t('wallet_referral_withdraw_paid_title', user_lang)}\n\n"
        f"{t('wallet_referral_withdraw_paid_body', user_lang, amount=f'{amount:.2f}')}",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✓  Withdrawal #{req_id} marked as paid — {amount:.2f} ₽ to user {uid}")


@router.callback_query(F.data.startswith("withdrawal_reject_"))
async def withdrawal_rejected(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        return
    parts = cb.data.split("_")
    req_id = int(parts[2])
    uid = int(parts[3])
    req = process_withdrawal(req_id, "rejected")
    if not req:
        await cb.answer("Not found")
        return
    amount = req["amount_rub"]
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    user_lang = get_lang(uid)
    await bot.send_message(
        uid,
        f"{t('wallet_referral_withdraw_rejected_title', user_lang)}\n\n"
        f"{t('wallet_referral_withdraw_rejected_body', user_lang, amount=f'{amount:.2f}')}",
        parse_mode="HTML"
    )
    await cb.message.edit_text(f"✕  Withdrawal #{req_id} rejected — {amount:.2f} ₽ refunded to user {uid}")
