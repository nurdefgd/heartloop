from fastapi import APIRouter, HTTPException
from typing import List
import random
from ..demo.test_data import DEMO_USERS, DEMO_INTERESTS, generate_demo_match, generate_demo_chat_history

router = APIRouter(prefix="/demo", tags=["demo"])

@router.post("/login")
async def demo_login():
    """Быстрый вход в демо-режим"""
    return {
        "access_token": "demo_token",
        "token_type": "bearer",
        "user": DEMO_USERS[0]
    }

@router.get("/matches")
async def get_demo_matches():
    """Получить список демо-матчей"""
    matches = []
    for user in DEMO_USERS[1:]:  # Исключаем первого пользователя (текущий)
        match_data = generate_demo_match()
        matches.append({
            "user": user,
            "match_data": match_data
        })
    return matches

@router.get("/swipe")
async def get_demo_profile():
    """Получить случайный профиль для свайпа"""
    profile = random.choice(DEMO_USERS[1:])
    profile["compatibility"] = random.randint(60, 99)
    return profile

@router.get("/chat/{user_id}")
async def get_demo_chat(user_id: str):
    """Получить демо-историю чата"""
    return {
        "messages": generate_demo_chat_history(),
        "user": next((u for u in DEMO_USERS if u["username"] == user_id), None)
    }

@router.get("/interests")
async def get_demo_interests() -> List[str]:
    """Получить список интересов для выбора"""
    return DEMO_INTERESTS

@router.post("/profile/update")
async def update_demo_profile(profile_data: dict):
    """Обновить демо-профиль (имитация)"""
    return {
        "message": "Profile updated successfully",
        "profile": {**DEMO_USERS[0], **profile_data}
    } 