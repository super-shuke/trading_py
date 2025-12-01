from fastapi import FastAPI
from contextlib import asynccontextmanager
from router.index import register_routers
from sql.client import db
from trading import check_and_notify
import psutil


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...,生命周期开始")
    db.init_db()
    register_routers(app)
    print("数据库连接成功")
    yield


# @app.post("/check_quick_price")
# def check_quick_price(list: list[str], interval: int):
#     result = check_and_notify(list, interval=interval)
#     return result

app = FastAPI(lifespan=lifespan)


@app.get("/status")
def get_status():
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 获取内存信息
    memory = psutil.virtual_memory()

    cpu_info = f"CPU使用率: {cpu_usage}%"
    return {"cpu_usage": cpu_usage, "cpu_info": cpu_info, "memory": memory}
