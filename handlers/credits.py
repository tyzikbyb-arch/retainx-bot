import math
import time
import datetime
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import COIN_TO_USD, MIN_TOPUP_USD, USDT_WALLET, REFERRAL_PERCENT, BOT_TOKEN, UNLIMITED_TIER_CONFIG, UNLIMITED_PLANS
from database import get_coins, add_coins, spend_coins, get_referred_by, get_lang, has_unlimited, get_unlimited_until, get_unlimited_tier, set_unlimited, can_buy_unlimited
from keyboards import kb, back_btn, menu_btn
from i18n import t

router = Router()

TRON_API = "https://apilist.tronscanapi.com/api/transaction-info"

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
        unlim_line = f"\n{tier_cfg['emoji']} <b>Безлимит {tier_name} активен</b> — ещё {mins}м {secs}с\n"

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
        buttons.append([InlineKeyboardButton(text="⚡  Безлимит — купить пакет", callback_data="unlimited_buy")])
        buttons.append([InlineKeyboardButton(text="ℹ  О безлимитных пакетах",   callback_data="unlim_info")])
    else:
        tier = get_unlimited_tier(uid) or "standard"
        tier_cfg = UNLIMITED_TIER_CONFIG.get(tier, UNLIMITED_TIER_CONFIG["standard"])
        tier_name = tier_cfg["name_ru"] if lang == "ru" else tier_cfg["name_en"]
        buttons.append([InlineKeyboardButton(text=f"⚡  Безлимит {tier_name} активен ✓", callback_data="unlimited_status")])
    buttons.append([InlineKeyboardButton(text=t("wallet_btn_referral", lang), callback_data="referral_info")])
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
    await cb.answer("⚡ Безлимит активен!", show_alert=False)

# ── Unlimited pass purchase — tiered coin flow ────────────────────────
_TIER_ORDER = ["standard", "pro", "vip"]

def _tier_info_text(tier: str) -> str:
    if tier == "standard":
        return (
            "  ✓  Seedance 2.0 Fast · Wan 2.7 · Grok 1.5\n"
            "  ✓  LTX 2.3 Pro · Veo 3.1 Lite\n"
            "  ✓  Kling 3.0 · Kling O3\n"
            "  ✕  Premium видео (Veo 3.1 Full, Sora 2)\n"
            "  ✕  Аудио / войсовер\n"
            "  ✕  Аватары\n"
            "  ⬆  Разрешение до 720p"
        )
    elif tier == "pro":
        return (
            "  ✓  Всё из Стандарт (до 1080p)\n"
            "  ✓  Premium: Veo 3.1 · Veo 3.1 Fast · Sora 2\n"
            "  ✓  Аудио / войсовер\n"
            "  ✕  Аватары\n"
            "  ⬆  Разрешение до 1080p"
        )
    else:  # vip
        return (
            "  ✓  Всё из Про\n"
            "  ✓  Разрешение до 4K\n"
            "  ✕  Аватары"
        )

