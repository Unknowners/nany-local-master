# 🎯 Правила розробки для Cursor AI

## 📚 Документація проекту

Перед початком роботи обов'язково прочитайте:
- [Стандарти кодування](./coding-standards.md)
- [Архітектура FastAPI](./fastapi-architecture.md) 
- [Робочий процес](./development-workflow.md)
- [Шаблони коду](./code-templates.md) - для швидкого копіювання
- [Безпека терміналу](./terminal-safety.md) - **КРИТИЧНО ВАЖЛИВО!**

## 🗄️ База даних та міграції - КРИТИЧНО ВАЖЛИВО!

### ❗ **Правило №1: ЗАБОРОНЕНО змінювати схему БД без міграцій**

- 🚫 **НЕ ДОЗВОЛЕНО**: Створювати/змінювати таблиці через прямі SQL команди
- 🚫 **НЕ ДОЗВОЛЕНО**: Використовувати `psql`, `docker exec` для зміни схеми
- ✅ **ОБОВ'ЯЗКОВО**: Всі зміни схеми тільки через Alembic міграції
- ✅ **ОБОВ'ЯЗКОВО**: Спочатку створити SQLAlchemy модель, потім міграцію
- ✅ **ОБОВ'ЯЗКОВО**: Кожна зміна схеми = нова міграція з описовою назвою

```python
# ❌ НЕ ДОЗВОЛЕНО: прямі SQL команди
docker exec -i postgres psql -c "CREATE TABLE courses (...)"

# ✅ ОБОВ'ЯЗКОВО: через міграції
# 1. Додати модель в models.py
class Course(Base):
    __tablename__ = "courses"
    # ...

# 2. Створити міграцію
alembic revision --autogenerate -m "Add course tables"

# 3. Застосувати міграцію
alembic upgrade head
```

### 🔄 **Порядок роботи з БД:**
1. **Модель** → `models.py` (SQLAlchemy модель)
2. **Міграція** → `alembic revision` (автогенерація або вручну)
3. **Застосування** → `alembic upgrade head` (або через Docker)
4. **Тестування** → перевірити що все працює
5. **Документування** → оновити table_map в main.py

### ⚠️ **Виключення:**
- Якщо Alembic не може підключитися до Docker бази, створити міграцію вручну
- Завжди додавати нові моделі в імпорти та table_map endpoints

## 🧪 Тестування - КРИТИЧНО ВАЖЛИВО!

### ❗ **Правило №2: TDD - СПОЧАТКУ ТЕСТИ, ПОТІМ КОД**

**🔴 ЧЕРВОНИЙ → 🟢 ЗЕЛЕНИЙ → 🔵 РЕФАКТОР**

#### **Обов'язковий порядок розробки:**
1. **СПОЧАТКУ** написати тест (червоний)
2. **ПОТІМ** написати мінімальний код для проходження тесту (зелений)
3. **ПІСЛЯ** рефакторити код (синій)
4. **ПОВТОРИТИ** для наступної функції

```python
# ❌ ЗАБОРОНЕНО: писати код без тестів
def create_user(data):
    # код без попереднього тесту - ЗАБОРОНЕНО!
    pass

# ✅ ПРАВИЛЬНО: TDD підхід
# 1. СПОЧАТКУ тест:
def test_create_user_success():
    # Given
    user_data = {"name": "Test", "email": "test@example.com"}
    
    # When  
    result = create_user(user_data)
    
    # Then
    assert result.id is not None
    assert result.name == "Test"
    assert result.email == "test@example.com"

def test_create_user_invalid_email():
    # Given
    invalid_data = {"name": "Test", "email": "invalid"}
    
    # When & Then
    with pytest.raises(ValidationError):
        create_user(invalid_data)

# 2. ПОТІМ код:
def create_user(data):
    # Мінімальна реалізація для проходження тестів
    if "@" not in data["email"]:
        raise ValidationError("Invalid email")
    return User(id=uuid4(), name=data["name"], email=data["email"])
```

### 📋 **Обов'язкові типи тестів:**

