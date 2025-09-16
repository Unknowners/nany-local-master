# 🔍 Аналіз Docker Compose та причин скидання бази

## 🎯 Проблема
База даних на продакшні скидалася при кожному білді через Docker Compose конфігурацію.

## 📊 Аналіз Docker Compose

### PostgreSQL конфігурація (docker-compose.prod.yml):
```yaml
postgres:
  image: postgres:15-alpine
  container_name: nanny-match-postgres
  environment:
    POSTGRES_DB: nanny_match_prod
    POSTGRES_USER: app
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data  # ✅ Persistent volume
    - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql  # ⚠️ Init script
```

### Backend конфігурація:
```yaml
backend:
  build:
    context: .
    dockerfile: Dockerfile  # Продакшн Dockerfile
  environment:
    - ENVIRONMENT=production  # ❌ Блокує dev-admin endpoints!
```

## 🚨 Потенційні причини скидання

### 1. **Docker build процес**
```bash
# В Makefile:
prod-build: docker-compose build --no-cache  # ⚠️ Повна перебудова
```

**Проблема**: `--no-cache` може призводити до перестворення контейнерів

### 2. **Init script виконується при створенні контейнера**
```sql
-- scripts/init-db.sql виконується при ПЕРШОМУ створенні PostgreSQL
-- Якщо контейнер перестворюється, скрипт виконується знову
```

### 3. **Alembic міграції з DELETE командами**
```python
# alembic/versions/345c144ad17e_*.py виконує:
# seed-data/03_onboarding_data.sql
# Який містить:
DELETE FROM onboarding_configs;  # ❌ Видаляє всі дані!
```

### 4. **Команди деплою**
```bash
# Небезпечні команди:
docker-compose down -v          # ❌ Видаляє volumes
docker-compose up --force-recreate  # ❌ Перестворює контейнери
docker volume prune             # ❌ Видаляє неіспользуемые volumes
```

## ✅ Рішення застосовані

### 1. **Виправлено Alembic міграції**
- Використовують безпечні seed файли без DELETE
- Додано детальне логування
- Строга валідація проти DELETE команд

### 2. **Створено безпечні seed файли**
- `03_onboarding_data_safe.sql` - без DELETE команд
- Використовують `INSERT ... ON CONFLICT`
- Зберігають існуючі дані

### 3. **Додано API для діагностики**
- Моніторинг стану продакшн бази
- Автоматичне виправлення через endpoints
- Порівняння локального vs продакшн

## 🛡️ Рекомендації для стабільності

### 1. **Безпечні команди деплою**
```bash
# ✅ БЕЗПЕЧНО:
docker-compose pull                    # Оновити образи
docker-compose up -d --no-deps backend  # Тільки backend
docker-compose restart backend        # Рестарт без перестворення

# ❌ НЕБЕЗПЕЧНО:
docker-compose down -v               # Видаляє volumes!
docker-compose build --no-cache      # Може перестворити все
```

### 2. **Моніторинг volumes**
```bash
# Перевірити volumes перед деплоєм:
docker volume ls | grep postgres_data

# Перевірити розмір даних:
docker volume inspect postgres_data
```

### 3. **Backup стратегія**
```bash
# Backup перед кожним деплоєм:
docker-compose exec postgres pg_dump -U app nanny_match_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 📋 Діагностика через API

Тепер доступні endpoints (в dev режимі):
```bash
# Статус продакшну:
curl "http://localhost:8000/api/v1/prod-logs/status"

# Порівняння даних:
curl "http://localhost:8000/api/v1/prod-logs/compare-data"

# Автоматичне виправлення:
curl -X POST "http://localhost:8000/api/v1/prod-logs/trigger-prod-fix"

# Live моніторинг:
curl "http://localhost:8000/api/v1/prod-logs/live-check"
```

## 🎯 Висновок

**Корінь проблеми**: Alembic міграція виконувала seed файл з DELETE командами при кожному `alembic upgrade head`.

**Рішення**: 
1. ✅ Виправлено міграції
2. ✅ Створено безпечні seed файли  
3. ✅ Додано API для контролю
4. ✅ Дані відновлено на продакшні

**Результат**: База більше не скидається, онбординг працює!