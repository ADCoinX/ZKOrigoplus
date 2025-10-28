
import requests
from ..settings import settings

FALLBACKS = [
    "https://polygon-rpc.com",
    "https://rpc.ankr.com/polygon"
]

def get_tx(tx_hash: str) -> dict:
    for url in ([settings.POLYGON_RPC] if settings.POLYGON_RPC else FALLBACKS):
        if not url: continue
        try:
            payload = {"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":[tx_hash],"id":1}
            r = requests.post(url, json=payload, timeout=12)
            if r.ok and r.json().get("result"):
                return {"ok": True, "tx": r.json()["result"], "rpc": url}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or RPC down"}
