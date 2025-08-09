from flask import Flask, render_template, request
from stocks import livePrice

app = Flask(__name__)

@app.route("/")
def home():
    symbol = request.args.get("symbol", "AAPL")
    quote = livePrice(symbol)
    current_price = quote.get("c")  # 'c' is current price
    return render_template("index.html", symbol=symbol, price=current_price)

if __name__ == "__main__":
    app.run(debug=True)
