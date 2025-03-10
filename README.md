# Love Breeze - Современное приложение для знакомств

Love Breeze - это инновационное приложение для знакомств, которое помогает людям находить свою вторую половинку через умный алгоритм подбора пар и современный пользовательский интерфейс.

## Особенности

- 🎯 Умный алгоритм подбора пар
- 🌍 Поиск людей поблизости
- 💬 Мгновенный чат
- 📸 Поддержка фото и видео
- 🔒 Безопасная верификация пользователей
- 🎮 Интерактивные профили
- 🤝 Система icebreakers для начала общения

## Технический стек

### Backend
- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Socket.IO

### Frontend
- React
- Tailwind CSS
- Framer Motion

## Установка и запуск

### Требования
- Python 3.8 или выше
- PostgreSQL
- Node.js и npm

### Установка бэкенда

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
cd backend
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

4. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

### Установка фронтенда

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Запустите сервер разработки:
```bash
npm run dev
```

## API документация

После запуска бэкенд-сервера, документация API доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Лицензия

MIT 