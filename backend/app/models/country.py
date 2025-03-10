from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String(2), unique=True)  # ISO 2-letter code
    phone_code = Column(String)
    min_age = Column(Integer)  # Минимальный возраст для регистрации
    requires_phone_verification = Column(Boolean, default=True)
    requires_email_verification = Column(Boolean, default=True)
    is_gdpr_applicable = Column(Boolean, default=False)  # Применяется ли GDPR
    is_active = Column(Boolean, default=True)  # Доступна ли страна для регистрации
    
    # Дополнительные правовые требования
    requires_parental_consent = Column(Boolean, default=False)
    requires_id_verification = Column(Boolean, default=False)
    max_photos_allowed = Column(Integer, default=9)
    data_retention_days = Column(Integer, default=365)  # Срок хранения данных 