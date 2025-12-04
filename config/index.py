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

# --- 认证配置 ---
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token 有效期 30 分钟
