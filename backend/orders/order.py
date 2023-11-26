import json
import sys

sys.path.append("/Users/christiannonis/Documents/Projects/trading-bot-gpt")


import openai
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from main import openai_key, alpaca_secret_paper, alpaca_api_key_paper, trading_client
from orders.functions import (
    analyze_market_with_gpt,
    get_market_data,
    make_trade_decision,
    selected_assets,
    create_dataset,
)
from orders.orders import data_client, start_date, end_date

for asset, data in selected_assets(trading_client, data_client, start_date, end_date):
    try:
        analysis_str = analyze_market_with_gpt(data, asset)
        analysis_json = json.loads(analysis_str)
        if (
            analysis_json["long"]
            or analysis_json["short"]
            and analysis_json["stop_loss"]
            and analysis_json["take_profit"]
        ):
            make_trade_decision(
                analysis_json, asset, trading_client, data, order_amount=100
            )
        else:
            raise Exception("Invalid response from GPT-3.5")
    except Exception as e:
        print(e)
        continue
