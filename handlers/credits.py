import math
import time
import datetime
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import COIN_TO_USD, MIN_TOPUP_USD, USDT_WALLET, REFERRAL_PERCENT, REFERRAL_TIERS, BOT_TOKEN, UNLIMITED_TIER_CONFIG, UNLIMITED_PLANS
from database import (
    get_coins, add_coins, spend_coins, get_referred_by, get_lang, has_unlimited,
    get_unlimited_until, get_unlimited_tier, set_unlimited, can_buy_unlimited,
    get_referral_count, get_referral_buyers_count, is_ref_first_topup_done,
    mark_ref_first_topup_done, try_mark_ref_first_topup_done,
    get_is_blogger, get_active_promo, set_active_promo, clear_active_promo,
    get_promo_code, get_promo_code_by_uid, increment_promo_uses, create_promo_code,
)
from keyboards import kb, back_btn, menu_btn
from i18n import t

router = Router()

TRON_API = "https://apilist.tronscanapi.com/api/transaction-info"

# Shared bot instance for outbound notifications — avoids per-call session overhead.
_notify_bot = None

def _get_notify_bot():
    global _notify_bot
    if _notify_bot is None:
        from aiogram import Bot as _Bot
        _notify_bot = _Bot(token=BOT_TOKEN)
    return _notify_bot

class TopupStates(StatesGroup):
    entering_amount = State()
    entering_tx = State()

# ── Wallet ─────────────────────────────────────────────────────────────
async def show_wallet(target, state: FSMContext = None):
    if state:
        await state.clear()
    uid = target.from_user.id if isinstance(target, (Message, CallbackQuery)) else target
    lang = get_lang(uid)
    coins = get_coins(uid)
    usd_val = round(coins * COIN_TO_USD, 2)

    # Unlimited pass status
    unlim_active = has_unlimited(uid)
    unlim_line = ""
    if unlim_active:
        until_ts = get_unlimited_until(uid) or 0
        remaining = max(0, until_ts - int(time.time()))
        mins = remaining // 60
        secs = remaining % 60
        tier = get_unlimited_tier(uid) or "standard"
        tier_cfg = UNLIMITED_TIER_CONFIG.get(tier, UNLIMITED_TIER_CONFIG["standard"])
        tier_name = tier_cfg["name_ru"] if lang == "ru" else tier_cfg["name_en"]
        unlim_line = t("unlim_active_line", lang, emoji=tier_cfg["emoji"], name=tier_name, mins=mins, secs=secs)

    text = (
        f"{t('wallet_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('wallet_balance', lang, coins=coins, usd=usd_val)}\n"
        f"{unlim_line}\n"
        f"{t('wallet_rate', lang)}\n"
        f"{t('wallet_min_topup', lang)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    buttons = [
        [InlineKeyboardButton(text=t("wallet_btn_add_coins", lang), callback_data="topup_start")],
    ]
    if not unlim_active:
        buttons.append([InlineKeyboardButton(text=t("unlim_btn_buy", lang), callback_data="unlimited_buy")])
        buttons.append([InlineKeyboardButton(text=t("unlim_btn_info", lang), callback_data="unlim_info")])
    else:
        tier = get_unlimited_tier(uid) or "standard"
        tier_cfg = UNLIMITED_TIER_CONFIG.get(tier, UNLIMITED_TIER_CONFIG["standard"])
        tier_name = tier_cfg["name_ru"] if lang == "ru" else tier_cfg["name_en"]
        buttons.append([InlineKeyboardButton(text=t("unlim_btn_active", lang, name=tier_name), callback_data="unlimited_status")])
    buttons.append([InlineKeyboardButton(text=t("wallet_btn_referral", lang), callback_data="referral_info")])
    if get_is_blogger(uid):
        buttons.append([InlineKeyboardButton(text=t("wallet_referral_promo_btn", lang), callback_data="my_promo")])
    else:
        active_promo = get_active_promo(uid)
        if active_promo:
            promo_info = get_promo_code(active_promo)
            pct = promo_info["pct"] if promo_info else 30
            buttons.append([InlineKeyboardButton(
                text=t("promo_active_btn", lang, code=active_promo, pct=pct),
                callback_data="promo_cancel"
            )])
        elif not is_ref_first_topup_done(uid):
            buttons.append([InlineKeyboardButton(text=t("promo_btn", lang), callback_data="promo_enter")])
    buttons.append([menu_btn(lang)])

    keyboard = kb(*buttons)
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data == "wallet")
async def wallet_cb(cb: CallbackQuery, state: FSMContext):
    await show_wallet(cb, state)

