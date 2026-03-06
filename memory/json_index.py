import json
import os
from datetime import date

class Trinetra_memory:
    def __init__(self):
        # 1. Pehle pata karo ki ye file kahan baithi hai
        base_path = os.path.dirname(os.path.abspath(__file__)) 
        
        # 2. Isse ek step piche (Main Project Folder) ka address pakka karo
        parent_path = os.path.dirname(base_path) 
        
        # 3. Ab file ko wahi 'parent' folder mein save karo
        self.file_name = os.path.join(parent_path, "Trinetra_Master_Memory.json")

        # 🌟 DEFAULT DATA: Naye din ka khaali dimaag
        self.default_data = {
            "last_date": str(date.today()), # Aaj ki date save hogi
            "discipline": {
                "current_mode": "",
                "current_max_trades": 0,
                "trades_taken": 0,
                "bonus_trade_used": False,
                "hard_lock_activated": False
            },
            "khatra": {
                "ek_din_ka_risk": 0.0,
                "ek_din_ka_total_loss": 0.0
            }
        }

    # ==========================================
    # 📖 DATA LOAD (With Smart Date Reset & Crash Protection)
    # ==========================================
    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    saved_data = json.load(file)
                
                # 🕒 DATE CHECK: Kya panna palat gaya hai?
                aaj_ki_date = str(date.today())
                purani_date = saved_data.get("last_date", "")

                if aaj_ki_date != purani_date:
                    print("---> [TERMINAL LOG] 🌅 [NEW DAY] Naya din shuru! Trinetra ne journal reset kar diya.")
                    # Naya din hai, toh purani file hata kar default save kar dete hain
                    self.save_data(self.default_data) 
                    return self.default_data
                else:
                    print("---> [TERMINAL LOG] ✅ [MEMORY] Purani yaadein wapas mil gayi!")
                    return saved_data
                    
            except json.JSONDecodeError:
                # Agar JSON file corrupt ho gayi ho toh system crash na ho
                print("---> [TERMINAL LOG] ⚠️ [MEMORY WARNING] File corrupt mili. Default memory load ki jaa rahi hai.")
                return self.default_data
        else:
            print("---> [TERMINAL LOG] 📁 [MEMORY] Nayi file banayi jaa rahi hai.")
            return self.default_data

    # ==========================================
    # 💾 DATA SAVE (Diary mein likhna)
    # ==========================================
    def save_data(self, naya_data):
        # Save karte waqt aaj ki date stamp zaroor lagao
        naya_data["last_date"] = str(date.today())
        
        with open(self.file_name, "w") as file:
            json.dump(naya_data, file, indent=4)
            print("---> [TERMINAL LOG] 💾 [MEMORY] Data Master Journal mein save ho gaya!")