from datetime import date, timedelta
import random

# Тестовые пользователи
DEMO_USERS = [
    {
        "username": "alex_demo",
        "full_name": "Alex Johnson",
        "email": "alex@demo.com",
        "birth_date": date(1995, 5, 15),
        "gender": "male",
        "bio": "Люблю путешествия и фотографию 📸 Ищу человека со схожими интересами!",
        "profile_photo": "/demo/photos/alex.jpg",
        "location": "Москва",
        "interests": ["photography", "travel", "music"]
    },
    {
        "username": "maria_demo",
        "full_name": "Maria Smith",
        "email": "maria@demo.com",
        "birth_date": date(1997, 8, 23),
        "gender": "female",
        "bio": "Обожаю йогу и здоровый образ жизни 🧘‍♀️ Ищу позитивного человека!",
        "profile_photo": "/demo/photos/maria.jpg",
        "location": "Санкт-Петербург",
        "interests": ["yoga", "fitness", "cooking"]
    },
    {
        "username": "david_demo",
        "full_name": "David Brown",
        "email": "david@demo.com",
        "birth_date": date(1993, 12, 7),
        "gender": "male",
        "bio": "Программист, геймер, любитель кофе ☕️ Ищу человека для совместных приключений!",
        "profile_photo": "/demo/photos/david.jpg",
        "location": "Москва",
        "interests": ["gaming", "technology", "coffee"]
    }
]

# Тестовые интересы
DEMO_INTERESTS = [
    "travel", "photography", "music", "yoga", "fitness", "cooking",
    "gaming", "technology", "coffee", "art", "books", "movies",
    "sports", "dancing", "hiking", "food", "pets", "fashion"
]

# Тестовые сообщения для чата
DEMO_MESSAGES = [
    "Привет! Как дела? 👋",
    "Отличные фотографии! Где они были сделаны?",
    "Может быть встретимся на чашечку кофе? ☕️",
    "Какие планы на выходные?",
    "Я тоже обожаю путешествовать! Какие страны уже посетил(а)?",
    "Любимый фильм?",
    "Давай созвонимся?",
    "Какую музыку слушаешь?"
]

def generate_demo_match():
    """Генерирует тестовый матч между пользователями"""
    return {
        "match_percentage": random.randint(75, 99),
        "created_at": date.today() - timedelta(days=random.randint(1, 30)),
        "last_message": random.choice(DEMO_MESSAGES)
    }

def generate_demo_chat_history():
    """Генерирует историю сообщений для демо-чата"""
    messages = []
    for _ in range(random.randint(5, 10)):
        messages.append({
            "text": random.choice(DEMO_MESSAGES),
            "timestamp": date.today() - timedelta(days=random.randint(1, 7)),
            "is_read": random.choice([True, False])
        })
    return messages 