import os
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
                    joined INTEGER DEFAULT 0
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
            cur.execute("SELECT coins FROM users WHERE uid = %s", (uid,))
            row = cur.fetchone()
            if not row or row[0] < amount:
                return False
            cur.execute("UPDATE users SET coins = coins - %s WHERE uid = %s", (amount, uid))
        conn.commit()
        return True

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

# Initialize on import
try:
    init_db()
except Exception as e:
    print(f"DB init error: {e}")
