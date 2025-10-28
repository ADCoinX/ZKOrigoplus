
import requests
from ..settings import settings

FALLBACKS = [
    "https://api.mainnet-beta.solana.com",
    "https://rpc.ankr.com/solana"
]

def get_tx(tx_sig: str) -> dict:
    for url in ([settings.SOLANA_RPC] if settings.SOLANA_RPC else FALLBACKS):
        if not url: continue
        try:
            payload = {"jsonrpc":"2.0","id":1,"method":"getTransaction","params":[tx_sig, {"encoding":"json"}]}
            r = requests.post(url, json=payload, timeout=12)
            if r.ok and r.json().get("result"):
                return {"ok": True, "tx": r.json()["result"], "rpc": url}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or RPC down"}
