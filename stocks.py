import finnhub
import os
from dotenv import load_dotenv

load_dotenv()

client = finnhub.Client(api_key=os.getenv("FINNHUB_KEY"))

def livePrice(stock):
    return client.quote(stock)

