import hmac
import hashlib
import time
import json
import httpx
from app.core.config import get_settings


async def dispatch_to_make(scenario: str, payload: dict) -> dict:
    settings = get_settings()
    if not settings.make_webhook_base_url or not settings.make_webhook_secret:
        raise RuntimeError('Make.com webhook URL and secret must be configured')
    body = {'scenario': scenario, 'payload': payload}
    timestamp = str(int(time.time()))
    raw = json.dumps(body, separators=(',', ':')).encode()
    signature = hmac.new(settings.make_webhook_secret.encode(), timestamp.encode() + b'.' + raw, hashlib.sha256).hexdigest()
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            settings.make_webhook_base_url.rstrip('/') + f'/{scenario}',
            json=body,
            headers={'X-Timestamp': timestamp, 'X-Signature': signature},
        )
        response.raise_for_status()
        return response.json() if response.content else {'ok': True}
