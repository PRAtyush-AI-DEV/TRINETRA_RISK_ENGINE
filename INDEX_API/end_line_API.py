# === KHATRA CHECK MODULE (NSE/BSE Circuit Breaker) ===

class Khatra_Manager:
    def __init__(self, ek_din_ka_risk):
        # Jab din shuru hoga, user apni aukaat (limit) batayega
        self.ek_din_ka_risk = float(ek_din_ka_risk)  # Guard ne limit ko apne dimaag mein likha
        self.ek_din_ka_total_loss = 0.0  # Shuru mein loss zero hai
        print(f"---> [TERMINAL LOG] 🛡️ Khatra Manager Ready! Daily Limit: ₹{self.ek_din_ka_risk}")

    # 👈 FIX: Bracket mein 'quantity' add kiya gaya hai
    def check_trade_aukaat(self, ek_trade_ka_risk, quantity):
        """Ye function API se har naye trade se pehle call hoga"""
        bacha_hua_risk = self.ek_din_ka_risk - self.ek_din_ka_total_loss
        print(f"\n---> [TERMINAL LOG] 🔍 Risk Check: Trade Risk ₹{ek_trade_ka_risk} | Bachi Limit: ₹{bacha_hua_risk}")

        # Rule 1: Limit already ZERO ya Negative (Ab Trinetra nahi bacha sakta)
        if bacha_hua_risk <= 0:
            msg = "⛔ SYSTEM LOCKED: Aaj ka poora loss limit hit ho chuka hai. Terminal band karo aur kal aana!"
            print(f"---> [TERMINAL LOG] {msg}")
            return False, msg, None

        # Rule 2: Trade ka risk bachi hui aukaat se bada hai -> THE SMART SOLUTION 💡
        if ek_trade_ka_risk > bacha_hua_risk:
            # Solution Formula: Bacha hua paisa / Quantity = Naya SL Points
            if quantity > 0:
                naya_sl_points = bacha_hua_risk / quantity
                msg = f"❌ ERROR: Is trade ka risk (₹{ek_trade_ka_risk}) bachi hui limit (₹{bacha_hua_risk}) se zyada hai."

                # Trinetra ki Advice
                solution = f"💡 TRINETRA SOLUTION: Agar ye trade lena hi hai, toh apna Stoploss (SL) max {int(naya_sl_points)} points ka rakho. Tab aapki limit cross nahi hogi!"
                
                print(f"---> [TERMINAL LOG] {msg}")
                print(f"---> [TERMINAL LOG] {solution}")
                return False, msg, solution
            else:
                return False, "❌ ERROR: Quantity 0 hai, trade nahi ho sakta.", None
            
        # Rule 3: WARNING! Kya limit ke 80% ke paas pohoch gaye hain?
        if (self.ek_din_ka_total_loss + ek_trade_ka_risk) >= (self.ek_din_ka_risk * 0.8):
            print(f"---> [TERMINAL LOG] ⚠️ WARNING: Aap daily limit ke 80% ke paas hain! (Loss: ₹{self.ek_din_ka_total_loss})")
            return True, "⚠️ WARNING: Limit ke 80% ke paas ho, par trade allowed hai. Dhyan se!", None

        # Agar sab theek hai toh Hari Jhandi (Green Signal)
        print("---> [TERMINAL LOG] ✅ SAFE: NSE Trade Allowed")
        return True, "✅ SAFE: NSE Trade Allowed", None

    def update_loss(self, loss_amount):
        """Jab API se SL Hit ka signal aayega, tab ye loss update karega"""
        self.ek_din_ka_total_loss += loss_amount
        print(f"---> [TERMINAL LOG] 📉 Khata Updated: Aaj ka Total Loss ab ₹{self.ek_din_ka_total_loss} ho gaya hai (Limit: ₹{self.ek_din_ka_risk})")


def show_live_dashboard(self):
        """Terminal mein VIP style scoreboard dikhane ke liye"""
        bacha_hua = self.ek_din_ka_risk - self.ek_din_ka_total_loss
        
        # Color aur style ke liye ASCII Box
        print("\n" + "=".center(50, "="))
        print(" 🔱 TRINETRA LIVE SCOREBOARD 🔱 ".center(50, " "))
        print("=".center(50, "="))
        print(f" 💼 Daily Limit   : ₹{self.ek_din_ka_risk}")
        print(f" 📉 Current Loss  : ₹{self.ek_din_ka_total_loss}")
        
        # Agar aukaat khatam toh RED (🔴), bachi hai toh GREEN (🟢)
        if bacha_hua > 0:
            print(f" 🟢 Bachi Aukaat  : ₹{bacha_hua}")
        else:
            print(f" 🔴 Bachi Aukaat  : ₹{bacha_hua} (LIMIT CROSSED!)")
        print("=".center(50, "=") + "\n")