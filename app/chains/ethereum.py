
import os, requests
from ..settings import settings

# Public fallbacks (subject to rate limits). Prefer your own RPC via .env
FALLBACKS = [
    "https://rpc.ankr.com/eth",
    "https://cloudflare-eth.com",
    "https://rpc.ethermine.org"
]

def _rpc_url():
    return settings.ETH_RPC or FALLBACKS[0]

def get_tx(tx_hash: str) -> dict:
    # Simple JSON-RPC eth_getTransactionByHash
    for url in ([settings.ETH_RPC] if settings.ETH_RPC else FALLBACKS):
        if not url: continue
        try:
            payload = {"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":[tx_hash],"id":1}
            r = requests.post(url, json=payload, timeout=12)
            if r.ok and r.json().get("result"):
                return {"ok": True, "tx": r.json()["result"], "rpc": url}
        except Exception:
            continue
    return {"ok": False, "error": "tx not found or RPC down"}
