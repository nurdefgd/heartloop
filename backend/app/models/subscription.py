from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from ..database import Base

class SubscriptionPlan(Base):
    """Модель для планов подписки"""
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # free, premium, vip
    price = Column(Float, default=0.0)
    daily_swipes = Column(Integer, default=50)  # Бесплатные 50 свайпов в день
    features = Column(String)  # JSON строка с доступными функциями
    
    # Дополнительные возможности для разных планов
    super_likes_per_day = Column(Integer, default=0)
    rewind_enabled = Column(Boolean, default=False)  # Возможность вернуться к предыдущему профилю
    hide_ads = Column(Boolean, default=False)
    see_who_likes = Column(Boolean, default=False)
    priority_matches = Column(Boolean, default=False)
    unlimited_likes = Column(Boolean, default=False)

class UserSubscription(Base):
    """Модель для подписок пользователей"""
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=False)

class SwipeLimit(Base):
    """Модель для отслеживания дневных свайпов"""
    __tablename__ = "swipe_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    swipes_used = Column(Integer, default=0)
    swipes_remaining = Column(Integer, default=50)  # Начальный лимит
    reset_time = Column(DateTime(timezone=True))  # Время следующего обновления лимита

# Предустановленные планы подписки
DEFAULT_SUBSCRIPTION_PLANS = [
    {
        "name": "Free",
        "price": 0.0,
        "daily_swipes": 50,
        "super_likes_per_day": 1,
        "rewind_enabled": False,
        "hide_ads": False,
        "see_who_likes": False,
        "priority_matches": False,
        "unlimited_likes": False,
        "features": "Базовый поиск, 50 свайпов в день, 1 Super Like в день"
    },
    {
        "name": "Premium",
        "price": 9.99,
        "daily_swipes": 100,
        "super_likes_per_day": 5,
        "rewind_enabled": True,
        "hide_ads": True,
        "see_who_likes": True,
        "priority_matches": False,
        "unlimited_likes": False,
        "features": "100 свайпов в день, 5 Super Likes, просмотр кто лайкнул, без рекламы"
    },
    {
        "name": "VIP",
        "price": 19.99,
        "daily_swipes": 999999,  # Неограниченно
        "super_likes_per_day": 10,
        "rewind_enabled": True,
        "hide_ads": True,
        "see_who_likes": True,
        "priority_matches": True,
        "unlimited_likes": True,
        "features": "Неограниченные свайпы, приоритетный показ, все премиум функции"
    }
] 