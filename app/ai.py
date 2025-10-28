
def score(context: dict) -> dict:
    # Simple explainable heuristics
    # Inputs may include: account_age_days, tx_24h, contract_type, chain, is_rwa, amount_usd
    s = 100
    reasons = []

    age = context.get("account_age_days")
    if age is not None and age < 7:
        s -= 25; reasons.append("New address (<7d)")

    tx24 = context.get("tx_24h")
    if tx24 is not None and tx24 > 50:
        s -= 30; reasons.append("High 24h velocity")

    if context.get("is_rwa"):
        # RWA preferred but check policy
        pass

    amt = context.get("amount_usd")
    if amt is not None and amt > 100000:
        s -= 20; reasons.append("Large amount >100k USD")

    chain = context.get("chain")
    if chain in {"ethereum","polygon","bnb"} and context.get("contract_type") == "unknown":
        s -= 10; reasons.append("Unknown EVM contract")

    tier = "Low" if s >= 70 else ("Medium" if s >= 40 else "High")
    return {"riskScore": max(s,0), "tier": tier, "reasons": reasons[:5]}
