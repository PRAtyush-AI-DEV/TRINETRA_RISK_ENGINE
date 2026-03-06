# --- main_index.py (THE INDIAN COMMANDER) ---
import time
import sys
import os

# --- THE FOLDER BRIDGE (Shared Master Memory ke liye) ---
current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.dirname(current_folder)
if parent_folder not in sys.path:
    sys.path.append(parent_folder)
# ---------------------

# STEP 1: Sabhi NAYI INDIAN Files se unki Classes ko import karna
# Dhyan dein: Apni files ka exact naam yahan likhein (maine _index lagaya hai)
from json_index import Trinetra_memory
from decipline_rules_index import Trinetra_Discipline
from math_engine_index import Trinetra_Calculator
from end_line_index import Khatra_Manager
from profit_tralling_sl_index import paisa_nikalo

def run_trinetra():
    print("🔱 TRINETRA (INDIAN MARKET) SYSTEM STARTING... 🔱\n")

    # STEP 2: Central Master Memory Load Karna
    memory = Trinetra_memory()
    system_data = memory.load_data() 

    # STEP 3: Basic Input (Jo poore din mein sirf ek baar chahiye)
    try:
         # 1. Check karo kya memory mein pehle se Risk Limit set hai?
        saved_risk = system_data["khatra"]["ek_din_ka_risk"]

        if saved_risk == 0.0:
            # Pehli baar setup ho raha hai
            daily_loss_limit = float(input("\n👉 Aaj ka Total Daily Loss Limit (₹) set karein: "))
        else:
            # Purana data mil gaya, usey hi lock kar do
            daily_loss_limit = saved_risk
            print(f"✅ LOCKED Daily Loss Limit (Memory): ₹{daily_loss_limit}")
        
        total_capital = float(input("👉 Trading Capital (Balance) kitna hai?: "))
    except ValueError:
        print("❌ Sahi numbers daaliye! System band ho raha hai.")
        sys.exit()

    # STEP 4: Baaki Objects Banana aur Setup Karna
    guard = Khatra_Manager(daily_loss_limit)
    discipline = Trinetra_Discipline()
    calculator = Trinetra_Calculator()
    
    # ==========================================
    # 🌟 DATA SYNC LOGIC: MASTER MEMORY SE DATA WAPAS LAANA 
    # ==========================================
    discipline.current_max_trades = system_data["discipline"]["current_max_trades"]
    discipline.trades_taken = system_data["discipline"]["trades_taken"]
    discipline.bonus_trade_used = system_data["discipline"]["bonus_trade_used"]
    discipline.hard_lock_activated = system_data["discipline"]["hard_lock_activated"]
    
    guard.ek_din_ka_total_loss = system_data["khatra"]["ek_din_ka_total_loss"]
    trade_counter = discipline.trades_taken 

    # TRADER TYPE LOCK LOGIC
    if discipline.current_max_trades == 0:
        discipline.initial_setup() 
        print("\n✅ Setup Ready Hai! NSE Trading Shuru Karein.")
        time.sleep(2)
    else:
        mode_name = "INDEX SCALPER" if discipline.current_max_trades == 3 else "INDEX INTRADAY"
        print(f"\n🔒 LOCKED FOR TODAY: Aap pehle hi '{mode_name}' mode select kar chuke hain.")
        print(f"📊 Trades Completed: {trade_counter} / {discipline.current_max_trades}")
        print(f"📉 Current Loss Tracker: ₹{guard.ek_din_ka_total_loss}")
        print("\n✅ Welcome Back! Trading Resume Karein.")
        time.sleep(2)

    # ==========================================
    # STEP 5: THE MAIN TRADING LOOP 
    # ==========================================
    while True:
        print("\n" + "="*50)
        user_action = input("👉 Naya Trade lena hai? (Type 'BUY', 'SELL' ya 'EXIT'): ").strip().upper()

        if user_action == 'EXIT':
            break 

        elif user_action in ['BUY', 'SELL']:
            # 1. DISCIPLINE CHECK
            is_allowed = discipline.check_trade_logic(trade_counter)

            if not is_allowed:
                if discipline.hard_lock_activated:
                    print("🔒 System Locked. Aaj ke liye trading khatam.")
                    break 
                continue 

            # 2. TRADE KI DETAILS LENA
            print("\n--- 📝 NSE TRADE DETAILS ---")
            try:
                symbol = input("🔹 Symbol (NIFTY/BANKNIFTY/RELIANCE): ").upper()
                
                # 🚨 INDIAN API ABHI NAHI HAI, ISLIYE MANUAL INPUT LAGA RAHE HAIN
                entry_price = float(input("🔹 Current / Entry Price: "))
                
                sl_price = float(input("🔹 Stop Loss Price: "))
                target_price = float(input("🔹 Target Price: "))
                risk_percentage = float(input("🔹 Risk % per trade (e.g. 1 or 2): "))
                
            except ValueError:
                print("⚠️ Error: Galat input! Sirf numbers daalein.")
                continue 

            # 3. MATH ENGINE: Quantity Calculate Karna
            # Dhyan dein: Leverage 1 pass kar rahe hain kyunki Math Engine khud SEBI rules (5x ya 1x) laga lega
            final_quantity = calculator.get_trade_quantity(symbol, total_capital, entry_price, sl_price, risk_percentage, leverage=1)

            if final_quantity is None:
                print("❌ Math Engine ne reject kar diya. Trade Cancelled.")
                continue  

            # 4. KHATRA MANAGER (GUARD): Risk Check Karna
            current_trade_risk = total_capital * (risk_percentage / 100)
            is_safe, message = guard.check_trade_aukaat(current_trade_risk)

            if not is_safe:
                print(message)
                continue  
            else:
                print(message)
                print(f"✅ FINAL APPROVAL: {final_quantity} Quantity ke sath NSE trade confirm!")
                
                # 🚨 Yahan "Indian Shakti" (Broker API) ka order fire hoga jab hum use banayenge!
                # shoot_indian_order(symbol, user_action.lower(), final_quantity)
                
                trade_counter += 1 
                
                # 5. LIVE TRACKING (Paisa Nikalo)
                t_type = 'B' if user_action == 'BUY' else 'S'
                print("\n🚀 TRINETRA TRACKER ACTIVATED...")
                
                trade_tracker = paisa_nikalo(symbol , t_type, entry_price, target_price, final_quantity, sl_price)
                trade_tracker.start_tracking()

                # 6. TRADE KHATAM HONE KE BAAD LOSS UPDATE KARNA
                print("\n📊 Trade Status Report:")
                loss_input = input("👉 Agar is trade mein LOSS hua hai, toh amount daalein (Profit ya No-Loss ke liye 0 likhein): ")
                try:
                    actual_loss = float(loss_input)
                    if actual_loss > 0:
                        guard.update_loss(actual_loss)
                except ValueError:
                    print("⚠️ Invalid input. Loss ko 0 maan kar aage badh rahe hain.")
                    
        else:
            print("⚠️ Ghalat command! Bas 'BUY', 'SELL' ya 'EXIT' likho.")

    # ==========================================
    # STEP 6: SYSTEM EXIT & MASTER MEMORY SAVE
    # ==========================================
    print("\n💾 System band ho raha hai. Trinetra aaj ka data yaad rakh raha hai...")
    
    naya_data = {
        "discipline": {
            "current_max_trades": discipline.current_max_trades,
            "trades_taken": trade_counter,
            "bonus_trade_used": discipline.bonus_trade_used,
            "hard_lock_activated": discipline.hard_lock_activated
        },
        "khatra": {
            "ek_din_ka_total_loss": guard.ek_din_ka_total_loss
        }
    }
    
    memory.save_data(naya_data)
    print("\n🔱 TRINETRA (INDIAN) SYSTEM SUCCESSFULLY CLOSED 🔱")

# --- EXECUTION TRIGGER ---
if __name__ == "__main__":
    run_trinetra()