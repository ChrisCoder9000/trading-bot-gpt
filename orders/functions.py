import datetime
import os
import sys

import pandas as pd

from utils import replacement_function

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
    if data.empty:
        return "No data found"

    prompt_data = {
        "asset": asset,
        "rows": data.to_string(),
    }

    prompt = replacement_function(prompt_data, "prompt_analisi_ordine.txt")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=2000,
    )

    obj_res = json.loads(response.choices[0].message.content.strip())

    # Creazione delle stringhe da stampare e scrivere nel file
    output_str = "\n"
    output_str += f"Order for {asset} -- Time: {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n"
    output_str += f"type: {'long' if obj_res['long'] else 'short'}\n"
    output_str += f"stop_loss: {obj_res['stop_loss']}\n"
    output_str += f"take_profit: {obj_res['take_profit']}\n"

    # Stampa le stringhe
    print(output_str)

    output_str += f"explaination: {obj_res['explaination']}"

    # Scrivi le stringhe e i dati JSON nel file
    with open(f"{os.getcwd()}/orders/history.log", "a") as file:
        file.write(output_str + "\n")

    return response.choices[0].message.content.strip()


def make_trade_decision(analysis, asset, trading_client, dataset, order_amount):
    qty = order_amount / dataset["close"].iloc[-1]
    print(f"Quantity: {qty}")

    if analysis["long"]:
        order_data = MarketOrderRequest(
            symbol=asset, qty=qty, side=OrderSide.BUY, time_in_force=TimeInForce.DAY
        )
    elif analysis["short"]:
        order_data = MarketOrderRequest(
            symbol=asset, qty=qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
        )

    # Invia l'ordine di entrata
    order_response = trading_client.submit_order(order_data=order_data)

    # Crea gli ordini di stop loss e take profit separatamente
    if order_response.status == "filled":
        # Ordine di Stop Loss
        stop_loss_order = StopLossRequest(
            stop_price=analysis["stop_loss"],
            # Aggiungi ulteriori parametri se necessario
        )
        trading_client.submit_order(stop_loss_order)

        # Ordine di Take Profit
        take_profit_order = TakeProfitRequest(
            limit_price=analysis["take_profit"],
            # Aggiungi ulteriori parametri se necessario
        )
        trading_client.submit_order(take_profit_order)
    # print(f"quantity: {order_amount / dataset['close'].iloc[-1]}")
    # if analysis["long"]:
    #     bracket__order_data = MarketOrderRequest(
    #         symbol=asset,
    #         qty=order_amount / dataset["close"].iloc[-1],
    #         side=OrderSide.BUY,
    #         time_in_force=TimeInForce.DAY,
    #         order_class=OrderClass.BRACKET,
    #         take_profit=TakeProfitRequest(limit_price=analysis["take_profit"]),
    #         stop_loss=StopLossRequest(stop_price=analysis["stop_loss"]),
    #     )
    #     trading_client.submit_order(order_data=bracket__order_data)

    # elif analysis["short"]:
    #     bracket__order_data = MarketOrderRequest(
    #         symbol=asset,
    #         qty=order_amount / dataset["close"].iloc[-1],
    #         side=OrderSide.SELL,
    #         time_in_force=TimeInForce.DAY,
    #         order_class=OrderClass.BRACKET,
    #         take_profit=TakeProfitRequest(limit_price=analysis["take_profit"]),
    #         stop_loss=StopLossRequest(stop_price=analysis["stop_loss"]),
    #     )
    #     trading_client.submit_order(order_data=bracket__order_data)


def get_all_assets(trading_client: TradingClient):
    assets = trading_client.get_all_assets()
    assets = [asset for asset in assets if asset.tradable and asset.fractionable]
    return assets


def create_dataset(data_client, asset, start_date, end_date):
    try:
        bar_request = StockBarsRequest(
            symbol_or_symbols=asset,
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date,
        )
        bars = data_client.get_stock_bars(bar_request)
        return bars.df
    except Exception as e:
        print(f"Error with: {asset} | {e}")
        return pd.DataFrame()


def select_top_assets(assets_data, threshold=10):
    sorted_assets = sorted(
        assets_data.items(),
        key=lambda x: x[1]["volume"].mean() if not x[1].empty else 0,
        reverse=True,
    )
    return sorted_assets[:threshold]


def selected_assets(trading_client, data_client, start_date, end_date):
    all_assets = get_all_assets(trading_client)[:40]

    assets_count = len(all_assets)
    assets_data = {}

    for asset in all_assets:
        print(f"Analyzing {asset.symbol} ({all_assets.index(asset)}/{assets_count})")
        dataset = create_dataset(data_client, asset.symbol, start_date, end_date)
        assets_data[asset.symbol] = dataset

        dataset = create_dataset(data_client, asset.symbol, start_date, end_date)
        assets_data[asset.symbol] = dataset

        print(
            f"Finished analyzing {asset.symbol} ({all_assets.index(asset)}/{assets_count})"
        )

    return select_top_assets(assets_data)
