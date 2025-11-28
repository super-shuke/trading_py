from market.index import get_crypto_analysis
from tg.tg_bot import send_telegram_message

# -----币种类型
SYMBOL = "BTCUSDT"
# 加密货币
SCREENER = "crypto"
EXCHANGE = "BINANCE"


def check_and_notify():
    # 1. 获取数据
    try:
        data = get_crypto_analysis()

        # 2. 组装消息文本 (使用了 f-string 换行)
        msg = (
            f"📢 市场更新: {SYMBOL}\n"
            f"💰 当前价格: {data['price']}\n"
            f"📊 建议操作: {data['recommendation']}\n"
            f"🟢 买入信号: {data['buy_votes']}\n"
            f"🔴 卖出信号: {data['sell_votes']}"
        )

        # 3. 发送给 TG
        send_telegram_message(msg)

        return {"status": "success", "data": data, "message_sent": True}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
