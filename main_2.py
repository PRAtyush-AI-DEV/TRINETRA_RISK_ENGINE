# =================================================================
# KADAM 1: Bahar se tools (Mistri) aur apne database ka saaman lao
# =================================================================
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime

# Apne 'database' folder se pipe (get_db) aur register ka design (models) mangwao
from database.db_setup import get_db, engine
from database import models
from INDEX_API.decipline_API import Trinetra_Discipline
from INDEX_API.math_API import Trinetra_Calculator  # Naya Mistri
from INDEX_API.profit_tralling_API import paisa_nikalo
from INDEX_API.end_line_API import Khatra_Manager

# =================================================================
# KADAM 2: Dukaan ka shutter kholo (System Start)
# =================================================================
# 👇 NAYI LINE: VIP Parking (Register) yahan banega 👇
active_trades = {}
app = FastAPI(title="SHAKTI - Trinetra Engine")
# Discipline Engine start karke counter par rakh lo
discipline = Trinetra_Discipline()
calculator = Trinetra_Calculator()

# Global variable banayenge taaki poore din system isko yaad rakhe
circuit_breaker = None

# 👇 NAYI LINE: Ye Neon ko bolegi ki missing tables automatically bana do! 👇
models.Base.metadata.create_all(bind=engine)

# =================================================================
# KADAM 3: Ek Welcome Board lagao (Testing ke liye)
# =================================================================
@app.get("/")
def welcome_board():
    return {"message": "🔱 TRINETRA SYSTEM IS LIVE & READY 🔱"}


# =================================================================
# KADAM 4: NAYI PARCHI (Risk aur Capital ke sath)
# =================================================================
class TradeInput(BaseModel):
    symbol: str
    trade_direction : str                   # NAYA: 'B' for Buy, 'S' for Sell
    entry_price: float
    sl_price: float       
    target_price: float                # NAYA: Target Price             # NAYA: Stoploss ka price
    current_capital: float             # NAYA: Jeb mein total paisa
    risk_per_trade_percentage: float   # NAYA: Kitne % risk lena hai (jaise 1.0 ya 2.0)
    request_bonus_trade: bool = False  # PURANA: Bonus trade ka switch

class TraderProfile(BaseModel):
    trader_type : str  # User yahan "SCALPER" ya "INTRADAY" likhega
    daily_risk_limit : float  # 👈 NAYA: User khud batayega uski daily limit kya hai

# =================================================================
# SETTINGS COUNTER: Trader Type Set Karo (ONE-TIME LOCK)
# =================================================================

@app.post("/set_trader_type")
def set_trader_type(profile: TraderProfile):
    global circuit_breaker  # 👈 FIX: Is line ke bina Python manager ko bhool jayega
    
    # User ne jo limit batayi, usse Manager ko de do
    circuit_breaker = Khatra_Manager(ek_din_ka_risk=profile.daily_risk_limit)
    
    # Receptionist ne parchi seedha Discipline Engine (Manager) ko de di
    engine_response = discipline.set_profile(profile.trader_type)
    
    if engine_response["status"] == "error":
        return {"error": engine_response["message"]}
        
    return {
        "message": engine_response["message"],
        "khatra_alert": f"🛡️ Circuit Breaker ON: Aaj ka max risk ₹{profile.daily_risk_limit} set ho gaya."
    }

   # =================================================================
# KADAM 5: SHAKTI VIP Counter (Trade Entry Gate)
# =================================================================
@app.post("/add_shakti_trade")
def add_shakti_trade(trade: TradeInput, db: Session = Depends(get_db)):
    
    # RULE 1: Aaj ke trades gino
    aaj_ki_subah = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    aaj_ke_trades = db.query(models.TradeRecord).filter(
        models.TradeRecord.timestamp >= aaj_ki_subah
    ).count()
    
    # ===========================================================
    # RULE 2: SMART DISCIPLINE BOUNCER (Hard Lock & Bonus Check)
    # ===========================================================
    discipline_check = discipline.check_trade_logic(
        current_trades=aaj_ke_trades, 
        request_bonus_trade=trade.request_bonus_trade
    )

    if not discipline_check["allowed"]:
        return {
            "error": discipline_check["message"],
            "status": discipline_check["status"],
            "cooldown_seconds": discipline_check.get("cooldown_seconds", 0)
        }

    # ===========================================================
    # RULE 2.5: SHAKTI MATH ENGINE (Risk & Capital Check)
    # ===========================================================
    math_result = calculator.get_trade_quantity(
        symbol=trade.symbol,
        current_capital=trade.current_capital,
        entry_price=trade.entry_price,
        sl_price=trade.sl_price,
        risk_per_trade_percentage=trade.risk_per_trade_percentage
    )

    # Agar Math Engine ne error diya (Margin kam hai, ya SL same hai)
    if math_result["status"] == "error":
        return {"error": f"🚫 MATH ALERT: {math_result['message']}"}
        
    # Agar sab theek hai, toh Calculator se Asli Quantity nikal lo
    asli_quantity = math_result["quantity"]
    trade_ka_asli_risk = math_result["risk_amount"] # Math engine se seedha risk utha lo

    # ===========================================================
    # NAYA RULE: KHATRA MANAGER (Circuit Breaker Check)
    # ===========================================================
    if circuit_breaker is None:
        return {"error": "Bhai, pehle /set_trader_type par jaakar apni Daily Limit set karo!"}

   # 👈 FIX: Yahan 'quantity=asli_quantity' add kiya gaya hai, aur 3 variables nikale hain
    is_safe, khatra_msg, trinetra_solution = circuit_breaker.check_trade_aukaat(
        ek_trade_ka_risk=trade_ka_asli_risk, 
        quantity=asli_quantity
    )
    if not is_safe:
        return {"error": khatra_msg} # Agar limit cross ho rahi hai toh trade yahin rok do
    
    
    # 👈 NAYI LINE: Terminal par Dashboard print karo
    circuit_breaker.show_live_dashboard() 

    if not is_safe:
        return {
            "error": khatra_msg,
            "solution": trinetra_solution # NAYA: Swagger mein user ko solution dikhega
        }

    # ===========================================================
    # RULE 3 & 4: Database mein save karo
    # ===========================================================
    naya_trade = models.TradeRecord(
        symbol=trade.symbol,
        trade_direction=trade.trade_direction,  # 👈 Isko add kar de taaki DB mein 'B'/'S' save ho
        entry_price=trade.entry_price,
        quantity=asli_quantity    # <--- YAHAN AB ENGINE WALI SAFE QUANTITY JAYEGI
    )

    db.add(naya_trade)
    db.commit()
    db.refresh(naya_trade)

    # ===========================================================
    # RULE 5: TRAILING ENGINE KO TRADE SAUNP DO
    # ===========================================================
    tracker = paisa_nikalo(
        symbol=trade.symbol,
        trader_type=trade.trade_direction,  # 👈 'trade.trader_type' ko badalkar ye kiya
        entry_price=trade.entry_price,
        target_price=trade.target_price,    # 👈 Ye line missing thi, engine ko target batana zaroori hai
        total_quantity=asli_quantity,
        current_sl=trade.sl_price
    )

    # Trade ID ke naam se is trade ka dimaag register mein save kar lo
    active_trades[naya_trade.id] = tracker

    return {
        "message": f"✅ SHAKTI APPROVED: Trade Save Hua! ({discipline_check['message']})", 
        "trade_id": naya_trade.id,
        "status": discipline_check["status"],
        "math_report": {
            "allotted_quantity": asli_quantity,
            "margin_used": math_result["margin_required"],
            "total_risk": math_result["risk_amount"]
        }
    }

