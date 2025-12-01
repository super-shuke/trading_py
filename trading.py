from store.market.index import get_typeof_data
from tg.tg_bot import send_telegram_message

# -----币种类型
SYMBOL = "BTCUSDT"
# 加密货币
SCREENER = "crypto"
EXCHANGE = "BINANCE"


def format_market_message(data):
    """
    将 market.py 返回的字典数据转换为 Telegram 消息文本
    """
    if not data:
        return "❌ 无法获取数据"

    # 1. 根据涨跌幅设置 Emoji (涨绿跌红)
    # 注意：change 可能是 None，要做容错处理
    change = data.get("change", 0)
    change_emoji = "🟢" if change >= 0 else "🔴"

    # 2. 根据建议设置 Emoji
    rec = data.get("recommendation", "UNKNOWN")
    rec_emoji = "🤔"
    if "BUY" in rec:
        rec_emoji = "🚀"  # 买入信号
    elif "SELL" in rec:
        rec_emoji = "⚠️"  # 卖出信号

    # 3. 组装消息 (使用 Markdown 格式)
    # 价格和关键数据加粗，代码块包裹数字以方便复制
    msg = (
        f"{rec_emoji} **市场监控: #{data['symbol']}**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 **现价**: `{data['price']}`\n"
        f"📊 **涨跌**: {change_emoji} `{round(change, 2)}%`\n"
        f"📢 **建议**: **{rec}**\n\n"
        f"📉 **24H 概览**:\n"
        f"• 开盘: `{data['open']}`\n"
        f"• 最高: `{data['high']}`\n"
        f"• 最低: `{data['low']}`\n"
        f"• 量能: `{int(data['volume']) if data['volume'] else 0}`\n\n"
        f"🛠 **技术指标**:\n"
        f"• RSI (14): `{round(data['rsi'], 2)}`\n"
        f"• MACD: `{round(data['macd'], 2)}`"
    )

    return msg


def check_and_notify(currency_list_or_str, interval=15):
    # 1. 获取数据
    try:
        data = get_typeof_data(currency_list_or_str, interval=interval)

        ms_post = []
        # 2. 组装消息文本 (使用了 f-string 换行)
        print(data)
        for analysis in data:
            ms_post.append(format_market_message(analysis))

        # 3. 发送给 TG
        send_telegram_message("-----".join(ms_post))

        return {"status": "success", "data": data, "message_sent": True}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
