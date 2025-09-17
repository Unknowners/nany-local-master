# 🚀 Покращена структура бекенду з доменним підходом

## 🎯 Мета
Створити чітку доменну структуру де кожен модуль відповідає за свою область

## 📁 Нова структура по доменах

```
app/
├── main.py                    # FastAPI app + реєстрація роутерів
├── database.py               # Підключення до БД
├── dependencies.py           # Загальні залежності
│
├── domains/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py         # Auth ендпоінти
│   │   ├── service.py        # Auth бізнес-логіка
│   │   ├── queries.py        # Auth SQL запити
│   │   ├── schemas.py        # Auth Pydantic схеми
│   │   └── utils.py          # JWT, хешування паролів
│   │
│   ├── swipes/
│   │   ├── __init__.py
│   │   ├── router.py         # Swipes ендпоінти
│   │   ├── service.py        # Swipes бізнес-логіка
│   │   ├── queries.py        # Swipes SQL запити
│   │   └── schemas.py        # Swipes схеми
│   │
│   ├── matches/
│   │   ├── __init__.py
│   │   ├── router.py         # Matches ендпоінти
│   │   ├── service.py        # Matches логіка
│   │   ├── queries.py        # Matches SQL
│   │   └── schemas.py        # Matches схеми
│   │
│   ├── search/
│   │   ├── __init__.py
│   │   ├── router.py         # Search ендпоінти
│   │   ├── service.py        # Search логіка
│   │   ├── queries.py        # Search SQL
│   │   └── schemas.py        # Search схеми
│   │
│   ├── onboarding/
│   │   ├── __init__.py
│   │   ├── router.py         # Onboarding ендпоінти
│   │   ├── service.py        # Onboarding логіка
│   │   ├── queries.py        # Onboarding SQL
│   │   └── schemas.py        # Onboarding схеми
│   │
│   ├── chats/
│   │   ├── __init__.py
│   │   ├── router.py         # Chat ендпоінти
│   │   ├── service.py        # Chat логіка
│   │   ├── queries.py        # Chat SQL
│   │   └── schemas.py        # Chat схеми
│   │
│   ├── profiles/
│   │   ├── __init__.py
│   │   ├── router.py         # Profile ендпоінти
│   │   ├── service.py        # Profile логіка
│   │   ├── queries.py        # Profile SQL
│   │   └── schemas.py        # Profile схеми
│   │
│   ├── reference/
│   │   ├── __init__.py
│   │   ├── router.py         # Reference ендпоінти
│   │   ├── service.py        # Reference логіка
│   │   ├── queries.py        # Reference SQL
│   │   └── schemas.py        # Reference схеми
│   │
│   └── admin/
│       ├── __init__.py
│       ├── router.py         # Admin ендпоінти
│       ├── service.py        # Admin логіка
│       ├── queries.py        # Admin SQL
│       └── schemas.py        # Admin схеми
│
├── shared/
│   ├── __init__.py
│   ├── exceptions.py         # Кастомні винятки
│   ├── utils.py             # Загальні утиліти
│   ├── constants.py         # Константи
│   └── validators.py        # Загальні валідатори
│
├── alembic/                 # Міграції
│   ├── versions/
│   └── env.py
│
└── tests/                   # Тести по доменах
    ├── auth/
    ├── swipes/
    ├── matches/
    └── ...
```

## 🔥 Приклад структури домену

### domains/auth/router.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from .service import AuthService
from .schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/v1/auth", tags=["🔐 Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    return service.login(request.phone, request.password)

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(request)
```

### domains/auth/service.py
```python
from sqlalchemy.orm import Session
from sqlalchemy import text
from .queries import AuthQueries
from .utils import verify_password, create_access_token
from ..shared.exceptions import AuthenticationError

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def login(self, phone: str, password: str):
        # Отримуємо користувача
        user = self.db.execute(
            text(AuthQueries.GET_USER_BY_PHONE), 
            {"phone": phone}
        ).fetchone()
        
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        
        # Створюємо токен
        token = create_access_token({"user_id": user.user_id})
        
        return {
            "access_token": token,
            "user": {
                "user_id": user.user_id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            }
        }
```

### domains/auth/queries.py
```python
class AuthQueries:
    GET_USER_BY_PHONE = """
        SELECT user_id, phone, first_name, last_name, email, role, 
               password_hash, onboarding_completed, created_at
        FROM profiles 
        WHERE phone = :phone
    """
    
    CREATE_USER = """
        INSERT INTO profiles (user_id, phone, first_name, last_name, 
                            email, role, password_hash, created_at)
        VALUES (:user_id, :phone, :first_name, :last_name, 
                :email, :role, :password_hash, NOW())
        RETURNING user_id, phone, first_name, last_name, role
    """
    
    UPDATE_USER_PASSWORD = """
        UPDATE profiles 
        SET password_hash = :password_hash, updated_at = NOW()
        WHERE user_id = :user_id
    """
```

### domains/auth/schemas.py
```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    phone: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserResponse(BaseModel):
    user_id: str
    phone: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
```

## ✅ Переваги такої структури

### 1. 🎯 Чіткий розподіл відповідальності
- Кожен домен відповідає тільки за свою область
- Легко знайти потрібний код
- Менше плутанини

### 2. 👥 Командна робота
- Різні розробники можуть працювати над різними доменами
- Менше конфліктів в Git
- Легше розподіляти задачі

### 3. 🧪 Тестування
- Кожен домен можна тестувати окремо
- Мокати тільки потрібні залежності
- Швидші тести

### 4. 🔄 Рефакторинг
- Можна переписувати по одному домену
- Не впливає на інші частини системи
- Легше експериментувати

### 5. 📦 Імпорти
- Чіткі залежності між доменами
- Менше циклічних імпортів
- Легше контролювати архітектуру

### 6. 🚀 Продуктивність
- Завантажуються тільки потрібні модулі
- Швидший старт додатку
- Менше пам'яті

## 🔄 План міграції

### Крок 1: Створити структуру доменів
```bash
mkdir -p app/domains/{auth,swipes,matches,search,onboarding,chats,profiles,reference,admin}
mkdir -p app/shared
mkdir -p tests/{auth,swipes,matches,search,onboarding,chats,profiles,reference,admin}
```

### Крок 2: Перенести код по доменах
- Почати з auth (найпростіший)
- Потім swipes та matches
- Поступово всі інші

### Крок 3: Оновити main.py
```python
from domains.auth.router import router as auth_router
from domains.swipes.router import router as swipes_router
from domains.matches.router import router as matches_router
# ... інші домени

app.include_router(auth_router)
app.include_router(swipes_router)
app.include_router(matches_router)
```

### Крок 4: Додати тести
- Тести для кожного домену окремо
- Інтеграційні тести між доменами

## 🎯 Результат

- **Чіткіша архітектура**: Кожен домен має свою відповідальність
- **Легше підтримувати**: Знаєш де шукати код
- **Швидша розробка**: Менше часу на пошук потрібного файлу
- **Кращі тести**: Можна тестувати кожен домен окремо
- **Командна робота**: Менше конфліктів при роботі в команді

Це набагато краща структура для довгострокового розвитку проекту!
