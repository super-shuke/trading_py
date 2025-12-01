from tradingview_ta import TA_Handler, Interval, Exchange, get_multiple_analysis

from config.index import GLOBAL_EXCHANGE


SYMBOL = "BTCUSDT"
SCREENER = "crypto"


# currency集合 需要订阅的币种
crypto_set = set()

# 订阅币种数据集合 字典类型 快照数据
subscribed_crypto_data = {}


def add_crypto_analysis(symbolList: list[str]):
    for sym in symbolList:
        if sym in crypto_set:
            continue
        else:
            crypto_set.add(sym)
    for sub in crypto_set:
        if not subscribed_crypto_data.get(sub):
            subscribed_crypto_data[sub]

    return get_all_crypto_analysis(list(subscribed_crypto_data.keys()))


def remove_crypto_analysis(symbolList: list[str]):
    for sym in symbolList:
        if sym in crypto_set:
            crypto_set.remove(sym)
            subscribed_crypto_data.pop(sym)
    return True


# 根据传入参数类型 获取对应快照数据 默认15分钟周期
def get_typeof_data(symbol_or_list, interval=Interval.INTERVAL_15_MINUTES):
    if isinstance(symbol_or_list, list):
        return get_all_crypto_analysis(symbol_or_list, interval=interval)
    if isinstance(symbol_or_list, str):
        return get_crypto_analysis(symbol_or_list)
    else:
        print("参数类型错误")
        return None


# 统一清洗数据格式
def _format_data(symbol, analysis):
    if not analysis:
        return None
    ind = analysis.indicators
    return {
        "symbol": symbol,
        # --- 市场快照数据 (OHLCV) ---
        "price": ind.get("close"),  # 当前价格
        "open": ind.get("open"),  # 开盘价
        "high": ind.get("high"),  # 最高价
        "low": ind.get("low"),  # 最低价
        "volume": ind.get("volume"),  # 成交量
        "change": ind.get("change"),  # 涨跌幅
        # --- 技术指标 ---
        "recommendation": analysis.summary["RECOMMENDATION"],  # "BUY", "STRONG_SELL"
        "rsi": ind.get("RSI", 0),
        "macd": ind.get("MACD.macd", 0),
        "summary": analysis.summary,
    }


# 统一错误处理
def _handle_error(e):
    error_msg = str(e)
    if "429" in error_msg:
        print(f"🛑 [Market] 触发频率限制 (429)！")
        print("   原因：请求太快。批量接口已优化此问题，但在短时间内也不要频繁调用。")
    else:
        print(f"⚠️ [Market] 获取数据失败: {error_msg}")
    return None


# 获取单个币种的技术分析数据
def get_crypto_analysis(symbol=SYMBOL, interval=Interval.INTERVAL_15_MINUTES):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener=SCREENER,
            exchange=GLOBAL_EXCHANGE,
            interval=interval,
        )
        analysis = handler.get_analysis()

        return list(_format_data(symbol=symbol, analysis=analysis))
    except Exception as e:
        return _handle_error(e)


# 获取所有订阅币种的技术分析数据
def get_all_crypto_analysis(
    symbol_list: list[str],
    interval=Interval.INTERVAL_15_MINUTES,
    screener=SCREENER,
    exchange=GLOBAL_EXCHANGE,
):
    if not symbol_list:
        return []
    formatted_symbols = [f"{exchange}:{s}" for s in symbol_list]
    try:
        print("获取数据中...", formatted_symbols)
        analyses = get_multiple_analysis(
            symbols=formatted_symbols,
            screener=screener,
            interval=interval,
        )

        result = []
        for symbol in symbol_list:
            analysis = analyses.get(f"{exchange}:{symbol}")
            if analysis:
                result.append(_format_data(symbol=symbol, analysis=analysis))
        return result
    except Exception as e:
        return _handle_error(e)
