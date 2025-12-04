import requests

from app.core.config import Settings

settings = Settings()


# --- 发送 Telegram 个人消息 ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage"
    for chat_id in settings.TG_CHAT_ID:
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
    url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TG_CHANNEL_ID,
        "text": message,
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"发送 Telegram 消息失败: {e}")
        return False

    return True
