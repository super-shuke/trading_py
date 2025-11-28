from tradingview_ta import TA_Handler, Interval, Exchange

SYMBOL = "BTCUSDT"
SCREENER = "crypto"
EXCHANGE = "BINANCE"


def get_crypto_analysis(symbol=SYMBOL):
    handler = TA_Handler(
        symbol=symbol,
        screener=SCREENER,
        exchange=EXCHANGE,
        interval=Interval.INTERVAL_15_MINUTES,
    )
    analysis = handler.get_analysis()

    return {
        "price": analysis.indicators["close"],
        "recommendation": analysis.summary["RECOMMENDATION"],
        "buy_votes": analysis.summary["BUY"],
        "sell_votes": analysis.summary["SELL"],
    }
