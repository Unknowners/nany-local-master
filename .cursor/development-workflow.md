# 🔄 Робочий процес розробки

## 💻 Безпечне використання терміналу - ВАЖЛИВО!

### ❗ НЕ використовувати команди які можуть зависнути

**🚫 ЗАБОРОНЕНІ команди:**
- `curl http://localhost:8080` ← може зависнути назавжди
- `npm run dev` ← інтерактивний, використовуй `npm run dev &`
- `docker logs container` ← може бути величезний, використовуй `--tail=10`
- `psql -c "SELECT * FROM table"` ← може повернути мільйони записів

**✅ БЕЗПЕЧНІ альтернативи:**
- `curl -s -f -m 5 http://localhost:8080/health` ← таймаут 5 сек
- `lsof -ti :8080` ← швидка перевірка порту  
- `docker ps --format "{{.Names}}: {{.Status}}"` ← короткий статус
- `tail -10 backend.log` ← тільки останні рядки

## 🛠️ Інструменти розробки

### Обов'язкові інструменти
```bash
# Форматування коду
pip install black isort

# Лінтинг та типи
pip install flake8 mypy

# Тестування (ОБОВ'ЯЗКОВО!)
pip install pytest pytest-asyncio pytest-cov httpx factory-boy

# Безпека
pip install bandit safety
```

### Конфігурація інструментів

#### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## 📋 Pre-commit hooks

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

## 🧪 Тестування

### Структура тестів
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class TestUserService:
    def test_create_user_success(self, db_session: Session):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}
        service = UserService(db_session)
        
        # Act
        result = service.create_user(user_data)
        
        # Assert
        assert result.email == "test@example.com"
        assert result.id is not None
    
    def test_create_user_duplicate_email(self, db_session: Session):
        # Arrange & Act & Assert
        with pytest.raises(UserAlreadyExistsError):
            service.create_user({"email": "existing@example.com"})
```

### Фікстури для тестів
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def db_session(engine):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
```

## 🚀 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        black --check .
        isort --check-only .
        flake8 .
        mypy .
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Security check
      run: |
        bandit -r app/
        safety check
```

## 📝 Git Workflow

### Структура гілок
```
main                    # Продакшн код
├── develop            # Розробка
├── feature/user-auth  # Нові фічі
├── bugfix/login-fix   # Виправлення багів
└── hotfix/security    # Критичні виправлення
```

### Commit повідомлення
```
feat: додати аутентифікацію користувачів
fix: виправити помилку валідації email
docs: оновити документацію API
style: форматування коду
refactor: рефакторинг сервісу користувачів
test: додати тести для онбордингу
chore: оновити залежності
```

## 🔍 Code Review

### Чеклист для ревью
- [ ] Код відповідає стандартам проекту
- [ ] Всі тести проходять
- [ ] Додана документація
- [ ] Немає дублювання коду
- [ ] Обробляються винятки
- [ ] Безпека врахована
- [ ] Продуктивність оптимальна

### Коментарі в PR
```
# Позитивні коментарі
✅ Гарне використання типів!
✅ Чудова обробка помилок
✅ Добре покриття тестами

# Конструктивні зауваження
💡 Можна винести це в окремий метод
🔧 Варто додати валідацію тут
📝 Потрібен docstring для цього методу
```

## 📊 Моніторинг якості коду

### Метрики
- **Покриття тестами**: мінімум 80%
- **Складність коду**: максимум 10 (cyclomatic complexity)
- **Дублювання**: максимум 3%
- **Технічний борг**: контролювати через SonarQube

### Інструменти
```bash
# Покриття тестами
pytest --cov=app --cov-report=html

# Складність коду
radon cc app/ -a

# Дублювання коду
pylint --load-plugins=pylint.extensions.check_elif app/
```

## 🎯 Definition of Done

Завдання вважається виконаним, коли:

- [ ] Код написаний згідно стандартів
- [ ] Всі тести написані та проходять
- [ ] Code review пройдено
- [ ] Документація оновлена
- [ ] CI/CD pipeline проходить
- [ ] Безпека перевірена
- [ ] Продуктивність протестована
- [ ] Деплой на staging успішний

## 🚨 Troubleshooting

### Часті проблеми та рішення

#### Import помилки
```bash
# Перевірити PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Або використовувати editable install
pip install -e .
```

## 🧪 Тестування - ОБОВ'ЯЗКОВА ЧАСТИНА РОЗРОБКИ

### ❗ Правило: Код без тестів = НЕПРИЙНЯТНИЙ код

#### Запуск тестів
```bash
# Запустити всі тести
pytest

# З покриттям коду (мін. 80%)
pytest --cov=app --cov-report=html --cov-report=term

# Тільки швидкі тести
pytest -m "not slow"

# Конкретний модуль
pytest tests/test_auth.py -v
```

#### Структура тестів
```bash
tests/
├── conftest.py          # Налаштування pytest та fixtures
├── unit/               # Юніт-тести (швидкі)
│   ├── test_services.py
│   ├── test_utils.py
│   └── test_models.py
├── integration/        # Інтеграційні тести (з БД)
│   ├── test_api_auth.py
│   ├── test_api_admin.py
│   └── test_database.py
├── e2e/               # End-to-end тести
│   └── test_user_flow.py
└── fixtures/          # Тестові дані
    ├── users.py
    └── courses.py
```

#### Приклад тесту API
```python
def test_create_course_success(client, auth_headers):
    """Тест успішного створення курсу"""
    course_data = {
        "title": "Python Basics",
        "description": "Learn Python programming",
        "category": "programming"
    }
    
    response = client.post(
        "/api/v1/courses", 
        json=course_data, 
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == course_data["title"]
    assert "id" in data
```

#### Тести не проходять
```bash
# Запустити з детальним виводом
pytest -v -s

# Запустити конкретний тест
pytest tests/test_auth.py::test_login -v

# Показати покриття коду
pytest --cov=app --cov-report=term-missing
```

#### Проблеми з базою даних
```bash
# Перевірити міграції
alembic current
alembic upgrade head

# Створити нову міграцію
alembic revision --autogenerate -m "description"
```