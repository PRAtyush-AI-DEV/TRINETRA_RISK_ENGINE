import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel

# --- STEP 1: FOLDER PATH SETTING ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from INDEX_API.math_API import Trinetra_Calculator
from INDEX_API.decipline_API import Trinetra_Discipline
from INDEX_API.end_line_API import Khatra_Manager
from INDEX_API.profit_tralling_API import paisa_nikalo
from memory.json_index import Trinetra_memory

app = FastAPI()

# ======================================================
# 🔱 ENGINE OBJECTS INITIATION
# ======================================================
print("\n---> [SYSTEM] Booting Up Trinetra Engines...")

memory = Trinetra_memory()
data = memory.load_data()

calculator = Trinetra_Calculator()
discipline = Trinetra_Discipline()

# Logic to load saved states
discipline.current_mode = data["discipline"].get("current_mode", "")
discipline.trades_taken = data["discipline"].get("trades_taken", 0)
discipline.current_max_trades = data["discipline"].get("current_max_trades", 0)

khatra = Khatra_Manager(data["khatra"].get("ek_din_ka_risk", 5000.0))
khatra.ek_din_ka_total_loss = data["khatra"].get("ek_din_ka_total_loss", 0.0)

tracker = None

# ======================================================
# 📦 PYDANTIC MODELS
# ======================================================
class TraderType(BaseModel):
    trader_type: str

class UpdateLimitInput(BaseModel):
    new_daily_limit: float

class DailyRiskInput(BaseModel):
    trade_risk: float

class DisciplineCheckInput(BaseModel):
    request_bonus_trade: bool = False

class TradeInput(BaseModel):
    symbol: str
    capital: float
    entry: float
    sl: float
    risk: float

class TradeTrackerInput(BaseModel):
    symbol: str
    trader_type: str
    entry: float
    target: float
    quantity: float
    sl: float

class PriceInput(BaseModel):
    price: float

# ======================================================
# 🏠 ROUTES
# ======================================================
@app.get("/")
def home():
    return {"message": "🔱 TRINETRA API RUNNING (INDIAN MARKET MODE) 🔱"}

@app.post("/set_daily_limit")
def set_daily_limit(input_data: UpdateLimitInput):
    khatra.ek_din_ka_risk = input_data.new_daily_limit
    save_memory()
    return {"message": f"Daily Limit updated to ₹{khatra.ek_din_ka_risk}"}

@app.post("/set_trader_type")
def set_trader_type(input_data: TraderType):
    if hasattr(discipline, 'current_mode') and discipline.current_mode != "":
        return {"error": "🛑 FRAUD ALERT: Din ke beech mein mode change allow nahi hai!"}
    
    t_type = input_data.trader_type.lower()
    if t_type == "scalper":
        discipline.current_max_trades = 3
        discipline.current_mode = "INDEX SCALPER"
    elif t_type == "intraday":
        discipline.current_max_trades = 2
        discipline.current_mode = "INDEX INTRADAY"
    else:
        return {"error": "Invalid type. Use 'scalper' or 'intraday'."}
    
    save_memory()
    return {"mode": discipline.current_mode, "max_trades": discipline.current_max_trades}

@app.post("/calculate_quantity")
def calculate(input_data: TradeInput):
    result = calculator.get_trade_quantity(
        input_data.symbol, input_data.capital, input_data.entry, input_data.sl, input_data.risk
    )
    return result

@app.post("/start_trade_tracker")
def start_trade_tracker(input_data: TradeTrackerInput):
    global tracker
    status = discipline.check_trade_logic(discipline.trades_taken)
    
    if not status["allowed"]:
        return {"error": "Discipline Block", "details": status}

    tracker = paisa_nikalo(
        input_data.symbol, input_data.trader_type, input_data.entry, input_data.target, input_data.quantity, input_data.sl
    )
    discipline.trades_taken += 1
    save_memory()
    return {"message": f"Trade started for {input_data.symbol}", "total_trades": discipline.trades_taken}

@app.post("/update_price")
def update_price(input_data: PriceInput):
    global tracker
    if tracker is None:
        return {"error": "No active trade."}

    result = tracker.process_price(input_data.price)
    if result["status"] in ["SL HIT", "TARGET HIT"]:
        if result["status"] == "SL HIT" and result.get("loss", 0) > 0:
            khatra.update_loss(result["loss"])
        save_memory()
        tracker = None 
    return result

def save_memory():
    memory.save_data({
        "discipline": {
            "current_mode": discipline.current_mode,
            "current_max_trades": discipline.current_max_trades,
            "trades_taken": discipline.trades_taken,
            "bonus_trade_used": getattr(discipline, 'bonus_trade_used', False),
            "hard_lock_activated": getattr(discipline, 'hard_lock_activated', False)
        },
        "khatra": {
            "ek_din_ka_risk": khatra.ek_din_ka_risk,
            "ek_din_ka_total_loss": khatra.ek_din_ka_total_loss
        }
    })