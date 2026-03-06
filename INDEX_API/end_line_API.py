# === KHATRA CHECK MODULE (NSE/BSE Circuit Breaker) ===

class Khatra_Manager:
    def __init__(self, ek_din_ka_risk):
        # Jab din shuru hoga, user apni aukaat (limit) batayega
        self.ek_din_ka_risk = float(ek_din_ka_risk)  # Guard ne limit ko apne dimaag mein likha
        self.ek_din_ka_total_loss = 0.0  # Shuru mein loss zero hai
        print(f"---> [TERMINAL LOG] 🛡️ Khatra Manager Ready! Daily Limit: ₹{self.ek_din_ka_risk}")

    def check_trade_aukaat(self, ek_trade_ka_risk):
        """Ye function API se har naye trade se pehle call hoga"""
        
        print(f"\n---> [TERMINAL LOG] 🔍 Risk Check: Naye trade ka risk ₹{ek_trade_ka_risk}")

        # Rule 1: Kya ek trade ka risk poore din ki aukaat se bada hai?
        if ek_trade_ka_risk > self.ek_din_ka_risk:
            msg = f"❌ ERROR: Ek trade ka risk (₹{ek_trade_ka_risk}) aapke Daily Limit (₹{self.ek_din_ka_risk}) se bada hai!"
            print(f"---> [TERMINAL LOG] {msg}")
            return False, msg

        # Rule 2: Kya aaj ka daily limit ALREADY hit ho chuka hai?
        if (self.ek_din_ka_total_loss + ek_trade_ka_risk) > self.ek_din_ka_risk:
            msg = "⛔ SYSTEM LOCKED: Aapka aaj ka NSE Daily Stoploss limit hit ho chuka hai. Terminal band karo aur kal aana!"
            print(f"---> [TERMINAL LOG] {msg}")
            return False, msg

        # Rule 3: WARNING! Kya limit ke 80% ke paas pohoch gaye hain?
        if (self.ek_din_ka_total_loss + ek_trade_ka_risk) >= (self.ek_din_ka_risk * 0.8):
            print(f"---> [TERMINAL LOG] ⚠️ WARNING: Aap apne daily limit ke bohot paas hain! (Current Loss: ₹{self.ek_din_ka_total_loss})")
            print("---> [TERMINAL LOG] Take Control! Dhyan se F&O / Equity trade lein. Capital bachayein.")
            return True, "⚠️ WARNING: Limit ke 80% ke paas ho, par trade allowed hai. Dhyan se!"

        # Agar sab theek hai toh Hari Jhandi (Green Signal) de do
        print("---> [TERMINAL LOG] ✅ SAFE: NSE Trade Allowed")
        return True, "✅ SAFE: NSE Trade Allowed"

    def update_loss(self, loss_amount):
        """Jab API se SL Hit ka signal aayega, tab ye loss update karega"""
        self.ek_din_ka_total_loss += loss_amount
        print(f"---> [TERMINAL LOG] 📉 Khata Updated: Aaj ka Total Loss ab ₹{self.ek_din_ka_total_loss} ho gaya hai (Limit: ₹{self.ek_din_ka_risk})")