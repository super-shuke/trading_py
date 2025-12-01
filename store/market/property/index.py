from config import GLOBAL_EXCHANGE, GLOBAL_SCREENER
from tradingview_ta import Interval, get_multiple_analysis

from store.market.index import _format_data


class MarketSubscription:
    def __init__(self):
        self._subList = set()
        self._subscriptions = {}

    @property
    def _subscriptions(self):
        return self._subscriptions

    @property
    def _subList(self):
        return sorted(list(self._subList))

    @_subList.setter
    def _subList(self, new_data):
        if not isinstance(new_data, list):
            print("❌ 错误：必须传入列表")
            return
        for sym in new_data:
            if sym in self._subList:
                continue
            else:
                self._subList.add(sym)
        formatted_symbols = [f"{GLOBAL_EXCHANGE}:{s}" for s in new_data]
        analyses = get_multiple_analysis(
            symbols=formatted_symbols,
            screener=GLOBAL_SCREENER,
            interval=Interval.INTERVAL_15_MINUTES,
        )
        for symbol in new_data:
            analysis = analyses.get(f"{GLOBAL_EXCHANGE}:{symbol}")
            if analysis:
                self._subscriptions[symbol] = _format_data(symbol, analysis)
