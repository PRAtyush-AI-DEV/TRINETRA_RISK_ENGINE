import time
import ctypes 
import sys

class Trinetra_Discipline:
    def __init__(self):
        # --- YE RAHE AAPKE VARIABLES (EK BHI NAAM CHANGE NAHI HUA HAI) ---
        self.current_max_trades = 0    # abhi intao zero hai
        self.trades_taken = 0         # abhi ek bhi tradenhi liya gaya hai
        self.bonus_trade_used = False # abhi bonus trade use nhi hua hai
        self.cooldown_start_time = None # timer abhi zero pr set hai
        self.hard_lock_activated = False 

    # --- 3. POP-UP FUNCTION ---
    def show_popup(self, title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x0)

    # --- FUNCTION 1: SETUP ---
    def initial_setup(self):
        while True:
            trader_type = input("👉 Enter trader type (scalper/intraday): ").lower()

            if trader_type == "scalper":
                self.current_max_trades = 3
                print("✅ Mode: INDEX SCALPER (Limit: 3 Trades)")
                break

            elif trader_type == "intraday":
                self.current_max_trades = 2
                print("✅ Mode: INDEX INTRADAY (Limit: 2 Trades)")
                break

            else:
                print("⚠️ Check the spelling (Type 'scalper' or 'intraday')")

    # --- FUNCTION 2: MAIN LOGIC ---
    def check_trade_logic(self, current_trades):
        # Saare global yahan self ban gaye hain
        self.trades_taken = current_trades

        # --- SABSE PEHLE: HARD LOCK CHECK ---
        if self.hard_lock_activated:
            print("\n❌ HARD LOCK ACTIVATED: Indian Market System is closed.")
            return False 

        # --- PHASE 1: Normal Trading ---
        if self.trades_taken < self.current_max_trades:
            print(f"✅ SUCCESS: NSE Trade {self.trades_taken + 1} Approved.")
            return True 

        # --- PHASE 2: Limit Hit & Cooldown ---
        elif self.trades_taken == self.current_max_trades:
            print(f"\n🛑 OVERTRADING ALERT: {self.current_max_trades} trades pure ho gaye.")
            self.show_popup("Trinetra Alert", "Limit Reached! Screen se hato.")

            # ✅ SIMPLE TIMER 
            remaining = 10
            while remaining > 0:
                print(f"🚫 Wait... {remaining}s left to calm down   ", end="\r")
                time.sleep(1)
                remaining -= 1
            
            print("\n✅ Cooldown Pura Hua! Dimaag shaant?")
         
            if self.bonus_trade_used == False:
                print("🔓 UNLOCK: Aap wapas NSE market dekh sakte hain.")
                print("⚠️ WARNING: Ye aaj ka AAKHRI (Bonus) trade hai. Overtrading mat karna.")

                confirm = input("👉 Type 'YES' for Bonus Trade and Exit: ").strip().upper()
                
                if confirm == "YES":
                    self.bonus_trade_used = True
                    self.hard_lock_activated = True 
                    print(f"✅ SUCCESS: Index Trade {self.trades_taken + 1} Approved.")
                    print(f"✅ BONUS TRADE Approved. Lock Armed.")
                    return True 
                else:
                    print("🚫 Bonus Trade Cancelled. Good Discipline!")
                    return False
            else:
                print(f"Hard lock activated: {self.hard_lock_activated}")
                return False
        
        else:
            print("🛑 Critical Error: SEBI Limit Cross!")
            return False

# ======================================================
# 🧪 REALISTIC MANUAL TEST (Starts from 0)
# ======================================================
if __name__ == "__main__":
    print("--- TRINETRA: Indian Market Discipline System ---")
    print("\n--- 🧪 REALISTIC TEST MODE ON ---")
    
    # 1. Object banaya (User 1)
    user1 = Trinetra_Discipline()
    
    # 2. Setup call kiya
    user1.initial_setup()
    
    # 3. TRADE START FROM ZERO
    live_counter = 0 
    print(f"\n🏁 Market Open. Current Trades: {live_counter}")
    
    while True:
        try:
            print("\n" + "="*40)
            print(f"📊 STATUS: [ Trades Done: {live_counter} / Limit: {user1.current_max_trades} ]")
            print("-" * 40)
            
            user_ka_input = input("👉 Action lein ('BUY' likhein ya 'EXIT'): ").strip().upper()
            
            if user_ka_input == 'EXIT':
                print("👋 Session Closed. Exiting...")
                break
            
            elif user_ka_input == 'BUY':
                print(f"\n... Analyzing Nifty/BankNifty Trade {live_counter + 1} Logic ...")
                time.sleep(1) 

                # Object ke logic ko call kiya
                is_allowed = user1.check_trade_logic(live_counter)

                if is_allowed == True:
                    print(f"🚀 ORDER EXECUTED! (Trade {live_counter + 1} Complete)")
                    live_counter += 1  
                
                if user1.hard_lock_activated == True:
                     print("\n🛑 SYSTEM LOCKED: Aaj ka quota khatam. Terminal Band Karo!")
                     break
            else:
                print("⚠️ Ghalat command! Bas 'BUY' likho.")
            
        except ValueError:
            print("⚠️ Error aaya!")

    print("\n--- 🧪 TEST FINISHED ---")