#### **1. Unit тести (найважливіші):**
```python
# Кожна функція, метод, клас
def test_user_service_create_user():
    # Тестує UserService.create_user()
    pass

def test_password_hash_utility():
    # Тестує hash_password()
    pass
```

#### **2. Integration тести:**
```python  
# API endpoints
async def test_auth_login_endpoint():
    response = await client.post("/api/v1/auth/login", json=data)
    assert response.status_code == 200

# База даних
def test_user_repository_save():
    user = User(name="Test")
    saved_user = user_repository.save(user)
    assert saved_user.id is not None
```

#### **3. Frontend тести:**
```typescript
// Компоненти
test('LoginForm submits correct data', () => {
  render(<LoginForm />)
  // тест UI взаємодії
})

// Хуки
test('useAuth returns user data', () => {
  const { result } = renderHook(() => useAuth())
  // тест логіки хуків
})
```

### 🚀 **Інструменти та налаштування:**

#### **Backend:**
```bash
# Встановлення:
pip install pytest pytest-cov pytest-asyncio httpx factory-boy

# Запуск тестів:
pytest tests/ -v                    # Всі тести
pytest tests/unit/ -v               # Unit тести  
pytest tests/integration/ -v        # Integration тести
pytest --cov=app tests/             # З покриттям
pytest tests/test_auth.py::test_login -v  # Конкретний тест
```

#### **Frontend:**
```bash
# Встановлення:
npm install -D vitest @testing-library/react @testing-library/jest-dom msw

# Запуск тестів:
npm test                            # Всі тести
npm test -- --coverage              # З покриттям
npm test -- auth                    # Тести auth
```

### 📊 **Мінімальні вимоги покриття:**
- **Unit тести**: 90%+ покриття
- **Integration тести**: Всі API endpoints
- **Frontend тести**: Всі компоненти та хуки
- **E2E тести**: Критичні user flows

### 🚫 **ЗАБОРОНЕНО без тестів:**
- Додавати нові API endpoints
- Створювати нові сервіси  
- Змінювати бізнес-логіку
- Додавати нові компоненти
- Змінювати схеми баз даних
- Додавати нову функціональність

### ✅ **Приклад правильного TDD:**

```python
# 1. ЧЕРВОНИЙ: Спочатку тест (не проходить)
def test_send_otp_success():
    result = send_otp("+380501234567", "registration")
    assert result["success"] is True
    assert "otp_hash" in result

def test_send_otp_invalid_phone():
    with pytest.raises(ValidationError):
        send_otp("invalid", "registration")

# 2. ЗЕЛЕНИЙ: Мінімальний код (тест проходить)
def send_otp(phone, purpose):
    if not phone.startswith("+380"):
        raise ValidationError("Invalid phone")
    return {"success": True, "otp_hash": "test_hash"}

# 3. СИНІЙ: Рефакторинг (тести все ще проходять)
def send_otp(phone, purpose):
    validate_phone(phone)  # Винесли в окрему функцію
    otp_hash = generate_otp_hash(phone, purpose)
    return {"success": True, "otp_hash": otp_hash}
```

## 💻 Правила використання терміналу - КРИТИЧНО!

### ❗ **Правило №3: НЕ використовувати команди які можуть зависнути**

**🚫 ЗАБОРОНЕНІ команди:**
```bash
# ❌ НЕ ВИКОРИСТОВУВАТИ - можуть зависнути
curl http://localhost:8080          # може зависнути назавжди
npm run dev                         # інтерактивний процес
psql -c "SELECT * FROM big_table"   # може повернути багато даних
docker logs container_name          # може бути величезний лог

# ✅ БЕЗПЕЧНІ альтернативи
curl -m 5 http://localhost:8080     # таймаут 5 секунд
curl -s -I http://localhost:8080    # тільки заголовки
npm run dev > /dev/null 2>&1 &      # у фоні
psql -c "SELECT * FROM table LIMIT 5"  # обмежити результат
docker logs container_name --tail=10   # тільки останні 10 рядків
```

