import requests

from config.index import TG_TOKEN, TG_CHAT_ID, TG_CHANNEL_ID


# --- 发送 Telegram 个人消息 ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    for chat_id in TG_CHAT_ID:
        payload = {
            "chat_id": chat_id,
            "text": message,
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"发送 Telegram 消息失败: {e}")
            return False
    return True


# --- 发送 Telegram 频道消息 ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHANNEL_ID,
        "text": message,
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"发送 Telegram 消息失败: {e}")
        return False

    return True