@router.callback_query(F.data == "unlimited_status")
async def unlimited_status_cb(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    await cb.answer(t("unlim_active_toast", lang), show_alert=False)

# ── Unlimited pass purchase — tiered coin flow ────────────────────────
_TIER_ORDER = ["standard", "pro", "vip"]

def _tier_info_text(tier: str, lang: str) -> str:
    _key = {"standard": "unlim_tier_std_info", "pro": "unlim_tier_pro_info", "vip": "unlim_tier_vip_info"}
    return t(_key.get(tier, "unlim_tier_std_info"), lang)

async def _show_unlim_plans(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    rows = []
    for tier in _TIER_ORDER:
        cfg = UNLIMITED_TIER_CONFIG[tier]
        price_1h = UNLIMITED_PLANS[tier][1]
        name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
        rows.append([InlineKeyboardButton(
            text=t("unlim_info_tier_btn", lang, emoji=cfg["emoji"], name=name, coins=price_1h),
            callback_data=f"ulim_info_{tier}"
        )])
    rows.append([InlineKeyboardButton(text=t("unlim_support_btn", lang), url="https://t.me/RetainXStudio")])
    rows.append([back_btn("wallet", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        f"{t('unlim_info_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('unlim_info_body', lang)}",
        reply_markup=kb(*rows),
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(F.data == "unlimited_buy")
async def unlimited_buy(cb: CallbackQuery, state: FSMContext):
    await _show_unlim_plans(cb)

@router.callback_query(F.data.startswith("ulim_t_"))
async def unlim_tier_selected(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.answer(t("unlim_support_toast", lang), show_alert=True)
    return
    tier = cb.data[7:]
    if tier not in UNLIMITED_TIER_CONFIG:
        await cb.answer()
        return
    lang = get_lang(cb.from_user.id)
    cfg = UNLIMITED_TIER_CONFIG[tier]
    name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
    plans = UNLIMITED_PLANS[tier]
    info = _tier_info_text(tier, lang)

    rows = [
        [InlineKeyboardButton(text=t("unlim_dur_1h", lang, coins=plans[1]), callback_data=f"ulim_d_{tier}_1")],
        [InlineKeyboardButton(text=t("unlim_dur_2h", lang, coins=plans[2]), callback_data=f"ulim_d_{tier}_2")],
        [InlineKeyboardButton(text=t("unlim_dur_3h", lang, coins=plans[3]), callback_data=f"ulim_d_{tier}_3")],
        [back_btn("unlimited_buy", lang=lang), menu_btn(lang)],
    ]
    await cb.message.edit_text(
        f"{t('unlim_tier_title', lang, name=name)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{info}\n\n"
        f"{t('unlim_select_duration', lang)}",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("ulim_d_"))
async def unlim_duration_selected(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.answer(t("unlim_support_toast", lang), show_alert=True)
    return
    parts = cb.data[7:].split("_")
    if len(parts) != 2:
        await cb.answer()
        return
    tier, hours_str = parts[0], parts[1]
    hours = int(hours_str)
    if tier not in UNLIMITED_TIER_CONFIG or hours not in UNLIMITED_PLANS.get(tier, {}):
        await cb.answer()
        return
    lang = get_lang(cb.from_user.id)
    cfg = UNLIMITED_TIER_CONFIG[tier]
    name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
    coins_cost = UNLIMITED_PLANS[tier][hours]
    user_coins = get_coins(cb.from_user.id)

    if user_coins < coins_cost:
        await cb.answer(t("unlim_not_enough", lang, need=coins_cost, have=user_coins), show_alert=True)
        return

    await cb.message.edit_text(
        f"{t('unlim_confirm_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('unlim_confirm_tier', lang, name=name)}\n"
        f"{t('unlim_confirm_dur', lang, hours=hours)}\n"
        f"{t('unlim_confirm_cost', lang, cost=coins_cost)}\n"
        f"{t('unlim_confirm_balance', lang, coins=user_coins)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(
                text=t("unlim_btn_activate", lang, cost=coins_cost),
                callback_data=f"ulim_c_{tier}_{hours}"
            )],
            [back_btn(f"ulim_t_{tier}", lang=lang), menu_btn(lang)],
        ),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("ulim_c_"))
async def unlim_confirm(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    await cb.answer(t("unlim_support_toast", lang), show_alert=True)
    return
    parts = cb.data[7:].split("_")
    if len(parts) != 2:
        await cb.answer()
        return
    tier, hours_str = parts[0], parts[1]
    hours = int(hours_str)
    uid = cb.from_user.id
    lang = get_lang(uid)

    if tier not in UNLIMITED_TIER_CONFIG or hours not in UNLIMITED_PLANS.get(tier, {}):
        await cb.answer(t("unlim_error_retry", lang), show_alert=True)
        return

    coins_cost = UNLIMITED_PLANS[tier][hours]
    if not spend_coins(uid, coins_cost):
        await cb.answer(t("unlim_no_balance", lang), show_alert=True)
        return

    duration_secs = hours * 3600
    until = set_unlimited(uid, duration_secs, tier)
    until_str = datetime.datetime.fromtimestamp(until).strftime("%H:%M")
    cfg = UNLIMITED_TIER_CONFIG[tier]
    name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]

    await cb.message.edit_text(
        f"{t('unlim_activated_title', lang, name=name)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('unlim_activated_body', lang, time=until_str, hours=hours, cost=coins_cost)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )
    await cb.answer()

# ── Unlimited info section ───────────────────────────────────────────────
def _build_tier_page(tier: str, lang: str) -> str:
    p = UNLIMITED_PLANS[tier]
    _key = {"standard": "unlim_page_std", "pro": "unlim_page_pro", "vip": "unlim_page_vip"}
    return t(_key[tier], lang, p1=p[1], p2=p[2], p3=p[3])

@router.callback_query(F.data == "unlim_info")
async def unlim_info(cb: CallbackQuery):
    await _show_unlim_plans(cb)

@router.callback_query(F.data.startswith("ulim_info_"))
async def unlim_info_tier(cb: CallbackQuery):
    tier = cb.data[10:]
    if tier not in UNLIMITED_TIER_CONFIG:
        await cb.answer()
        return
    lang = get_lang(cb.from_user.id)
    nav = {"standard": ("pro", "vip"), "pro": ("standard", "vip"), "vip": ("pro", None)}
    prev_tier, next_tier = nav[tier]
    _label = {"standard": "⚡  Standard", "pro": "⚡⚡  Pro", "vip": "♛  VIP"}
    nav_row = []
    if prev_tier:
        nav_row.append(InlineKeyboardButton(text=f"←  {_label[prev_tier]}", callback_data=f"ulim_info_{prev_tier}"))
    if next_tier:
        nav_row.append(InlineKeyboardButton(text=f"{_label[next_tier]}  →", callback_data=f"ulim_info_{next_tier}"))
    rows = []
    if nav_row:
        rows.append(nav_row)
    rows.append([InlineKeyboardButton(text=t("unlim_support_btn", lang), url="https://t.me/RetainXStudio")])
    rows.append([back_btn("unlimited_buy", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        _build_tier_page(tier, lang),
        reply_markup=kb(*rows),
        parse_mode="HTML",
    )
    await cb.answer()

# ── Top-up start ─────────────────────────────────────────────────────────
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
    uid = cb.from_user.id
    lang = get_lang(uid)
    promo_code = get_active_promo(uid)
    pct = 0
    discounted = amount
    if promo_code:
        promo_rec = get_promo_code(promo_code)
        if promo_rec:
            pct = promo_rec["pct"]
            discounted = round(amount * (1 - pct / 100), 2)
    coins = math.floor(discounted / COIN_TO_USD)
    stars_amount = int(discounted * 100)
    if pct:
        amount_lines = (
            f"{t('wallet_confirm_original', lang, amount=f'${amount:.2f}')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'${discounted:.2f}', pct=pct)}\n"
        )
    else:
        amount_lines = f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{amount_lines}"
        f"{t('wallet_confirm_receive', lang, coins=coins)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{discounted}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{discounted}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await cb.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=discounted)

async def show_payment_options_msg(msg: Message, state: FSMContext, amount: float):
    uid = msg.from_user.id
    lang = get_lang(uid)
    promo_code = get_active_promo(uid)
    pct = 0
    discounted = amount
    if promo_code:
        promo_rec = get_promo_code(promo_code)
        if promo_rec:
            pct = promo_rec["pct"]
            discounted = round(amount * (1 - pct / 100), 2)
    coins = math.floor(discounted / COIN_TO_USD)
    stars_amount = int(discounted * 100)
    if pct:
        amount_lines = (
            f"{t('wallet_confirm_original', lang, amount=f'${amount:.2f}')}\n"
            f"{t('wallet_confirm_discounted', lang, discounted=f'${discounted:.2f}', pct=pct)}\n"
        )
    else:
        amount_lines = f"{t('wallet_confirm_amount', lang, amount=f'{amount:.2f}')}\n"
    text = (
        f"{t('wallet_confirm_title', lang)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{amount_lines}"
        f"{t('wallet_confirm_receive', lang, coins=coins)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{t('wallet_choose_payment', lang)}"
    )
    keyboard = kb(
        [InlineKeyboardButton(text=t("wallet_btn_pay_stars", lang, stars=stars_amount), callback_data=f"pay_stars_{discounted}")],
        [InlineKeyboardButton(text=t("wallet_btn_pay_usdt", lang), callback_data=f"pay_usdt_{discounted}")],
        [back_btn("topup_start", lang=lang), menu_btn(lang)],
    )
    await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(topup_amount=discounted)

# ── USDT payment ───────────────────────────────────────────────────────────
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

# ── Auto-verify TX hash ──────────────────────────────────────────────────
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
            await _handle_referral_bonus(uid, coins)
            _used_promo = get_active_promo(uid)
            if _used_promo:
                clear_active_promo(uid)
                increment_promo_uses(_used_promo)
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
            await _send_for_manual_review(msg, tx_hash, amount, coins, uid)
            await state.clear()

    except Exception as e:
        await _send_for_manual_review(msg, tx_hash, amount, coins, uid)
        await state.clear()

async def verify_tron_tx(tx_hash: str, expected_amount: float) -> tuple[bool, float]:
    url = f"{TRON_API}?hash={tx_hash}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()

    if not data or data.get("contractRet") != "SUCCESS":
        return False, 0

    trc20_transfers = data.get("trc20TransferInfo", [])
    for transfer in trc20_transfers:
        if transfer.get("contract_address") == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
            to_address = transfer.get("to_address", "")
            amount_raw = int(transfer.get("amount_str", "0"))
            actual_usd = amount_raw / 1_000_000
            if to_address == USDT_WALLET:
                if actual_usd >= expected_amount * 0.99:
                    return True, actual_usd

    return False, 0

async def _send_for_manual_review(msg: Message, tx_hash: str, amount: float, coins: int, uid: int):
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
    await bot.session.close()
    lang = get_lang(uid)
    await msg.answer(
        f"{t('wallet_review_title', lang)}\n\n"
        f"{t('wallet_review_body', lang)}",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )

# ── Stars payment ─────────────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("pay_stars_"))
async def pay_stars(cb: CallbackQuery, state: FSMContext):
    from aiogram import Bot
    lang = get_lang(cb.from_user.id)
    amount = float(cb.data.replace("pay_stars_", ""))
    coins = math.floor(amount / COIN_TO_USD)
    stars_amount = int(amount * 100)
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_invoice(
            chat_id=cb.from_user.id,
            title=t("wallet_stars_invoice_title", lang),
            description=t("wallet_stars_invoice_desc", lang, coins=coins),
            payload=f"topup_{coins}_{cb.from_user.id}",
            currency="XTR",
            prices=[LabeledPrice(label=t("wallet_stars_label", lang, coins=coins), amount=stars_amount)],
            provider_token="",
        )
    finally:
        await bot.session.close()
    await cb.answer()

@router.message(F.successful_payment)
async def successful_stars_payment(msg: Message):
    lang = get_lang(msg.from_user.id)
    payload = msg.successful_payment.invoice_payload
    uid = msg.from_user.id

    if payload.startswith("unlimited_hour_"):
        until = set_unlimited(uid, 3600, "standard")
        until_str = datetime.datetime.fromtimestamp(until).strftime("%H:%M")
        cfg = UNLIMITED_TIER_CONFIG["standard"]
        name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
        await msg.answer(
            f"{t('unlim_activated_title', lang, name=name)}\n\n"
            f"{t('unlim_activated_body', lang, time=until_str, hours=1, cost=0)}",
            parse_mode="HTML"
        )
        return

    parts = payload.split("_")
    coins = int(parts[1])
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
    _used_promo = get_active_promo(uid)
    if _used_promo:
        clear_active_promo(uid)
        increment_promo_uses(_used_promo)
    await msg.answer(
        f"{t('wallet_stars_success_title', lang)}\n\n"
        f"{t('wallet_stars_success_body', lang, coins=coins, coins2=get_coins(uid))}",
        parse_mode="HTML"
    )

# ── Admin confirm/reject ──────────────────────────────────────────────────
@router.callback_query(F.data.startswith("confirm_topup_"))
async def admin_confirm_topup(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        await cb.answer()
        return
    _, _, uid_str, coins_str = cb.data.split("_", 3)
    uid = int(uid_str)
    coins = int(coins_str)
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
    _used_promo = get_active_promo(uid)
    if _used_promo:
        clear_active_promo(uid)
        increment_promo_uses(_used_promo)
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    try:
        user_lang = get_lang(uid)
        await bot.send_message(
            uid,
            f"{t('wallet_topup_confirmed_title', user_lang)}\n\n"
            f"{t('wallet_topup_confirmed_body', user_lang, coins=coins, balance=get_coins(uid))}",
            parse_mode="HTML"
        )
    finally:
        await bot.session.close()
    await cb.message.edit_text(f"✓  Confirmed — {coins} coins → user {uid}", parse_mode="HTML")
    await cb.answer()

@router.callback_query(F.data.startswith("reject_topup_"))
async def admin_reject_topup(cb: CallbackQuery):
    from config import ADMIN_ID
    if cb.from_user.id != ADMIN_ID:
        await cb.answer()
        return
    uid = int(cb.data.split("_")[-1])
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)
    try:
        user_lang = get_lang(uid)
        await bot.send_message(uid, t("wallet_topup_rejected", user_lang))
    finally:
        await bot.session.close()
    await cb.message.edit_text(f"✕  Rejected — user {uid}")
    await cb.answer()

async def _handle_referral_bonus(uid: int, coins_added: int):
    ref_uid = get_referred_by(uid)
    if not ref_uid:
        return

    # Atomic: returns True only the first time per referred user (race-safe)
    was_first = try_mark_ref_first_topup_done(uid)

    # Tier based on buyers count (mark first done BEFORE counting so this buyer is included)
    buyers = get_referral_buyers_count(ref_uid)
    tier = REFERRAL_TIERS[0]
    for t_item in REFERRAL_TIERS:
        if buyers >= t_item["min"]:
            tier = t_item

    percentage = tier["first"] if was_first else tier["repeat"]

    bonus = round(coins_added * percentage / 100)
    if bonus <= 0:
        return

    add_coins(ref_uid, bonus)
    try:
        ref_lang = get_lang(ref_uid)
        await _get_notify_bot().send_message(
            ref_uid,
            f"{t('wallet_referral_bonus_title', ref_lang)}\n\n"
            f"{t('wallet_referral_bonus_body', ref_lang, bonus=bonus, percentage=percentage)}",
            parse_mode="HTML"
        )
    except Exception:
        pass

# ── Referral info ───────────────────────────────────────────────────────────
@router.callback_query(F.data == "referral_info")
async def referral_info(cb: CallbackQuery):
    import urllib.parse
    uid = cb.from_user.id
    lang = get_lang(uid)

    ref_count = get_referral_count(uid)
    buyers = get_referral_buyers_count(uid)

    # Tier is based on buyers (number of referrals who made a purchase)
    tier = REFERRAL_TIERS[0]
    for t_item in REFERRAL_TIERS:
        if buyers >= t_item["min"]:
            tier = t_item

    tier_name = tier["name_ru"] if lang == "ru" else tier["name_en"]

    BAR_LEN = 10
    if tier["next"] is None:
        tier_block = t("wallet_referral_tier_max", lang, name=tier_name)
    else:
        next_idx = REFERRAL_TIERS.index(tier) + 1
        next_tier = REFERRAL_TIERS[next_idx]
        next_name = next_tier["name_ru"] if lang == "ru" else next_tier["name_en"]
        filled = min(BAR_LEN, round(buyers / tier["next"] * BAR_LEN)) if tier["next"] else BAR_LEN
        bar = "▓" * filled + "░" * (BAR_LEN - filled)
        tier_block = (
            f"  ◉  <b>{tier_name}</b>\n"
            f"  [{bar}]  {buyers} / {tier['next']} → {next_name}"
        )

    link = f"https://t.me/RetainXStudioBot?start=ref_{uid}"
    share_text = t("wallet_referral_share_text", lang) + link
    tg_share = f"https://t.me/share/url?url={urllib.parse.quote(link)}&text={urllib.parse.quote(share_text)}"

    text = (
        f"{t('wallet_referral_title', lang)}\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{tier_block}\n"
        f"{t('wallet_referral_rate', lang, first=tier['first'], repeat=tier['repeat'])}\n\n"
        f"{t('wallet_referral_stats_line', lang, count=ref_count, buyers=buyers)}\n\n"
        f"{t('wallet_referral_link_label', lang)}\n"
        f"<code>{link}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    await cb.message.edit_text(
        text,
        reply_markup=kb(
            [InlineKeyboardButton(text=t("wallet_referral_share_btn", lang), url=tg_share)],
            [back_btn("wallet", lang=lang), menu_btn(lang)],
        ),
        parse_mode="HTML"
    )
    await cb.answer()

# ── Promo code handlers ────────────────────────────────────────────────────
@router.callback_query(F.data == "promo_enter")
async def promo_enter(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    await cb.message.edit_text(
        f"{t('promo_enter_title', lang)}\n\n{t('promo_enter_desc', lang)}",
        reply_markup=kb([back_btn("wallet", lang=lang), menu_btn(lang)]),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data == "promo_cancel")
async def promo_cancel(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    clear_active_promo(uid)
    await cb.answer(t("promo_cancelled", lang))
    await show_wallet(cb)

@router.callback_query(F.data == "my_promo")
async def my_promo_page(cb: CallbackQuery):
    uid = cb.from_user.id
    lang = get_lang(uid)
    promo = get_promo_code_by_uid(uid)
    if not promo:
        await cb.message.edit_text(
            f"{t('my_promo_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n{t('my_promo_none', lang)}",
            reply_markup=kb(
                [InlineKeyboardButton(text=t("my_promo_create_btn", lang), callback_data="my_promo_create")],
                [back_btn("wallet", lang=lang), menu_btn(lang)],
            ),
            parse_mode="HTML"
        )
    else:
        await cb.message.edit_text(
            f"{t('my_promo_title', lang)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{t('my_promo_code_label', lang, code=promo['code'])}\n"
            f"{t('my_promo_discount_label', lang, pct=promo['pct'])}\n"
            f"{t('my_promo_uses_label', lang, uses=promo['uses'])}\n\n"
            f"{t('my_promo_share_hint', lang)}",
            reply_markup=kb([back_btn("wallet", lang=lang), menu_btn(lang)]),
            parse_mode="HTML"
        )
    await cb.answer()

@router.callback_query(F.data == "my_promo_create")
async def my_promo_create(cb: CallbackQuery):
    import random, string
    uid = cb.from_user.id
    if not get_is_blogger(uid):
        await cb.answer()
        return
    if get_promo_code_by_uid(uid):
        await my_promo_page(cb)
        return
    code = ""
    for _ in range(10):
        candidate = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not get_promo_code(candidate):
            code = candidate
            break
    if not code:
        await cb.answer("Error generating code, try again.", show_alert=True)
        return
    create_promo_code(uid, code)
    await my_promo_page(cb)
