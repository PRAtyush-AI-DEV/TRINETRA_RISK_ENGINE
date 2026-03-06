from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Database folder se tools import kar rahe hain
from database.db_setup import get_db
from database import models

print("🚀 TRINETRA V2 ENGINE (CLOUD DATABASE) BOOTING UP...")

app = FastAPI()

# 📦 User se data lene ka format
class TradeInput(BaseModel):
    symbol: str
    trader_type: str
    entry_price: float
    quantity: float

# 🏠 API Route (Cloud me save karne ke liye)
@app.get("/")
def home():
    return("trinetra satrtng")

@app.post("/add_trade")
def add_trade(trade: TradeInput, db: Session = Depends(get_db)):
    # 1. Database table ke hisaab se data taiyar karo
    naya_trade = models.TradeRecord(
        symbol=trade.symbol,
        trader_type=trade.trader_type,
        entry_price=trade.entry_price,
        quantity=trade.quantity,
        status="OPEN"
    )
    
    # 2. Pipe me daalo aur permanently lock (commit) kar do
    db.add(naya_trade)
    db.commit()
    db.refresh(naya_trade)
    
    return {
        "message": "✅ Trade successfully Cloud Tijori me save ho gaya!", 
        "trade_id": naya_trade.id
    }

# 🏠 Naya Route: Cloud se saare trades wapas mangwane ke liye
@app.get("/get_all_trades")
def get_all_trades(db: Session = Depends(get_db)):
    # 1. Munshi ko bolo ki 'trades' table se saara data utha laye
    saare_trades = db.query(models.TradeRecord).all()
    
    # 2. Wo saara data return kar do
    return saare_trades