import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from .. import db
from ..models import PremiumOrder
import stripe
import uuid

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_MODE = os.getenv("STRIPE_MODE", "simulate")
PLATFORM_WEB_URL = os.getenv("PLATFORM_WEB_URL", "http://localhost:8080")


def get_db():
    db_sess = db.SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

@router.post("/create-checkout-session")
def create_checkout_session(payload: dict, db: Session = next(get_db())):
    """
    Create a Stripe Checkout Session. Supports 'simulate' mode when STRIPE_MODE=simulate.
    payload should include: {product_name, price_cents}
    """
    product_name = payload.get("product_name", "BizStack Product")
    price_cents = int(payload.get("price_cents", 1000))

    if STRIPE_MODE == "simulate":
        # create a fake session id and a local simulate URL
        session_id = f"sim_{uuid.uuid4().hex}"
        session_url = f"{PLATFORM_WEB_URL}/simulate/checkout/{session_id}"
        # store a placeholder in DB as a pending order (optional)
        try:
            order = PremiumOrder(
                user_id=None,
                stripe_checkout_id=session_id,
                amount=price_cents/100.0,
                currency="usd",
                product=product_name,
            )
            db.add(order)
            db.commit()
            db.refresh(order)
        except Exception:
            # non-fatal: continue
            pass
        return {"id": session_id, "url": session_url}

    # Real Stripe path
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product_name},
                    "unit_amount": price_cents,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=PLATFORM_WEB_URL + "/?checkout=success",
            cancel_url=PLATFORM_WEB_URL + "/?checkout=cancel",
        )
        return {"id": session.id, "url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    event = None
    try:
        if STRIPE_MODE != "simulate" and webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            # naive parse for simulate / test without secret
            import json
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    # Handle checkout.session.completed
    if event and getattr(event, 'type', None) == "checkout.session.completed":
        session = event.data.object
        try:
            db_sess = next(get_db())
            order = PremiumOrder(
                user_id=session.get("customer", None),
                stripe_checkout_id=session.get("id"),
                amount=(session.get("amount_total") or 0) / 100.0,
                currency=session.get("currency", "usd"),
                product=(session.get("metadata") or {}).get("product_name") if session.get("metadata") else None,
            )
            db_sess.add(order)
            db_sess.commit()
        except Exception:
            pass

    return JSONResponse(status_code=200, content={"status": "ok"})

@router.get("/simulate/checkout/{session_id}")
def simulate_checkout(session_id: str):
    """
    Local simulate checkout page — in a real deployment this would be a Stripe
    hosted page. For dev, this endpoint simulates immediate payment completion
    by invoking the webhook processing path and then redirecting to success.
    """
    # Simulate webhook payload structure
    fake_event = {
        "id": f"evt_{uuid.uuid4().hex}",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_id,
                "amount_total": 1000,
                "currency": "usd",
                "customer": None,
                "metadata": {"product_name": "Simulated Product"}
            }
        }
    }

    # Directly call the webhook handler logic to persist the order
    try:
        # Use db session to create PremiumOrder
        db_sess = next(get_db())
        sess_obj = fake_event['data']['object']
        order = PremiumOrder(
            user_id=sess_obj.get('customer'),
            stripe_checkout_id=sess_obj.get('id'),
            amount=(sess_obj.get('amount_total') or 0) / 100.0,
            currency=sess_obj.get('currency', 'usd'),
            product=(sess_obj.get('metadata') or {}).get('product_name'),
        )
        db_sess.add(order)
        db_sess.commit()
    except Exception:
        pass

    # Redirect to the configured success URL
    return RedirectResponse(url=PLATFORM_WEB_URL + "/?checkout=success", status_code=302)