**🛡️ ОБОВ'ЯЗКОВІ параметри:**
- **Таймаути**: `-m 5`, `--timeout=5`, `--max-time 5`
- **Обмеження**: `LIMIT`, `--tail`, `| head -10`
- **Тихий режим**: `-s`, `--silent`, `> /dev/null`
- **Неінтерактивний**: `--yes`, `--no-input`, `-y`

### ⚡ **Швидкі перевірки замість довгих команд:**

```bash
# ✅ Замість curl до веб-сторінки
lsof -ti :8080                      # перевірити чи порт зайнятий
ps aux | grep "npm" | head -3       # перевірити процеси

# ✅ Замість читання великих файлів  
wc -l file.log                      # кількість рядків
tail -5 file.log                    # останні 5 рядків
head -10 file.log                   # перші 10 рядків

# ✅ Замість інтерактивних команд
docker ps --format "table {{.Names}}\t{{.Status}}"  # статус контейнерів
```

### 🔧 **Безпечні команди для перевірки:**

```bash
# Перевірка сервісів
curl -s -f -m 5 http://localhost:8000/health || echo "Service down"
docker ps --filter "name=nanny" --format "{{.Names}}: {{.Status}}"

# Перевірка портів
lsof -ti :8000 && echo "Port 8000 busy" || echo "Port 8000 free"

# Перевірка бази даних  
docker exec container_name pg_isready -U user -d db || echo "DB down"

# Перевірка процесів
pgrep -f "npm run dev" && echo "Frontend running" || echo "Frontend stopped"
```

## 🏗️ Архітектурні принципи

### 1. **Модульність - ОБОВ'ЯЗКОВО!**
- ❌ **НЕ писати все в один файл main.py**
- ✅ Розділяти код на роутери, сервіси, репозиторії
- ✅ Кожен модуль має одну відповідальність

### 2. **Структура проекту**
```
app/
├── routers/          # API endpoints
├── services/         # Бізнес-логіка  
├── repositories/     # Доступ до даних
├── models/          # SQLAlchemy моделі
├── schemas/         # Pydantic схеми
└── utils/           # Утиліти
```

### 3. **Шари відповідальності**
- **Router**: HTTP логіка, валідація запитів
- **Service**: Бізнес-логіка, координація
- **Repository**: Доступ до БД, CRUD операції
- **Model**: Структура даних, доменна логіка

## 🔧 Обов'язкові вимоги

### 1. **Типізація**
```python
# ✅ ЗАВЖДИ використовувати типи
def get_user(user_id: str) -> Optional[User]:
    pass

# ❌ Без типів - ЗАБОРОНЕНО
def get_user(user_id):
    pass
```

### 2. **Обробка помилок**
```python
# ✅ Специфічні винятки
class UserNotFoundError(Exception):
    pass

# ❌ Загальні винятки - ЗАБОРОНЕНО  
raise Exception("Error")
```

### 3. **Логування**
```python
# ✅ Структуроване логування
logger.info(f"✅ User {user_id} created successfully")
logger.error(f"❌ Failed to create user: {error}")

# ❌ Print statements - ЗАБОРОНЕНО
print("User created")
```

## 📋 Чеклист перед кожним commit

### 🧪 **ТЕСТУВАННЯ (ОБОВ'ЯЗКОВО):**
- [ ] **Написані тести ПЕРЕД кодом** (TDD підхід)
- [ ] **Всі тести проходять** (`pytest tests/ -v`)
- [ ] **Покриття ≥ 80%** (`pytest --cov=app tests/`)
- [ ] **Нові endpoints протестовані** (позитивні + негативні сценарії)
- [ ] **Не поламався існуючий функціонал** (regression тести)

### 💻 **ЯКІСТЬ КОДУ:**
- [ ] Код розділений на модулі (не все в main.py)
- [ ] Додані типи для всіх функцій
- [ ] Написані docstrings для публічних методів
- [ ] Обробляються всі винятки
- [ ] Додане логування для важливих операцій
- [ ] Немає дублювання коду
- [ ] Код відформатований (black, isort)

