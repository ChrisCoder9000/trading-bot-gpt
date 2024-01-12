from alpaca.trading.client import TradingClient

from backend.app_secrets import (
    alpaca_api_key_paper,
    alpaca_secret_paper,
    openai_key,
    open_ai_org,
    alpaca_secret_market_endpoint_paper,
)

trading_client = TradingClient(alpaca_api_key_paper, alpaca_secret_paper, paper=True)
