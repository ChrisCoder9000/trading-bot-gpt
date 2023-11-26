import json
from flask import Blueprint, jsonify, request

from orders.functions import analyze_market_with_gpt, create_dataset
from orders.orders import data_client, start_date, end_date
from orders.functions import analyze_market_with_gpt, create_dataset

api = Blueprint("api", __name__)


@api.route("/api/analize", methods=["GET"])
def analize():
    asset = request.args.get("asset")

    stock_data = create_dataset(data_client, asset, start_date, end_date)

    result_str = analyze_market_with_gpt(stock_data, asset)
    result = json.loads(result_str)

    return jsonify(
        {
            "asset": asset,
            "timeframe": {
                "start_date": start_date,
                "end_date": end_date,
                "candles": "1h",
            },
            "result": {
                "type": result["long"] and "long" or "short",
                "open_price": result["open_price"],
                "stop_loss": result["stop_loss"],
                "take_profit": result["take_profit"],
                "explaination": result["explaination"],
            },
        }
    )
