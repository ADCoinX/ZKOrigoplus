
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .settings import settings
from .metrics import init_db, add_hit, summary
from .utils import anon_ip, ensure_dir
from . import ai
import os, hashlib

# chain adapters
from .chains import ethereum, polygon, bnb, solana, xrpl, hedera, stellar
from .iso import builders as iso_builders

app = FastAPI(title="zkOrigo Plus", version="1.0.0")

# Static UI
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Ensure data dirs
ensure_dir(settings.DATA_DIR)
ensure_dir(settings.ISO_EXPORT_DIR)
init_db()

# --- Auth dependency ---
def require_key(request: Request):
    conf = [k.strip() for k in settings.API_KEYS.split(",") if k.strip()]
    key = request.headers.get("X-Api-Key")
    if not conf or key not in conf:
        raise HTTPException(401, "Missing/invalid API key")
    return True

# --- Models ---
class VerifyReq(BaseModel):
    chain: str
    tx: str

class ScoreReq(BaseModel):
    context: dict

class ISOReq(BaseModel):
    structure: str # pacs.008 | pain.001 | camt.053
    refs: dict = {}
    note: str | None = None

# --- Routes ---
@app.get("/")
def home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.get("/v1/healthz")
def healthz():
    return {"ok": True}

@app.get("/v1/metrics/summary")
def metrics_summary():
    return summary()

@app.post("/v1/verify")
def verify(req: VerifyReq, request: Request, _=Depends(require_key)):
    iphash = anon_ip(request.client.host if request.client else "", settings.LOG_SALT)
    ua = request.headers.get("User-Agent","")[:120]

    chain = req.chain.lower()
    result = {"ok": False, "error": "unsupported"}

    try:
        if chain == "ethereum":
            result = ethereum.get_tx(req.tx)
        elif chain == "polygon":
            result = polygon.get_tx(req.tx)
        elif chain == "bnb":
            result = bnb.get_tx(req.tx)
        elif chain == "solana":
            result = solana.get_tx(req.tx)
        elif chain == "xrpl":
            result = xrpl.get_tx(req.tx)
        elif chain == "hedera":
            result = hedera.get_tx(req.tx)
        elif chain == "stellar":
            result = stellar.get_tx(req.tx)
        else:
            raise HTTPException(400, "Unsupported chain")
    except Exception as e:
        result = {"ok": False, "error": str(e)}

    status = 200 if result.get("ok") else 400
    add_hit("/v1/verify", "POST", iphash, ua, status, chain)
    return JSONResponse(result, status_code=status)

@app.post("/v1/ai/score")
def ai_score(req: ScoreReq, request: Request, _=Depends(require_key)):
    iphash = anon_ip(request.client.host if request.client else "", settings.LOG_SALT)
    ua = request.headers.get("User-Agent","")[:120]
    out = ai.score(req.context or {})
    add_hit("/v1/ai/score", "POST", iphash, ua, 200, (req.context or {}).get("chain"))
    return out

@app.post("/v1/iso/export")
def iso_export(req: ISOReq, request: Request, _=Depends(require_key)):
    iphash = anon_ip(request.client.host if request.client else "", settings.LOG_SALT)
    ua = request.headers.get("User-Agent","")[:120]

    struct = req.structure.lower()
    data = {
        "msg_id": "zkorigo-" + hashlib.sha256(os.urandom(8)).hexdigest()[:8],
        "end_to_end_id": req.refs.get("tx") or req.refs.get("e2e") or "N/A",
        "unstructured": req.note or "On-chain reference",
        "supplementary": {k:str(v) for k,v in (req.refs or {}).items()}
    }

    if struct == "pacs.008":
        xml = iso_builders.pacs008(data)
    elif struct == "pain.001":
        xml = iso_builders.pain001(data)
    elif struct == "camt.053":
        xml = iso_builders.camt053(data)
    else:
        raise HTTPException(400, "Unsupported structure")

    # Save to file (or S3 in AWS)
    fname = f"{struct}_{data['msg_id']}.xml"
    path = os.path.join(settings.ISO_EXPORT_DIR, fname)
    with open(path, "wb") as f:
        f.write(xml)

    add_hit("/v1/iso/export", "POST", iphash, ua, 200, None)
    return {"ok": True, "file": path}
