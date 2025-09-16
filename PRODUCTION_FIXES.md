# 🔧 Виправлення проблем продакшн середовища

## 🎯 Проблема
На продакшні не заповнювалися довідники та онбординги через неправильні шляхи до файлів у міграціях та скриптах.

## ✅ Виправлені проблеми

### 1. Синтаксична помилка в app/main.py
**Проблема**: IndentationError на лінії 141
**Рішення**: Виправлено вирівнювання коду в блоці try-except

### 2. Неправильні шляхи в Alembic міграції
**Файл**: `alembic/versions/345c144ad17e_add_complete_onboarding_and_reference_.py`
**Проблема**: Міграція шукала файли в `../../nanny-match-ukraine/fastapi-backend-data/`
**Рішення**: Змінено шляхи на `../../schema` та `../../seed-data`

### 3. Неправильні шляхи в seed скрипті
**Файл**: `scripts/seed_data_complete.py`
**Проблема**: Скрипт шукав файли в `../../nanny-match-ukraine/fastapi-backend-data/`
**Рішення**: Змінено шляхи на `../seed-data`

### 4. Створено скрипт виправлення для продакшну
**Файл**: `fix_production_data.py`
**Призначення**: Автоматичне виправлення даних на продакшні з обробкою помилок

## 🚀 Інструкції для деплою на продакшн

### 1. Локальне тестування (завершено ✅)
```bash
cd nanny-match-backend
export DATABASE_URL="postgresql://app:app@localhost:5432/nanny_match"
python fix_production_data.py
```

### 2. Деплой на продакшн
```bash
# 1. Запуск міграцій
make prod-migrate
# або
docker-compose exec backend alembic upgrade head

# 2. Заповнення даних
make prod-seed
# або
docker-compose exec backend python scripts/seed_data_complete.py

# 3. Альтернативно - використати скрипт виправлення
docker-compose exec backend python fix_production_data.py
```

### 3. Перевірка результату
```bash
# Підключення до бази даних продакшн
docker-compose exec postgres psql -U app -d nanny_match_prod

# Перевірка довідників
SELECT COUNT(*) FROM data_categories;
SELECT COUNT(*) FROM reference_values;

# Перевірка онбордингу
SELECT COUNT(*) FROM onboarding_configs;
SELECT COUNT(*) FROM onboarding_steps;
SELECT COUNT(*) FROM onboarding_fields;
```

## 📊 Очікувані результати

Після виправлення повинні бути наступні дані:
- **Категорії довідників**: ~14
- **Значення довідників**: ~48
- **Конфігурації онбордингу**: 2 (parent, nanny)
- **Кроки онбордингу**: ~16 (7 для батьків + 9 для нянь)
- **Поля онбордингу**: залежить від конфігурації

## 🔍 Діагностика проблем

### Якщо міграції не спрацьовують:
```bash
# Перевірити статус міграцій
docker-compose exec backend alembic current
docker-compose exec backend alembic history

# Примусово застосувати конкретну міграцію
docker-compose exec backend alembic upgrade 345c144ad17e
```

### Якщо seed data не завантажуються:
```bash
# Перевірити наявність файлів
docker-compose exec backend ls -la /app/seed-data/

# Запустити скрипт виправлення
docker-compose exec backend python fix_production_data.py
```

### Перевірка API онбордингу:
```bash
# Тестування API
curl -X GET https://nany.datavertex.me/api/v1/onboarding/configs
curl -X GET https://nany.datavertex.me/api/v1/onboarding/steps/parent
curl -X GET https://nany.datavertex.me/api/v1/reference/categories
```

## 🛡️ Безпека

- Всі скрипти мають обробку помилок
- Дублікати ігноруються автоматично
- Транзакції використовуються для цілісності даних
- Логування всіх операцій

## 📝 Примітки

1. **Резервне копіювання**: Завжди робіть backup перед застосуванням змін на продакшні
2. **Тестування**: Всі зміни протестовані на локальному середовищі
3. **Моніторинг**: Після деплою перевірте логи та API endpoints
4. **Rollback**: У разі проблем можна відкотити міграції: `alembic downgrade -1`

## 🎉 Результат

Після застосування всіх виправлень:
- ✅ Довідники заповнюються автоматично
- ✅ Онбординг конфігурації створюються
- ✅ API онбордингу працює коректно
- ✅ Frontend отримує всі необхідні дані