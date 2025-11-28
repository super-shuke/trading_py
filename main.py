from fastapi import FastAPI
from trading import check_and_notify
import psutil


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/status")
def get_status():
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 获取内存信息
    memory = psutil.virtual_memory()

    cpu_info = f"CPU使用率: {cpu_usage}%"
    return {"cpu_usage": cpu_usage, "cpu_info": cpu_info, "memory": memory}


@app.get("/check_price")
def check_price():
    result = check_and_notify()
    return result
