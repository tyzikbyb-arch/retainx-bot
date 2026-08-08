import os
import time
import logging
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

log = logging.getLogger(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:EIZkqhsYzRUQVftlgMDiBeZlBcALiNbA@postgres.railway.internal:5432/railway"
)

@contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid BIGINT PRIMARY KEY,
                    coins INTEGER DEFAULT 0,
                    referred_by BIGINT DEFAULT NULL,
                    joined INTEGER DEFAULT 0,
                    lang TEXT DEFAULT 'en'
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    username TEXT,
                    tool TEXT,
                    params JSONB,
                    coins INTEGER,
                    price_usd REAL,
                    status TEXT DEFAULT 'processing',
                    created INTEGER,
                    file_id TEXT DEFAULT NULL,
                    file_type TEXT DEFAULT NULL
                )
            """)
            # Add columns if they don't exist (for existing tables)
            try:
                cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS file_id TEXT DEFAULT NULL")
                cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS file_type TEXT DEFAULT NULL")
            except Exception as e:
                log.warning(f"DB migration (orders file cols): {e}")
            # Fix missing SERIAL sequence on orders.id (table may have been created without one)
            try:
                cur.execute("CREATE SEQUENCE IF NOT EXISTS orders_id_seq")
                cur.execute("SELECT setval('orders_id_seq', GREATEST(COALESCE((SELECT MAX(id) FROM orders), 0), 1))")
                cur.execute("ALTER TABLE orders ALTER COLUMN id SET DEFAULT nextval('orders_id_seq')")
            except Exception as e:
                log.warning(f"DB migration (orders_id_seq): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS lang TEXT DEFAULT 'en'")
            except Exception as e:
                log.warning(f"DB migration (users.lang): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS unlimited_until INTEGER DEFAULT NULL")
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS can_buy_unlimited INTEGER DEFAULT 0")
            except Exception as e:
                log.warning(f"DB migration (users.unlimited): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_blogger INTEGER DEFAULT 0")
            except Exception as e:
                log.warning(f"DB migration (users.is_blogger): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS unlimited_tier TEXT DEFAULT NULL")
            except Exception as e:
                log.warning(f"DB migration (users.unlimited_tier): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS ref_first_done BOOLEAN DEFAULT FALSE")
            except Exception as e:
                log.warning(f"DB migration (users.ref_first_done): {e}")
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS active_promo TEXT DEFAULT NULL")
            except Exception as e:
                log.warning(f"DB migration (users.active_promo): {e}")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS promo_codes (
                    code TEXT PRIMARY KEY,
                    uid BIGINT NOT NULL,
                    pct INTEGER DEFAULT 30,
                    uses INTEGER DEFAULT 0,
                    created INTEGER
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS artlist_accounts (
                    id SERIAL PRIMARY KEY,
                    label TEXT,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    cookies_json TEXT,
                    status TEXT DEFAULT 'active',
                    assigned_worker TEXT,
                    last_used INTEGER,
                    last_error TEXT,
                    exhausted_at INTEGER,
                    created INTEGER
                )
            """)
        conn.commit()

# ── User functions ────────────────────────────────────────────
def get_user(uid: int) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            if row:
                return dict(row)
            cur.execute(
                "INSERT INTO users (uid, coins, joined) VALUES (%s, 0, %s) RETURNING *",
                (uid, int(time.time()))
            )
            conn.commit()
            return dict(cur.fetchone())

