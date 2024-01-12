from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alphastocks.settings import alpaca_secret_paper, alpaca_api_key_paper
from alpaca.trading.client import TradingClient


data_client = StockHistoricalDataClient(
    api_key=alpaca_api_key_paper, secret_key=alpaca_secret_paper
)

trading_client = TradingClient(alpaca_api_key_paper, alpaca_secret_paper, paper=True)


start_date = datetime.now() - timedelta(days=7)
end_date = datetime.now() - timedelta(hours=2)


import os
import re


def replacement_function(data, path):
    with open(f"{os.getcwd()}/{path}", "r") as file:
        prompt = file.read()

    def replacement_function(match):
        keys = match.group(1).split('"]["')
        value = data
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return ""
            value = value[key]
        return str(value)

    pattern = re.compile(r'{data\["(.*?)"\]}')
    compact_prompt = " ".join(prompt.split())
    compact_prompt = pattern.sub(replacement_function, compact_prompt)

    return compact_prompt


def calc_gpt_cost(input: str, output: str, model: str):
    pass
