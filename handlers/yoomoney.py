import asyncio
import hashlib
import logging
import math

from aiohttp import web

from config import YOOMONEY_SECRET, COIN_TO_RUB, BOT_TOKEN, ADMIN_ID
from database import add_coins, get_lang, record_yoomoney_payment

log = logging.getLogger(__name__)


def _verify_signature(data: dict) -> bool:
    fields = [
        data.get("notification_type", ""),
        data.get("operation_id", ""),
        data.get("amount", ""),
        data.get("currency", ""),
        data.get("datetime", ""),
        data.get("sender", ""),
        data.get("codepro", ""),
        YOOMONEY_SECRET,
        data.get("label", ""),
    ]
    expected = hashlib.sha1("&".join(fields).encode("utf-8")).hexdigest()
    return expected == data.get("sha1_hash", "")


async def yoomoney_webhook(request: web.Request) -> web.Response:
    try:
        data = dict(await request.post())
        log.info(f"YooMoney webhook received: type={data.get('notification_type')} "
                 f"op={data.get('operation_id')} amount={data.get('amount')} label={data.get('label')}")

        secret_set = bool(YOOMONEY_SECRET)
        if not secret_set:
            log.error("YooMoney: YOOMONEY_SECRET is not set — cannot verify signature, rejecting")
            return web.Response(status=500, text="secret not configured")

        if not _verify_signature(data):
            log.warning(f"YooMoney: invalid signature (check YOOMONEY_SECRET matches YooMoney account settings). "
                        f"notification_type={data.get('notification_type')} op={data.get('operation_id')}")
            return web.Response(status=400, text="bad signature")

        if data.get("notification_type") != "p2p-incoming":
            log.info(f"YooMoney: ignoring notification_type={data.get('notification_type')!r}")
            return web.Response(text="ok")

        label = data.get("label", "").strip()
        if not label or not label.isdigit():
            log.warning(f"YooMoney: missing/invalid label={label!r} — payment cannot be linked to a user")
            return web.Response(text="ok")

        operation_id = data.get("operation_id", "")
        user_id = int(label)
        # withdraw_amount = what the sender actually paid (before YooMoney fee)
        # amount = what we received (after fee deducted by YooMoney)
        # We calculate coins from withdraw_amount so the user gets exactly what
        # they paid for, not less due to commission. Fall back to amount if absent.
        withdraw_amount = data.get("withdraw_amount", "")
        amount_received = float(data.get("amount", "0"))
        amount_rub = float(withdraw_amount) if withdraw_amount else amount_received
        coins = math.floor(amount_rub / COIN_TO_RUB)
        log.info(f"YooMoney: withdraw_amount={withdraw_amount!r} amount={amount_received} "
                 f"→ using {amount_rub} RUB → {coins} coins for user {user_id}")

        if coins <= 0:
            log.warning(f"YooMoney: zero coins for {amount_rub} RUB (COIN_TO_RUB={COIN_TO_RUB})")
            return web.Response(text="ok")

        try:
            is_new = record_yoomoney_payment(operation_id, user_id, amount_rub, coins)
        except Exception as db_err:
            log.error(f"YooMoney: DB error recording payment op={operation_id}: {db_err}")
            return web.Response(status=500, text="db error")

        if not is_new:
            log.info(f"YooMoney: duplicate operation_id={operation_id}, skipping")
            return web.Response(text="ok")

        add_coins(user_id, coins)

        try:
            from handlers.credits import _handle_referral_bonus
            asyncio.create_task(_handle_referral_bonus(user_id, coins, payment_type="yoomoney"))
        except Exception as e:
            log.warning(f"Referral bonus failed: {e}")

        import aiohttp as _http
        user_lang = get_lang(user_id)
        from i18n import t
        async with _http.ClientSession() as session:
            try:
                await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": user_id,
                        "text": (
                            f"{t('wallet_yoomoney_success_title', user_lang)}\n\n"
                            f"{t('wallet_yoomoney_success_body', user_lang, amount=f'{amount_rub:.2f}', coins=coins)}"
                        ),
                        "parse_mode": "HTML",
                    },
                )
            except Exception as e:
                log.error(f"Failed to notify user {user_id}: {e}")
            try:
                await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_ID,
                        "text": (
                            f"✓  YooMoney payment\n"
                            f"User: {user_id}\n"
                            f"{amount_rub} ₽  →  {coins} coins\n"
                            f"Op: {operation_id}"
                        ),
                    },
                )
            except Exception:
                pass

        return web.Response(text="ok")

    except Exception as e:
        log.error(f"YooMoney webhook error: {e}")
        return web.Response(status=500, text="error")
