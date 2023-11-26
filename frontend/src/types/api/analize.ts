export interface IAnalizeRequest {
  asset: string;
  lang: string;
}

export interface IAnalizeResponse {
  asset: string;
  timeframe: {
    start_date: string;
    end_date: string;
    candles: string;
  };
  result: {
    type: "long" | "short";
    open_price: number;
    stop_loss: number;
    take_profit: number;
    explaination: string;
  };
}
