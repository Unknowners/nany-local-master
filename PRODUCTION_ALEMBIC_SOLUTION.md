# 🔧 Рішення проблеми Alembic на продакшні

## 🎯 Проблема
На продакшн сервері відсутні дані онбордингу через те, що:
1. **Dev-admin endpoints** не працюють в production режимі
2. **Alembic міграції** не застосовувалися правильно
3. **Seed data** не завантажувався

## 📊 Діагностика показала:

| Компонент | Локально | Продакшн | Проблема |
|-----------|----------|----------|----------|
| Конфігурації онбордингу | 2 | **0** | ❌ Відсутні |
| Кроки онбордингу | 16 | **0** | ❌ Відсутні |
| Поля онбордингу | 8 | **0** | ❌ Відсутні |
| Категорії довідників | 14 | 6 | ⚠️ Неповні |
| Значення довідників | 48 | 2 | ⚠️ Неповні |

## ✅ Рішення

### 1. Додано admin_init роутер
**Файл**: `app/main.py`
```python
from .routers import auth, admin, onboarding, admin_init
app.include_router(admin_init.router)
```

### 2. Доступні admin endpoints на продакшні:
```bash
# Перевірка статусу БД
GET /api/v1/admin/status

# Ініціалізація БД (потребує секретний ключ)
POST /api/v1/admin/init-database
Headers: X-Init-Secret: your-secret-key
```

## 🚀 Інструкції для виправлення

### Варіант 1: Через admin API (після деплою змін)
```bash
# 1. Встановити секретний ключ на продакшн сервері
export ADMIN_INIT_SECRET="your-secure-secret-key-here"

# 2. Перевірити статус
curl "https://nany.datavertex.me/api/v1/admin/status"

# 3. Ініціалізувати БД
curl -X POST "https://nany.datavertex.me/api/v1/admin/init-database" \
  -H "X-Init-Secret: your-secure-secret-key-here"
```

### Варіант 2: Через Docker Compose (стандартний)
```bash
# На продакшн сервері
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data_complete.py
```

### Варіант 3: Через Makefile
```bash
make prod-migrate
make prod-seed
```

## 🔍 Перевірка Alembic на продакшні

### Перевірити, чи встановлений Alembic:
```bash
docker-compose exec backend python -c "import alembic; print('✅ Alembic available')"
docker-compose exec backend alembic --version
```

### Перевірити стан міграцій:
```bash
docker-compose exec backend alembic current
docker-compose exec backend alembic history
```

### Перевірити файли міграцій:
```bash
docker-compose exec backend ls -la /app/alembic/versions/
```

## 📋 Файли для деплою

Після оновлення `app/main.py` потрібно:
1. **Зробити commit змін**
2. **Задеплоїти на продакшн** (rebuild контейнера)
3. **Встановити ADMIN_INIT_SECRET** в змінних середовища
4. **Використати admin API** для ініціалізації

## 🎉 Очікуваний результат

Після виправлення:
- ✅ **2 конфігурації** онбордингу (parent + nanny)
- ✅ **16 кроків** онбордингу (7 parent + 9 nanny)
- ✅ **14 категорій** довідників
- ✅ **48 значень** довідників
- ✅ **Фронтенд працює** без помилок "дані кроку не знайдено"

## 🛡️ Безпека

Admin endpoints захищені секретним ключем, який має бути встановлений тільки на продакшн сервері в змінних середовища.