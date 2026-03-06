from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .db_setup import Base

class TradeRecord(Base):
    __tablename__ = "trades" # Ye teri table ka asli naam hoga Neon par

    # Ye sab tere columns (Excel sheet ki headings) hain:
    id = Column(Integer, primary_key=True, index=True) # Trade Number (1, 2, 3...)
    symbol = Column(String, index=True)                # Jaise "NIFTY", "BANKNIFTY"
    trader_type = Column(String)                       # "SCALPER" ya "INTRADAY"
    entry_price = Column(Float)                        # Kis price par liya
    quantity = Column(Float)                           # Kitni quantity
    status = Column(String, default="OPEN")            # "OPEN", "TARGET HIT", ya "SL HIT"
    pnl = Column(Float, default=0.0)                   # Kitna profit/loss hua
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # Time