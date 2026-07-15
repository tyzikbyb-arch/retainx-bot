import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Transaction
from routes.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

CREDIT_PACKS = {
    20:   100,
    100:  500,
    200:  1000,
    500:  2500,
    1000: 4500,
    2000: 8000,
}


class CheckoutRequest(BaseModel):
    credits: int


@router.post("/checkout")
async def create_checkout(body: CheckoutRequest, user: User = Depends(get_current_user)):
    if body.credits not in CREDIT_PACKS:
        raise HTTPException(status_code=422, detail="Invalid credit pack")

    price_cents = CREDIT_PACKS[body.credits]
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "usd", "unit_amount": price_cents, "product_data": {"name": f"RetainX Studio — {body.credits} Credits", "description": f"{body.credits} credits · 1 credit = $0.05"}}, "quantity": 1}],
        mode="payment",
        success_url=f"{FRONTEND_URL}/billing?success=1",
        cancel_url=f"{FRONTEND_URL}/billing",
        metadata={"user_id": str(user.id), "credits": str(body.credits)},
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        user_id = int(sess["metadata"]["user_id"])
        credits = int(sess["metadata"]["credits"])
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.credits += credits
            db.add(Transaction(user_id=user_id, type="purchase", credits=credits, usd_amount=sess["amount_total"] / 100, stripe_payment_id=sess["payment_intent"], description=f"Credit top-up (+{credits} cr)"))
            db.commit()

    return {"ok": True}


@router.get("/transactions")
def get_transactions(skip: int = 0, limit: int = 50, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == user.id).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
