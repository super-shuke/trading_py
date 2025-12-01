import requests

TG_BOT_TOKEN = "8522584076:AAFNel1mLnA6G4LDMPCzuxFpcP-QMfQ2cRs"
TG_CHAT_ID =["7946620555","6933752785"]


# --- 发送 Telegram 消息 ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
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
    
