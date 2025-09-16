# 🚀 Nanny Match - Платформа для пошуку нянь

Сучасна платформа для пошуку та підбору нянь в Україні з повним циклом онбордингу, автентифікації та управління профілями.

## 🌟 Основні можливості

- **👥 Двостороння платформа** - Для батьків та нянь
- **🔐 Безпечна автентифікація** - JWT токени, SMS OTP, bcrypt хешування
- **📱 Повний онбординг** - Динамічна конфігурація для різних ролей
- **🗄️ Розширені довідники** - Категорії, послуги, навички, локації
- **💬 SMS інтеграція** - TurboSMS для OTP та сповіщень
- **☁️ S3 сховище** - Зберігання фото та документів
- **🐳 Docker підтримка** - Повна контейнеризація
- **🔄 Гнучкі бекенди** - FastAPI, Supabase, локальна розробка

## 🏗️ Архітектура

```
nany/
├── nanny-match-backend/          # FastAPI Backend
│   ├── app/                      # Основна логіка
│   ├── alembic/                  # Міграції БД
│   ├── docker-compose.dev.yml    # Docker конфігурація
│   └── requirements.txt          # Python залежності
├── nanny-match-ukraine/          # React Frontend
│   ├── src/                      # React компоненти
│   ├── fastapi-backend-data/     # SQL схеми та дані
│   └── package.json              # Node.js залежності
└── README.md                     # Цей файл
```

## 🚀 Швидкий старт

### **1. Клонування репозиторію:**
```bash
git clone <repository-url>
cd nany
```

### **2. Запуск через Docker (рекомендовано):**
```bash
# Запуск всіх сервісів
cd nanny-match-backend
docker-compose -f docker-compose.dev.yml up -d

# Перевірка статусу
docker-compose -f docker-compose.dev.yml ps
```

### **3. Запуск локально:**
```bash
# Windows
start-dev.bat

# Linux/Mac
chmod +x start-dev.sh
./start-dev.sh

# Або через Makefile
make dev
```

## 🌐 Доступні сервіси

| Сервіс | URL | Опис |
|--------|-----|------|
| **Frontend** | http://localhost:8080 | React додаток |
| **Backend API** | http://localhost:8000 | FastAPI сервер |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Database** | localhost:5432 | PostgreSQL |
| **Redis** | localhost:6379 | Кеш та OTP |

## 🔧 Технологічний стек

### **Backend:**
- **FastAPI** - Веб фреймворк
- **PostgreSQL** - Основна база даних
- **Redis** - Кеш та OTP зберігання
- **SQLAlchemy** - ORM
- **Alembic** - Міграції БД
- **PyJWT** - JWT токени
- **bcrypt** - Хешування паролів
- **TurboSMS** - SMS API

### **Frontend:**
- **React 18** - UI фреймворк
- **TypeScript** - Типізація
- **Vite** - Збірка
- **React Router** - Маршрутизація
- **Zod** - Валідація
- **React Hook Form** - Форми
- **Tailwind CSS** - Стилізація

### **DevOps:**
- **Docker** - Контейнеризація
- **Docker Compose** - Оркестрація
- **Nginx** - Проксі (опціонально)

## 📊 База даних

### **Основні таблиці:**
- `profiles` - Профілі користувачів
- `data_categories` - Категорії довідників
- `reference_values` - Довідкові значення
- `onboarding_configs` - Конфігурації онбордингу
- `onboarding_steps` - Кроки онбордингу
- `user_onboarding_data` - Дані онбордингу користувачів

### **Міграції:**
```bash
cd nanny-match-backend
alembic upgrade head
```

## 🔐 Автентифікація

### **JWT токени:**
- **Access Token** - 15 хвилин
- **Refresh Token** - 7 днів
- **Алгоритм**: HS256

### **SMS OTP:**
- **Провайдер**: TurboSMS
- **Термін дії**: 5 хвилин
- **Зберігання**: Redis

### **Паролі:**
- **Хешування**: bcrypt
- **Сіль**: Автоматична
- **Мінімум**: 8 символів

## 📱 Онбординг

### **Конфігурація:**
- **Динамічна** - Налаштовується через БД
- **Роль-специфічна** - Різні кроки для батьків та нянь
- **Валідація** - Zod схеми на фронтенді

### **Кроки для батьків:**
1. Особиста інформація
2. Інформація про сім'ю
3. Вимоги до няні
4. Бюджет
5. Додаткові налаштування

### **Кроки для нянь:**
1. Особиста інформація
2. Досвід роботи
3. Послуги
4. Розклад
5. Додаткові налаштування

## 🗄️ Довідники

### **Категорії:**
- **Особиста інформація**: Стать, вікові групи, локації, мови
- **Послуги та навички**: Послуги, навички, області досвіду
- **Освіта**: Рівні освіти, сертифікати
- **Робота**: Типи розкладу, оплата, досвід
- **Характеристики**: Риси характеру, інтереси

### **Використання:**
```sql
-- Отримати всі категорії
SELECT * FROM data_categories WHERE is_active = true;

-- Отримати значення категорії
SELECT rv.* FROM reference_values rv
JOIN data_categories dc ON rv.category_id = dc.id
WHERE dc.code = 'services' AND rv.is_active = true;
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

# Перевірка міграцій
alembic current
alembic history
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

## 📚 Документація

### **Backend:**
- [README.md](nanny-match-backend/README.md) - Основна документація
- [API_EXAMPLES.md](nanny-match-backend/API_EXAMPLES.md) - Приклади API
- [SMS_GUIDE.md](nanny-match-backend/SMS_GUIDE.md) - SMS функціональність
- [S3_STORAGE_GUIDE.md](nanny-match-backend/S3_STORAGE_GUIDE.md) - S3 сховище
- [DEPLOYMENT.md](nanny-match-backend/DEPLOYMENT.md) - Розгортання

### **Frontend:**
- [README.md](nanny-match-ukraine/README.md) - Основна документація
- [PROJECT_OVERVIEW.md](nanny-match-ukraine/PROJECT_OVERVIEW.md) - Огляд проекту
- [FRONTEND_DEVELOPMENT_GUIDE.md](nanny-match-ukraine/FRONTEND_DEVELOPMENT_GUIDE.md) - Розробка
- [FASTAPI_BACKEND_GUIDE.md](nanny-match-ukraine/FASTAPI_BACKEND_GUIDE.md) - Інтеграція з FastAPI

### **Загальна:**
- [QUICK_START.md](QUICK_START.md) - Швидкий старт
- [PROJECT_STRUCTURE.md](nanny-match-backend/PROJECT_STRUCTURE.md) - Структура проекту

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

## 🚀 Розгортання

### **Development:**
```bash
make dev
```

### **Staging:**
```bash
make deploy-staging
```

### **Production:**
```bash
make deploy-production
```

## 🤝 Внесок у проект

1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/amazing-feature`)
3. Commit зміни (`git commit -m 'Add amazing feature'`)
4. Push до branch (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

Цей проект ліцензовано під MIT License - дивіться [LICENSE](LICENSE) файл для деталей.

## 📞 Підтримка

- **Email**: support@nanny-match.com
- **Telegram**: @nanny_match_support
- **GitHub Issues**: [Створити issue](https://github.com/your-repo/issues)

---

**🚀 Готово до розробки! Використовуйте `make dev` для найпростішого запуску!**

**💡 Порада**: Для швидкого старту просто запустіть `docker-compose -f docker-compose.dev.yml up -d` в папці `nanny-match-backend`!