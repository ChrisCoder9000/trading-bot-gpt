import sys

import pandas as pd

sys.path.append("/Users/christiannonis/Documents/Projects/trading-bot-gpt")

import json
import openai
from alpaca.trading.requests import (
    MarketOrderRequest,
    TakeProfitRequest,
    StopLossRequest,
)
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient


def get_market_data(asset, start_date, end_date, data_client):
    bar_request = StockBarsRequest(
        symbol_or_symbols=asset,
        timeframe=TimeFrame.Hour,
        start=start_date,
        end=end_date,
    )
    bars = data_client.get_stock_bars(bar_request)
    return bars.df


def analyze_market_with_gpt(data, asset):
    prompt = f'Analizza i seguenti dati di mercato per {asset} e fornisci un\'opinione di trading:\n\n{data.to_string()}\n\nDimmi se dovrei aprire una posizione long o short. Dimmi dove mettere il mio stop loss e take profit. Timeframe 1H. Rispondimi solo con json in questo formato: {{"long": boolean, "short": boolean, "stop_loss": float, "take_profit": float, "open_price": float}}'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=2000,
    )
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


def make_trade_decision(analysis_json, asset, trading_client):
    analysis = json.loads(analysis_json)
    if analysis["long"]:
        bracket__order_data = MarketOrderRequest(
            symbol=asset,
            qty=1,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.BRACKET,
            take_profit=TakeProfitRequest(limit_price=analysis["take_profit"]),
            stop_loss=StopLossRequest(stop_price=analysis["stop_loss"]),
        )
        trading_client.submit_order(order_data=bracket__order_data)

    elif analysis["short"]:
        bracket__order_data = MarketOrderRequest(
            symbol=asset,
            qty=1,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.BRACKET,
            take_profit=TakeProfitRequest(limit_price=analysis["take_profit"]),
            stop_loss=StopLossRequest(stop_price=analysis["stop_loss"]),
        )
        trading_client.submit_order(order_data=bracket__order_data)


def get_all_assets(trading_client: TradingClient):
    assets = trading_client.get_all_assets()
    assets = [asset for asset in assets if asset.tradable]
    return assets


def create_dataset(data_client, asset, start_date, end_date):
    bar_request = StockBarsRequest(
        symbol_or_symbols=asset,
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date,
    )
    try:
        bars = data_client.get_stock_bars(bar_request)
        return bars.df
    except Exception as e:
        print(f"Error with: {asset} | {e}")
        return pd.DataFrame()


def select_top_assets(assets_with_volume, threshold=10):
    sorted_assets = sorted(assets_with_volume.items(), key=lambda x: x[1], reverse=True)
    return [asset for asset, volume in sorted_assets[:threshold]]


def selected_assets(trading_client, data_client, start_date, end_date):
    all_assets = get_all_assets(trading_client)[:20]

    assets_count = len(all_assets)
    asset_volumes = {}

    for asset in all_assets:
        print(f"Analyzing {asset.symbol} ({all_assets.index(asset)}/{assets_count})")
        dataset = create_dataset(data_client, asset.symbol, start_date, end_date)

        if not dataset.empty:
            asset_volumes[asset.symbol] = dataset["volume"].mean()
        else:
            asset_volumes[asset.symbol] = 0

        print(
            f"Finished analyzing {asset.symbol} ({all_assets.index(asset)}/{assets_count})"
        )

    return select_top_assets(asset_volumes)
