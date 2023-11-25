# HOW TO

- add following secrets to an app_secrets.py file in the root:
  - alpaca_api_key_paper
  - alpaca_secret_paper
  - alpaca_secret_market_endpoint_paper
  - openai_key
  - open_ai_org

## Basic functionality

start the env if you want with `python3 -m venv env` and `source env/bin/activate`

1. Retrieve last x assets from Alpaca API (see orders/functions.py:get_all_assets())
2. Select the assets with the highest volume (see orders/functions.py:select_top_assets())
3. Asks gpt to create a json with order data (see orders/functions.py:analyze_market_with_gpt())
4. Open the position (see orders/functions.py:make_trade_decision())

everything is handled on the orders/orders.py file so to run the script just run `python orders/orders.py`
or `python3 orders/orders.py` depending on your python version

the code is not watching for the market, it just runs once and then exits. To make it run every x minutes
