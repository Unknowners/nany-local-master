# 🔧 Виправлення онбордингу на продакшні

## 🎯 Проблема
На продакшн сервері `https://nany.datavertex.me`:
- ✅ Конфігурації онбордингу є (2 штуки)
- ❌ **Кроки онбордингу відсутні** (0 для обох конфігурацій)
- ⚠️ Довідники неповні (тільки 6 категорій замість 14)

## 📊 Поточний стан

### Конфігурації онбордингу:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Реєстрація няні", 
    "target_role": "nanny",
    "кроків": 0  // ❌ ПРОБЛЕМА
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002", 
    "name": "Реєстрація батьків",
    "target_role": "parent",
    "кроків": 0  // ❌ ПРОБЛЕМА
  }
]
```

### Очікуваний стан:
- **Parent конфігурація**: 7 кроків
- **Nanny конфігурація**: 9 кроків  
- **Довідники**: 14 категорій, ~48 значень

## 🚀 Рішення

### Варіант 1: Через Docker Compose (рекомендовано)
```bash
# 1. Підключитися до продакшн сервера
ssh user@your-production-server

# 2. Перейти в директорію проекту
cd /path/to/nanny-match-backend

# 3. Застосувати міграції
docker-compose exec backend alembic upgrade head

# 4. Запустити seed data
docker-compose exec backend python scripts/seed_data_complete.py

# 5. Перевірити результат
docker-compose exec backend python fix_production_data.py
```

### Варіант 2: Через Makefile
```bash
# Якщо є Makefile команди
make prod-migrate
make prod-seed
```

### Варіант 3: Перевірка та діагностика
```bash
# Перевірити статус міграцій
docker-compose exec backend alembic current
docker-compose exec backend alembic history

# Перевірити наявність seed файлів
docker-compose exec backend ls -la /app/seed-data/
```

## ✅ Перевірка після виправлення

### 1. Перевірка кроків онбордингу:
```bash
# Parent кроки (має бути 7)
curl "https://nany.datavertex.me/api/v1/onboarding_steps?config_id=550e8400-e29b-41d4-a716-446655440002"

# Nanny кроки (має бути 9)  
curl "https://nany.datavertex.me/api/v1/onboarding_steps?config_id=550e8400-e29b-41d4-a716-446655440001"
```

### 2. Перевірка довідників:
```bash
# Категорії (має бути ~14)
curl "https://nany.datavertex.me/api/v1/data_categories"

# Значення (має бути ~48)
curl "https://nany.datavertex.me/api/v1/reference_values"
```

## 🔍 Діагностика проблем

### Якщо seed data не застосовується:
1. **Перевірити логи**:
```bash
docker-compose logs backend | grep -i "seed\|onboarding\|error"
```

2. **Перевірити файли seed data**:
```bash
docker-compose exec backend ls -la /app/seed-data/
```

3. **Вручну виконати SQL**:
```bash
# Підключитися до БД
docker-compose exec postgres psql -U app -d nanny_match_prod

# Перевірити таблиці
\dt

# Перевірити дані
SELECT COUNT(*) FROM onboarding_steps;
SELECT COUNT(*) FROM reference_values;
```

## 📝 Файли для оновлення

Переконайтеся, що на продакшн сервері є актуальні файли:
- ✅ `schema/06_onboarding_tables.sql`
- ✅ `schema/07_reference_tables.sql`
- ✅ `seed-data/01_enums_data.sql`
- ✅ `seed-data/02_reference_data.sql`
- ✅ `seed-data/03_onboarding_data.sql`
- ✅ `scripts/seed_data_complete.py`
- ✅ `fix_production_data.py`

## 🎉 Очікуваний результат

Після виправлення фронтенд зможе:
- ✅ Завантажувати кроки онбордингу для nanny та parent
- ✅ Отримувати повний список довідників
- ✅ Проходити онбординг без помилки "дані кроку не знайдено"

## 🚨 Критично важливо

**Проблема не в CORS** - CORS працює ідеально!  
**Проблема в відсутності даних** - кроки онбордингу не завантажилися на продакшні.

Після виправлення даних всі функції фронтенду працюватимуть нормально!