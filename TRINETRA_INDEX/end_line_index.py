# === KHATRA CHECK MODULE (NSE/BSE Circuit Breaker) ===

class Khatra_Manager:
    def __init__(self, ek_din_ka_risk):
        # Jab din shuru hoga, user apni aukaat (limit) batayega
        self.ek_din_ka_risk = ek_din_ka_risk  # Guard ne limit ko apne dimaag mein likha
        self.ek_din_ka_total_loss = 0.0  # Shuru mein loss zero hai

    def check_trade_aukaat(self, ek_trade_ka_risk):
        """Ye function har naye trade se pehle check karega ki trade lena safe hai ya nahi"""
        
        # Rule 1: Kya ek trade ka risk poore din ki aukaat se bada hai?
        if ek_trade_ka_risk > self.ek_din_ka_risk:
            return False, f"❌ ERROR: Ek trade ka risk (₹{ek_trade_ka_risk}) aapke Daily Limit (₹{self.ek_din_ka_risk}) se bada hai!"

        # Rule 2: Kya aaj ka daily limit ALREADY hit ho chuka hai?
        if (self.ek_din_ka_total_loss + ek_trade_ka_risk) >= self.ek_din_ka_risk:
            return False, "⛔ SYSTEM LOCKED: Aapka aaj ka NSE Daily Stoploss limit hit ho chuka hai. Terminal band karo aur kal aana!"

        # Rule 3: WARNING! Kya limit ke 80% ke paas pohoch gaye hain?
        if self.ek_din_ka_total_loss >= (self.ek_din_ka_risk * 0.8):
            print(f"\n⚠️ WARNING: Aap apne daily limit ke bohot paas hain! (Current Loss: ₹{self.ek_din_ka_total_loss})")
            print("Take Control! Dhyan se F&O / Equity trade lein. Capital bachayein.")

        # Agar sab theek hai toh Hari Jhandi (Green Signal) de do
        return True, "✅ SAFE: NSE Trade Allowed"

    def update_loss(self, loss_amount):
        """Jab kisi trade mein loss hoga, toh ye function total loss ko update karega"""
        self.ek_din_ka_total_loss += loss_amount
        print(f"📉 Khata Updated: Aaj ka Total Loss ab ₹{self.ek_din_ka_total_loss} ho gaya hai (Limit: ₹{self.ek_din_ka_risk})")

    
# # The "Hiring" Formula (Object Banane ka Tarika):
# # [Worker ka Naam] = [Job ka Title/Class] ( [Shuruati Instruction/Data] )

# # The "Action / Kaam Karwao" Formula:
# # [Worker Ka Naam] . [Kaam / Action ka Naam] ( [Kaam ki Detail / Data] )

if __name__ == "__main__":
    
    # 1. Guard ko duty di
    guard_ki_limit = float(input("Enter the daily loss (Limit): ₹"))
    guard = Khatra_Manager(guard_ki_limit)

    while True:
        # User se pucho ki is trade mein kitna risk le rahe ho
        current_risk = float(input("\n👉 Naye trade ka risk kitna hai? ₹"))

        # 2. Guard se pucha (Risk amount pass kiya)
        is_safe, message = guard.check_trade_aukaat(current_risk)
        
        # 3. NORMAL IF-ELSE LOGIC:
        if is_safe == True:
            print(message)               
            # Guard ko wahi risk amount do loss update karne ke liye
            guard.update_loss(current_risk)      
            
        else:
            print(message)               
            print("🛑 Guard ne trade rok diya, koi loss update nahi hoga.")
            break