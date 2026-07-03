import os
import random
import time
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:EIZkqhsYzRUQVftlgMDiBeZlBcALiNbA@postgres.railway.internal:5432/railway"
)

def get_conn():
    return psycopg2.connect(DATABASE_URL)

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
            except Exception:
                pass
            # Migrate orders.id from SERIAL (auto-increment) to BIGINT (random IDs)
            try:
                cur.execute("ALTER TABLE orders ALTER COLUMN id DROP DEFAULT")
                cur.execute("ALTER TABLE orders ALTER COLUMN id TYPE BIGINT USING id::BIGINT")
                cur.execute("DROP SEQUENCE IF EXISTS orders_id_seq")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS lang TEXT DEFAULT 'en'")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS referral_balance REAL DEFAULT 0")
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS topup_count INTEGER DEFAULT 0")
            except Exception:
                pass
            cur.execute("""
                CREATE TABLE IF NOT EXISTS referral_earnings (
                    id SERIAL PRIMARY KEY,
                    referrer_id BIGINT NOT NULL,
                    from_user_id BIGINT NOT NULL,
                    amount_rub REAL NOT NULL,
                    percentage INTEGER NOT NULL,
                    payment_type TEXT NOT NULL,
                    created INTEGER NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS withdrawal_requests (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    amount_rub REAL NOT NULL,
                    requisites TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created INTEGER NOT NULL,
                    processed INTEGER DEFAULT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS yoomoney_payments (
                    operation_id TEXT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    amount_rub REAL NOT NULL,
                    coins INTEGER NOT NULL,
                    created INTEGER NOT NULL
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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS promo_codes (
                    code TEXT PRIMARY KEY,
                    owner_uid BIGINT NOT NULL,
                    discount_pct INTEGER NOT NULL DEFAULT 30,
                    uses_count INTEGER NOT NULL DEFAULT 0,
                    created INTEGER NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS promo_uses (
                    id SERIAL PRIMARY KEY,
                    code TEXT NOT NULL,
                    user_uid BIGINT NOT NULL UNIQUE,
                    created INTEGER NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pending_yoomoney_promos (
                    user_id BIGINT PRIMARY KEY,
                    expected_coins INTEGER NOT NULL,
                    promo_code TEXT NOT NULL,
                    created INTEGER NOT NULL,
                    expected_payment_rub REAL NOT NULL DEFAULT 0
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usdt_payments (
                    tx_hash TEXT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    amount_usd REAL NOT NULL,
                    coins INTEGER NOT NULL,
                    created INTEGER NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stars_payments (
                    charge_id TEXT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    coins INTEGER NOT NULL,
                    created INTEGER NOT NULL
                )
            """)
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_blogger BOOLEAN DEFAULT FALSE")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE pending_yoomoney_promos ADD COLUMN IF NOT EXISTS expected_payment_rub REAL NOT NULL DEFAULT 0")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS username TEXT DEFAULT NULL")
            except Exception:
                pass
        conn.commit()

# ── User functions ────────────────────────────────────────────
def get_user(uid: int) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO users (uid, coins, joined) VALUES (%s, 0, %s) ON CONFLICT (uid) DO NOTHING",
                (uid, int(time.time()))
            )
            conn.commit()
            cur.execute("SELECT * FROM users WHERE uid = %s", (uid,))
            return dict(cur.fetchone())

def update_username(uid: int, username: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET username = %s WHERE uid = %s", (username, uid))
        conn.commit()

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
                "UPDATE users SET coins = coins - %s WHERE uid = %s AND coins >= %s",
                (amount, uid, amount)
            )
            success = cur.rowcount == 1
        conn.commit()
        return success

