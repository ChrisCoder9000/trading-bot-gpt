import sys

sys.path.append("/Users/christiannonis/Documents/Projects/trading-bot-gpt")


import openai
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from main import openai_key, alpaca_secret_paper, alpaca_api_key_paper, trading_client
from functions import (
    analyze_market_with_gpt,
    get_market_data,
    make_trade_decision,
    selected_assets,
    create_dataset,
)

openai.api_key = openai_key
data_client = StockHistoricalDataClient(
    api_key=alpaca_api_key_paper, secret_key=alpaca_secret_paper
)

start_date = datetime.now() - timedelta(days=7)
end_date = datetime.now() - timedelta(hours=2)

for asset in selected_assets(trading_client, data_client, start_date, end_date):
    data = create_dataset(asset, start_date, end_date, data_client)

    print(data)

    # analysis_json = analyze_market_with_gpt(data, asset)
    # make_trade_decision(analysis_json, asset, trading_client)
