from flask import Flask, render_template, request, redirect, url_for
from stocks import livePrice
from scheduler import start_scheduler
import csv
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os
from collections import defaultdict

app = Flask(__name__)

start_scheduler()
CSV_FILE = "prices.csv"


        
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

    # Load tracked stocks fresh each time
    tracked_stocks = []
    with open("tracked_stocks.txt") as f:
        for i in f:
            tracked_stocks.append(i.strip())

    # Table data
    table_data = defaultdict(list)
    with open("prices.csv", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            table_data[row[1]].append(row)

    return render_template(
        "index.html",
        symbol=symbol,
        price=current_price,
        table_data=table_data,
        ts=tracked_stocks
    )




@app.route("/graphs")
def graphs():
    if not os.path.exists(CSV_FILE):
        return "No data yet."

    df = pd.read_csv(CSV_FILE, names=["timestamp", "symbol", "price"])

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    graphs_html = []
    for symbol, group in df.groupby("symbol"):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=group["timestamp"],
            y=group["price"],
            mode="lines+markers",
            name=symbol,
            hovertemplate="$%{y:.2f}<extra></extra>",
            fillcolor="black"
        ))

        fig.update_layout(
            title=f"{symbol} Stock Price",
            xaxis_title="Time",
            yaxis_title="Price"
        )
        fig.update_layout(
            title=f"{symbol} Stock Price",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            
            xaxis=dict(
                gridcolor='gray',
                zerolinecolor='gray',
                showline=True,
                linecolor='white',
                tickfont=dict(color='white'),
                title=dict(font=dict(color='white'))
            ),
            yaxis=dict(
                gridcolor='gray',
                zerolinecolor='gray',
                showline=True,
                linecolor='white',
                tickfont=dict(color='white'),
                title=dict(font=dict(color='white'))
            )
        )


        graph_html = pio.to_html(fig, full_html=True)
        graphs_html.append(graph_html)

    return render_template("graphs.html", graphs=graphs_html)

if __name__ == "__main__":
    app.run(debug=True)