def remove_coins(uid: int, amount: int) -> int:
    """Deduct up to `amount` coins from user, clamped at 0. Returns actual amount deducted."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            # FOR UPDATE locks the row so concurrent calls can't both pass the guard
            cur.execute("SELECT coins FROM users WHERE uid = %s FOR UPDATE", (uid,))
            row = cur.fetchone()
            if not row:
                return 0
            actual = min(amount, row[0])
            if actual > 0:
                cur.execute("UPDATE users SET coins = coins - %s WHERE uid = %s", (actual, uid))
        conn.commit()
        return actual

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

# ── Order functions ───────────────────────────────────────────
def _gen_order_id(cur) -> int:
    for _ in range(20):
        oid = random.randint(1000, 9_999_999)
        cur.execute("SELECT 1 FROM orders WHERE id = %s", (oid,))
        if not cur.fetchone():
            return oid
    raise RuntimeError("Failed to generate unique order ID after 20 attempts")

def create_order(user_id, username, tool, params, coins, price_usd) -> int:
    import json
    with get_conn() as conn:
        with conn.cursor() as cur:
            oid = _gen_order_id(cur)
            cur.execute("""
                INSERT INTO orders (id, user_id, username, tool, params, coins, price_usd, status, created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'processing', %s)
            """, (oid, user_id, username, tool, json.dumps(params), coins, price_usd, int(time.time())))
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

def get_all_users() -> list:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.uid, u.coins, u.joined, u.username,
                       COUNT(o.id) as order_count
                FROM users u
                LEFT JOIN orders o ON o.user_id = u.uid
                GROUP BY u.uid, u.coins, u.joined, u.username
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

def get_referral_balance(uid: int) -> float:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT referral_balance FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return float(row[0]) if row and row[0] else 0.0

def add_referral_balance(uid: int, amount_rub: float):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (uid, coins, joined, referral_balance)
                VALUES (%s, 0, %s, %s)
                ON CONFLICT (uid) DO UPDATE SET referral_balance = users.referral_balance + %s
            """, (uid, int(time.time()), amount_rub, amount_rub))
        conn.commit()

def deduct_referral_balance(uid: int, amount_rub: float):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET referral_balance = GREATEST(0, referral_balance - %s) WHERE uid = %s",
                (amount_rub, uid)
            )
        conn.commit()

def increment_topup_count(uid: int) -> int:
    """Increment topup_count atomically and return the value BEFORE incrementing (0 = first topup)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Single atomic statement: increment and return old value in one round-trip.
            # RETURNING evaluates after the SET, so `topup_count - 1` is the pre-update value.
            cur.execute(
                "UPDATE users SET topup_count = topup_count + 1 WHERE uid = %s RETURNING topup_count - 1",
                (uid,)
            )
            row = cur.fetchone()
        conn.commit()
        return row[0] if row else 0

def add_referral_earning(referrer_id: int, from_user_id: int, amount_rub: float, percentage: int, payment_type: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO referral_earnings (referrer_id, from_user_id, amount_rub, percentage, payment_type, created)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (referrer_id, from_user_id, amount_rub, percentage, payment_type, int(time.time())))
        conn.commit()

def create_withdrawal_request(uid: int, amount_rub: float, requisites: str) -> int:
    """Deducts balance and creates withdrawal request atomically. Returns request id.
    Raises ValueError if balance is insufficient."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT referral_balance FROM users WHERE uid = %s FOR UPDATE", (uid,))
            row = cur.fetchone()
            balance = float(row[0]) if row and row[0] else 0.0
            if balance < amount_rub:
                raise ValueError("Insufficient referral balance")
            cur.execute(
                "UPDATE users SET referral_balance = referral_balance - %s WHERE uid = %s",
                (amount_rub, uid)
            )
            cur.execute("""
                INSERT INTO withdrawal_requests (user_id, amount_rub, requisites, created)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (uid, amount_rub, requisites, int(time.time())))
            req_id = cur.fetchone()[0]
        conn.commit()
        return req_id

def process_withdrawal(req_id: int, status: str):
    """Mark withdrawal as paid or rejected. On rejection, refunds balance."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM withdrawal_requests WHERE id = %s", (req_id,))
            req = cur.fetchone()
            if not req:
                return None
            if req["status"] != "pending":
                # Already processed — do nothing to prevent double-refunds.
                return dict(req)
            cur.execute(
                "UPDATE withdrawal_requests SET status = %s, processed = %s WHERE id = %s",
                (status, int(time.time()), req_id)
            )
            if status == "rejected":
                cur.execute(
                    "UPDATE users SET referral_balance = referral_balance + %s WHERE uid = %s",
                    (req["amount_rub"], req["user_id"])
                )
        conn.commit()
        return dict(req)