# =================================================================
# KADAM 6: LIVE TRACKING COUNTER (Price Update Gate)
# =================================================================
class PriceInput(BaseModel):
    trade_id: int
    current_price: float

# main_2.py ke aakhiri mein

@app.post("/update_price")
def update_price(data: PriceInput, db: Session = Depends(get_db)): # 👈 db connection zaroori hai
    
    # 1. Check karo ki kya trade zinda hai?
    if data.trade_id not in active_trades:
        return {"error": "Trade ya toh exist nahi karta, ya close ho chuka hai!"}

    # 2. Register se us specific trade ka dimaag (tracker) nikalo
    tracker = active_trades[data.trade_id]

    # 3. Naya price tracker ko do aur result lo
    result = tracker.process_price(data.current_price)

    # ==========================================================
    # 🛑 NAYA LOGIC: AGAR TRADE KHATAM HO GAYA (Target ya SL hit)
    # ==========================================================
    if result["status"] in ["TARGET HIT", "SL HIT"]:
        
        # Database se is trade ki purani parchi nikalo
        closed_trade = db.query(models.TradeRecord).filter(models.TradeRecord.id == data.trade_id).first()
        
        if closed_trade:
            closed_trade.status = result["status"]
            
            final_pnl = 0.0 # Shuru mein 0
            
            if result["status"] == "TARGET HIT":
                final_pnl = result.get("profit", 0.0) # 👈 FIX: Asli profit
                sign = "🟢 +" 
            elif result["status"] == "SL HIT":
                loss_amount = result.get("loss", 0.0)
                final_pnl = -loss_amount # 👈 FIX: Asli loss (Minus mein)
                sign = "🔴 " 
                
                # Circuit Breaker ke register mein loss likh do
                if circuit_breaker:
                    circuit_breaker.update_loss(loss_amount)
                    circuit_breaker.show_live_dashboard() # 👈 NAYA: Loss hote hi dashboard update hoga

            # 👈 FIX: Ab DB mein 0.0 nahi, asli PnL save hoga!
            closed_trade.pnl = final_pnl 
            db.commit()

            # Response mein ek naya 'pnl_report' bhejo
            result["pnl_report"] = f"{sign}{final_pnl}" 
            result["message"] = f"{result['status']}! PnL: {result['pnl_report']}"

        # VIP Register se gaadi nikal do (Khel Khatam)
        del active_trades[data.trade_id]

    return result

@app.get("/daily_summary")
def get_daily_summary(db: Session = Depends(get_db)):
    # 1. Pichle 24 ghante ka waqt nikalna (Timezone lafda khatam karne ke liye)
    pichle_24_ghante = datetime.datetime.now() - datetime.timedelta(hours=24)
    
    # 2. Database se trades uthao
    trades = db.query(models.TradeRecord).filter(
        models.TradeRecord.timestamp >= pichle_24_ghante
    ).all()

    if not trades:
        return {"message": "Pichle 24 ghante mein koi trade nahi mila."}

    # 3. Baaki calculations (Same rahenge)
    total_trades = len(trades)
    winning_trades = len([t for t in trades if t.pnl > 0])
    losing_trades = len([t for t in trades if t.pnl < 0])
    net_pnl = sum(t.pnl for t in trades)
    
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    return {
        "report_period": "Last 24 Hours",
        "summary": {
            "total_trades": total_trades,
            "wins": winning_trades,
            "losses": losing_trades,
            "win_rate": f"{round(win_rate, 2)}%",
            "net_pnl": f"{'🟢 +' if net_pnl >= 0 else '🔴 '}{round(net_pnl, 2)}"
        },
        "trades_detail": [
            {"id": t.id, "symbol": t.symbol, "status": t.status, "pnl": t.pnl}
            for t in trades
        ]
    }