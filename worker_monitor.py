import asyncio
import logging

log = logging.getLogger(__name__)

ALERT_KEY_PREFIX = "retainx:manual_alert:"
ALERT_TTL = 7200  # 2 hours — don't re-alert the same order for this long


async def check_workers_alive(redis_url: str) -> bool:
    """Returns True if at least one worker has a live heartbeat in Redis."""
    try:
        import redis.asyncio as aioredis
        r = await aioredis.from_url(redis_url, decode_responses=True)
        keys = await r.keys("worker:*:heartbeat")
        await r.aclose()
        return len(keys) > 0
    except Exception as e:
        log.error(f"[monitor] check_workers_alive error: {e}")
        return True  # assume alive on error — avoid false alerts


async def send_no_workers_alert(order_id: int, user_id: int, username: str,
                                 tool: str, params: dict, coins: int, redis_url: str) -> bool:
    """
    Send manual order alert to admin if not already sent for this order.
    Returns True if alert was sent, False if already alerted.
    """
    from config import ADMIN_ID, BOT_TOKEN
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    try:
        import redis.asyncio as aioredis
        r = await aioredis.from_url(redis_url, decode_responses=True)
        alert_key = f"{ALERT_KEY_PREFIX}{order_id}"
        already = await r.get(alert_key)
        if already:
            await r.aclose()
            return False
        await r.setex(alert_key, ALERT_TTL, "1")
        await r.aclose()
    except Exception as e:
        log.error(f"[monitor] Redis error tracking alert for #{order_id}: {e}")

    prompt = (params.get("prompt") or "—")[:300]
    if len(params.get("prompt") or "") > 300:
        prompt += "…"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅  Done", callback_data=f"delivered_{order_id}"),
        InlineKeyboardButton(text="❌  Cancel", callback_data=f"cancel_order_{order_id}"),
    ]])

    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            ADMIN_ID,
            f"🔔  <b>Manual Order Required</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  ⚠️ No workers are online.\n\n"
            f"  Order     #{order_id}\n"
            f"  User       @{username or '—'} (<code>{user_id}</code>)\n"
            f"  Tool        <b>{tool}</b>\n"
            f"  Coins     <b>{coins}◈</b>\n\n"
            f"  Prompt:\n<code>{prompt}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"  Tap <b>Done</b> after completing manually,\n"
            f"  or <b>Cancel</b> to refund the user.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        log.info(f"[monitor] Manual order alert sent for #{order_id}")
        return True
    except Exception as e:
        log.error(f"[monitor] Failed to send alert for #{order_id}: {e}")
        return False
    finally:
        await bot.session.close()


async def stale_order_monitor(bot, redis_url: str):
    """
    Background task: every 5 minutes, check for stale processing orders.
    If no workers are alive, alert admin for each un-alerted stale order.
    """
    await asyncio.sleep(60)  # initial delay — let bot settle on startup
    while True:
        try:
            workers_alive = await check_workers_alive(redis_url)
            if not workers_alive:
                from database import get_stale_orders
                stale = get_stale_orders(min_age_seconds=900)  # 15 minutes
                for order in stale:
                    params = order.get("params") or {}
                    await send_no_workers_alert(
                        order_id=order["id"],
                        user_id=order["user_id"],
                        username=order.get("username") or "",
                        tool=order.get("tool") or "—",
                        params=params,
                        coins=order.get("coins") or 0,
                        redis_url=redis_url,
                    )
        except Exception as e:
            log.error(f"[monitor] stale_order_monitor error: {e}")
        await asyncio.sleep(300)  # every 5 minutes
