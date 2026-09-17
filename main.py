Sebas Paper Crypto Trading Bot v1.0
Live BTC price from CoinGecko - PAPER ONLY
import time
import csv
import os
from datetime import datetime
import requests

BALANCE = 10000.0
BTC = 0.0
BUY_DROP = 0.002  # 0.2% drop to buy (for demo)
SELL_GAIN = 0.003 # 0.3% gain to sell
CSV_FILE = "trades.csv"
last_buy_price = None

def telegram_alert(msg):
    # stub for later - will send to Telegram
    print(f"[TELEGRAM STUB] {msg}")

def get_btc_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        return r.json()["bitcoin"]["usd"]
    except:
        return None

def log_trade(event, price, balance, pnl="", details=""):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp","event","price","balance","pnl","details"])
        writer.writerow([datetime.now().isoformat(), event, price, balance, pnl, details])

print("SEBAS BOT v1.0 LIVE - Paper Mode")
log_trade("START", 0, BALANCE, "", "bot started")

while True:
    price = get_btc_price()
    if price is None:
        print("Price fetch failed, retrying...")
        time.sleep(10)
        continue
    
    print(f"Price: {price} | Balance: ${BALANCE:.2f} | BTC: {BTC}")
    log_trade("PRICE", price, BALANCE, "", f"btc={BTC}")

    # BUY logic
    if BTC == 0:
        # simple demo: buy on any tick for first trade, then use drop logic
        if last_buy_price is None or price < last_buy_price * (1 - BUY_DROP):
            buy_amount = BALANCE / price
            BTC = buy_amount
            BALANCE = 0
            last_buy_price = price
            msg = f"BUY {BTC:.6f} BTC at ${price}"
            print(msg)
            log_trade("BUY", price, BALANCE, "", msg)
            telegram_alert(msg)

    # SELL logic
    else:
        if price > last_buy_price * (1 + SELL_GAIN):
            sell_value = BTC * price
            pnl = sell_value - 10000
            BALANCE = sell_value
            msg = f"SELL at ${price} | P/L ${pnl:.2f}"
            print(msg)
            log_trade("SELL_WIN", price, BALANCE, pnl, msg)
            telegram_alert(msg)
            BTC = 0
            last_buy_price = price

    time.sleep(10)