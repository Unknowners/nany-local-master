# 🏛️ Архітектура FastAPI проекту

## 📁 Структура директорій

```
app/
├── __init__.py
├── main.py                    # Тільки роутери та middleware
├── config.py                  # Конфігурація та налаштування
├── database.py               # Підключення до БД
├── dependencies.py           # Загальні залежності FastAPI
├── exceptions.py             # Кастомні винятки
├── middleware.py             # Middleware компоненти
├── models/                   # 📁 SQLAlchemy моделі
│   ├── __init__.py
│   ├── base.py              # Базова модель
│   ├── user.py              # Користувачі
│   ├── onboarding.py        # Онбординг моделі
│   └── ...
├── schemas/                  # 📁 Pydantic схеми
│   ├── __init__.py
│   ├── user.py              # Схеми користувачів
│   ├── onboarding.py        # Схеми онбордингу
│   └── ...
├── routers/                  # 📁 API роутери
│   ├── __init__.py
│   ├── auth.py              # Аутентифікація
│   ├── users.py             # Користувачі
│   ├── onboarding.py        # Онбординг
│   └── ...
├── services/                 # 📁 Бізнес-логіка
│   ├── __init__.py
│   ├── auth_service.py      # Сервіс аутентифікації
│   ├── user_service.py      # Сервіс користувачів
│   ├── onboarding_service.py # Сервіс онбордингу
│   └── ...
├── repositories/             # 📁 Доступ до даних
│   ├── __init__.py
│   ├── base_repository.py   # Базовий репозиторій
│   ├── user_repository.py   # Репозиторій користувачів
│   └── ...
├── utils/                    # 📁 Утиліти
│   ├── __init__.py
│   ├── auth.py              # Утиліти аутентифікації
│   ├── validators.py        # Валідатори
│   ├── formatters.py        # Форматування даних
│   └── ...
├── core/                     # 📁 Ядро системи
│   ├── __init__.py
│   ├── security.py          # Безпека
│   ├── logging.py           # Логування
│   └── ...
└── tests/                    # 📁 Тести
    ├── __init__.py
    ├── conftest.py          # Конфігурація тестів
    ├── test_auth.py         # Тести аутентифікації
    └── ...
```

## 🔧 FastAPI компоненти

### 1. Роутери
```python
from fastapi import APIRouter, Depends, HTTPException
from ..services.user_service import UserService
from ..schemas.user import UserCreate, UserResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends()
) -> UserResponse:
    """Створити нового користувача"""
    return await user_service.create_user(user_data)
```

### 2. Залежності (Dependency Injection)
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)
```

### 3. Pydantic схеми
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 🗃️ Шари архітектури

### 1. Роутери (Presentation Layer)
- Тільки HTTP логіка
- Валідація запитів/відповідей
- Аутентифікація/авторизація
- Серіалізація даних

### 2. Сервіси (Business Logic Layer)
- Бізнес-логіка додатку
- Координація між репозиторіями
- Валідація бізнес-правил
- Обробка транзакцій

### 3. Репозиторії (Data Access Layer)
- Доступ до бази даних
- CRUD операції
- Запити до БД
- Кешування

### 4. Моделі (Domain Layer)
- SQLAlchemy моделі
- Бізнес-сутності
- Доменна логіка

## 🔄 Потік даних

```
HTTP Request → Router → Service → Repository → Database
                ↓         ↓          ↓
HTTP Response ← Pydantic ← Business ← SQLAlchemy
```

## 🛡️ Безпека

### JWT Аутентифікація
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user_by_id(db, user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Валідація даних
```python
from pydantic import validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

## 🚀 Продуктивність

### Асинхронність
```python
async def get_user_with_profile(user_id: str) -> UserWithProfile:
    # Паралельне виконання запитів
    user_task = asyncio.create_task(get_user(user_id))
    profile_task = asyncio.create_task(get_profile(user_id))
    
    user, profile = await asyncio.gather(user_task, profile_task)
    return UserWithProfile(user=user, profile=profile)
```

### Кешування
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_permissions(user_id: str) -> List[str]:
    """Кешуємо права користувача"""
    return db.query(Permission).filter_by(user_id=user_id).all()
```