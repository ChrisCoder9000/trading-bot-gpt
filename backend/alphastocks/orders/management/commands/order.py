import json
from django.core.management.base import BaseCommand
from orders.functions import (
    analyze_market_with_gpt,
    make_trade_decision,
    selected_assets,
)
from orders.utils import data_client, start_date, end_date
from orders.utils import trading_client


class Command(BaseCommand):
    help = "Ordering stocks based on GPT-3.5 analysis"

    def order(self):
        for asset, data in selected_assets(
            trading_client, data_client, start_date, end_date, count=500
        ):
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

    def handle(self, *args, **kwargs):
        self.order()
        self.stdout.write(self.style.SUCCESS("Ordini eseguiti con successo!"))
