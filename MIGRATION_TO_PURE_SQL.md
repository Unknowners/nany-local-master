# 🚀 План міграції з SQLAlchemy ORM на чисті SQL + Alembic

## 🎯 Мета
Повністю відмовитися від SQLAlchemy ORM та перейти на:
- Чисті SQL запити через `sqlalchemy.text()`
- Alembic для міграцій замість ручних SQL файлів
- Простіші та швидші запити
- Легше дебагити та підтримувати

## 📋 План виконання

### ФАЗА 1: Підготовка інфраструктури ✅
- [x] Створити `SimpleSQLService` з базовими методами
- [x] Створити `simple_api` роутер для тестування
- [x] Додати debug ендпоінти для перевірки таблиць

### ФАЗА 2: Налаштування Alembic
- [ ] Ініціалізувати Alembic в проекті
- [ ] Створити базову міграцію з поточної схеми БД
- [ ] Перенести існуючі міграції в Alembic формат
- [ ] Налаштувати автогенерацію міграцій

### ФАЗА 3: Переписування критичних ендпоінтів
#### 3.1 Аутентифікація та користувачі
- [ ] `/api/v1/auth/*` - логін, реєстрація, OTP
- [ ] `/api/v1/profiles` - CRUD операції з профілями
- [ ] `/api/v1/auth/me` - отримання поточного користувача

#### 3.2 Онбординг
- [ ] `/api/v1/onboarding/save-simple`
- [ ] `/api/v1/onboarding/complete`
- [ ] `/api/v1/user_onboarding_data`

#### 3.3 Свайпи та матчі
- [ ] `/api/v1/swipes` - створення свайпів
- [ ] `/api/v1/swipes/my-likes` - мої лайки
- [ ] `/api/v1/swipes/received-likes` - отримані лайки
- [ ] `/api/v1/matches` - матчі

#### 3.4 Пошук
- [ ] `/api/v1/search/nannies/complete` - пошук нянь
- [ ] `/api/v1/search/parents/complete` - пошук батьків
- [ ] `/api/v1/nannies` - список нянь
- [ ] `/api/v1/parents` - список батьків

#### 3.5 Чати та повідомлення
- [ ] `/api/v1/chats` - список чатів
- [ ] `/api/v1/chats/{chat_id}/messages` - повідомлення
- [ ] Створення чатів при матчах

#### 3.6 Довідники
- [ ] `/api/v1/reference/categories`
- [ ] `/api/v1/reference/values/{category}`

### ФАЗА 4: Адміністративні ендпоінти
- [ ] Всі `/api/v1/admin/*` ендпоінти
- [ ] Статистика та лічильники
- [ ] Управління користувачами

### ФАЗА 5: Очищення коду
- [ ] Видалити SQLAlchemy моделі з `models.py`
- [ ] Видалити ORM сервіси
- [ ] Видалити старі роутери
- [ ] Оновити документацію

## 🛠 Технічний підхід

### Структура нового коду:
```
app/
├── services/
│   ├── sql_service.py          # Базовий SQL сервіс
│   ├── auth_sql_service.py     # Аутентифікація
│   ├── swipes_sql_service.py   # Свайпи та матчі
│   ├── search_sql_service.py   # Пошук
│   └── chat_sql_service.py     # Чати
├── routers/
│   ├── auth_sql.py            # Нові роутери з SQL
│   ├── swipes_sql.py
│   └── ...
├── alembic/                   # Alembic міграції
│   ├── versions/
│   └── env.py
└── schemas/                   # Pydantic схеми (залишаються)
```

### Переваги нового підходу:
1. **Прозорість**: Видно точно який SQL виконується
2. **Швидкість**: Немає ORM overhead
3. **Контроль**: Повний контроль над запитами
4. **Дебаг**: Легко логувати та дебагити SQL
5. **Міграції**: Alembic автоматично генерує міграції
6. **Типи**: Немає проблем з UUID vs VARCHAR

### Приклад нового коду:
```python
class AuthSQLService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_phone(self, phone: str) -> Optional[Dict]:
        query = """
            SELECT user_id, phone, first_name, last_name, 
                   role, onboarding_completed, created_at
            FROM profiles 
            WHERE phone = :phone
        """
        return self.execute_single(query, {"phone": phone})
    
    def create_user(self, user_data: Dict) -> Dict:
        query = """
            INSERT INTO profiles (user_id, phone, first_name, last_name, 
                                role, password_hash, created_at)
            VALUES (:user_id, :phone, :first_name, :last_name, 
                    :role, :password_hash, NOW())
            RETURNING user_id, phone, first_name, last_name, role
        """
        return self.execute_single(query, user_data)
```

## 📊 Прогрес виконання

### Поточний статус:
- ✅ Створено базову інфраструктуру
- ✅ Простий API для тестування
- 🔄 Тестування простих ендпоінтів
- ⏳ Налаштування Alembic

### Наступні кроки:
1. Протестувати простий API
2. Налаштувати Alembic
3. Почати переписування по одному ендпоінту
4. Поступово замінювати старі роутери

## 🎯 Результат
- Простіша архітектура
- Швидші запити
- Легше підтримувати
- Менше багів з типами даних
- Автоматичні міграції через Alembic