### 🔥 **КРИТИЧНО - НЕ КОМІТИТИ БЕЗ ТЕСТІВ!**
```bash
# ❌ ЗАБОРОНЕНО комітити без тестів:
git commit -m "Add new feature"  # Без тестів!

# ✅ ПРАВИЛЬНО:
# 1. Написати тести
pytest tests/test_new_feature.py -v

# 2. Переконатися що тести проходять  
pytest tests/ -v

# 3. Перевірити покриття
pytest --cov=app tests/

# 4. Тільки тоді комітити
git commit -m "Add new feature with tests (coverage: 85%)"
```

## 🚫 Заборонені практики

### ❌ Що НЕ робити:
1. **Писати все в main.py** - розділяйте на модулі!
2. **Функції без типів** - завжди додавайте типи
3. **Загальні винятки** - використовуйте специфічні
4. **Print для логування** - використовуйте logger
5. **Магічні числа** - виносьте в константи
6. **Дублювання коду** - створюйте утиліти
7. **Функції без docstrings** - документуйте публічні методи
8. **Тимчасові endpoints** - ніколи не створювати endpoints з префіксом TEMPORARY
9. **Моки в продакшні** - використовувати тільки реальні дані та міграції

## ✅ Рекомендовані практики

### 1. **Створення нового endpoint**
```python
# 1. Створити схему в schemas/
class UserCreate(BaseModel):
    email: EmailStr
    name: str

# 2. Додати метод в сервіс
class UserService:
    def create_user(self, data: UserCreate) -> User:
        pass

# 3. Додати endpoint в роутер
@router.post("/users/", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(data)
```

### 2. **Обробка помилок**
```python
# В сервісі
def get_user(self, user_id: str) -> User:
    user = self.repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user

# В роутері  
@router.get("/users/{user_id}")
async def get_user(user_id: str, service: UserService = Depends()):
    try:
        return await service.get_user(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
```

## 🎯 Коли створювати новий модуль

### Створюйте новий роутер коли:
- Додаєте нову функціональність (auth, users, orders)
- Роутер стає більше 200 рядків
- Логічно відокремлена область

### Створюйте новий сервіс коли:
- Складна бізнес-логіка
- Потрібна координація між репозиторіями
- Транзакційні операції

### Створюйте новий репозиторій коли:
- Нова сутність в БД
- Специфічні запити до БД
- Кешування даних

## 🔍 Code Review критерії

### Автоматично відхиляється якщо:
- Весь код в main.py
- Немає типів у функціях
- Використовуються загальні винятки
- Немає обробки помилок
- Print замість logger

### Схвалюється якщо:
- Модульна структура
- Повна типізація
- Правильна обробка помилок
- Структуроване логування
- Документація коду

## 🚀 Швидкий старт для нової фічі

1. **Планування**
   - Визначити які endpoints потрібні
   - Спроектувати схеми даних
   - Продумати бізнес-логіку

2. **Створення структури**
   ```bash
   # Створити файли
   touch app/routers/new_feature.py
   touch app/services/new_feature_service.py
   touch app/schemas/new_feature.py
   ```

3. **Реалізація**
   - Почати з схем (schemas)
   - Створити сервіс з бізнес-логікою
   - Додати роутер з endpoints
   - Підключити роутер в main.py

4. **Тестування**
   - Написати unit тести для сервісу
   - Написати integration тести для API
   - Перевірити всі edge cases

## 🚀 Продакшн деплойменти - КРИТИЧНО ВАЖЛИВО!

### ❗ **Правило №4: Тільки офіційні методи для продакшну**

**✅ ДОЗВОЛЕНІ методи виправлення продакшн даних:**
```bash
# 1. Alembic міграції
docker-compose exec backend alembic upgrade head

# 2. Seed data скрипти  
docker-compose exec backend python scripts/seed_data_complete.py

# 3. Makefile команди
make prod-migrate
make prod-seed

# 4. Офіційні скрипти виправлення
docker-compose exec backend python fix_production_data.py
```

