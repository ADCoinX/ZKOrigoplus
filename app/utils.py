
from hashlib import sha256
from typing import Optional
import os, re

def anon_ip(ip: str, salt: str) -> str:
    if not ip:
        return "unknown"
    # keep only ipv4 digits/dots (basic)
    ip_clean = re.sub(r"[^0-9.]", "", ip)
    return sha256((ip_clean + "|" + salt).encode()).hexdigest()[:16]

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
