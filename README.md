
# zkOrigo Plus — Compliance Layer API (Stateless, Multi-Chain)

zkOrigo Plus is a **stateless compliance API** for multi-chain validation, **ISO 20022 XML export**,
basic **AI risk scoring**, and **traction analytics** (privacy-first). Ready to deploy on AWS or locally via Docker.

**Not a payment rail. Not a consensus layer. It’s a compliance layer.**

## Key Capabilities
- **Multi-chain tx validation** (Ethereum/Polygon/BNB/Solana/XRPL/Hedera/Stellar) via public RPCs or your own nodes.
- **ISO 20022 XML export** (`pacs.008`, `pain.001`, `camt.053`) with on-chain references; saved to disk (or S3 in AWS).
- **AI risk scoring (heuristics)** — fast, CPU-only. Returns score 0–100 with reasons.
- **Traction analytics** — counts API hits, anonymizes IP, stores no PII. Persists across redeploys.
- **Enterprise UI** — clean, corporate landing at `/` with your large logo `zkOrigo_logo.png`.
- **Monetization-ready** — API-key auth, rate limit, usage counters. Stripe integration hooks included (optional).

## Quick Start (Local)
1. Copy your logo to: `static/zkOrigo_logo.png` (use this exact filename).
2. Create `.env` from example:
   ```bash
   cp .env.example .env
   ```
3. Run with Docker:
   ```bash
   docker compose up --build
   ```
   Or run directly:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```

Open: `http://localhost:8080/docs` for API, `http://localhost:8080/` for UI.

## AWS Notes
- Use the same repo. For AWS, set env vars for your RPC URLs or leave to public fallbacks.
- For persistent metrics in AWS, mount EBS volume to `/app_data` or configure DynamoDB (adapter hook included).

## Endpoints (v1)
- `POST /v1/verify` — validate on-chain tx across supported chains.
- `POST /v1/ai/score` — risk heuristics for wallet/tx context.
- `POST /v1/iso/export` — generate ISO XML; returns file path/URL.
- `GET  /v1/metrics/summary` — traction counts (no PII).
- `GET  /v1/healthz` — health check.
- `GET  /` — enterprise UI.

## Security & Privacy
- Stateless: no keys or PII stored.
- Metrics anonymize IP (hash with salt) and user-agent truncated.
- Configure API keys via `API_KEYS` env (comma-separated).

## License
MIT
