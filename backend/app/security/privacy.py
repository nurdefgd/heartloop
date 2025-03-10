from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Настройки безопасности
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PrivacySettings(BaseModel):
    """Настройки приватности пользователя"""
    show_online_status: bool = True
    show_last_seen: bool = True
    show_profile_photo: bool = True
    show_age: bool = True
    show_location: bool = True
    allow_messages_from: str = "matches_only"  # matches_only, verified_only, all
    allow_voice_calls: bool = True
    allow_video_calls: bool = True
    block_screenshots: bool = True
    data_deletion_on_inactive_days: int = 365

class DataProtection:
    """Класс для защиты персональных данных"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля"""
        return PWD_CONTEXT.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return PWD_CONTEXT.verify(plain_password, hashed_password)
    
    @staticmethod
    def mask_phone_number(phone: str) -> str:
        """Маскировка номера телефона"""
        if not phone:
            return ""
        return f"{'*' * (len(phone) - 4)}{phone[-4:]}"
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Маскировка email"""
        if not email or '@' not in email:
            return ""
        username, domain = email.split('@')
        masked_username = f"{username[0]}{'*' * (len(username) - 2)}{username[-1]}"
        return f"{masked_username}@{domain}"

class GDPRCompliance:
    """Соответствие требованиям GDPR"""
    
    @staticmethod
    def export_user_data(user_id: int) -> dict:
        """Экспорт всех данных пользователя"""
        # Здесь будет логика сбора всех данных пользователя
        pass
    
    @staticmethod
    def delete_user_data(user_id: int) -> bool:
        """Полное удаление данных пользователя"""
        # Здесь будет логика удаления всех данных
        pass
    
    @staticmethod
    def log_data_access(user_id: int, accessed_by: int, data_type: str):
        """Логирование доступа к данным"""
        # Здесь будет логика записи логов доступа
        pass

class DataEncryption:
    """Шифрование чувствительных данных"""
    
    @staticmethod
    def encrypt_message(message: str, key: str) -> str:
        """Шифрование сообщения"""
        # Здесь будет логика шифрования
        pass
    
    @staticmethod
    def decrypt_message(encrypted_message: str, key: str) -> str:
        """Дешифрование сообщения"""
        # Здесь будет логика дешифрования
        pass

# Настройки по умолчанию для разных регионов
PRIVACY_SETTINGS_BY_REGION = {
    "EU": PrivacySettings(
        show_online_status=False,
        show_last_seen=False,
        block_screenshots=True,
        data_deletion_on_inactive_days=180  # GDPR требование
    ),
    "USA": PrivacySettings(
        show_online_status=True,
        show_last_seen=True,
        block_screenshots=False,
        data_deletion_on_inactive_days=365
    ),
    "DEFAULT": PrivacySettings()
} 