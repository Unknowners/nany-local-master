# 🏗️ Стандарти кодування та архітектури

## 📋 Загальні принципи

### SOLID принципи
- **Single Responsibility**: Кожен клас/функція має одну відповідальність
- **Open/Closed**: Відкрито для розширення, закрито для модифікації  
- **Liskov Substitution**: Підкласи мають заміняти базові класи
- **Interface Segregation**: Багато специфічних інтерфейсів краще одного загального
- **Dependency Inversion**: Залежність від абстракцій, не від конкретних реалізацій

### DRY (Don't Repeat Yourself)
- Виносити повторюваний код в функції/класи
- Використовувати константи замість магічних чисел
- Створювати утиліти для загальних операцій

### KISS (Keep It Simple, Stupid)
- Простота краще складності
- Читабельність коду важливіша за "розумність"
- Якщо код потребує коментарів - можливо, його варто переписати

## 🧪 Тестування (ОБОВ'ЯЗКОВО!)

### ❗ Правило: ВСЯ функціональність ОБОВ'ЯЗКОВО покривається тестами

**Що тестувати:**
- ✅ **Всі API endpoints** - позитивні та негативні сценарії
- ✅ **Бізнес-логіка** - сервіси, утиліти, валідації
- ✅ **База даних** - моделі, міграції, запити
- ✅ **Аутентифікація** - JWT, дозволи, ролі
- ✅ **Інтеграції** - SMS, email, зовнішні API
- ✅ **Frontend компоненти** - хуки, утиліти, UI

### 🎯 Мінімальне покриття: 80%

```python
# ✅ Приклад тесту для API endpoint
def test_create_course_success():
    """Тест успішного створення курсу"""
    course_data = {
        "title": "Test Course",
        "description": "Test Description",
        "category": "programming"
    }
    response = client.post("/api/v1/courses", json=course_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == course_data["title"]

def test_create_course_unauthorized():
    """Тест створення курсу без авторизації"""
    course_data = {"title": "Test Course"}
    response = client.post("/api/v1/courses", json=course_data)
    assert response.status_code == 401
```

### 📁 Структура тестів
```
tests/
├── unit/           # Юніт-тести (функції, класи)
├── integration/    # Інтеграційні тести (API + DB)
├── e2e/           # End-to-end тести
├── fixtures/      # Тестові дані
└── conftest.py    # Налаштування pytest
```

### 🚀 Інструменти тестування

**Backend (Python):**
- `pytest` - основний фреймворк
- `pytest-asyncio` - для async тестів
- `httpx` - для тестування API
- `factory_boy` - генерація тестових даних
- `pytest-cov` - покриття коду

**Frontend (TypeScript):**
- `vitest` - основний фреймворк
- `@testing-library/react` - тестування компонентів
- `@testing-library/jest-dom` - DOM матчери
- `msw` - мокування API

### 📝 Правила написання тестів

1. **Один тест = одна перевірка**
2. **Назви тестів описують сценарій**: `test_user_login_with_invalid_password_returns_401`
3. **Arrange-Act-Assert** структура
4. **Незалежність тестів** - кожен тест може виконуватися окремо
5. **Очищення після тестів** - використовувати fixtures та teardown

## 🎯 Правила кодування

### 1. Іменування
```python
# ✅ Добре
class UserService:
    def get_user_by_id(self, user_id: str) -> User:
        pass

# ❌ Погано
class usrSrv:
    def getUsrById(self, id):
        pass
```

### 2. Типізація (обов'язково!)
```python
# ✅ Завжди використовувати типи
from typing import List, Optional, Dict, Any

def get_users(
    limit: int = 10, 
    offset: int = 0,
    filters: Optional[Dict[str, Any]] = None
) -> List[User]:
    pass

# ❌ Без типів
def get_users(limit=10, offset=0, filters=None):
    pass
```

### 3. Обробка помилок
```python
# ✅ Специфічні винятки
class UserNotFoundError(Exception):
    """Користувача не знайдено"""
    pass

def get_user(user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

### 4. Docstrings (обов'язково для публічних методів)
```python
def calculate_user_score(
    user_id: str, 
    criteria: List[str],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Розраховує оцінку користувача на основі критеріїв.
    
    Args:
        user_id: Унікальний ідентифікатор користувача
        criteria: Список критеріїв для оцінки
        weights: Ваги для кожного критерію (опціонально)
    
    Returns:
        Оцінка користувача від 0.0 до 10.0
    
    Raises:
        UserNotFoundError: Якщо користувача не знайдено
        InvalidCriteriaError: Якщо критерії некоректні
    """
    pass
```

## 📊 Логування

### Структуроване логування
```python
import logging
import json

logger = logging.getLogger(__name__)

def log_user_action(user_id: str, action: str, details: dict = None):
    log_data = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    logger.info(json.dumps(log_data))
```

## 📋 Чеклист перед commit

- [ ] Код відповідає стандартам форматування (black, isort)
- [ ] Всі тести проходять
- [ ] Додані типи для всіх функцій
- [ ] Написані docstrings для публічних методів
- [ ] Немає дублювання коду
- [ ] Обробляються всі можливі винятки
- [ ] Логування додано для важливих операцій

**Пам'ятайте**: Код пишеться один раз, але читається багато разів! 🎯