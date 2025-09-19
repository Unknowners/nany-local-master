# 📋 Nanny Match - Повна документація проекту

## 🎯 Огляд проекту

**Nanny Match** - це сучасна платформа для пошуку та підбору нянь в Україні з повним циклом онбордингу, автентифікації та управління профілями. Проект складається з чотирьох незалежних Git репозиторіїв та забезпечує двосторонню взаємодію між батьками та нянями.

## 🏗️ Архітектура системи

### Структура репозиторіїв

Проект організований як **моно-репозиторій з чотирма незалежними Git репозиторіями**:

```
nany/ (головний репозиторій)
├── nanny-match-backend/              # FastAPI Backend
├── nanny-match-ukraine/              # Користувацький Frontend (порт 8080)
├── nanny-match-ukraine-adminfront/   # Адмін Frontend (порт 8081)
└── [загальні конфігурації та скрипти]
```

### 1. **Головний репозиторій** (`nany/`)
- **Призначення**: Координація та загальні конфігурації
- **Вміст**:
  - `restart-all.sh` - основний скрипт запуску всієї системи
  - `start-dev.sh` - скрипт для розробки
  - `Makefile` - команди для управління проектом
  - Загальна документація проекту
  - `app/` - спільний код (роутери, сервіси)
  - `docker-compose.yml` - PostgreSQL для локальної розробки

### 2. **Backend репозиторій** (`nanny-match-backend/`)
- **Технології**: Python, FastAPI, PostgreSQL, Redis, SQLAlchemy
- **Порт**: 8000
- **Основні компоненти**:
  - JWT автентифікація з refresh токенами
  - SMS OTP через TurboSMS
  - Динамічний онбординг з конфігурацією через БД
  - Розширена система довідників
  - S3 інтеграція для файлів
  - Alembic міграції

### 3. **Користувацький Frontend** (`nanny-match-ukraine/`)
- **Технології**: React 18, TypeScript, Vite, Tailwind CSS
- **Порт**: 8080
- **Призначення**: Основний додаток для батьків та нянь
- **Функції**:
  - Реєстрація та автентифікація
  - Багатокроковий онбординг
  - Профілі користувачів
  - Пошук та матчинг
  - Чати та повідомлення

### 4. **Адмін Frontend** (`nanny-match-ukraine-adminfront/`)
- **Технології**: React 18, TypeScript, Vite, Tailwind CSS
- **Порт**: 8081
- **Призначення**: Адміністрування системи
- **Функції**:
  - Управління користувачами
  - Статистика та аналітика
  - Налаштування системи
  - Модерація контенту

## 🔧 Технологічний стек

### Backend
- **FastAPI** - Веб фреймворк з автоматичною документацією
- **PostgreSQL** - Основна реляційна база даних
- **Redis** - Кеш та зберігання OTP кодів
- **SQLAlchemy** - ORM для роботи з базою даних
- **Alembic** - Система міграцій
- **PyJWT** - JWT токени для автентифікації
- **bcrypt** - Безпечне хешування паролів
- **TurboSMS** - SMS API для OTP кодів
- **boto3** - S3 інтеграція для файлів

### Frontend
- **React 18** - UI фреймворк з хуками
- **TypeScript** - Статична типізація
- **Vite** - Швидка збірка та розробка
- **React Router** - Клієнтська маршрутизація
- **Zod** - Валідація схем даних
- **React Hook Form** - Управління формами
- **Tailwind CSS** - Utility-first CSS фреймворк
- **Lucide React** - Іконки

### DevOps
- **Docker & Docker Compose** - Контейнеризація
- **Nginx** - Зворотний проксі (опціонально)
- **Git** - Контроль версій (4 репозиторії)

## 🚀 Запуск системи

### Автоматичний запуск (рекомендовано)
```bash
# З кореневого каталогу
./restart-all.sh
```

Скрипт автоматично:
1. Зупинить всі попередні процеси
2. Запитає про тип backend (локальний/хмарний)
3. Запустить PostgreSQL через Docker
4. Запустить backend (якщо локальний)
5. Запустить користувацький frontend на порту 8080
6. Запустить адмін frontend на порту 8081

### Ручний запуск компонентів

#### 1. База даних (PostgreSQL)
```bash
# Запуск PostgreSQL через Docker
docker-compose up -d postgres
```

