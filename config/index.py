# --- 交易所配置 ---
# 默认交易所 (BINANCE, OKX, COINBASE 等)
GLOBAL_EXCHANGE = "BINANCE"

# 筛选器类型 (crypto, america, forex 等)
GLOBAL_SCREENER = "crypto"

# --- 监控目标 ---
# 你的默认监控列表
GLOBAL_TARGETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT"]


# 自动任务的时间间隔 (秒)
CRAWL_INTERVAL = 60

# --- Telegram 配置 (选填) ---

# 如果你想把 TG 配置也统一管理，可以放这里
TG_TOKEN = "8522584076:AAFNel1mLnA6G4LDMPCzuxFpcP-QMfQ2cRs"

# tg账号chatID
TG_CHAT_ID = ["7946620555", "6933752785"]
# tg频道id
TG_CHANNEL_ID = "@频道id"

# uuid
SECRET_KEY = "8210256d-5591-452e-86b7-2ef032627817"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token 有效期 30 分钟
