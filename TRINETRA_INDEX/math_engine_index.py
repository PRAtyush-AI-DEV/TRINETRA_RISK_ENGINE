import math

class Trinetra_Calculator:
    def __init__(self):
        # YAHAN SE CRYPTO GAYAB: Sirf Indian Markets bache hain!
       # ✅ LATEST 2026 NSE LOT SIZES (Updated per SEBI guidelines)
        self.market_lot_sizes = {
            "NIFTY": 65,
            "BANKNIFTY": 30,
            "FINNIFTY": 60,
            "MIDCPNIFTY": 120,
            "NIFTYNXT50": 25,
            "SENSEX": 10  # BSE ka lot size
        }
        
        # Index names list ko bhi update kar do
        self.index_names = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "NIFTYNXT50", "SENSEX"]
        print("✅ INDIAN TRINETRA MATH ENGINE INITIATED...")


    def get_trade_quantity(self, symbol, current_capital, entry_price, sl_price, risk_per_trade_percentage, leverage ):
        print(f"\n--- 🧮 CALCULATING (INDIAN MARKET): {symbol.upper()} ---")

        # 1. TOTAL RISK (Paise ka Hisaab - Sirf Rupay)
    
        risk_amount_in_rupees = current_capital * (risk_per_trade_percentage / 100)
        
        # Crypto check hata diya, sirf INR print hoga
        print(f"Risk per trade: ₹{risk_amount_in_rupees:.2f}")

        # 2. SL GAP (Premium ya Stock Difference)
        SL_gap = abs(entry_price - sl_price)
        print(f"SL gap: {SL_gap} points")

        # Error Check: Entry aur SL same nahi ho sakte
        if SL_gap == 0:
            print("❌ Error: Entry aur SL same nahi ho sakte!")
            return None

        # --- SMART TRAFFIC POLICE (Routing & Leverage) ---
        symbol = symbol.upper()
        
        # RAASTA 1: INDEX (Options/Futures - Leverage 1x hi rahega)
        if symbol in self.index_names:
            print(f"⚠️ ALERT: Index Option buying mein koi leverage nahi milta. Set to 1x!")
            leverage = 1
        

        # RAASTA 3: STOCKS (Intraday 5x - Indian Market ka default)
        else:
            print(f"ℹ️ Path: NSE Equity Intraday. Fixed 5x leverage applied!")
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
            print(f"✅ F&O Lot Size Rule Applied: {lot} qty per lot")
      
        else:
            # --- RAASTA 3: STOCKS (Normal Quantity) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            final_quantity = int(total_quantity) # Stock fractions mein nahi hota
            print(f"✅ NSE Cash Stock Logic Applied (Fractions Not Allowed)")

        # 🛑 SAFETY LOCK 1: Zero Quantity Check
        print(f"Total allowed quantity: {final_quantity}")
        if final_quantity <= 0:
            print("❌ REJECTED: Risk per trade bohot kam hai, is SL ke saath ek bhi lot nahi aayega!")
            return None
        
        
        # 5. THE BILLING (Margin Kitna Chahiye)
        capital_required = final_quantity * entry_price
        
        # --- THE LEVERAGE MAGIC ---
        if symbol in self.index_names:
            capital_needed = capital_required / leverage
            print(f"Total Contract Value: ₹{capital_required:.2f}")
            print(f"Margin Needed (After {leverage}x SEBI Leverage): ₹{capital_needed:.2f}")  

        else:
            # --- RAASTA 3: STOCKS (Normal Quantity) ---
            total_quantity = risk_amount_in_rupees / SL_gap
            final_quantity = int(total_quantity) # Stock fractions mein nahi hota
            print(f"✅ NSE Cash Stock Logic Applied (Fractions Not Allowed)")


        # 6. --- REALITY CHECK (Aukaat Check) 
        margin_in_rupees = capital_needed

        # Kya paas mein paisa hai?
        if margin_in_rupees > current_capital:
            print(f"❌ REJECTED: Margin kam pad raha hai!")
            print(f"👉 Broker maang raha hai: ₹{margin_in_rupees:.2f} | Aapke paas hai: ₹{current_capital}")
            return None

        if final_quantity <= 0:
            print("❌ REJECTED: Risk calculation error.")
            return None
        
        return final_quantity

# --- TESTING BLOCK (Manager) ---
if __name__ == "__main__":
    print("--- TRINETRA: NSE/BSE POSITION SIZING ENGINE ---")
    try:
        user_ka_capital = float(input("👉 Total Capital (₹): "))
        trinetra = Trinetra_Calculator()

        while True:
            print("\n" + "="*30)

            symbol = input("🔹 Symbol (NIFTY/BANKNIFTY/RELIANCE): ").upper()
            
            if symbol.isdigit():
                 print(f"❌ ERROR: '{symbol}' ek symbol hai, number nahi!")
                 continue
                 
            entry  = float(input("🔹 Entry Price : "))
            sl     = float(input("🔹 Stop Loss: "))
            risk   = float(input("🔹 Risk % (e.g. 1 or 2): "))
            
            # Leverage poochega par Indian mode mein ignore karke apne aap override kar dega
            leverage = float(input("🔹 Leverage (Koi fayda nahi, SEBI rules chalenge!): "))
            
            trinetra.get_trade_quantity(symbol, user_ka_capital, entry, sl, risk, leverage )
            
            if input("\nEk aur trade check karna hai? (y/n): ").lower() != 'y':
                break
    except ValueError:
        print("⚠️ Error: Galat input! Sirf numbers daalein.")
    print("\n👋 Calculator Closed.")