#### 2. Backend (FastAPI)
```bash
cd nanny-match-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Користувацький Frontend
```bash
cd nanny-match-ukraine
npm run dev -- --port 8080
```

#### 4. Адмін Frontend
```bash
cd nanny-match-ukraine-adminfront
npm run dev -- --port 8081
```

### Доступні сервіси після запуску

| Сервіс | URL | Опис |
|--------|-----|------|
| **Користувацький додаток** | http://localhost:8080 | Основний React додаток |
| **Адмін панель** | http://localhost:8081 | Адміністрування системи |
| **Backend API** | http://localhost:8000 | FastAPI сервер |
| **API Документація** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Альтернативна документація |
| **База даних** | localhost:5432 | PostgreSQL |

## 🔐 Система автентифікації

### JWT токени
- **Access Token**: 15 хвилин життя
- **Refresh Token**: 7 днів життя
- **Алгоритм**: HS256
- **Автоматичне оновлення** на фронтенді

### SMS OTP
- **Провайдер**: TurboSMS
- **Термін дії**: 5 хвилин
- **Зберігання**: Redis
- **Тестовий режим**: Включений для розробки

### Паролі
- **Хешування**: bcrypt з автоматичною сіллю
- **Мінімальна довжина**: 8 символів
- **Валідація**: На фронтенді та бекенді

### Тестові користувачі
```
Батько:
- Телефон: +380663556014
- Пароль: testpass123
- Роль: parent

Няня:
- Телефон: +380663556015
- Пароль: testpass123
- Роль: nanny
```

## 📱 Система онбордингу

### Архітектура
- **Динамічна конфігурація** через базу даних
- **Роль-специфічні кроки** для батьків та нянь
- **Валідація** через Zod схеми
- **Прогрес-бар** з візуальним відображенням

### Кроки для батьків
1. **Особиста інформація**: Ім'я, телефон, email, локація
2. **Інформація про сім'ю**: Кількість дітей, їх вік, особливості
3. **Вимоги до няні**: Необхідні послуги, навички, досвід
4. **Бюджет**: Грошові рамки та тип оплати
5. **Додаткові налаштування**: Графік, особливі вимоги

### Кроки для нянь
1. **Особиста інформація**: Ім'я, телефон, email, локація
2. **Досвід роботи**: Роки досвіду, вікові групи, сертифікати
3. **Послуги**: Типи послуг, які надає
4. **Розклад**: Доступність, графік роботи
5. **Додаткові налаштування**: Навички, особливості

## 🗄️ База даних

### Основні таблиці

#### Користувачі та профілі
- `profiles` - Профілі користувачів з основною інформацією
- `user_onboarding_data` - Дані онбордингу користувачів

#### Довідкова система
- `data_categories` - Категорії довідників
- `reference_values` - Довідкові значення
- `onboarding_configs` - Конфігурації онбордингу
- `onboarding_steps` - Кроки онбордингу

#### Основні довідники
- **Стать**: Чоловіча, Жіноча
- **Вікові групи**: 0-1 рік, 1-3 роки, 3-6 років, 6-12 років, 12-18 років
- **Локації**: Київ, Харків, Одеса, Дніпро, Львів, Запоріжжя
- **Мови**: Українська, Англійська, Російська, Польська, Німецька, Французька
- **Послуги**: Догляд за дитиною, Навчання, Приготування їжі, Прибирання, Супровід, Нічний догляд
- **Навички**: Перша допомога, Музика, Мистецтво, Спорт, Плавання, Водіння

### Міграції
```bash
cd nanny-match-backend
alembic upgrade head
```

## 🔄 Система перемикання бекендів

Frontend підтримує три типи бекендів:

### 1. Supabase (хмарний)
```
URL: http://localhost:8080?backend=supabase
Використання: Продакшн та швидка розробка
```

### 2. FastAPI локальний
```
URL: http://localhost:8080?backend=fastapi-local
Використання: Локальна розробка з повним контролем
```

### 3. FastAPI віддалений
```
URL: http://localhost:8080?backend=fastapi-remote
Використання: Тестування з віддаленим сервером
```

## ⚠️ Правила роботи з Git

### КРИТИЧНО ВАЖЛИВО: Окремі коміти для кожного репозиторію

**НІКОЛИ** не комітити зміни з кореневого каталогу для backend/frontend файлів!

```bash
# ✅ ПРАВИЛЬНО: Коміт в головному репозиторії
cd /Users/anton/Desktop/nany
git add .
git commit -m "📋 Додано загальну документацію"
git push

# ✅ ПРАВИЛЬНО: Коміт в backend
cd /Users/anton/Desktop/nany/nanny-match-backend
git add .
git commit -m "🔧 Виправлено API автентифікації"
git push

# ✅ ПРАВИЛЬНО: Коміт в користувацькому frontend
cd /Users/anton/Desktop/nany/nanny-match-ukraine
git add .
git commit -m "🎨 Оновлено UI онбордингу"
git push

