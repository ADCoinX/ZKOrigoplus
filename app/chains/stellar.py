
import requests
from ..settings import settings

FALLBACKS = [
    "https://horizon.stellar.org",
]

def get_tx(tx_hash: str) -> dict:
    for base in ([settings.STELLAR_HORIZON] if settings.STELLAR_HORIZON else FALLBACKS):
        if not base: continue
        try:
            r = requests.get(f"{base}/transactions/{tx_hash}", timeout=12)
            if r.ok and r.json().get("hash"):
                return {"ok": True, "tx": r.json(), "rpc": base}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or horizon down"}