def get_referral_stats(uid: int) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT referral_balance FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            balance = float(row[0]) if row and row[0] else 0.0
            cur.execute(
                "SELECT COALESCE(SUM(amount_rub), 0) FROM referral_earnings WHERE referrer_id = %s",
                (uid,)
            )
            total_earned = float(cur.fetchone()[0])
            cur.execute(
                "SELECT COUNT(*) FROM withdrawal_requests WHERE user_id = %s AND status = 'pending'",
                (uid,)
            )
            pending_withdrawals = cur.fetchone()[0]
            cur.execute(
                "SELECT COUNT(*) FROM users WHERE referred_by = %s",
                (uid,)
            )
            referral_count = cur.fetchone()[0]
            cur.execute(
                "SELECT COUNT(DISTINCT from_user_id) FROM referral_earnings WHERE referrer_id = %s",
                (uid,)
            )
            buyers_count = cur.fetchone()[0]
        return {
            "balance": balance,
            "total_earned": total_earned,
            "pending_withdrawals": pending_withdrawals,
            "referral_count": referral_count,
            "buyers_count": buyers_count,
        }

def get_referral_list(uid: int) -> list:
    """Returns referrals with their own sub-referral counts for blogger tracking."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    u.uid,
                    u.joined,
                    u.topup_count,
                    (SELECT o.username FROM orders o
                     WHERE o.user_id = u.uid AND o.username IS NOT NULL AND o.username != ''
                     LIMIT 1) as username,
                    (SELECT COUNT(*) FROM users sub
                     WHERE sub.referred_by = u.uid) as sub_count,
                    (SELECT COUNT(*) FROM users sub
                     WHERE sub.referred_by = u.uid AND sub.topup_count > 0) as sub_buyers
                FROM users u
                WHERE u.referred_by = %s
                ORDER BY sub_count DESC, u.joined DESC
            """, (uid,))
            return [dict(r) for r in cur.fetchall()]

def record_yoomoney_payment(operation_id: str, user_id: int, amount_rub: float, coins: int) -> bool:
    """Insert payment record. Returns True if new, False if duplicate operation_id."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO yoomoney_payments (operation_id, user_id, amount_rub, coins, created) "
                "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (operation_id) DO NOTHING",
                (operation_id, user_id, amount_rub, coins, int(time.time()))
            )
            is_new = cur.rowcount == 1
        conn.commit()
        return is_new


def get_stale_orders(min_age_seconds: int = 900) -> list:
    """Return processing orders older than min_age_seconds seconds."""
    cutoff = int(time.time()) - min_age_seconds
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM orders WHERE status = 'processing' AND created < %s ORDER BY created ASC",
                (cutoff,)
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


# ── Promo code functions ──────────────────────────────────────

def get_is_blogger(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT is_blogger FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return bool(row and row[0])

def set_blogger(uid: int, value: bool):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET is_blogger = %s WHERE uid = %s", (value, uid))
        conn.commit()

def create_promo_code(owner_uid: int, username: str) -> str:
    """Generate and store a unique promo code for a blogger. Returns the code."""
    import string
    prefix = ''.join(c for c in (username or "").upper() if c.isalpha())[:6] or "USER"
    for _ in range(20):
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        code = f"{prefix}-{suffix}"
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM promo_codes WHERE code = %s", (code,))
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO promo_codes (code, owner_uid, discount_pct, uses_count, created) "
                        "VALUES (%s, %s, 30, 0, %s)",
                        (code, owner_uid, int(time.time()))
                    )
                    conn.commit()
                    return code
    raise RuntimeError("Failed to generate unique promo code after 20 attempts")

def get_promo_code(code: str):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM promo_codes WHERE code = %s", (code.upper().strip(),))
            row = cur.fetchone()
            return dict(row) if row else None

def get_my_promo_code(owner_uid: int):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM promo_codes WHERE owner_uid = %s ORDER BY created DESC LIMIT 1",
                (owner_uid,)
            )
            row = cur.fetchone()
            return dict(row) if row else None

def has_used_promo(user_uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM promo_uses WHERE user_uid = %s", (user_uid,))
            return cur.fetchone() is not None

def has_topped_up(uid: int) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT topup_count FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            return bool(row and row[0] and row[0] > 0)

def use_promo_code(code: str, user_uid: int):
    """Mark promo as used by this user and increment the code's uses_count."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO promo_uses (code, user_uid, created) VALUES (%s, %s, %s) "
                "ON CONFLICT (user_uid) DO NOTHING",
                (code.upper().strip(), user_uid, int(time.time()))
            )
            if cur.rowcount > 0:
                cur.execute(
                    "UPDATE promo_codes SET uses_count = uses_count + 1 WHERE code = %s",
                    (code.upper().strip(),)
                )
        conn.commit()