# ✅ ПРАВИЛЬНО: Коміт в адмін frontend
cd /Users/anton/Desktop/nany/nanny-match-ukraine-adminfront
git add .
git commit -m "📊 Додано статистику користувачів"
git push
```

### .gitignore конфігурація
Головний репозиторій ігнорує підрепозиторії:
```
nanny-match-backend/
nanny-match-ukraine/
nanny-match-ukraine-adminfront/
```

## 🧪 Тестування

### API тестування
```bash
# Health check
curl http://localhost:8000/health

# Логін тестового користувача
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+380663556014", "password": "testpass123"}'

# Конфігурації онбордингу
curl http://localhost:8000/api/v1/onboarding/configs

# Довідники
curl http://localhost:8000/api/v1/reference/categories
```

### Frontend тестування
```bash
cd nanny-match-ukraine
npm test

cd nanny-match-ukraine-adminfront
npm test
```

### SMS тестування
1. Перейдіть на: http://localhost:8080?backend=fastapi-local
2. Перевірте в куті: "Backend: fastapi-local"
3. Перейдіть на /forgot-password
4. Введіть номер: +380663556014
5. SMS код з'явиться в логах бекенду

## 🚨 Troubleshooting

### Очищення процесів
```bash
# Зупинити ВСІ старі процеси
pkill -f "npm.*dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true  
pkill -f "uvicorn" 2>/dev/null || true

# Очистити порти примусово
lsof -ti :8080 | xargs -r kill -9 2>/dev/null || true
lsof -ti :8000 | xargs -r kill -9 2>/dev/null || true
lsof -ti :8081 | xargs -r kill -9 2>/dev/null || true
```

### Docker проблеми
```bash
# Перезапуск контейнерів
docker-compose down
docker-compose up -d

# Перевірка логів
docker-compose logs -f postgres
```

### База даних
```bash
# Підключення до БД
docker exec -it nany_postgres psql -U postgres -d nany_db

# Перевірка таблиць
\dt

# Перевірка даних
SELECT * FROM profiles LIMIT 5;
```

### Frontend проблеми
```bash
# Очищення кешу
rm -rf node_modules
npm cache clean --force
npm install
```

## 📊 Моніторинг та логування

### Backend логи
```bash
cd nanny-match-backend
tail -f debug.log
```

### Frontend логи
- Консоль браузера для помилок JavaScript
- Network tab для API запитів
- Vite dev server логи в терміналі

### База даних
```bash
# Моніторинг запитів
docker exec -it nany_postgres psql -U postgres -d nany_db -c "SELECT * FROM pg_stat_activity;"
```

## 🔮 Майбутні покращення

### В розробці
- [ ] Система матчингу батьків та нянь
- [ ] Чати та повідомлення
- [ ] Система рейтингів та відгуків
- [ ] Календар та бронювання
- [ ] Платіжна система
- [ ] Мобільний додаток

### Технічні покращення
- [ ] Кешування на рівні API
- [ ] Оптимізація запитів до БД
- [ ] CDN для статичних файлів
- [ ] Автоматичні тести
- [ ] CI/CD pipeline
- [ ] Моніторинг продакшн

## 📚 Додаткова документація

### Backend
- [README.md](nanny-match-backend/README.md) - Основна документація backend
- [API_EXAMPLES.md](nanny-match-backend/API_EXAMPLES.md) - Приклади API
- [SMS_GUIDE.md](nanny-match-backend/SMS_GUIDE.md) - SMS функціональність
- [S3_STORAGE_GUIDE.md](nanny-match-backend/S3_STORAGE_GUIDE.md) - S3 сховище

### Frontend
- [README.md](nanny-match-ukraine/README.md) - Документація користувацького frontend
- [PROJECT_OVERVIEW.md](nanny-match-ukraine/PROJECT_OVERVIEW.md) - Огляд проекту
- [FRONTEND_DEVELOPMENT_GUIDE.md](nanny-match-ukraine/FRONTEND_DEVELOPMENT_GUIDE.md) - Гід розробки

### Загальна
- [QUICK_START.md](QUICK_START.md) - Швидкий старт
- [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Структура репозиторіїв
- [DEVELOPMENT_INSTRUCTIONS.md](DEVELOPMENT_INSTRUCTIONS.md) - Інструкції розробки

## 🤝 Внесок у проект

1. Fork відповідний репозиторій
2. Створіть feature branch (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт змін (`git commit -m 'Add amazing feature'`)
4. Push до branch (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📞 Підтримка

- **Email**: support@nanny-match.com
- **Telegram**: @nanny_match_support
- **GitHub Issues**: Створюйте issues в відповідному репозиторії

---

**🚀 Готово до розробки! Використовуйте `./restart-all.sh` для найпростішого запуску всієї системи!**

**💡 Пам'ятайте**: Завжди комітьте зміни в правильному репозиторії та очищуйте процеси перед запуском!

