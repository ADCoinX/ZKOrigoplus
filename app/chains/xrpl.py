
import requests
from ..settings import settings

FALLBACKS = [
    "https://s2.ripple.com:51234/",
    "https://xrplcluster.com/"
]

def get_tx(tx_hash: str) -> dict:
    for url in ([settings.XRPL_RPC] if settings.XRPL_RPC else FALLBACKS):
        if not url: continue
        try:
            payload = {"method":"tx", "params":[{"transaction": tx_hash, "binary": False}]}
            r = requests.post(url, json=payload, timeout=12)
            js = r.json()
            if js.get("result", {}).get("validated") is not None:
                return {"ok": True, "tx": js["result"], "rpc": url}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or RPC down"}
