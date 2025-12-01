from fastapi import FastAPI
from .user.index import router as user_router


def register_routers(app: FastAPI):
    routers_list = [user_router]
    count = 0
    for router in routers_list:
        app.include_router(router)
        count += 1

    router_names = [r.prefix or "root" for r in routers_list]
    print(f"✅ [Router] 已显式加载 {count} 个模块: {router_names}")
