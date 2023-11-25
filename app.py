import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from orders.functions import analyze_market_with_gpt, create_dataset
from orders.orders import data_client, start_date, end_date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prerate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Definizione del modello del database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# Creazione del database (eseguire una sola volta)
# @app.before_first_request
# def create_tables():
#     db.create_all()


# Endpoint per ottenere e aggiungere elementi
@app.route("/api/analize", methods=["GET"])
def get_items():
    asset = request.args.get("asset")

    stock_data = create_dataset(data_client, asset, start_date, end_date)

    result_str = analyze_market_with_gpt(stock_data, asset)
    result = json.loads(result_str)

    return jsonify(
        {
            "asset": asset,
            "timeframe": {
                "start_date": start_date.strftime("%d/%m/%Y, %H:%M:%S"),
                "end_date": end_date.strftime("%d/%m/%Y, %H:%M:%S"),
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


def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route("/items", methods=["POST"])
def add_item():
    data = request
