# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from stocks import livePrice
import csv
from datetime import datetime

def get_tracked_stocks():
    try:
        with open("tracked_stocks.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["AAPL"]

def log_stock_price():
    symbols = get_tracked_stocks()
    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        for symbol in symbols:
            price_data = livePrice(symbol)
            price = price_data['c']
            writer.writerow([datetime.now(), symbol, price])
            print(f"Logged {symbol} at {price}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(log_stock_price, 'interval', minutes=1)
    scheduler.start()
