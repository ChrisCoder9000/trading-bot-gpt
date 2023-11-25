class TradingModel:
    def __init__(
        self,
        timestamp: str,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float,
        trade_count: int,
        vwap: float,
    ):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.trade_count = trade_count
        self.vwap = vwap
