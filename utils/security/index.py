from datetime import datetime, timedelta, timezone
import jwt

from app.core.config import Settings
from config.index import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

settings = Settings()


# 生成token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    # 加密
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# 解密token 并验证token
def decode_access_token(token: str) -> dict | None:
    try:
        # 解密
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        print("Token 已过期")
        return None
    except jwt.InvalidTokenError:
        print("无效的 Token")
        return None
