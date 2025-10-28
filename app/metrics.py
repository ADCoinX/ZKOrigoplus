
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from .settings import settings

Base = declarative_base()
DB_PATH = os.path.join(settings.DATA_DIR, "metrics.sqlite")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Hit(Base):
    __tablename__ = "hits"
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime, server_default=func.now())
    endpoint = Column(String(64))
    method = Column(String(8))
    client = Column(String(64))       # anonymized IP hash
    ua = Column(String(128))          # user agent (truncated)
    status = Column(Integer)
    chain = Column(String(32), nullable=True)

def init_db():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    Base.metadata.create_all(engine)

def add_hit(endpoint: str, method: str, client: str, ua: str, status: int, chain: str | None = None):
    with SessionLocal() as s:
        s.add(Hit(endpoint=endpoint, method=method, client=client, ua=ua[:120], status=status, chain=chain))
        s.commit()

def summary():
    from sqlalchemy import select
    with SessionLocal() as s:
        total = s.execute(select(func.count(Hit.id))).scalar() or 0
        per_endpoint = s.execute(
            select(Hit.endpoint, func.count(Hit.id)).group_by(Hit.endpoint)
        ).all()
        per_chain = s.execute(
            select(Hit.chain, func.count(Hit.id)).group_by(Hit.chain)
        ).all()
        return {
            "total_hits": total,
            "by_endpoint": dict(per_endpoint),
            "by_chain": {k or "unknown": v for k, v in per_chain},
        }