**🚫 ЗАБОРОНЕНІ методи:**
```bash
# ❌ НЕ ВИКОРИСТОВУВАТИ на продакшні
curl -X POST /init-production-db          # тимчасові endpoints
docker exec postgres psql -c "INSERT..."  # прямі SQL запити
python create_mock_data.py                 # моки та тестові дані
```

### 🔍 **Діагностика проблем продакшну:**
```bash
# Перевірка стану міграцій
docker-compose exec backend alembic current
docker-compose exec backend alembic history

# Перевірка даних
docker-compose exec postgres psql -U app -d nanny_match_prod -c "SELECT COUNT(*) FROM onboarding_steps;"

# Перевірка логів
docker-compose logs backend | tail -20
```

### 📋 **Стандартний процес виправлення:**
1. **Написати тести** - спочатку тести для нової функціональності
2. **Діагностика** - визначити проблему через тести
3. **Локальне тестування** - всі тести мають проходити  
4. **Створення міграції** - якщо потрібні зміни схеми (з тестами!)
5. **Оновлення seed data** - якщо потрібні нові дані (з тестами!)
6. **Запуск всіх тестів** - переконатися що нічого не зламалося
7. **Деплой** - застосувати через офіційні команди
8. **Верифікація** - перевірити що все працює

### 🤖 **Автоматизація тестування:**

#### **Pre-commit хуки (обов'язково):**
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/ -v
        language: python
        pass_filenames: false
        always_run: true
        
      - id: pytest-cov
        name: pytest with coverage
        entry: pytest --cov=app --cov-fail-under=80 tests/
        language: python
        pass_filenames: false
        always_run: true
```

#### **Git hooks:**
```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "🧪 Running tests before commit..."
pytest tests/ -v || exit 1
pytest --cov=app --cov-fail-under=80 tests/ || exit 1
echo "✅ All tests passed!"
```

#### **Makefile команди:**
```bash
test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest --cov=app --cov-fail-under=80 tests/

test-watch: ## Run tests in watch mode
	pytest-watch tests/

ci-test: ## Run tests for CI
	pytest tests/ -v --junitxml=test-results.xml --cov=app --cov-report=xml
```

## 💡 Поради для ефективної роботи

1. **Почніть з малого** - створіть мінімальну робочу версію
2. **Рефакторьте поступово** - не намагайтеся переписати все одразу
3. **Тестуйте часто** - запускайте тести після кожної зміни
4. **Документуйте по ходу** - не залишайте документацію на потім
5. **Просіть ревью** - свіжий погляд завжди корисний
6. **Використовуйте офіційні методи** - особливо для продакшну
7. **ЗАВЖДИ тестуйте перед комітом** - запускайте pytest перед git commit

## 🚨 Що робити якщо тести падають

### ❌ **Якщо тести не проходять:**
```bash
# 1. НЕ КОМІТИТИ! Спочатку виправити тести
git add .  # ❌ НЕ РОБИТИ!

# 2. Запустити тести та подивитися помилки
pytest tests/ -v --tb=short

# 3. Виправити код або тести
# 4. Повторити до проходження всіх тестів
pytest tests/ -v

# 5. Тільки тоді комітити
git commit -m "Feature with tests"
```

### 🔄 **Якщо зламався існуючий функціонал:**
```bash
# 1. Відкотити зміни
git reset --hard HEAD~1

# 2. Написати regression тест
def test_existing_functionality_still_works():
    # тест для існуючого функціоналу
    pass

# 3. Переконатися що тест проходить на старому коді
pytest tests/test_regression.py -v

# 4. Внести зміни так, щоб всі тести проходили
```

### 🎯 **Золоте правило:**
**НІКОЛИ НЕ КОМІТИТИ КОД, ЯКИЙ НЕ ПОКРИТИЙ ТЕСТАМИ!**

**НІКОЛИ НЕ КОМІТИТИ КОД, ЯКИЙ ЛАМАЄ ІСНУЮЧІ ТЕСТИ!**

---

**Пам'ятайте**: 
- 🧪 **Тести спочатку** - код потім! 
- 🔍 **Якісний код** сьогодні = менше проблем завтра!
- 🛡️ **Тести** - це ваш щит від багів! 🎯