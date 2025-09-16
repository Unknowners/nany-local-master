# 🚀 Швидкий старт - Nanny Match Ukraine

## ⚡ Найпростіший спосіб запуску

### **Docker (рекомендовано):**
```bash
# Клонування репозиторію
git clone <repository-url>
cd nany

# Запуск всіх сервісів
cd nanny-match-backend
docker-compose -f docker-compose.dev.yml up -d

# Перевірка статусу
docker-compose -f docker-compose.dev.yml ps
```

### **Windows:**
```bash
# Подвійний клік на файл
start-dev.bat

# Або в командному рядку
start-dev.bat
```

### **Linux/Mac:**
```bash
# Зробити виконуваним та запустити
chmod +x start-dev.sh
./start-dev.sh
```

### **Універсально (Makefile):**
```bash
# Встановити залежності
make install

# Запустити розробку
make dev
```

## 🎯 Що відбувається

### **Docker запуск:**
1. **PostgreSQL** - База даних на порту 5432
2. **Redis** - Кеш та OTP на порту 6379
3. **Backend** - FastAPI на порту 8000
4. **Frontend** - React на порту 8080

### **Локальний запуск:**
1. **Backend** - FastAPI сервер
2. **Frontend** - React додаток
3. **Автоматичне підключення** - Frontend до Backend

## 🌐 Доступні сервіси

| Сервіс | URL | Опис |
|--------|-----|------|
| **Frontend** | http://localhost:8080 | React додаток |
| **Backend API** | http://localhost:8000 | FastAPI сервер |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Database** | localhost:5432 | PostgreSQL |
| **Redis** | localhost:6379 | Кеш та OTP |

## 🔐 Тестові користувачі

### **Батько:**
- **Телефон**: +380663556014
- **Пароль**: testpass123
- **Роль**: parent

### **Няня:**
- **Телефон**: +380663556015
- **Пароль**: testpass123
- **Роль**: nanny

## 📱 SMS функціональність

- **Провайдер**: TurboSMS
- **OTP термін дії**: 5 хвилин
- **Тестовий режим**: Включений для розробки
- **Повторна відправка**: Обмежена

## 🗄️ База даних

### **Основні таблиці:**
- `profiles` - Профілі користувачів
- `data_categories` - Категорії довідників
- `reference_values` - Довідкові значення
- `onboarding_configs` - Конфігурації онбордингу
- `onboarding_steps` - Кроки онбордингу
- `user_onboarding_data` - Дані онбордингу

### **Довідники:**
- **Стать**: Чоловіча, Жіноча
- **Вікові групи**: 0-1 рік, 1-3 роки, 3-6 років, 6-12 років, 12-18 років
- **Локації**: Київ, Харків, Одеса, Дніпро, Львів, Запоріжжя
- **Мови**: Українська, Англійська, Російська, Польська, Німецька, Французька
- **Послуги**: Догляд за дитиною, Навчання, Приготування їжі, Прибирання, Супровід, Нічний догляд, Догляд за домашніми тваринами
- **Навички**: Перша допомога, Музика, Мистецтво, Спорт, Плавання, Водіння, Робота з особливими потребами

## 📋 Онбординг

### **Кроки для батьків:**
1. **Особиста інформація** - Ім'я, телефон, email
2. **Інформація про сім'ю** - Діти, їх вік, особливості
3. **Вимоги до няні** - Послуги, навички, досвід
4. **Бюджет** - Грошові рамки
5. **Додаткові налаштування** - Графік, локація

### **Кроки для нянь:**
1. **Особиста інформація** - Ім'я, телефон, email
2. **Досвід роботи** - Роки досвіду, вікові групи
3. **Послуги** - Типи послуг, які надає
4. **Розклад** - Доступність, графік роботи
5. **Додаткові налаштування** - Навички, сертифікати

## 🔍 Перевірка роботи

### **1. Перевірка сервісів:**
```bash
# Health check
curl http://localhost:8000/health

# API документація
open http://localhost:8000/docs

# Frontend
open http://localhost:8080
```

### **2. Тестування автентифікації:**
```bash
# Логін тестового користувача
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+380663556014", "password": "testpass123"}'
```

### **3. Перевірка онбордингу:**
```bash
# Конфігурації онбордингу
curl http://localhost:8000/api/v1/onboarding/configs

# Кроки для батьків
curl http://localhost:8000/api/v1/onboarding/steps/parent
```

### **4. Перевірка довідників:**
```bash
# Категорії довідників
curl http://localhost:8000/api/v1/reference/categories

# Послуги
curl http://localhost:8000/api/v1/reference/values/services
```

## 🚨 Troubleshooting

### **Docker проблеми:**
```bash
# Перезапуск контейнерів
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d

# Перевірка логів
docker-compose -f docker-compose.dev.yml logs -f
```

### **База даних:**
```bash
# Підключення до БД
docker exec -it nanny-match-postgres-dev psql -U app -d nanny_match

# Перевірка таблиць
\dt

# Перевірка даних
SELECT * FROM profiles LIMIT 5;
```

### **Frontend проблеми:**
```bash
# Очищення кешу
cd nanny-match-ukraine
rm -rf node_modules
npm cache clean --force
npm install
```

### **Backend проблеми:**
```bash
# Перевірка залежностей
cd nanny-match-backend
pip install -r requirements.txt

# Перевірка змінних середовища
cat .env
```

## 🧪 Тестування

### **API тести:**
```bash
cd nanny-match-backend
python test_api.py
```

### **SMS тести:**
```bash
cd nanny-match-ukraine
npm run test:sms
```

### **Frontend тести:**
```bash
cd nanny-match-ukraine
npm test
```

## 📚 Додаткові ресурси

### **Документація:**
- **[README.md](README.md)** - Основна документація
- **[ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md)** - Гід по онбордингу
- **[API_EXAMPLES.md](nanny-match-backend/API_EXAMPLES.md)** - Приклади API

### **Backend:**
- **[README.md](nanny-match-backend/README.md)** - Документація backend
- **[SMS_GUIDE.md](nanny-match-backend/SMS_GUIDE.md)** - SMS функціональність
- **[S3_STORAGE_GUIDE.md](nanny-match-backend/S3_STORAGE_GUIDE.md)** - S3 сховище

### **Frontend:**
- **[README.md](nanny-match-ukraine/README.md)** - Документація frontend
- **[PROJECT_OVERVIEW.md](nanny-match-ukraine/PROJECT_OVERVIEW.md)** - Огляд проекту
- **[FRONTEND_DEVELOPMENT_GUIDE.md](nanny-match-ukraine/FRONTEND_DEVELOPMENT_GUIDE.md)** - Розробка

## 🎯 Наступні кроки

1. **Запустіть проект** - Використовуйте Docker або локальний запуск
2. **Протестуйте автентифікацію** - Увійдіть з тестовими користувачами
3. **Пройдіть онбординг** - Створіть профіль батька або няні
4. **Дослідіть API** - Використовуйте Swagger UI
5. **Розпочніть розробку** - Додавайте нові функції

---

**🚀 Готово! Використовуйте `docker-compose -f docker-compose.dev.yml up -d` для найшвидшого запуску!**

**💡 Порада**: Для швидкого старту просто запустіть Docker команду в папці `nanny-match-backend`!