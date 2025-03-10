import uvicorn
from backend.app.main import app
from backend.app.database import Base, engine
from backend.app.models import subscription, user, privacy_log

# Создаем все таблицы в базе данных
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Запускаем сервер на порту 8000
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоматическая перезагрузка при изменениях
        workers=4  # Количество рабочих процессов
    ) 