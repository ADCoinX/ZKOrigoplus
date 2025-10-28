
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8080
    ENV: str = "dev"
    API_KEYS: str = "dev-key-123"
    LOG_SALT: str = "change-this-random-salt"
    DATA_DIR: str = "/app_data"

    ISO_EXPORT_DIR: str = "/app_data/iso_exports"

    ETH_RPC: str | None = None
    POLYGON_RPC: str | None = None
    BNB_RPC: str | None = None
    SOLANA_RPC: str | None = None
    XRPL_RPC: str | None = None
    HEDERA_MIRROR: str | None = None
    STELLAR_HORIZON: str | None = None

    STRIPE_SECRET: str | None = None
    STRIPE_PRICE_PRO: str | None = None
    STRIPE_PRICE_ENTERPRISE: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
