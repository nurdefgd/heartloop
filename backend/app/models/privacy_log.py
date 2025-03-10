from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from ..database import Base

class PrivacyLog(Base):
    """Модель для логирования действий с приватными данными"""
    __tablename__ = "privacy_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action_type = Column(String)  # view_profile, message_sent, data_export, etc.
    accessed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String)
    device_info = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data_accessed = Column(JSON)  # Какие данные были затронуты
    is_authorized = Column(bool, default=False)
    location = Column(String, nullable=True)

class DataDeletionRequest(Base):
    """Модель для запросов на удаление данных"""
    __tablename__ = "data_deletion_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    request_date = Column(DateTime(timezone=True), server_default=func.now())
    scheduled_deletion_date = Column(DateTime(timezone=True))
    reason = Column(String, nullable=True)
    status = Column(String)  # pending, approved, completed, rejected
    confirmation_code = Column(String, unique=True)
    is_gdpr_request = Column(bool, default=False)

class PrivacySettings(Base):
    """Модель для хранения настроек приватности пользователя"""
    __tablename__ = "privacy_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    show_online_status = Column(bool, default=True)
    show_last_seen = Column(bool, default=True)
    show_profile_photo = Column(bool, default=True)
    show_age = Column(bool, default=True)
    show_location = Column(bool, default=True)
    allow_messages_from = Column(String, default="matches_only")
    allow_voice_calls = Column(bool, default=True)
    allow_video_calls = Column(bool, default=True)
    block_screenshots = Column(bool, default=True)
    two_factor_auth_enabled = Column(bool, default=False)
    data_deletion_on_inactive_days = Column(Integer, default=365)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now()) 