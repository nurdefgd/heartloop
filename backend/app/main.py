from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import demo

app = FastAPI(title="Love Breeze API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем демо-маршруты
app.include_router(demo.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Love Breeze API",
        "demo_mode": True,
        "docs_url": "/docs",
        "demo_credentials": {
            "email": "alex@demo.com",
            "password": "demo123"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 