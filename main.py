import schedule
import time
import yfinance as yf
import pandas_ta as ta
import requests
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Job:
    def __init__(self, runner_function: callable):
        self.runner_function = runner_function
        self.schedule = schedule

    def schedule_market_jobs(self):
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("16:00", "%H:%M")
        current = start_time
        while current <= end_time:
            # Schedule the job every 30 minutes
            self.schedule.every().day.at(current.strftime("%H:%M")).do(
                self.runner_function
            )

            print(f"Scheduling job at {current.strftime('%H:%M')}")
            current += timedelta(minutes=30)

    def run(self):
        while True:
            self.schedule.run_pending()
            time.sleep(1)


def task():
    try:
        tickers = [
            "BAJAJHFL.NS",
            "CDSL.NS",
            "DRREDDY.NS",
            "EPL.NS",
            "FINCABLES.NS",
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
            "TATATECH.NS",
            "TMCV.NS",
            "TMPV.NS",
            "TRANSRAILL.NS",
            "VBL.NS",
            "WIPRO.NS",
            "ZYDUSLIFE.NS",
        ]

        # Download historical data for the tickers
        data = yf.download(
            tickers=tickers,
            period="90d",
            interval="1d",
            multi_level_index=False,
        )

        # Indicator Configuration
        LENGTH = 14
        MAMODE = "rma"
        LOWER_LIMIT = 36
        UPPER_LIMIT = 64

        msg1 = "RSI Indicator🚨\n\n**🔽 Crossing lower limit:**\n"
        msg2 = "\n\n**🔼 Crossing upper limit:**\n"
        for ticker in tickers:
            rsi = (
                ta.rsi(
                    data["Close"][ticker],
                    length=LENGTH,
                    mamode=MAMODE,
                )
                .tail(1)
                .values[0]
            )
            if rsi < LOWER_LIMIT:
                msg1 += f"`{ticker}` - {rsi.round(2)}\n"
            if rsi > UPPER_LIMIT:
                msg2 += f"`{ticker}` - {rsi.round(2)}\n"

        data = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg1 + msg2}&parse_mode=Markdown"
        )
        if data.status_code == 200:
            print("Message sent successfully!")
        else:
            raise Exception(f"Failed to send message. Status code: {data.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    job = Job(runner_function=task)
    job.schedule_job()
    job.run()
