from fastapi import FastAPI
from config import *
from routes import *
# main.py
from fastapi import FastAPI
# 导入子路由文件中的 router 实例
from routes.user_routes import user_router
from routes.model_routes import model_router
from routes.record_routes import record_router

# 创建主应用实例
app = FastAPI()

# 将子路由注册到主应用
app.include_router(user_router)
app.include_router(model_router)
app.include_router(record_router)
# 可选：主应用中也可以定义根路由，用于测试
@app.get("/")
async def root():
    return {"message": "Root route"}

if __name__ == "__main__":
    import uvicorn
    # 配置端口为3000，开启热重载
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )

