from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.crawler import AdvancedCrawler
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

crawler_service = AdvancedCrawler()


@app.get("/status")
def get_status():
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 获取内存信息
    memory = psutil.virtual_memory()

    cpu_info = f"CPU使用率: {cpu_usage}%"
    return {"cpu_usage": cpu_usage, "cpu_info": cpu_info, "memory": memory}


@app.get("/goSports")
async def goto_sports(symbol: str|None = None):
    targetUrl = f"https://www.jin10.com/"
    news_titles = await crawler_service.fetch_dynamic_content(targetUrl)
    if not news_titles:
        return {"msg": "反爬太厉害了，没抓到数据，试试换个源"}
    else:
        return {"titles": news_titles}
