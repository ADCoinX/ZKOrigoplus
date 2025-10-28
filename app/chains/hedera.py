
import requests
from ..settings import settings

FALLBACKS = [
    "https://mainnet-public.mirrornode.hedera.com",
]

def get_tx(tx_id: str) -> dict:
    # Hedera mirror node expects transaction ID format; or use /transactions/{id}
    for base in ([settings.HEDERA_MIRROR] if settings.HEDERA_MIRROR else FALLBACKS):
        if not base: continue
        try:
            # try transaction by id
            r = requests.get(f"{base}/api/v1/transactions/{tx_id}", timeout=12)
            if r.ok:
                js = r.json()
                if js.get("transactions"):
                    return {"ok": True, "tx": js["transactions"][0], "rpc": base}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or mirror down"}
