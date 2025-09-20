# 🔍 **ДІАГНОСТИКА ПРОДАКШН БАЗИ ДАНИХ**

## 📊 **РЕЗУЛЬТАТИ ТЕСТУВАННЯ API**

### **✅ ЩО ПРАЦЮЄ:**
- **🌐 Сервер**: Живий та відповідає (200)
- **🔐 Авторизація**: `/api/v1/auth/me` працює (200)
- **📊 Лічильники**: `/api/v1/counters/dashboard/complete` працює (200)
- **👥 Profiles**: `/api/v1/profiles` працює (багато записів)
- **🎭 User_roles**: `/api/v1/user_roles` працює

### **❌ ЩО НЕ ПРАЦЮЄ:**
- **🔍 Search нянь**: `/api/v1/search/nannies/complete` → 500 "Помилка пошуку нянь"
- **👨‍👩‍👧‍👦 Search батьків**: `/api/v1/search/parents/complete` → 500 "Помилка пошуку батьків"
- **👩‍🍼 Nannies**: `/api/v1/nannies` → 200 але **ПОРОЖНЯ** (0 записів)
- **👨‍👩‍👧‍👦 Parents**: `/api/v1/parents` → 500 "Помилка отримання батьків"
- **📸 Profile_photos**: `/api/v1/profile_photos` → 404 (таблиця не існує)
- **💕 Swipes**: `/api/v1/swipes` → 404 (таблиця не існує)

---

## 🎯 **КОРЕНЕВІ ПРИЧИНИ ПРОБЛЕМ**

### **1. 🗄️ ВІДСУТНІ ТАБЛИЦІ:**
- **`profile_photos`** - не існує (404)
- **`swipes`** - не існує (404)

### **2. 📊 ПОРОЖНІ ТАБЛИЦІ:**
- **`nannies`** - існує але порожня (0 записів)

### **3. 🔧 ПРОБЛЕМИ З SQL ЗАПИТАМИ:**
- **`parents`** таблиця має проблеми (500 помилка)
- **Search ендпоінти** роблять JOIN з неіснуючими/порожніми таблицями

---

## 🛠️ **ПЛАН ВИПРАВЛЕННЯ**

### **🔥 КРИТИЧНО (зараз):**

#### **1. Запустити міграції бази даних:**
```bash
cd nanny-match-backend
export DATABASE_URL="postgresql://user:pass@host:port/db"
alembic upgrade head
```

#### **2. Створити відсутні таблиці:**
```sql
-- Таблиця для фото профілів
CREATE TABLE IF NOT EXISTS profile_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(user_id),
    photo_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Таблиця для свайпів
CREATE TABLE IF NOT EXISTS swipes (
    swipe_id BIGSERIAL PRIMARY KEY,
    from_user_id UUID NOT NULL REFERENCES profiles(user_id),
    to_user_id UUID NOT NULL REFERENCES profiles(user_id),
    swipe VARCHAR(10) NOT NULL CHECK (swipe IN ('like', 'pass')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (from_user_id, to_user_id)
);
```

#### **3. Додати тестових нянь:**
```sql
-- Додати записи в таблицю nannies для існуючих користувачів з роллю nanny
INSERT INTO nannies (user_id, age, hourly_rate, experience_years, about_me, education_level, languages_spoken, certifications, services_offered)
SELECT 
    p.user_id,
    25 as age,
    150.0 as hourly_rate,
    3 as experience_years,
    'Досвідчена няня' as about_me,
    'Вища' as education_level,
    ARRAY['українська', 'англійська'] as languages_spoken,
    ARRAY['Перша допомога'] as certifications,
    ARRAY['babysitting', 'tutoring'] as services_offered
FROM profiles p
WHERE p.role = 'nanny' 
AND NOT EXISTS (SELECT 1 FROM nannies n WHERE n.user_id = p.user_id);
```

#### **4. Виправити таблицю parents:**
```sql
-- Перевірити структуру таблиці parents
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'parents';

-- Якщо таблиця не існує, створити її
CREATE TABLE IF NOT EXISTS parents (
    user_id UUID PRIMARY KEY REFERENCES profiles(user_id),
    about_me TEXT,
    children_count INTEGER,
    children_ages TEXT,
    budget_min DECIMAL(10,2),
    budget_max DECIMAL(10,2),
    preferred_languages TEXT[],
    special_requirements TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### **⚠️ ВАЖЛИВО (після критичних виправлень):**

#### **5. Додати індекси для продуктивності:**
```sql
CREATE INDEX IF NOT EXISTS idx_profile_photos_user_id ON profile_photos(user_id);
CREATE INDEX IF NOT EXISTS idx_profile_photos_is_primary ON profile_photos(is_primary);
CREATE INDEX IF NOT EXISTS idx_swipes_from_user ON swipes(from_user_id);
CREATE INDEX IF NOT EXISTS idx_swipes_to_user ON swipes(to_user_id);
CREATE INDEX IF NOT EXISTS idx_nannies_user_id ON nannies(user_id);
CREATE INDEX IF NOT EXISTS idx_parents_user_id ON parents(user_id);
```

#### **6. Додати тестові фото:**
```sql
INSERT INTO profile_photos (user_id, photo_url, is_primary)
SELECT 
    user_id,
    '/placeholder.svg' as photo_url,
    true as is_primary
FROM profiles
WHERE NOT EXISTS (SELECT 1 FROM profile_photos pp WHERE pp.user_id = profiles.user_id);
```

---

## 🔧 **КОМАНДИ ДЛЯ ВИКОНАННЯ**

### **1. Підключення до продакшн бази:**
```bash
# Через Docker (якщо база в контейнері)
docker exec -it nany-postgres psql -U postgres -d nany_db

# Або через psql напряму
psql "postgresql://user:password@host:port/database"
```

### **2. Перевірка стану міграцій:**
```bash
cd nanny-match-backend
alembic current
alembic history
```

### **3. Запуск міграцій:**
```bash
cd nanny-match-backend
alembic upgrade head
```

### **4. Перевірка після виправлень:**
```bash
# Тестування API
curl -X GET "https://nany.datavertex.me/api/v1/search/nannies/complete?limit=3" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 **ОЧІКУВАНІ РЕЗУЛЬТАТИ ПІСЛЯ ВИПРАВЛЕНЬ**

### **✅ Після виконання плану:**
- **🔍 Search нянь**: 200 з даними
- **👨‍👩‍👧‍👦 Search батьків**: 200 з даними  
- **📸 Profile_photos**: 200 з тестовими фото
- **💕 Swipes**: 200 (готовий до використання)
- **📱 Фронтенд**: Почне працювати без помилок 500

### **📈 Покращення продуктивності:**
- Швидші запити завдяки індексам
- Правильні JOIN між таблицями
- Відсутність помилок 500

---

## 🚨 **ПОПЕРЕДЖЕННЯ**

### **⚠️ Перед виконанням:**
1. **Зробіть backup бази даних**
2. **Тестуйте на staging середовищі**
3. **Повідомте користувачів про технічні роботи**

### **🔒 Безпека:**
- Використовуйте транзакції для критичних змін
- Перевіряйте кожен крок
- Майте план відкату

---

## 🎯 **ПІДСУМОК**

**Проблема НЕ у фронтенді** - фронтенд правильно викликає API.

**Проблема в бекенді/базі даних:**
- Відсутні таблиці (`profile_photos`, `swipes`)
- Порожні таблиці (`nannies`)
- Проблеми з SQL запитами (`parents`)

**Після виправлення бази даних фронтенд почне працювати без змін!** 🚀
