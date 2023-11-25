from alpaca.trading.requests import GetAssetsRequest
from main import trading_client

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print("Account is currently restricted from trading.")

# Check how much money we can use to open new positions.
print("${} is available as buying power.".format(account.buying_power))