@router.callback_query(F.data == "unlimited_buy")
async def unlimited_buy(cb: CallbackQuery, state: FSMContext):
    lang = get_lang(cb.from_user.id)
    coins = get_coins(cb.from_user.id)
    rows = []
    for tier in _TIER_ORDER:
        cfg = UNLIMITED_TIER_CONFIG[tier]
        price_1h = UNLIMITED_PLANS[tier][1]
        name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
        rows.append([InlineKeyboardButton(
            text=f"{cfg['emoji']}  {name}  —  от {price_1h}◈",
            callback_data=f"ulim_t_{tier}"
        )])
    rows.append([InlineKeyboardButton(text="ℹ  Подробнее о пакетах", callback_data="unlim_info")])
    rows.append([back_btn("wallet", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        "⚡  <b>Безлимитные пакеты</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Ваш баланс:  <b>{coins}◈</b>\n\n"
        "  Выберите тариф:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("ulim_t_"))
async def unlim_tier_selected(cb: CallbackQuery, state: FSMContext):
    tier = cb.data[7:]
    if tier not in UNLIMITED_TIER_CONFIG:
        await cb.answer()
        return
    lang = get_lang(cb.from_user.id)
    cfg = UNLIMITED_TIER_CONFIG[tier]
    name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
    plans = UNLIMITED_PLANS[tier]
    info = _tier_info_text(tier)

    rows = [
        [InlineKeyboardButton(text=f"1 час  —  {plans[1]}◈", callback_data=f"ulim_d_{tier}_1")],
        [InlineKeyboardButton(text=f"2 часа  —  {plans[2]}◈  (−10%/ч)", callback_data=f"ulim_d_{tier}_2")],
        [InlineKeyboardButton(text=f"3 часа  —  {plans[3]}◈  (−20%/ч)", callback_data=f"ulim_d_{tier}_3")],
        [back_btn("unlimited_buy", lang=lang), menu_btn(lang)],
    ]
    await cb.message.edit_text(
        f"⚡  <b>Безлимит {name}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{info}\n\n"
        "  Выберите длительность:",
        reply_markup=kb(*rows),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("ulim_d_"))
async def unlim_duration_selected(cb: CallbackQuery, state: FSMContext):
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
        await cb.answer(f"Недостаточно монет. Нужно {coins_cost}◈, у вас {user_coins}◈.", show_alert=True)
        return

    hour_word = {1: "час", 2: "часа", 3: "часа"}.get(hours, "ч")
    await cb.message.edit_text(
        f"⚡  <b>Подтверждение покупки</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Тариф:          <b>{name}</b>\n"
        f"  Длительность:  <b>{hours} {hour_word}</b>\n"
        f"  Стоимость:     <b>{coins_cost}◈</b>\n"
        f"  Ваш баланс:   <b>{user_coins}◈</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━",
        reply_markup=kb(
            [InlineKeyboardButton(
                text=f"✓  Активировать — {coins_cost}◈",
                callback_data=f"ulim_c_{tier}_{hours}"
            )],
            [back_btn(f"ulim_t_{tier}", lang=lang), menu_btn(lang)],
        ),
        parse_mode="HTML"
    )
    await cb.answer()

@router.callback_query(F.data.startswith("ulim_c_"))
async def unlim_confirm(cb: CallbackQuery, state: FSMContext):
    parts = cb.data[7:].split("_")
    if len(parts) != 2:
        await cb.answer()
        return
    tier, hours_str = parts[0], parts[1]
    hours = int(hours_str)
    uid = cb.from_user.id
    lang = get_lang(uid)

    if tier not in UNLIMITED_TIER_CONFIG or hours not in UNLIMITED_PLANS.get(tier, {}):
        await cb.answer("Ошибка. Попробуйте снова.", show_alert=True)
        return

    coins_cost = UNLIMITED_PLANS[tier][hours]
    if not spend_coins(uid, coins_cost):
        await cb.answer("Недостаточно монет. Пополните баланс.", show_alert=True)
        return

    duration_secs = hours * 3600
    until = set_unlimited(uid, duration_secs, tier)
    until_str = datetime.datetime.fromtimestamp(until).strftime("%H:%M")
    cfg = UNLIMITED_TIER_CONFIG[tier]
    name = cfg["name_ru"] if lang == "ru" else cfg["name_en"]
    hour_word = {1: "час", 2: "часа", 3: "часа"}.get(hours, "ч")

    await cb.message.edit_text(
        f"⚡  <b>Безлимит {name} активирован!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  Действует до  <b>{until_str}</b>  ({hours} {hour_word})\n"
        "  Генерируйте сколько угодно!\n\n"
        f"  Списано:  <b>{coins_cost}◈</b>",
        reply_markup=kb([menu_btn(lang)]),
        parse_mode="HTML"
    )
    await cb.answer()

# ── Unlimited info section ───────────────────────────────────────────────
def _build_tier_page(tier: str) -> str:
    p = UNLIMITED_PLANS[tier]
    if tier == "standard":
        return (
            "⚡  <b>Безлимит Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Генерируйте видео и изображения без\n"
            "  ограничений — монеты не списываются.\n\n"
            "<b>📹 Видео — Standard:</b>\n"
            "  • Seedance 2.0 Fast\n"
            "  • Wan 2.7\n"
            "  • LTX 2.3 Pro\n"
            "  • Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5  <i>(макс. 480p)</i>\n\n"
            "<b>🎬 Видео — Kling:</b>\n"
            "  • Kling 3.0\n"
            "  • Kling O3\n\n"
            "  ✕  Premium видео (Veo 3.1, Sora 2)\n"
            "  ✕  Аудио и голос\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 720p\n\n"
            "<b>💰 Стоимость:</b>\n"
            f"  1 час   →  <b>{p[1]}◈</b>\n"
            f"  2 часа  →  <b>{p[2]}◈</b>  <i>(−10% за час)</i>\n"
            f"  3 часа  →  <b>{p[3]}◈</b>  <i>(−20% за час)</i>"
        )
    elif tier == "pro":
        return (
            "⚡⚡  <b>Безлимит Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Всё из Standard плюс Premium-модели\n"
            "  и аудио — в качестве до 1080p.\n\n"
            "<b>📹 Видео — Standard (до 1080p):</b>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • LTX 2.3 Pro · Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5\n\n"
            "<b>🎬 Видео — Kling (до 1080p):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium видео (до 1080p):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Аудио и голос:</b>\n"
            "  • ElevenLabs · Artlist и др.\n\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 1080p\n\n"
            "<b>💰 Стоимость:</b>\n"
            f"  1 час   →  <b>{p[1]}◈</b>\n"
            f"  2 часа  →  <b>{p[2]}◈</b>  <i>(−10% за час)</i>\n"
            f"  3 часа  →  <b>{p[3]}◈</b>  <i>(−20% за час)</i>"
        )
    else:  # vip
        return (
            "♛  <b>Безлимит VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Максимальный пакет — всё из Pro\n"
            "  с разрешением до 4K.\n\n"
            "  ✓  Все модели из Pro\n\n"
            "<b>📹 Standard-видео (до 4K):</b>\n"
            "  • LTX 2.3 Pro  <i>(720p / 1080p / 2K / 4K)</i>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • Veo 3.1 Lite · Grok Imagine 1.5\n\n"
            "<b>🎬 Kling (до 4K):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium видео (до 4K):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Аудио и голос</b>\n\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 4K\n\n"
            "<b>💰 Стоимость:</b>\n"
            f"  1 час   →  <b>{p[1]}◈</b>\n"
            f"  2 часа  →  <b>{p[2]}◈</b>  <i>(−10% за час)</i>\n"
            f"  3 часа  →  <b>{p[3]}◈</b>  <i>(−20% за час)</i>"
        )

@router.callback_query(F.data == "unlim_info")
async def unlim_info(cb: CallbackQuery):
    lang = get_lang(cb.from_user.id)
    rows = [
        [InlineKeyboardButton(text="⚡  Standard  —  от 268◈",   callback_data="ulim_info_standard")],
        [InlineKeyboardButton(text="⚡⚡  Pro  —  от 662◈",      callback_data="ulim_info_pro")],
        [InlineKeyboardButton(text="♛  VIP  —  от 1 619◈",      callback_data="ulim_info_vip")],
        [back_btn("unlimited_buy", lang=lang), menu_btn(lang)],
    ]
    await cb.message.edit_text(
        "⚡  <b>Безлимитные пакеты</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "  Генерируйте неограниченно в течение\n"
        "  1, 2 или 3 часов — без списания монет\n"
        "  за каждый запрос.\n\n"
        "  Выберите пакет чтобы узнать подробнее:",
        reply_markup=kb(*rows),
        parse_mode="HTML",
    )
    await cb.answer()

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
    rows.append([InlineKeyboardButton(text=f"🛒  Купить {_label[tier]}", callback_data=f"ulim_t_{tier}")])
    rows.append([back_btn("unlim_info", lang=lang), menu_btn(lang)])
    await cb.message.edit_text(
        _build_tier_page(tier),
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
    uid = msg.from_user.id

    if payload.startswith("unlimited_hour_"):
        until = set_unlimited(uid, 3600, "standard")
        until_str = datetime.datetime.fromtimestamp(until).strftime("%H:%M")
        await msg.answer(
            "⚡  <b>Безлимит активирован!</b>\n\n"
            f"  Действует до  <b>{until_str}</b>  (1 час)\n"
            "  Генерируйте сколько угодно!",
            parse_mode="HTML"
        )
        return

    parts = payload.split("_")
    coins = int(parts[1])
    add_coins(uid, coins)
    await _handle_referral_bonus(uid, coins)
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
                f"{t('wallet_referral_bonus_body', ref_lang, bonus=bonus, percentage=REFERRAL_PERCENT)}",
                parse_mode="HTML"
            )

# ── Referral info ───────────────────────────────────────────────────────────
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
