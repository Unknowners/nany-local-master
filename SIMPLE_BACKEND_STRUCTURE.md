# 🚀 Проста структура бекенду

## 🎯 Мета
Створити мінімальну, зручну структуру з 3-5 файлами замість 27+ роутерів

## 📁 Нова структура

```
app/
├── main.py              # FastAPI app + основні ендпоінти
├── database.py          # Підключення до БД
├── sql_queries.py       # Всі SQL запити в одному місці
├── auth.py              # Аутентифікація та JWT
├── schemas.py           # Pydantic схеми
└── alembic/             # Міграції
    ├── versions/
    └── env.py
```

## 🔥 Основна ідея

### main.py - Все в одному файлі
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from .database import get_db
from .auth import get_current_user
from .sql_queries import SQL

app = FastAPI(title="Nanny Match API")

# === AUTH ===
@app.post("/api/v1/auth/login")
async def login(phone: str, password: str, db = Depends(get_db)):
    user = db.execute(text(SQL.GET_USER_BY_PHONE), {"phone": phone}).fetchone()
    # логіка логіну
    return {"access_token": token}

# === SWIPES ===
@app.post("/api/v1/swipes")
async def create_swipe(data: dict, user = Depends(get_current_user), db = Depends(get_db)):
    result = db.execute(text(SQL.CREATE_SWIPE), {
        "from_user_id": user["user_id"],
        "to_user_id": data["target_user_id"],
        "swipe": data["swipe_type"]
    })
    return {"success": True}

# === SEARCH ===
@app.get("/api/v1/search/nannies")
async def search_nannies(user = Depends(get_current_user), db = Depends(get_db)):
    nannies = db.execute(text(SQL.SEARCH_NANNIES), {
        "user_id": user["user_id"]
    }).fetchall()
    return {"data": nannies}

# і так далі...
```

### sql_queries.py - Всі SQL запити
```python
class SQL:
    # AUTH
    GET_USER_BY_PHONE = """
        SELECT user_id, phone, first_name, last_name, role, password_hash
        FROM profiles WHERE phone = :phone
    """
    
    CREATE_USER = """
        INSERT INTO profiles (user_id, phone, first_name, last_name, role, password_hash)
        VALUES (:user_id, :phone, :first_name, :last_name, :role, :password_hash)
        RETURNING user_id, phone, first_name, last_name, role
    """
    
    # SWIPES
    CREATE_SWIPE = """
        INSERT INTO swipes (from_user_id, to_user_id, swipe, created_at)
        VALUES (:from_user_id, :to_user_id, :swipe, NOW())
        ON CONFLICT (from_user_id, to_user_id) 
        DO UPDATE SET swipe = :swipe, created_at = NOW()
        RETURNING swipe_id
    """
    
    GET_MY_LIKES = """
        SELECT s.to_user_id::text as target_user_id, p.first_name, p.last_name
        FROM swipes s
        JOIN profiles p ON p.user_id = s.to_user_id::text
        WHERE s.from_user_id = :user_id AND s.swipe = 'like'
        ORDER BY s.created_at DESC
    """
    
    # SEARCH
    SEARCH_NANNIES = """
        SELECT p.user_id, p.first_name, p.last_name, p.location
        FROM profiles p
        WHERE p.role = 'nanny' 
          AND p.approved = true 
          AND p.onboarding_completed = true
          AND p.user_id NOT IN (
              SELECT s.to_user_id::text 
              FROM swipes s 
              WHERE s.from_user_id = :user_id
          )
        ORDER BY p.created_at DESC
    """
    
    # MATCHES
    GET_MATCHES = """
        SELECT DISTINCT
            CASE WHEN s1.from_user_id = :user_id 
                 THEN s1.to_user_id::text
                 ELSE s1.from_user_id::text
            END as matched_user_id,
            p.first_name, p.last_name
        FROM swipes s1
        JOIN swipes s2 ON s1.from_user_id = s2.to_user_id 
                      AND s1.to_user_id = s2.from_user_id
        JOIN profiles p ON p.user_id = CASE 
            WHEN s1.from_user_id = :user_id THEN s1.to_user_id::text
            ELSE s1.from_user_id::text
        END
        WHERE (s1.from_user_id = :user_id OR s1.to_user_id = :user_id)
          AND s1.swipe = 'like' AND s2.swipe = 'like'
    """
```

## ✅ Переваги нової структури

1. **Простота**: Все в одному місці
2. **Швидкість розробки**: Не треба шукати по файлах
3. **Легко дебагити**: Весь код видно одразу
4. **Менше імпортів**: Мінімум залежностей
5. **Прозорість**: SQL запити в одному файлі
6. **Швидкість**: Менше файлів = швидше завантаження

## 🔄 План міграції

### Крок 1: Створити новий main.py
- Перенести всі ендпоінти в один файл
- Використовувати прості SQL запити
- Мінімум залежностей

### Крок 2: Створити sql_queries.py
- Всі SQL запити в одному класі
- Легко знайти та змінити
- Можна логувати всі запити

### Крок 3: Спростити auth.py
- Тільки JWT логіка
- Без ORM моделей

### Крок 4: Видалити зайве
- Всі роутери (27 файлів)
- Всі сервіси (7 файлів)
- ORM моделі
- Складні схеми

## 🎯 Результат

Замість 35+ файлів → **5 файлів**
- main.py (~500-800 рядків)
- sql_queries.py (~200-300 рядків)
- auth.py (~100 рядків)
- database.py (~50 рядків)
- schemas.py (~100 рядків)

**Всього: ~1000 рядків замість 5000+**

## 🚀 Приклад використання

```python
# Один файл, все зрозуміло
@app.get("/api/v1/my-likes")
async def get_my_likes(user = Depends(get_current_user), db = Depends(get_db)):
    likes = db.execute(text(SQL.GET_MY_LIKES), {"user_id": user["user_id"]}).fetchall()
    return {"likes": [dict(like) for like in likes]}

# Легко додати новий ендпоінт
@app.post("/api/v1/new-feature")
async def new_feature(data: dict, user = Depends(get_current_user), db = Depends(get_db)):
    result = db.execute(text(SQL.NEW_FEATURE_QUERY), data)
    return {"success": True}
```

Це набагато простіше та зручніше!
