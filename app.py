from flask import Flask, render_template, request, redirect, url_for
from stocks import livePrice
from scheduler import start_scheduler
import csv

app = Flask(__name__)

start_scheduler()

def add_stock(symbol):
    symbol = symbol.upper()
    with open("tracked_stocks.txt", "a") as f:
        f.write(symbol + "\n")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_symbol = request.form.get("symbol")
        if new_symbol:
            add_stock(new_symbol)
        return redirect(url_for("home"))

    symbol = request.args.get("symbol", "AAPL")
    quote = livePrice(symbol)
    current_price = quote.get("c")

    table_data = []
    with open("prices.csv", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            table_data.append(row)

    return render_template("index.html", symbol=symbol, price=current_price, table_data=table_data)

if __name__ == "__main__":
    app.run(debug=True)
