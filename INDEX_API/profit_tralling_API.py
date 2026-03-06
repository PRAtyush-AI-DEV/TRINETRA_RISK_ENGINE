class paisa_nikalo:
    def __init__(self, symbol, trader_type, entry_price, target_price, total_quantity, current_sl):
        # Data ko class ke andar set kar rahe hain
        self.symbol = symbol.upper()
        self.trader_type = trader_type.upper()     
        self.entry_price = float(entry_price)    
        self.target_price = float(target_price)  
        self.total_quantity = float(total_quantity)        
        self.current_sl = float(current_sl)    

        self.market_lot_sizes = {
            "NIFTY": 75, "BANKNIFTY": 15, "FINNIFTY": 40, "SENSEX": 10
        }
        self.index_names = ["NIFTY", "BANKNIFTY", "FINNIFTY", "SENSEX"]
        
        # --- SAFETY CHECK (Logic Validation) ---
        if self.trader_type == 'B':
            if self.current_sl >= self.entry_price or self.target_price <= self.entry_price:
                print("---> [TERMINAL LOG] ❌ ERROR: Buy trade mein Target upar aur SL neeche hona chahiye!")
                print("---> [TERMINAL LOG] 🛑 Converted buyer (B) to seller (S)")
                self.trader_type='S'
                
        elif self.trader_type == 'S':
            if self.current_sl <= self.entry_price or self.target_price >= self.entry_price:
                print("---> [TERMINAL LOG] ❌ ERROR: Sell trade mein Target neeche aur SL upar hona chahiye!")
                print("---> [TERMINAL LOG] 🛑 Converted seller (S) to buyer (B)")
                self.trader_type='B'

        # -- 🎯 THE SMART VERSION ---
        profit_ka_total_move = self.target_price - self.entry_price
        sl_ka_total_move = self.entry_price - self.current_sl

        # Target ki taraf 70% move
        self.profit_70_percent = self.entry_price + (profit_ka_total_move * 0.70)
        
        # SL area ko 30% par lana
        self.sl_30_percent = self.entry_price - (sl_ka_total_move * 0.30)

        # Trackers
        self.is_70_done = False

        print("\n" + "="*50)
        print(f"---> [TERMINAL LOG] 🚀 NSE {self.trader_type} TRADE START | Qty: {self.total_quantity} | SL: {self.current_sl}")
        print(f"---> [TERMINAL LOG] 🎯 70% Milestone: {self.profit_70_percent} | Safe SL (30%): {self.sl_30_percent}")
        print("="*50)


    # ==========================================
    # 🏃‍♂️ MAIN TRACKING FUNCTION (API ke liye optimized)
    # ==========================================
    def process_price(self, current_price):
        """
        Yeh function API se har baar naya price aane par ek baar chalega.
        Koi while loop ya input() nahi chahiye.
        """
        
        # Check if Target is Hit
        target_hit = (self.trader_type == 'B' and current_price >= self.target_price) or \
                     (self.trader_type == 'S' and current_price <= self.target_price)

        # Check if Stop Loss is Hit
        sl_hit = (self.trader_type == 'B' and current_price <= self.current_sl) or \
                 (self.trader_type == 'S' and current_price >= self.current_sl)
                 
        # Check if 70% Level is Hit 
        _70_hit = ((self.trader_type == 'B' and current_price >= self.profit_70_percent) or \
                   (self.trader_type == 'S' and current_price <= self.profit_70_percent)) and not self.is_70_done

        # --- ACTION 1: TARGET HIT ---
        if target_hit:
            total_profit = abs(current_price - self.entry_price) * self.total_quantity
            return {
                "status": "TARGET HIT", 
                "profit": total_profit,
                "message": f"🎉 MUBARAK HO! Target Hit ({current_price}). Total Profit: ₹{total_profit:.2f}"
            }

        # --- ACTION 2: STOP LOSS HIT ---
        elif sl_hit:
            loss = abs(self.entry_price - self.current_sl) * self.total_quantity
            if self.current_sl == self.entry_price:
                return {
                    "status": "SL HIT", 
                    "loss": 0,
                    "message": f"⏹️ TRAILING SL HIT at Cost ({current_price}). NO LOSS!"
                }
            else:
                return {
                    "status": "SL HIT", 
                    "loss": loss,
                    "message": f"❌ STOP LOSS HIT at {current_price}. Loss: ₹{loss:.2f}"
                }

        # --- ACTION 3: 70% LEVEL HIT ---
        elif _70_hit:
            self.current_sl = self.sl_30_percent
            self.is_70_done = True
            return {
                "status": "RUNNING", 
                "message": f"✅ 70% Area Covered! SL shifted to 30% risk area ({self.current_sl})"
            }

        # --- ACTION 4: NORMAL RUNNING ---
        else:
            return {
                "status": "RUNNING", 
                "message": f"⏳ Holding Position... (Market: {current_price} | SL: {self.current_sl})"
            }