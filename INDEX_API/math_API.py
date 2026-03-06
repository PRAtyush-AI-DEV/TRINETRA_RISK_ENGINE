import math

class Trinetra_Calculator:
    def __init__(self):
        # YAHAN SE CRYPTO GAYAB: Sirf Indian Markets bache hain!
        self.market_lot_sizes = {
            "NIFTY": 75, "BANKNIFTY": 15, "FINNIFTY": 40, "SENSEX": 10
        }
        self.index_names = ["NIFTY", "BANKNIFTY", "FINNIFTY", "SENSEX"]
        self.crypto_names = [] # Yeh khali rahega kyunki hum index wale folder mein hain
        print("---> [TERMINAL LOG] ✅ INDIAN TRINETRA MATH ENGINE INITIATED...")

    def get_trade_quantity(self, symbol, current_capital, entry_price, sl_price, risk_per_trade_percentage, leverage=1):
        symbol = symbol.upper()
        print(f"\n---> [TERMINAL LOG] 🧮 CALCULATING (INDIAN MARKET): {symbol}")

        # 1. TOTAL RISK (Paise ka Hisaab - Sirf Rupay)
        risk_amount_in_rupees = current_capital * (risk_per_trade_percentage / 100)
        print(f"---> [TERMINAL LOG] Risk per trade: ₹{risk_amount_in_rupees:.2f}")

        # 2. SL GAP (Premium ya Stock Difference)
        SL_gap = abs(entry_price - sl_price)
        print(f"---> [TERMINAL LOG] SL gap: {SL_gap} points")

        # Error Check: Entry aur SL same nahi ho sakte
        if SL_gap == 0:
            msg = "Entry aur SL same nahi ho sakte!"
            print(f"---> [TERMINAL LOG] ❌ Error: {msg}")
            return {"status": "error", "message": msg, "quantity": 0}

        # --- SMART TRAFFIC POLICE (Routing & Leverage) ---
        # RAASTA 1: INDEX (Options/Futures - Leverage 1x hi rahega)
        if symbol in self.index_names:
            print("---> [TERMINAL LOG] ⚠️ ALERT: Index Option buying mein koi leverage nahi milta. Set to 1x!")
            leverage = 1
        # RAASTA 2: STOCKS (Intraday 5x - Indian Market ka default)
        else:
            print("---> [TERMINAL LOG] ℹ️ Path: NSE Equity Intraday. Fixed 5x leverage applied!")
            leverage = 5
        
        # -----------------------------------------------------------
        # 4. MAIN MAGIC: RAW QUANTITY CALCULATION (Indian Market)
        # -----------------------------------------------------------
        if symbol in self.index_names:
            # --- RAASTA 1: INDEX (LOT SIZE WALA HISAAB) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            lot = self.market_lot_sizes[symbol]
            # Kitne Lot aayenge, uska round off
            final_quantity = int(total_quantity // lot) * lot
            print(f"---> [TERMINAL LOG] ✅ F&O Lot Size Rule Applied: {lot} qty per lot")
      
        else:
            # --- RAASTA 2: STOCKS (Normal Quantity) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            final_quantity = int(total_quantity) # Stock fractions mein nahi hota
            print("---> [TERMINAL LOG] ✅ NSE Cash Stock Logic Applied (Fractions Not Allowed)")

        # 🛑 SAFETY LOCK 1: Zero Quantity Check
        print(f"---> [TERMINAL LOG] Total allowed quantity: {final_quantity}")
        if final_quantity <= 0:
            msg = "Risk per trade bohot kam hai, is SL ke saath ek bhi lot nahi aayega!"
            print(f"---> [TERMINAL LOG] ❌ REJECTED: {msg}")
            return {"status": "error", "message": msg, "quantity": 0}
        
        # 5. THE BILLING (Margin Kitna Chahiye)
        capital_required = final_quantity * entry_price
        
        # --- THE LEVERAGE MAGIC ---
        capital_needed = capital_required / leverage  # (Yeh line pehle sirf index mein thi, ab theek kar di)

        if symbol in self.index_names:
            print(f"---> [TERMINAL LOG] Total Contract Value: ₹{capital_required:.2f}")
            print(f"---> [TERMINAL LOG] Margin Needed (After {leverage}x SEBI Leverage): ₹{capital_needed:.2f}")  
        else:
             print(f"---> [TERMINAL LOG] Total Stock Value: ₹{capital_required:.2f}")
             print(f"---> [TERMINAL LOG] Intraday Margin Needed (5x): ₹{capital_needed:.2f}")  

        # 6. --- REALITY CHECK (Aukaat Check) 
        margin_in_rupees = capital_needed

        # Kya paas mein paisa hai?
        if margin_in_rupees > current_capital:
            msg = f"Broker maang raha hai: ₹{margin_in_rupees:.2f} | Aapke paas hai: ₹{current_capital}"
            print(f"---> [TERMINAL LOG] ❌ REJECTED: Margin kam pad raha hai! {msg}")
            return {"status": "error", "message": f"Margin kam pad raha hai. {msg}", "quantity": 0}

        # SAB KUCH THEEK HAI (Return API dictionary)
        return {
            "status": "success",
            "message": "Quantity calculated successfully.",
            "quantity": final_quantity,
            "margin_required": margin_in_rupees,
            "risk_amount": risk_amount_in_rupees
        }