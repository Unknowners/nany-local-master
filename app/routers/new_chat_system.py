"""
🚀 НОВА СИСТЕМА ЧАТІВ ТА ЛАЙКІВ
Прості ендпоінти на основі нових таблиць: swipes, pairs, payments, chat_threads
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from ..core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["💰 Нова система чатів"])

@router.get("/test-new-system")
async def test_new_system():
    """Тестовий ендпоінт для перевірки роботи нової системи"""
    return {"success": True, "message": "Нова система чатів працює!"}

@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Тестовий ендпоінт для перевірки бази даних"""
    try:
        # Перевірити кількість записів в swipes
        result = db.execute(text("SELECT COUNT(*) as count FROM swipes;"))
        swipes_count = result.fetchone().count
        
        # Перевірити кількість записів в pairs
        result = db.execute(text("SELECT COUNT(*) as count FROM pairs;"))
        pairs_count = result.fetchone().count
        
        return {
            "success": True,
            "message": "База даних працює!",
            "data": {
                "swipes_count": swipes_count,
                "pairs_count": pairs_count
            }
        }
    except Exception as e:
        logger.error(f"Помилка тестування БД: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Помилка БД: {str(e)}")

@router.get("/nannies/simple")
async def get_simple_nannies(
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Простий ендпоінт для отримання нянь без авторизації"""
    try:
        nannies_sql = """
        SELECT p.user_id, p.first_name, p.last_name, p.age, p.city
        FROM profiles p
        WHERE p.role = 'nanny' 
          AND p.is_active = true
        ORDER BY p.created_at DESC
        LIMIT :limit;
        """
        
        result = db.execute(text(nannies_sql), {"limit": limit})
        
        nannies = []
        for row in result.fetchall():
            nannies.append({
                "user_id": str(row.user_id),
                "first_name": row.first_name,
                "last_name": row.last_name,
                "age": row.age,
                "city": row.city
            })
        
        return {
            "success": True,
            "nannies": nannies,
            "count": len(nannies)
        }
        
    except Exception as e:
        logger.error(f"Помилка отримання нянь: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Помилка отримання нянь: {str(e)}")