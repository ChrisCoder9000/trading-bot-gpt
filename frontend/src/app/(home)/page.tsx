"use client";

import { useLazyGetAnalisisQuery } from "@/services/api";
import { StyledHome } from "./styles";
import { useState } from "react";
import worldImage from "@/assets/world-links-2.jpg";
import Image from "next/image";

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [trigger, { data, isLoading, isError, error }] =
    useLazyGetAnalisisQuery();

  const handleSearchAsset = () => {
    trigger({
      asset: searchTerm,
      lang: "en",
    });
  };

  return (
    <StyledHome>
      <div className="hero-section">
        <h1>The easiest way to help take trade decisions</h1>
        <Image
          priority={true}
          className="world-image"
          src={worldImage}
          alt=""
        />
      </div>
      <div className="search-asset-container">
        <div className="cta-section">
          <h2 className="cta-title">Give it a try!</h2>
          <p className="cta-subtitle">Search by Ticker your favorite asset</p>
          <div className="input-container">
            <input
              placeholder="TSLA, AAPL, MSFT..."
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button onClick={handleSearchAsset}>Search</button>
          </div>
        </div>
        {data ? (
          <div className="search-result-table">
            <h3 className="analysis-title">Analysis Result</h3>
            <p className="description">{data.result.explaination}</p>
            <div className="wrapper-cells">
              <div className="wrapper-prices">
                <div>
                  <h3>Open price </h3>
                  <p>{data.result.open_price}</p>
                </div>
                <div>
                  <h3>Stop loss </h3>
                  <p>{data.result.stop_loss}</p>
                </div>
                <div>
                  <h3>Take profit </h3>
                  <p>{data.result.take_profit}</p>
                </div>
              </div>
              <div className="wrapper-details">
                <div>
                  <h3>Candles</h3>
                  <p>{data.timeframe.candles}</p>
                </div>
                <div>
                  <h3>Start Date</h3>
                  <p>{new Date(data.timeframe.start_date).toLocaleString()}</p>
                </div>
                <div>
                  <h3>End Date</h3>
                  <p>{new Date(data.timeframe.end_date).toLocaleString()}</p>
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </StyledHome>
  );
}
