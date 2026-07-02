"""
Background braille-spinner for order-placed messages.

After an order is placed, start() edits the confirmation message every
~0.9 s cycling through FRAMES so the user sees live activity. The task
stops automatically when:
  - stop(oid) is called (admin delivery path)
  - the order status in DB changes to delivered/cancelled (worker path)
  - max_sec elapses (safety fallback)
"""

import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

from config import BOT_TOKEN

log = logging.getLogger(__name__)

FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# oid -> (asyncio.Task, base_text, chat_id, message_id)
_active: dict[int, tuple] = {}

# ---------- wait-time estimates per tool name (keyword, minutes) ----------
_WAIT_RULES: list[tuple[str, int]] = [
    ("sora",              10),
    ("heygen avatar",     10),
    ("aurora avatar",      8),
    ("heygen translate",   6),
    ("heygen",             8),
    ("ltx",                5),
    ("wan",                5),
    ("seedance",           5),
    ("minimax",            5),
    ("kling",              6),
    ("grok",               3),
    # voiceover models
    ("eleven",             2),
    ("cartesia",           2),
]

def wait_minutes(tool: str, order_type: str = "video") -> int:
    tl = tool.lower()
    for kw, mins in _WAIT_RULES:
        if kw in tl:
            return mins
    return 2 if order_type in ("voiceover", "image") else 5


# ---------- internal runner ----------

async def _run(oid: int, chat_id: int, message_id: int, base_text: str, max_sec: int):
    from database import get_order  # local import to avoid circular deps at module load
    bot = Bot(token=BOT_TOKEN)
    idx = 0
    elapsed = 0.0
    interval = 0.9
    poll_every = 60  # seconds between DB status checks
    try:
        while elapsed < max_sec:
            frame = FRAMES[idx % len(FRAMES)]
            try:
                await bot.edit_message_text(
                    f"{base_text}  {frame}",
                    chat_id=chat_id,
                    message_id=message_id,
                    parse_mode="HTML",
                )
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                continue
            except TelegramBadRequest as e:
                if "message is not modified" not in str(e):
                    log.debug("[SPINNER] #%s TelegramBadRequest: %s", oid, e)
            except Exception as e:
                log.debug("[SPINNER] #%s error: %s", oid, e)

            idx += 1
            await asyncio.sleep(interval)
            elapsed += interval

            # Periodically check DB so we stop when worker auto-delivers
            if int(elapsed) % poll_every < interval:
                try:
                    order = await asyncio.to_thread(get_order, oid)
                    if order and order.get("status") in ("delivered", "cancelled"):
                        break
                except Exception:
                    pass
    except asyncio.CancelledError:
        pass
    finally:
        _active.pop(oid, None)
        try:
            await bot.session.close()
        except Exception:
            pass


# ---------- public API ----------

def start(oid: int, chat_id: int, message_id: int, base_text: str, minutes: int):
    """Start the spinner for order *oid*. Stops after 2× estimated minutes."""
    max_sec = minutes * 60 * 2 + 120
    task = asyncio.create_task(_run(oid, chat_id, message_id, base_text, max_sec))
    _active[oid] = (task, base_text, chat_id, message_id)
    log.debug("[SPINNER] started for order #%s (%s min est.)", oid, minutes)


async def stop(oid: int):
    """Cancel the spinner and reset the message to a clean static state."""
    entry = _active.pop(oid, None)
    if not entry:
        return
    task, base_text, chat_id, message_id = entry
    task.cancel()
    try:
        await asyncio.wait_for(asyncio.shield(task), timeout=1.5)
    except Exception:
        pass
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.edit_message_text(
            base_text, chat_id=chat_id, message_id=message_id, parse_mode="HTML"
        )
        await bot.session.close()
    except Exception:
        pass
