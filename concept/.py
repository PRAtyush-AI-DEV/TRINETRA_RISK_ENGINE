# ======================================================
# 🔱 ENGINE OBJECTS INITIATION (Startup Memory Load / State Hydration)
# ======================================================
print("\n---> [SYSTEM] Booting Up Trinetra Engines...")

# 🗄️ KADAM 1: Diary Kholna (The Memory Vault)
# GOLDEN FORMULA: DESTINATION (Left) = SOURCE (Right)
memory = Trinetra_memory()  # Record Keeper ko hire kiya
data = memory.load_data()   # Locker khola aur JSON diary ka poora data 'data' variable mein daal diya

# 🧮 KADAM 2: Math Engine (The Calculator)
# Logic: Yeh 'Stateless' engine hai. Ise kal ka kuch yaad nahi rakhna hota.
# Isliye isme humne JSON diary se koi data feed nahi kiya.
calculator = Trinetra_Calculator()

# 👮‍♂️ KADAM 3: Discipline Engine (The Rules Bouncer)
discipline = Trinetra_Discipline()  # Guard duty par aa gaya (Par abhi iska dimaag blank hai)

# 🧪 THE DOT FORMULA: [KISKA?] . [KYA?] = [KAHAN SE AAYEGA?]
# Logic: Guard (discipline) ki jeb (.) attribute = JSON diary (data) ki memory .get(key, Default Plan B)
discipline.trades_taken = data["discipline"].get("trades_taken", 0)
discipline.current_max_trades = data["discipline"].get("current_max_trades", 0)
discipline.bonus_trade_used = data["discipline"].get("bonus_trade_used", False)
discipline.hard_lock_activated = data["discipline"].get("hard_lock_activated", False)

# 🛡️ KADAM 4: Khatra Manager (The Daily Risk Guard)
# Step 4.1: The First Instruction (Aukaat tay karna)
# Diary se aaj ka risk limit nikala. Agar chitti missing hai, toh default 5000.0 (Fail-Safe) maan liya.
daily_limit = data["khatra"].get("ek_din_ka_risk", 5000.0)

# Guard paida hote hi (__init__ constructor ke zariye) usko 5000 ki limit de di.
khatra = Khatra_Manager(daily_limit) 

# Step 4.2: The Memory Injection (Purana hisaab dena)
# GOLDEN FORMULA: Guard ki jeb (Left) = Diary ka purana loss (Right)
# Taki agar system dopahar mein restart ho, toh Guard subah ka loss bhool na jaye.
khatra.ek_din_ka_total_loss = data["khatra"].get("ek_din_ka_total_loss", 0.0)

# 🚁 KADAM 5: Live Tracker (The Empty Helipad)
# Logic: Server start hote hi koi trade live nahi hota. Isliye Tracker (Drone) abhi hawa mein nahi hai.
# 'None' ka matlab hai Global memory mein jagah reserve hai, par abhi wo poori tarah khali hai.
tracker = None