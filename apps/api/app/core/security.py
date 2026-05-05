import hmac
import hashlib
import time
from fastapi import Header, HTTPException, Request
from .config import get_settings


def verify_hmac_signature(raw_body: bytes, signature: str | None, timestamp: str | None) -> None:
    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail='Missing webhook signature')
    try:
        ts = int(timestamp)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail='Invalid webhook timestamp') from exc
    if abs(int(time.time()) - ts) > 300:
        raise HTTPException(status_code=401, detail='Webhook timestamp expired')
    secret = get_settings().webhook_signing_secret.encode()
    payload = f'{timestamp}.'.encode() + raw_body
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail='Invalid webhook signature')


async def verified_webhook(request: Request, x_signature: str | None = Header(None), x_timestamp: str | None = Header(None)) -> bytes:
    raw = await request.body()
    verify_hmac_signature(raw, x_signature, x_timestamp)
    return raw
