import math

class Trinetra_Calculator:
    def __init__(self):
        # YAHAN SE CRYPTO GAYAB: Sirf Indian Markets bache hain!
        self.market_lot_sizes = {
            "NIFTY": 65, "BANKNIFTY": 30, "FINNIFTY": 60, "SENSEX": 20 , "MIDCAPNIFTY": 120
        }
        # Naya (Sahi Order - Longest First):
        self.index_names = ["BANKNIFTY", "FINNIFTY", "MIDCAPNIFTY", "SENSEX", "NIFTY"]
        self.crypto_names = [] # Yeh khali rahega kyunki hum index wale folder mein hain
        print("---> [TERMINAL LOG] ✅ INDIAN TRINETRA MATH ENGINE INITIATED...")

    def get_trade_quantity(self, symbol, current_capital, entry_price, sl_price, risk_per_trade_percentage, leverage=1):
        symbol = symbol.upper()
        print(f"\n---> [TERMINAL LOG] 🧮 CALCULATING (INDIAN MARKET): {symbol}")

        # 🕵️‍♂️ NAYA DNA LOGIC: Symbol ke andar Index dhoondo (Nayi Lines)
        is_option = symbol.endswith("CE") or symbol.endswith("PE")
        # found_index = next((idx for idx in self.index_names if idx in symbol), None)
        found_index = next((idx for idx in self.index_names if symbol.startswith(idx)), None)
        # for idx in self.index_names:
        # if idx in symbol:
        # return idx
        is_index_trade = found_index is not None or is_option
        # if found_index is not None or is_option:
        #      is_index_trade = True
        # else:
        #      is_index_trade = False
        
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

        if is_index_trade: # 👈 Modified: Ab ye substrings bhi pehchanega
            print("---> [TERMINAL LOG] ⚠️ ALERT: Index Option buying mein koi leverage nahi milta. Set to 1x!")
            leverage = 1
        # RAASTA 2: STOCKS (Intraday 5x - Indian Market ka default)
        else:
            print("---> [TERMINAL LOG] ℹ️ Path: NSE Equity Intraday. Fixed 5x leverage applied!")
            leverage = 5
        
        # -----------------------------------------------------------
        # 4. MAIN MAGIC: RAW QUANTITY CALCULATION (Indian Market)
        # -----------------------------------------------------------
        if is_index_trade: # 👈 Modified
            # --- RAASTA 1: INDEX (LOT SIZE WALA HISAAB) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            print(f"---> [TERMINAL LOG] ✅ Quantity applied by you: {total_quantity}")
            # Smart Lot Selection: Agar NIFTY symbol ke andar hai, toh NIFTY ka lot lo
            lot = self.market_lot_sizes.get(found_index, 1) if found_index else 1
            # Kitne Lot aayenge, uska round off
            final_quantity = int(total_quantity // lot) * lot
            print(f"---> [TERMINAL LOG] ✅ F&O Lot Size Rule Applied: {lot} qty per lot")
      
        else:
            # --- RAASTA 2: STOCKS (Normal Quantity) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            final_quantity = int(total_quantity) # Stock fractions mein nahi hota
            print("---> [TERMINAL LOG] ✅ NSE Cash Stock Logic Applied (Fractions Not Allowed)")

        print(f"---> [TERMINAL LOG] Total allowed quantity: {final_quantity}")
        
        # 🛑 SAFETY LOCK 1: Zero Quantity Check
        if final_quantity <= 0:
            # YAHAN ADD KARO SUGGESTION LOGIC
            lot_size = self.market_lot_sizes.get(found_index, 1) if found_index else 1
            min_capital_needed = (SL_gap * lot_size) / (risk_per_trade_percentage / 100)
            
            msg = f"Risk per trade bohot kam hai. Kam se kam ₹{int(min_capital_needed)} capital chahiye ek lot ke liye!"
            print(f"---> [TERMINAL LOG] ❌ REJECTED: {msg}")
            return {
                "status": "error", 
                "message": msg, 
                "suggestion": f"Bhai, is SL ke sath trade lene ke liye kam se kam ₹{int(min_capital_needed)} capital chahiye.",
                "quantity": 0
            }
        
        # 5. THE BILLING (Margin Kitna Chahiye)
        capital_required = final_quantity * entry_price
        
        # --- THE LEVERAGE MAGIC ---
        capital_needed = capital_required / leverage  # (Yeh line pehle sirf index mein thi, ab theek kar di)

        if is_index_trade: # 👈 Modified
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
    