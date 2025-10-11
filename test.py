# remember to install pandas and pandas_ta
# we use the data we just downloaded by yfinance
import yfinance as yf
import pandas_ta as ta

from datetime import timedelta
from datetime import datetime

ticker = "TCS.NS"
from_date = datetime.today() - timedelta(days=90)
to_date = datetime.today()
interval = "1d"

data = yf.download(
    tickers=ticker,
    start=from_date,
    end=to_date,
    interval=interval,
    multi_level_index=False,
)
df = data.copy()
# data.to_csv('tcs_with_sma.csv')
# df = pd.read_csv("tcs_with_sma.csv")

df["RSI"] = ta.rsi(
    df["Close"],
    length=20,
    mamode="sma",
)
print(df.tail(30))

print(df.tail(1)["RSI"])
