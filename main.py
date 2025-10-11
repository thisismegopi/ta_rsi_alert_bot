import schedule
import time
import yfinance as yf
import pandas_ta as ta
import requests
import os

from datetime import timedelta
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Job:
    def __init__(self, runner_function: callable):
        self.runner_function = runner_function
        self.schedule = schedule

    def schedule_job(self):
        start_time = datetime.strptime("15:00", "%H:%M")

        self.schedule.every().day.at(start_time.strftime("%H:%M")).do(
            self.runner_function
        )

        print(f"Scheduling job at {start_time.strftime('%H:%M')}")

    def run(self):
        while True:
            self.schedule.run_pending()
            time.sleep(1)


def task():
    try:
        tickers = [
            "AGI.NS",
            "ANGELONE.NS",
            "AVANTIFEED.NS",
            "BAJAJHFL.NS",
            "CDSL.NS",
            "CELLO.NS",
            "DRREDDY.NS",
            "HEROMOTOCO.NS",
            "ICICIGI.NS",
            "IDFCFIRSTB.NS",
            "ITC.NS",
            "ITCHOTELS.NS",
            "JYOTHYLAB.NS",
            "KPITTECH.NS",
            "KTKBANK.NS",
            "MANAPPURAM.NS",
            "NATCOPHARM.NS",
            "SOUTHBANK.NS",
            "TATAMOTORS.NS",
            "TATASTEEL.NS",
            "VBL.NS",
            "WIPRO.NS",
            "ZYDUSLIFE.NS",
        ]
        from_date = datetime.today() - timedelta(days=90)
        to_date = datetime.today()
        interval = "1d"

        msg1 = "**RSI below 35:**\n"
        msg2 = "\n\n**RSI above 65:**\n"
        for ticker in tickers:
            data = yf.download(
                tickers=ticker,
                start=from_date,
                end=to_date,
                interval=interval,
                multi_level_index=False,
            )
            df = data.copy()

            df["RSI"] = ta.rsi(
                df["Close"],
                length=14,
                mamode="sma",
            )
            if df.tail(1)["RSI"].values[0] < 36:
                msg1 += f"`{ticker}` - {df.tail(1)['RSI'].values[0].round(2)}\n"
            if df.tail(1)["RSI"].values[0] > 64:
                msg2 += f"`{ticker}` - {df.tail(1)['RSI'].values[0].round(2)}\n"

        data = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg1 + msg2}&parse_mode=Markdown"
        )
        if data.status_code == 200:
            print("Message sent successfully!")
        else:
            raise Exception(f"Failed to send message. Status code: {data.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


job = Job(runner_function=task)
job.schedule_job()
job.run()