def set_pending_yoomoney_promo(user_id: int, expected_coins: int, promo_code: str, expected_payment_rub: float = 0):
    """Store expected coins and payment amount for a YooMoney promo so the webhook can verify both."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pending_yoomoney_promos (user_id, expected_coins, promo_code, created, expected_payment_rub)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                    SET expected_coins = EXCLUDED.expected_coins,
                        promo_code = EXCLUDED.promo_code,
                        created = EXCLUDED.created,
                        expected_payment_rub = EXCLUDED.expected_payment_rub
            """, (user_id, expected_coins, promo_code.upper().strip(), int(time.time()), expected_payment_rub))
        conn.commit()

def pop_pending_yoomoney_promo(user_id: int):
    """Read and delete the pending yoomoney promo for a user. Returns None if not found or expired (>24 h)."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM pending_yoomoney_promos WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            # Check expiry BEFORE deleting — if expired we still delete the
            # stale row but return None so the webhook falls back to raw amount.
            # Deleting after the check (pre-existing order) would lose the row
            # before we know whether to use it, giving the user fewer coins.
            if int(time.time()) - row["created"] > 86400:
                cur.execute("DELETE FROM pending_yoomoney_promos WHERE user_id = %s", (user_id,))
                conn.commit()
                return None
            cur.execute("DELETE FROM pending_yoomoney_promos WHERE user_id = %s", (user_id,))
        conn.commit()
    return dict(row)

def clear_pending_yoomoney_promo(user_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pending_yoomoney_promos WHERE user_id = %s", (user_id,))
        conn.commit()

def record_usdt_payment(tx_hash: str, user_id: int, amount_usd: float, coins: int) -> bool:
    """Persist a USDT TX hash. Returns True if new, False if already seen (replay)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usdt_payments (tx_hash, user_id, amount_usd, coins, created)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (tx_hash) DO NOTHING
            """, (tx_hash, user_id, amount_usd, coins, int(time.time())))
            is_new = cur.rowcount == 1
        conn.commit()
        return is_new

def record_stars_payment(charge_id: str, user_id: int, coins: int) -> bool:
    """Persist a Telegram Stars charge_id. Returns True if new, False if already seen (replay)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO stars_payments (charge_id, user_id, coins, created)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (charge_id) DO NOTHING
            """, (charge_id, user_id, coins, int(time.time())))
            is_new = cur.rowcount == 1
        conn.commit()
        return is_new


# Initialize on import
try:
    init_db()
except Exception as e:
    print(f"DB init error: {e}")