def is_new_user(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE uid = %s", (uid,))
            return cur.fetchone() is None

def get_coins(uid: int) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT coins FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row else 0

def add_coins(uid: int, amount: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, joined)
                VALUES (%s, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET coins = users.coins + %s
            """, (uid, amount, int(time.time()), amount))
        conn.commit()

def spend_coins(uid: int, amount: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET coins = coins - %s WHERE uid = %s AND coins >= %s RETURNING uid",
                (amount, uid, amount)
            )
            updated = cur.fetchone() is not None
        conn.commit()
        return updated

def set_referred_by(uid: int, ref_uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, referred_by, joined)
                VALUES (%s, 0, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET referred_by = EXCLUDED.referred_by
                WHERE users.referred_by IS NULL
            """, (uid, ref_uid, int(time.time())))
        conn.commit()

def get_referred_by(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT referred_by FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row else None

def get_referral_count(uid: int) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE referred_by = %s", (uid,))
            return cur.fetchone()[0]

def get_referral_buyers_count(uid: int) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE referred_by = %s AND ref_first_done = TRUE", (uid,))
            return cur.fetchone()[0]

def is_ref_first_topup_done(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ref_first_done FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return bool(row[0]) if row else False

def mark_ref_first_topup_done(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET ref_first_done = TRUE WHERE uid = %s", (uid,))
        conn.commit()

def try_mark_ref_first_topup_done(uid: int) -> bool:
    """Atomically mark first topup done. Returns True only the first time (race-safe)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET ref_first_done = TRUE WHERE uid = %s AND ref_first_done = FALSE RETURNING uid",
                (uid,)
            )
            was_first = cur.fetchone() is not None
        conn.commit()
        return was_first

def get_lang(uid: int) -> str:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT lang FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "en"

def set_lang(uid: int, lang: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, lang, joined)
                VALUES (%s, 0, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET lang = %s
            """, (uid, lang, int(time.time()), lang))
        conn.commit()

# ── Unlimited pass functions ──────────────────────────────────
def has_unlimited(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT unlimited_until FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            if not row or row[0] is None:
                return False
            return row[0] > int(time.time())

def get_unlimited_until(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT unlimited_until FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row else None

def set_unlimited(uid: int, duration_seconds: int = 3600, tier: str = None) -> int:
    until = int(time.time()) + duration_seconds
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, joined, unlimited_until, unlimited_tier)
                VALUES (%s, 0, %s, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET unlimited_until = %s, unlimited_tier = %s
            """, (uid, int(time.time()), until, tier, until, tier))
        conn.commit()
    return until

def get_unlimited_tier(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT unlimited_tier FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row else None

def can_buy_unlimited(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT can_buy_unlimited FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return bool(row and row[0])

def set_can_buy_unlimited(uid: int, val: bool):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, joined, can_buy_unlimited)
                VALUES (%s, 0, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET can_buy_unlimited = %s
            """, (uid, int(time.time()), int(val), int(val)))
        conn.commit()

# ── Order functions ───────────────────────────────────────────
def create_order(user_id, username, tool, params, coins, price_usd) -> int:
    import json
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders (user_id, username, tool, params, coins, price_usd, status, created)
                VALUES (%s, %s, %s, %s, %s, %s, 'processing', %s)
                RETURNING id
            """, (user_id, username, tool, json.dumps(params), coins, price_usd, int(time.time())))
            oid = cur.fetchone()[0]
        conn.commit()
        return oid

def get_order(oid: int) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM orders WHERE id = %s", (oid,))
            row = cur.fetchone()
            if not row:
                return None
            d = dict(row)
            if isinstance(d.get("params"), str):
                import json
                d["params"] = json.loads(d["params"])
            return d

def update_order_status(oid: int, status: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE orders SET status = %s WHERE id = %s", (status, oid))
        conn.commit()

def cancel_order_atomic(oid: int) -> tuple:
    """Cancel order and refund coins in a single transaction. Returns (success, user_id, coins)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE orders SET status = 'cancelled' WHERE id = %s AND status = 'processing' RETURNING user_id, coins",
                (oid,)
            )
            row = cur.fetchone()
            if not row:
                return False, None, None
            user_id, coins = row[0], row[1]
            cur.execute("UPDATE users SET coins = coins + %s WHERE uid = %s", (coins, user_id))
        conn.commit()
        return True, user_id, coins

def get_all_users() -> list:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.uid, u.coins, u.joined,
                       COUNT(o.id) as order_count
                FROM users u
                LEFT JOIN orders o ON o.user_id = u.uid
                GROUP BY u.uid, u.coins, u.joined
                ORDER BY u.joined DESC
            """)
            return [dict(r) for r in cur.fetchall()]

def get_stats() -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            total_users = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM orders")
            total_orders = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'delivered'")
            delivered = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'cancelled'")
            cancelled = cur.fetchone()[0]
            cur.execute("SELECT COALESCE(SUM(coins), 0) FROM orders WHERE status = 'delivered'")
            coins_spent = cur.fetchone()[0]
            cur.execute("SELECT COALESCE(SUM(price_usd), 0) FROM orders WHERE status = 'delivered'")
            revenue = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM users WHERE joined > extract(epoch from now() - interval '24 hours')")
            new_today = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM users WHERE joined > extract(epoch from now() - interval '7 days')")
            new_week = cur.fetchone()[0]
        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "delivered": delivered,
            "cancelled": cancelled,
            "coins_spent": int(coins_spent),
            "revenue": round(float(revenue), 2),
            "new_today": new_today,
            "new_week": new_week,
        }

def _load_orders_all() -> list:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM orders ORDER BY created DESC LIMIT 50")
            rows = cur.fetchall()
            result = []
            for row in rows:
                d = dict(row)
                if isinstance(d.get("params"), str):
                    import json
                    d["params"] = json.loads(d["params"])
                result.append(d)
            return result

def save_delivery(oid: int, file_id: str, file_type: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE orders SET status = 'delivered', file_id = %s, file_type = %s WHERE id = %s",
                (file_id, file_type, oid)
            )
        conn.commit()

def get_user_orders(uid: int) -> list:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM orders WHERE user_id = %s ORDER BY created DESC LIMIT 50",
                (uid,)
            )
            rows = cur.fetchall()
            result = []
            for row in rows:
                d = dict(row)
                if isinstance(d.get("params"), str):
                    import json
                    d["params"] = json.loads(d["params"])
                result.append(d)
            return result

# ── Artlist account pool ─────────────────────────────────────
def add_artlist_account(email: str, password: str, label: str = None) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO artlist_accounts (label, email, password, status, created)
                VALUES (%s, %s, %s, 'active', %s)
                RETURNING id
            """, (label, email, password, int(time.time())))
            aid = cur.fetchone()[0]
        conn.commit()
        return aid

def list_artlist_accounts() -> list:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM artlist_accounts ORDER BY id ASC")
            return [dict(r) for r in cur.fetchall()]

def get_artlist_account(account_id: int) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM artlist_accounts WHERE id = %s", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None

def set_artlist_account_status(account_id: int, status: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            if status == "active":
                cur.execute(
                    "UPDATE artlist_accounts SET status = %s, exhausted_at = NULL, last_error = NULL, assigned_worker = NULL WHERE id = %s",
                    (status, account_id)
                )
            else:
                cur.execute("UPDATE artlist_accounts SET status = %s WHERE id = %s", (status, account_id))
        conn.commit()

def remove_artlist_account(account_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM artlist_accounts WHERE id = %s", (account_id,))
        conn.commit()

def get_is_blogger(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT is_blogger FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return bool(row and row[0])

def set_blogger(uid: int, val: bool):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, joined, is_blogger)
                VALUES (%s, 0, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET is_blogger = %s
            """, (uid, int(time.time()), val, val))
        conn.commit()

# ── Promo code functions ──────────────────────────────────────
def create_promo_code(uid: int, code: str, pct: int = 30):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO promo_codes (code, uid, pct, uses, created) VALUES (%s, %s, %s, 0, %s) ON CONFLICT (code) DO NOTHING",
                (code, uid, pct, int(time.time()))
            )
        conn.commit()

def get_promo_code(code: str):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM promo_codes WHERE code = %s", (code,))
            row = cur.fetchone()
            return dict(row) if row else None

def get_promo_code_by_uid(uid: int):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM promo_codes WHERE uid = %s LIMIT 1", (uid,))
            row = cur.fetchone()
            return dict(row) if row else None

def increment_promo_uses(code: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE promo_codes SET uses = uses + 1 WHERE code = %s", (code,))
        conn.commit()

def get_active_promo(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT active_promo FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return row[0] if row else None

def set_active_promo(uid: int, code: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET active_promo = %s WHERE uid = %s", (code, uid))
        conn.commit()

def clear_active_promo(uid: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET active_promo = NULL WHERE uid = %s", (uid,))
        conn.commit()

# Initialize on import
try:
    init_db()
except Exception as e:
    print(f"DB init error: {e}")
