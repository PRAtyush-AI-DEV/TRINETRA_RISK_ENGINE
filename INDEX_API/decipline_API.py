import time

class Trinetra_Discipline:
    def __init__(self):
        # --- YE RAHE AAPKE VARIABLES (EK BHI NAAM CHANGE NAHI HUA HAI) ---
        self.current_max_trades = 0    # abhi intao zero hai
        self.trades_taken = 0         # abhi ek bhi tradenhi liya gaya hai
        self.bonus_trade_used = False # abhi bonus trade use nhi hua hai
        self.cooldown_start_time = None # timer abhi zero pr set hai
        self.hard_lock_activated = False 
        # 👇 YEH NAYI LINE ADD KAR DO
        self.current_mode = ""  # Shuru mein mode ekdum khali hai

    # --- FUNCTION 1: MAIN LOGIC (API Optimized) ---
    def check_trade_logic(self, current_trades, request_bonus_trade=False):
        """
        API se request aayegi. 
        'request_bonus_trade' tab True hoga jab frontend se user Bonus Trade ke liye "YES" bolega.
        """
        self.trades_taken = current_trades

        # --- SABSE PEHLE: HARD LOCK CHECK ---
        if self.hard_lock_activated:
            return {
                "allowed": False,
                "status": "HARD_LOCK",
                "message": "❌ HARD LOCK ACTIVATED: Indian Market System is closed. Terminal Band Karo!"
            }

        # --- PHASE 1: Normal Trading ---
        if self.trades_taken < self.current_max_trades:
            return {
                "allowed": True,
                "status": "NORMAL_TRADE",
                "message": f"✅ SUCCESS: NSE Trade {self.trades_taken + 1} Approved."
            }

        # --- PHASE 2: Limit Hit & Cooldown / Bonus Trade Logic ---
        elif self.trades_taken == self.current_max_trades:
            
            # Agar bonus trade pehle hi use ho chuka hai, toh hard lock lagao
            if self.bonus_trade_used:
                self.hard_lock_activated = True
                return {
                    "allowed": False,
                    "status": "HARD_LOCK",
                    "message": "🛑 Limit Cross ho chuki hai. Hard lock activated."
                }

            # Agar API request mein User ne explicit Bonus trade maanga hai (Frontend se "YES" aaya)
            if request_bonus_trade:
                self.bonus_trade_used = True
                self.hard_lock_activated = True 
                return {
                    "allowed": True,
                    "status": "BONUS_APPROVED",
                    "message": f"✅ BONUS TRADE Approved for Trade {self.trades_taken + 1}. Lock Armed."
                }
            
            # Agar limit hit hui hai aur ab tak bonus trade nahi maanga gaya
            # Toh hum API ko signal bhejenge ki user se puchho (Popup frontend par dikhega)
            else:
                return {
                    "allowed": False,
                    "status": "COOLDOWN_AND_PROMPT",
                    "cooldown_seconds": 10, # Frontend 10 second ka timer dikhayega
                    "message": f"🛑 OVERTRADING ALERT: {self.current_max_trades} trades pure ho gaye. 10 sec cooldown ke baad Bonus trade lenge?"
                }
        
        # --- PHASE 3: Error Failsafe ---
        else:
            self.hard_lock_activated = True
            return {
                "allowed": False,
                "status": "CRITICAL_ERROR",
                "message": "🛑 Critical Error: SEBI Limit Cross!"
            }

# Setup ke liye ab function ki jagah hum directly properties set karenge jab `main.py` me `set_trader_type` hit hoga. 
# Wo logic already aapke main.py me sahi likha hai.