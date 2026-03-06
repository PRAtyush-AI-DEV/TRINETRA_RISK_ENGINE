import tkinter as tk
from tkinter import messagebox

print("\n--- 🔱 TRINETRA: PROFIT SECURE (INDIAN MARKET DUAL MODE) 🔱 ---")

class paisa_nikalo:
    def __init__(self, symbol , trader_type, entry_price, target_price, total_quantity, current_sl):
        # Data ko class ke andar set kar rahe hain
        self.symbol = symbol.upper()
        self.trader_type = trader_type     
        self.entry_price = float(entry_price)    
        self.target_price = float(target_price)  
        self.total_quantity = float(total_quantity)        
        self.current_sl = float(current_sl)    

        # YAHAN SE CRYPTO GAYAB: Sirf Indian Markets bache hain
        self.market_lot_sizes = {
            "NIFTY": 75, "BANKNIFTY": 15, "FINNIFTY": 40, "SENSEX": 10
        }
        self.index_names = ["NIFTY", "BANKNIFTY", "FINNIFTY", "SENSEX"]
        # --- SAFETY CHECK (Logic Validation) ---

        if self.trader_type == 'B':
                if self.current_sl >= self.entry_price or self.target_price <= self.entry_price:
                    print("❌ ERROR: Buy trade mein Target upar aur SL neeche hona chahiye!")
                    print("🛑 You Are Converted buyer (B) to seller (S)--(next time be aware ) -- ")
                    self.trader_type='S'
            
                
        elif self.trader_type == 'S':
                 if self.current_sl <= self.entry_price or self.target_price >= self.entry_price:
                    print("❌ ERROR: Sell trade mein Target neeche aur SL upar hona chahiye!")
                    print("🛑 You Are Converted seller (S) to buyer (B)--(next time be aware ) -- ")
                    self.trader_type='B'
        

        # -- 🎯 THE SMART VERSION (Works for both B and S) ---
        profit_ka_total_move = self.target_price - self.entry_price
        sl_ka_total_move = self.entry_price - self.current_sl

        # Target ki taraf 70% move
        self.profit_70_percent = self.entry_price + (profit_ka_total_move * 0.70)
        
        # SL area ko 30% par lana (Buy mein - hota hai, Sell mein - - milke + ho jata hai)
        self.sl_30_percent = self.entry_price - (sl_ka_total_move * 0.30)

        # Trackers
        self.is_70_done = False
        self.target_popup_shown = False 

        print("\n" + "="*50)
        print(f"🚀 NSE {self.trader_type} TRADE START | Qty: {self.total_quantity} | SL: {self.current_sl}")
        print(f"🎯 70% Milestone: {self.profit_70_percent} | Safe SL (30%): {self.sl_30_percent}")
        print("="*50)

    # ==========================================
    # 🏃‍♂️ MAIN TRACKING FUNCTION (Loop yahan chalega)
    # ==========================================
    def start_tracking(self , curret_price):
        # --- MARKET SIMULATION LOOP ---
        while True:
            try:
                # Abhi manual hai, aage chal kar ise bhi API se jod denge!
                market_kaha_chl_raha = float(input("\n👉 Current NSE Market Price: "))
            except ValueError:
                continue

            # Check if Target is Hit
            target_hit = ((self.trader_type == 'B' and market_kaha_chl_raha >= self.target_price) or \
                          (self.trader_type == 'S' and market_kaha_chl_raha <= self.target_price)) and not self.target_popup_shown

            # Check if Stop Loss is Hit
            sl_hit = (self.trader_type == 'B' and market_kaha_chl_raha <= self.current_sl) or \
                     (self.trader_type == 'S' and market_kaha_chl_raha >= self.current_sl)
                     
            # Check if 70% Level is Hit 
            _70_hit = ((self.trader_type == 'B' and market_kaha_chl_raha >= self.profit_70_percent) or \
                           (self.trader_type == 'S' and market_kaha_chl_raha <= self.profit_70_percent)) and not self.is_70_done and not self.target_popup_shown

            # --- ACTION 1: TARGET HIT ---
            if target_hit:
                print(f"\n🎉 MUBARAK HO! Target Hit ({market_kaha_chl_raha}). Pop-up check karein...")
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)

                user_choice = messagebox.askyesno(
                    "TRINETRA: NSE PROFIT ALERT 💰", 
                    f"Market Price: {market_kaha_chl_raha}\nTarget Achieved!\n\n"
                    "YES ➤ Exit All (Full Profit)\n"
                    "NO  ➤ 50% Book + Trail SL to Cost (Risk Free)"
                )
                root.destroy()
                
                self.target_popup_shown = True

               # ✅ EXIT BLOCK
                if user_choice: # (If True / Yes)
                    total_profit = abs(market_kaha_chl_raha - self.entry_price) * self.total_quantity
                    print(f"✅ FULL EXIT. Total Profit: {self.currency}{total_profit:.2f}")
                    return total_profit
                
                else: # (If False / No)
                    half_qty = (self.total_quantity / 2) 
                    booked_profit = abs(market_kaha_chl_raha - self.entry_price) * half_qty
                    
                    self.total_quantity = self.total_quantity - half_qty 
                    self.current_sl = self.entry_price  
                    
                    print(f"🛡️ SAFE MODE: {self.currency}{booked_profit:.2f} Locked.")
                    print(f"📦 Remaining Qty: {self.total_quantity} | New SL: {self.current_sl} (Breakeven)")
                    print(f"👋 TRINETRA DUTY OVER: Bachi hui {half_qty} qty ka SL Cost par hai. Ab aage aap khud manage karein!")
                    return booked_profit


            # --- ACTION 2: STOP LOSS HIT ---
            elif sl_hit:
                    loss = abs(self.entry_price - self.current_sl) * self.total_quantity
                    if self.current_sl == self.entry_price:
                        print(f"⏹️ TRAILING SL HIT at Cost ({market_kaha_chl_raha}). Trade closed at NO LOSS for remaining qty!")
                    else:
                        print(f"❌ STOP LOSS HIT at {market_kaha_chl_raha}. Loss: ₹{loss:.2f}")
                        return -loss
                     
                
            # --- ACTION 3: 70% LEVEL HIT ---
            elif _70_hit:
                self.current_sl = self.sl_30_percent
                self.is_70_done = True
                print(f"✅ 70% Area Covered! SL shifted to 30% risk area ({self.current_sl})")
                
            else:
                print(f"⏳ Holding NSE Position... (Tgt: {self.target_price} | SL: {self.current_sl} | Qty: {self.total_quantity})")


# ==========================================
# 🧪 TESTING SECTION: YAHAN SE INPUT SHURU HONGE
# ==========================================
if __name__ == "__main__":
    try:
        symbol = input("Enter the symbol (e.g., NIFTY/RELIANCE): ")
        t_type = input("👉 Type (B for Buy / S for Sell): ").upper()
        e_price = float(input("🔵 Entry Price: "))
        t_price = float(input("🟢 Target Price: "))
        qty = float(input("📦 Quantity: "))
        s_loss = float(input("🔴 Initial Stop Loss: "))

        # Class ko input ke sath call kar rahe hain
        test_trade = paisa_nikalo(symbol , t_type, e_price, t_price, qty, s_loss)
        
        # Tracking chalu
        test_trade.start_tracking()

    except ValueError:
        print("❌ Sahab, sahi numbers daaliye!")