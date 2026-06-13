import json, os, time

import os
DB_FILE = os.environ.get("DB_PATH", "/tmp/db.json")

def _load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        return json.load(f)

def _save(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(uid: int) -> dict:
    db = _load()
    key = str(uid)
    if key not in db:
        db[key] = {"coins": 0, "orders": [], "referred_by": None, "joined": int(time.time())}
        _save(db)
    return db[key]

def set_user(uid: int, data: dict):
    db = _load()
    db[str(uid)] = data
    _save(db)

def add_coins(uid: int, amount: int):
    u = get_user(uid)
    u["coins"] += amount
    set_user(uid, u)

def spend_coins(uid: int, amount: int) -> bool:
    u = get_user(uid)
    if u["coins"] < amount:
        return False
    u["coins"] -= amount
    set_user(uid, u)
    return True

def get_coins(uid: int) -> int:
    return get_user(uid)["coins"]

def is_new_user(uid: int) -> bool:
    db = _load()
    return str(uid) not in db

def set_referred_by(uid: int, ref_uid: int):
    u = get_user(uid)
    if u["referred_by"] is None:
        u["referred_by"] = ref_uid
        set_user(uid, u)

def get_referred_by(uid: int):
    return get_user(uid).get("referred_by")

ORDER_FILE = os.environ.get("ORDERS_PATH", "/tmp/orders.json")

def _load_orders():
    if not os.path.exists(ORDER_FILE):
        return {"counter": 0, "orders": {}}
    with open(ORDER_FILE) as f:
        return json.load(f)

def _save_orders(data):
    with open(ORDER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_order(user_id, username, tool, params, coins, price_usd) -> int:
    data = _load_orders()
    data["counter"] += 1
    oid = data["counter"]
    data["orders"][str(oid)] = {
        "id": oid,
        "user_id": user_id,
        "username": username,
        "tool": tool,
        "params": params,
        "coins": coins,
        "price_usd": price_usd,
        "status": "processing",
        "created": int(time.time()),
    }
    _save_orders(data)
    return oid

def get_order(oid: int) -> dict:
    return _load_orders()["orders"].get(str(oid))

def update_order_status(oid: int, status: str):
    data = _load_orders()
    if str(oid) in data["orders"]:
        data["orders"][str(oid)]["status"] = status
        _save_orders(data)
