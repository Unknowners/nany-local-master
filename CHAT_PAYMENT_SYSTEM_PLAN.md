# 💰 ПЛАН СИСТЕМИ ОПЛАЧЕНИХ ЧАТІВ

## 🎯 ЗАГАЛЬНА ЛОГІКА

### **Умови для початку чату:**
1. **Взаємний лайк** (безкоштовно) - обидва користувачі лайкнули один одного
2. **Оплачений чат** (платно) - один користувач оплатив доступ до чату

### **Бізнес-процес:**
```
Користувач A лайкає користувача B
├── Користувач B також лайкнув A? 
│   ├── ТАК → ВЗАЄМНИЙ ЛАЙК → Чат доступний безкоштовно
│   └── НІ → Показати кнопку "Оплатити чат"
│       └── Після оплати → Чат доступний односторонньо
```

---

## 🗄️ АНАЛІЗ НАЯВНИХ ТАБЛИЦЬ

### **✅ ІСНУЮЧІ ТАБЛИЦІ В БД:**
```sql
-- Профілі користувачів ✅
profiles (user_id, first_name, last_name, role, phone, email, ...)

-- Старі таблиці (ВИДАЛИТИ) ❌
saved_parents (nanny_user_id, parent_user_id, created_at)
saved_nannies (parent_user_id, nanny_user_id, created_at)

-- Існуючі orders для платежів ✅
course_orders (id, user_id, status, created_at) -- використаємо як orders
```

### **🎯 НОВА АРХІТЕКТУРА (schema/11):**
```sql
-- Нові таблиці з готової схеми ✅
swipes (swipe_id, from_user_id, to_user_id, swipe_type, created_at)
pairs (pair_id, user_lo, user_hi, chat_state, paid_unlock_by)
payments (payment_id, payer_user_id, other_user_id, kind, status)
chat_threads (thread_id, pair_id, opened_by, open_reason)
chat_messages (message_id, thread_id, sender_user_id, body)
```

### **🔄 ЛОГІКА НА ОСНОВІ НОВИХ ТАБЛИЦЬ:**
1. **Лайк** → запис в `swipes` + оновлення `pairs`
2. **Взаємний лайк** → `pairs.chat_state = 'open'` + `chat_threads`
3. **Оплата чату** → запис в `payments` + `pairs.paid_unlock_by`
4. **Повідомлення** → запис в `chat_messages`

### **🔗 ПРОСТІ SQL ЗАПИТИ (НОВА АРХІТЕКТУРА):**

#### **Доступні няні (не лайкнуті):**
```sql
SELECT p.* FROM profiles p
WHERE p.role = 'nanny' 
AND p.user_id NOT IN (
  SELECT s.to_user_id FROM swipes s 
  WHERE s.from_user_id = :current_user_id AND s.swipe = 'like'
);
```

#### **Лайкнуті няні:**
```sql
SELECT p.*, 
  pr.chat_state,
  pr.pair_id,
  ct.thread_id as chat_id
FROM profiles p
JOIN swipes s ON p.user_id = s.to_user_id
LEFT JOIN pairs pr ON (
  (pr.user_lo = LEAST(:current_user_id, p.user_id) AND pr.user_hi = GREATEST(:current_user_id, p.user_id))
)
LEFT JOIN chat_threads ct ON ct.pair_id = pr.pair_id
WHERE s.from_user_id = :current_user_id AND s.swipe = 'like';
```

#### **Перевірка можливості чату:**
```sql
SELECT pr.chat_state, ct.thread_id as chat_id
FROM pairs pr
LEFT JOIN chat_threads ct ON ct.pair_id = pr.pair_id
WHERE pr.user_lo = LEAST(:current_user_id, :target_user_id)
  AND pr.user_hi = GREATEST(:current_user_id, :target_user_id);
```

### **🎯 ПЕРЕВАГИ НОВОЇ АРХІТЕКТУРИ:**
- ✅ **Готова схема** - schema/11_swipe_match_chat_tables.sql
- ✅ **Продумана архітектура** - pairs замість matches  
- ✅ **Всі тригери та індекси** - вже включені
- ✅ **Ефективні запити** - LEAST/GREATEST для пар
- ✅ **Розширюваність** - payments, chat_threads готові

---

## 📱 ПРОСТІ API ЕНДПОІНТИ (БЕЗ ДОМЕНІВ)

### **1. Лайк користувача** 
```http
POST /api/v1/like
Authorization: Bearer <token>
{
  "target_user_id": "uuid"
}

Response: {
  "success": true,
  "is_match": false, // true якщо взаємний лайк
  "chat_id": "uuid" // якщо створився чат
}

// Логіка:
// 1. Додати запис в swipes
// 2. Перевірити чи є зворотний лайк
// 3. Якщо так - додати в matches і створити чат
```

### **2. Оплата доступу до чату**
```http
POST /api/v1/pay-chat
Authorization: Bearer <token>
{
  "target_user_id": "uuid",
  "payment_data": {...}
}

Response: {
  "success": true,
  "chat_id": "uuid"
}

// Логіка:
// 1. Додати запис в orders
// 2. Створити чат з chat_type='paid'
```

### **3. Перевірка можливості чату**
```http
GET /api/v1/can-chat/{target_user_id}
Authorization: Bearer <token>

Response: {
  "can_chat": true,
  "chat_id": "uuid", // якщо чат існує
  "reason": "match" // або "paid"
}

// Логіка:
// 1. Перевірити чи є чат між користувачами
// 2. Якщо немає - перевірити можливість створення
```

### **4. Отримати мої чати**
```http
GET /api/v1/my-chats
Authorization: Bearer <token>

Response: {
  "chats": [
    {
      "chat_id": "uuid",
      "other_user": {...},
      "chat_type": "match", // або "paid"
      "last_message": "...",
      "unread_count": 3
    }
  ]
}
```

### **5. Список доступних нянь (не лайкнутих)**
```http
GET /api/v1/nannies/available
Authorization: Bearer <token>

Response: {
  "nannies": [
    {
      "user_id": "uuid",
      "first_name": "Марія",
      "last_name": "Петренко",
      "age": 25,
      "experience": "2 роки",
      "avatar_url": "...",
      "hourly_rate": 150
    }
  ]
}

// Логіка: SELECT * FROM profiles p 
// WHERE role='nanny' AND user_id NOT IN 
// (SELECT to_user_id FROM swipes WHERE from_user_id=current_user)
```

### **6. Список лайкнутих нянь**
```http
GET /api/v1/nannies/liked
Authorization: Bearer <token>

Response: {
  "nannies": [
    {
      "user_id": "uuid",
      "first_name": "Марія",
      "is_match": true, // взаємний лайк
      "can_chat": true,
      "chat_id": "uuid"
    }
  ]
}

// Логіка: SELECT p.*, s.created_at as liked_at FROM profiles p
// JOIN swipes s ON p.user_id = s.to_user_id 
// WHERE s.from_user_id = current_user AND s.swipe = 'like'
```

### **7. Список доступних батьків (не лайкнутих)**
```http
GET /api/v1/parents/available
Authorization: Bearer <token>

Response: {
  "parents": [
    {
      "user_id": "uuid",
      "first_name": "Олена",
      "children_count": 2,
      "location": "Київ"
    }
  ]
}
```

### **8. Список лайкнутих батьків**
```http
GET /api/v1/parents/liked
Authorization: Bearer <token>

Response: {
  "parents": [
    {
      "user_id": "uuid",
      "first_name": "Олена",
      "is_match": true,
      "can_chat": true,
      "chat_id": "uuid"
    }
  ]
}
```

---

## 🔄 ОНОВЛЕНІ ЕНДПОІНТИ ДЛЯ ПРОФІЛІВ

### **4. Доступні профілі (з інформацією про чати)**
```http
GET /api/v1/nannies/available
GET /api/v1/parents/available
Authorization: Bearer <token>

Response:
{
  "profiles": [
    {
      "user_id": "uuid",
      "first_name": "Марія",
      "last_name": "Петренко",
      "avatar_url": "https://...",
      "age": 25,
      "experience": "2 роки",
      "chat_status": {
        "can_chat": false,
        "reason": "no_permission",
        "is_mutual_match": false,
        "is_paid_chat": false,
        "i_liked": true,
        "they_liked": false
      }
    }
  ]
}
```

### **5. Збережені профілі (лайкнуті)**
```http
GET /api/v1/nannies/saved
GET /api/v1/parents/saved
Authorization: Bearer <token>

Response:
{
  "profiles": [
    {
      "user_id": "uuid",
      "first_name": "Марія",
      "last_name": "Петренко",
      "avatar_url": "https://...",
      "chat_status": {
        "can_chat": true,
        "reason": "mutual_match", // або "paid_chat"
        "is_mutual_match": true,
        "is_paid_chat": false,
        "payment_id": null
      }
    }
  ]
}
```

---

## 🎨 ЗМІНИ НА ФРОНТЕНДІ

### **Компонент CustomPaymentModal**
```typescript
// Оновити onPaymentSuccess callback
onPaymentSuccess={async () => {
  try {
    // 1. Відправити дані про оплату на бекенд
    const paymentResponse = await fastapi.request('POST', '/api/v1/chats/pay', {
      target_user_id: selectedUser.user_id,
      amount: 50,
      payment_data: {
        card_number: cardNumber,
        expiry: expiryDate,
        cvv: cvv
      }
    });

    if (paymentResponse.success) {
      toast({
        title: "Чат розблоковано! 🎉",
        description: "Тепер ви можете спілкуватися",
      });
      
      // 2. Перейти до чатів
      navigate('/messages');
    }
  } catch (error) {
    toast({
      title: "Помилка оплати",
      description: error.message,
      variant: "destructive"
    });
  }
}}
```

### **Компонент профілю (NannyProfile, ParentProfile)**
```typescript
// Перевірка дозволу на чат
const checkChatPermission = async (targetUserId: string) => {
  const response = await fastapi.request('GET', `/api/v1/chats/can-chat/${targetUserId}`);
  return response;
};

// Кнопки в профілі
const renderChatButton = (chatStatus) => {
  if (chatStatus.can_chat) {
    return (
      <Button onClick={() => navigate(`/chat/${targetUserId}`)}>
        💬 Написати
      </Button>
    );
  } else {
    return (
      <Button onClick={() => setShowPaymentModal(true)}>
        💰 Оплатити чат (50₴)
      </Button>
    );
  }
};
```

### **Сторінка Matches**
```typescript
// Оновити логіку отримання збережених профілів
const fetchSavedProfiles = async () => {
  const endpoint = userRole === 'parent' ? '/api/v1/nannies/saved' : '/api/v1/parents/saved';
  const response = await fastapi.request('GET', endpoint);
  
  // Профілі вже містять chat_status
  setSavedProfiles(response.profiles);
};
```

---

## 📋 ДЕТАЛЬНИЙ ПЛАН РЕАЛІЗАЦІЇ

### **🧹 ЕТАП 0: ОЧИЩЕННЯ СТАРОГО КОДУ** ⚠️

#### **📂 Бекенд очищення:**
- [ ] **0.1** Видалити ВСІ старі ендпоінти з `frontend_api_sql.py`:
  - `GET/POST/DELETE /api/v1/saved_nannies`
  - `GET/POST/DELETE /api/v1/saved_parents`
  - `GET /api/v1/search/nannies/complete`
  - `GET /api/v1/search/parents/complete`
  - `GET /api/v1/swipes/my-likes`
  - `POST /api/v1/swipes/create`
  - `DELETE /api/v1/swipes/{to_user_id}`
  - `GET /api/v1/matches`
  - `DELETE /api/v1/matches/{match_id}`
- [ ] **0.2** Видалити ВСІ домени з `main.py` та файлову систему:
  ```bash
  # Видалити з main.py імпорти:
  from .domains.swipes.router import router as swipes_domain_router
  from .domains.matches.router import router as matches_domain_router  
  from .domains.search.router import router as search_domain_router
  from .domains.chats.router import router as chats_domain_router
  
  # Видалити файли:
  rm -rf app/domains/swipes/
  rm -rf app/domains/matches/
  rm -rf app/domains/search/
  rm -rf app/domains/chats/
  ```

- [ ] **0.3** Видалити коментовані роутери з `main.py`
- [ ] **0.4** Очистити `app/models.py` від заглушок (Profile, SavedParent, SavedNanny, etc.)
- [ ] **0.5** Видалити застарілі роутери:
  ```bash
  rm -f app/routers/search_optimized.py
  rm -f app/routers/admin_chats.py  
  rm -f app/services/swipe_match_service.py
  ```

#### **🎨 Фронтенд план заміни ендпоінтів:**
- [ ] **0.6** Створити план заміни API викликів:

**Старі ендпоінти → Нові (спрощені):**
```javascript
// ВИДАЛЯЄМО (використаємо існуючі чат ендпоінти):
GET /api/v1/matches → використаємо існуючий чат ендпоінт
POST /api/v1/send-message → використаємо існуючий  
GET /api/v1/chat/{id}/messages → використаємо існуючий

// ЗАМІНЮЄМО НА НОВІ:
GET /api/v1/search/nannies/complete → GET /api/v1/nannies/available
GET /api/v1/swipes/my-likes → GET /api/v1/nannies/liked  
POST /api/v1/swipes/create → POST /api/v1/like
POST /api/v1/saved_nannies → POST /api/v1/like
DELETE /api/v1/saved_nannies → використаємо існуючий unlike
```

**Файли для оновлення (пізніше):**
- `SearchNannies.tsx` - замінити на `/nannies/available`
- `Matches.tsx` - замінити на `/my-chats`  
- `NannyProfile.tsx` - замінити на `/like` та `/unlike`

#### **🗑️ Конкретні файли для видалення/очищення:**

**Бекенд:**
```bash
# Видалити застарілі ендпоінти з frontend_api_sql.py:
- GET/POST/DELETE /api/v1/saved_nannies
- GET/POST/DELETE /api/v1/saved_parents  
- GET /api/v1/chats/pay (старий варіант)
- GET /api/v1/chats/my-paid (старий варіант)

# Видалити коментовані роутери з main.py
# Очистити app/models.py від заглушок
```

**Фронтенд (план на майбутнє):**
```bash
# Файли для оновлення API викликів (НЕ ЗАРАЗ):
nanny-match-ukraine/src/pages/SearchNannies.tsx
nanny-match-ukraine/src/pages/SearchParents.tsx
nanny-match-ukraine/src/pages/Matches.tsx
nanny-match-ukraine/src/pages/NannyProfile.tsx
nanny-match-ukraine/src/pages/ParentProfile.tsx

# Замінити API виклики згідно з планом вище
```

#### **🧪 Перевірка після очищення бекенду:**
- [ ] **0.7** Запустити бекенд та перевірити що немає помилок
- [ ] **0.7** Видалити зайві таблиці (після міграції даних):
  ```sql
  # ЗАЙВІ ТАБЛИЦІ ДЛЯ ВИДАЛЕННЯ:
  DROP TABLE IF EXISTS saved_parents;    -- замінено на pairs
  DROP TABLE IF EXISTS saved_nannies;    -- замінено на pairs  
  DROP TABLE IF EXISTS matches;          -- замінено на pairs (якщо є окрема таблиця)
  
  # МОЖЛИВО ЗАЙВІ (перевірити використання):
  DROP TABLE IF EXISTS bookings;         -- якщо не використовується
  DROP TABLE IF EXISTS certificates;     -- якщо не використовується
  ```

- [ ] **0.8** Перевірити що фронтенд все ще компілюється
- [ ] **0.9** Зафіксувати зміни в Git з коментарем "🧹 Cleanup backend old code"

### **🏗️ ЕТАП 1: АНАЛІЗ ТА ПІДГОТОВКА БД** ⭐

#### **🔍 АНАЛІЗ НАЯВНИХ ТАБЛИЦЬ:**
- [x] **1.1** Перевірити які таблиці існують на продакшені:
  ```bash
  # ТОЧНО Є (з логів та коду):
  ✅ profiles (user_id, phone, role, onboarding_completed)
  ✅ user_roles (user_id, role)
  ✅ onboarding_configs, onboarding_steps, onboarding_fields
  ✅ courses, course_orders, course_progress
  ✅ nannies, parents (основні профілі)
  ✅ nanny_services, nanny_education, nanny_languages, nanny_skills
  ✅ parent_children, parent_requirements
  ✅ saved_parents, saved_nannies (старі таблиці)
  ✅ bookings, reviews, certificates
  ✅ profile_photos, user_documents, user_videos
  
  # СХЕМА Є, АЛЕ НЕВІДОМО ЧИ ЗАСТОСОВАНА:
  ❓ swipes, pairs, payments (schema/11_swipe_match_chat_tables.sql)
  ❓ chat_threads, chat_messages, chat_last_reads
  ❓ otp_codes, otp_verifications, login_attempts
  ```

- [ ] **1.2** Перевірити структуру кожної таблиці:
  ```sql
  -- Для кожної таблиці виконати:
  SELECT column_name, data_type, is_nullable 
  FROM information_schema.columns 
  WHERE table_name = 'table_name';
  ```

- [x] **1.2** Аналіз структури існуючих таблиць:
  ```sql
  # PROFILES - готова для використання:
  - user_id VARCHAR (UUID) ✅
  - phone VARCHAR (унікальний) ✅  
  - role userrole ENUM ✅
  - onboarding_completed BOOLEAN ✅
  
  # COURSE_ORDERS - можна використати як ORDERS:
  - id VARCHAR (UUID) ✅
  - user_id VARCHAR ✅
  - status VARCHAR ✅
  - created_at TIMESTAMPTZ ✅
  ```

- [x] **1.3** Визначити що потрібно створити/змінити:
  ```bash
  # ПОТРІБНО ЗАСТОСУВАТИ (є схема):
  ✅ schema/11_swipe_match_chat_tables.sql - ІДЕАЛЬНА схема!
     - swipes (from_user_id, to_user_id, swipe_type)
     - pairs (user_lo, user_hi, chat_state, paid_unlock_by)  
     - payments (payer_user_id, other_user_id, kind, status)
     - chat_threads (pair_id, opened_by, open_reason)
     - chat_messages (thread_id, sender_user_id, body)
  
  # НЕ ПОТРІБНО СТВОРЮВАТИ:
  ❌ orders - використаємо course_orders
  ❌ chat_type колонка - є повна схема чатів
  ❌ matches таблиця - є pairs з chat_state
  ```

- [ ] **1.4** Застосувати schema/11_swipe_match_chat_tables.sql на продакшені

#### **✅ ВІДМІННІ НОВИНИ:**

**1. Ідеальна схема вже є:**
- `schema/11_swipe_match_chat_tables.sql` - повна схема для swipes, pairs, chats, payments
- Всі ENUM типи, індекси, тригери вже продумані
- Архітектура pairs замість matches - більш ефективна

**2. Існуючі таблиці підходять:**
- `profiles` має всі потрібні поля (user_id, role, phone)
- `course_orders` можна використати як `orders` для платежів
- Структура UUID та TIMESTAMPTZ вже налаштована

**3. Немає ORM залежностей:**
- Схема використовує чистий SQL
- Всі тригери та функції вже написані
- Індекси для продуктивності включені

#### **⚠️ ЗАЛИШИЛИСЯ ПРОБЛЕМИ:**

**1. Невідомо чи застосована схема:**
- Файл `11_swipe_match_chat_tables.sql` може не бути застосований
- Потрібно перевірити чи існують таблиці swipes, pairs, chat_threads

**2. Старі таблиці конфліктують:**
- `saved_parents`, `saved_nannies` - старий підхід
- Потрібно мігрувати дані або видалити

**3. ORM код в main.py:**
- Імпорт `models.py` якого немає
- Generic endpoint не працюватиме

#### **🛠️ ПЛАН ВИРІШЕННЯ (СПРОЩЕНИЙ):**
1. **Застосувати готову схему** - `schema/11_swipe_match_chat_tables.sql`
2. **Перевірити що створилося** - swipes, pairs, chat_threads, payments
3. **Видалити старі таблиці** - saved_parents, saved_nannies (після міграції даних)
4. **Використати course_orders як orders** - для платежів за чат

#### **🎯 РЕЗУЛЬТАТ:**
- ✅ Всі таблиці для нового функціоналу
- ✅ Ідеальна архітектура pairs + payments
- ✅ Готові тригери та індекси
- ✅ Без ORM залежностей

### **🔧 ЕТАП 2: ПРОСТІ API ЕНДПОІНТИ (6 штук)** ⭐
- [ ] **2.1** `POST /api/v1/like` - лайк користувача (з автоматичним матчем)
- [ ] **2.2** `POST /api/v1/pay-chat` - оплата доступу до чату  
- [ ] **2.3** `GET /api/v1/nannies/available` - доступні няні (не лайкнуті)
- [ ] **2.4** `GET /api/v1/nannies/liked` - лайкнуті няні
- [ ] **2.5** `GET /api/v1/parents/available` - доступні батьки (не лайкнуті)
- [ ] **2.6** `GET /api/v1/parents/liked` - лайкнуті батьки

**ВИДАЛЕНІ ЗАЙВІ:**
- ❌ `GET /api/v1/can-chat/{user_id}` - фронт сам перевірить
- ❌ `GET /api/v1/my-chats` - використаємо існуючий
- ❌ `POST /api/v1/send-message` - використаємо існуючий  
- ❌ `GET /api/v1/chat/{chat_id}/messages` - використаємо існуючий
- ❌ `DELETE /api/v1/unlike/{user_id}` - використаємо існуючий

### **🔧 ЕТАП 2.5: АДМІН ЕНДПОІНТИ (7 штук)** 🛡️
- [ ] **2.7** `GET /api/v1/admin/chats` - список чатів для адміна
- [ ] **2.8** `GET /api/v1/admin/matches` - список матчів для адміна  
- [ ] **2.9** `GET /api/v1/admin/chats/stats` - статистика чатів та матчів
- [ ] **2.10** `GET /api/v1/admin/chats/{thread_id}/messages` - повідомлення чату
- [ ] **2.11** `PUT /api/v1/admin/chats/{thread_id}/lock` - заблокувати чат
- [ ] **2.12** `PUT /api/v1/admin/chats/{thread_id}/unlock` - розблокувати чат
- [ ] **2.13** `DELETE /api/v1/admin/messages/{message_id}` - видалити повідомлення

**ЛОГІКА АДМІН ЕНДПОІНТІВ:**
```sql
-- Список чатів з інформацією про користувачів
SELECT ct.thread_id, p.user_lo, p.user_hi, p.chat_state, p.paid_unlock_by,
       pr1.first_name as user1_name, pr2.first_name as user2_name,
       COUNT(cm.message_id) as message_count
FROM chat_threads ct
JOIN pairs p ON ct.pair_id = p.pair_id  
JOIN profiles pr1 ON p.user_lo = pr1.user_id
JOIN profiles pr2 ON p.user_hi = pr2.user_id
LEFT JOIN chat_messages cm ON ct.thread_id = cm.thread_id
GROUP BY ct.thread_id, p.user_lo, p.user_hi, p.chat_state, p.paid_unlock_by, pr1.first_name, pr2.first_name
ORDER BY ct.created_at DESC;

-- Статистика
SELECT 
  COUNT(DISTINCT p.pair_id) as total_pairs,
  COUNT(DISTINCT CASE WHEN p.chat_state = 'open' THEN p.pair_id END) as active_chats,
  COUNT(DISTINCT CASE WHEN p.paid_unlock_by IS NOT NULL THEN p.pair_id END) as paid_chats,
  COUNT(DISTINCT cm.message_id) as total_messages
FROM pairs p
LEFT JOIN chat_threads ct ON p.pair_id = ct.pair_id
LEFT JOIN chat_messages cm ON ct.thread_id = cm.thread_id;
```

### **🧪 ЕТАП 3: ТЕСТУВАННЯ БЕКЕНДУ**
- [ ] **3.1** Тестувати створення таблиці `paid_chats`
- [ ] **3.2** Тестувати `POST /api/v1/chats/pay` з різними сценаріями
- [ ] **3.3** Тестувати `GET /api/v1/chats/can-chat/{target_user_id}`
- [ ] **3.4** Тестувати оновлені ендпоінти профілів
- [ ] **3.5** Тестувати інтеграцію з існуючими чатами

### **🎨 ЕТАП 4: ФРОНТЕНД ЗМІНИ**
- [ ] **4.1** Оновити `CustomPaymentModal` для виклику `POST /api/v1/chats/pay`
- [ ] **4.2** Оновити компоненти профілів (`NannyProfile`, `ParentProfile`)
- [ ] **4.3** Додати логіку перевірки `can-chat` перед показом кнопок
- [ ] **4.4** Оновити `SearchNannies` та `SearchParents` для chat_status
- [ ] **4.5** Оновити `Matches` для роботи з новою логікою
- [ ] **4.6** Додати обробку помилок оплати

### **🔗 ЕТАП 5: ІНТЕГРАЦІЙНЕ ТЕСТУВАННЯ**
- [ ] **5.1** Тестувати повний флоу: лайк → оплата → чат
- [ ] **5.2** Тестувати взаємні лайки без оплати
- [ ] **5.3** Тестувати відображення статусів чату
- [ ] **5.4** Тестувати обмеження доступу до чатів
- [ ] **5.5** Тестувати на різних ролях (parent/nanny)

### **🚀 ЕТАП 6: ДЕПЛОЙ ТА МОНІТОРИНГ**
- [ ] **6.1** Деплой бекенд змін на продакшн
- [ ] **6.2** Деплой фронтенд змін
- [ ] **6.3** Моніторинг помилок та продуктивності
- [ ] **6.4** Збір фідбеку від користувачів

---

## 🔍 ТЕСТОВІ СЦЕНАРІЇ

### **Сценарій 1: Взаємний лайк**
1. Користувач A лайкає користувача B
2. Користувач B лайкає користувача A
3. Створюється match
4. Обидва можуть писати безкоштовно

### **Сценарій 2: Односторонній лайк + оплата**
1. Користувач A лайкає користувача B
2. Користувач B НЕ лайкає користувача A
3. Користувач A бачить кнопку "Оплатити чат"
4. Користувач A оплачує
5. Користувач A може писати користувачу B

### **Сценарій 3: Без лайку та оплати**
1. Користувач A НЕ лайкав користувача B
2. Користувач A не може писати
3. Кнопка чату недоступна

---

## 📊 СТРУКТУРА ДАНИХ

### **Таблиця paid_chats**
```sql
id              | UUID    | PRIMARY KEY
payer_id        | UUID    | REFERENCES profiles(user_id)
target_user_id  | UUID    | REFERENCES profiles(user_id)
amount          | INTEGER | DEFAULT 50
paid_at         | TIMESTAMP WITH TIME ZONE
payment_data    | JSONB   | Дані про оплату
created_at      | TIMESTAMP WITH TIME ZONE
```

### **Індекси**
```sql
CREATE INDEX idx_paid_chats_payer ON paid_chats(payer_id);
CREATE INDEX idx_paid_chats_target ON paid_chats(target_user_id);
CREATE UNIQUE INDEX idx_paid_chats_unique ON paid_chats(payer_id, target_user_id);
```

---

## 📱 ДЕТАЛЬНИЙ ПЛАН ЗМІН ДЛЯ ФРОНТЕНДУ

### **🔄 Файли що потребують змін:**

#### **1. CustomPaymentModal.tsx**
```typescript
// Замінити onPaymentSuccess callback
onPaymentSuccess={async () => {
  try {
    // Викликати API оплати
    const response = await fastapi.request('POST', '/api/v1/chats/pay', {
      target_user_id: selectedUser.user_id,
      amount: 50,
      payment_data: { card_number, expiry, cvv }
    });
    
    if (response.success) {
      toast({ title: "Чат розблоковано! 🎉" });
      navigate('/messages');
    }
  } catch (error) {
    toast({ title: "Помилка оплати", variant: "destructive" });
  }
}}
```

#### **2. SearchNannies.tsx / SearchParents.tsx**
```typescript
// Додати перевірку дозволів на чат
const checkChatPermission = async (targetUserId: string) => {
  const response = await fastapi.request('GET', `/api/v1/chats/can-chat/${targetUserId}`);
  return response;
};

// Оновити кнопки профілю
const renderChatButton = (profile) => {
  const [chatStatus, setChatStatus] = useState(null);
  
  useEffect(() => {
    checkChatPermission(profile.user_id).then(setChatStatus);
  }, [profile.user_id]);
  
  if (chatStatus?.can_chat) {
    return <Button onClick={() => navigate(`/chat/${profile.user_id}`)}>💬 Написати</Button>;
  } else {
    return <Button onClick={() => setShowPaymentModal(true)}>💰 Оплатити чат (50₴)</Button>;
  }
};
```

#### **3. Matches.tsx**
```typescript
// Оновити логіку отримання збережених профілів
const fetchSavedProfiles = async () => {
  // Отримати лайкнуті профілі з chat_status
  const response = await fastapi.request('GET', '/api/v1/swipes/my-likes?include_chat_status=true');
  setSavedProfiles(response.profiles);
};

// Показувати статус чату для кожного профілю
const renderProfileCard = (profile) => (
  <div className="profile-card">
    <h3>{profile.first_name}</h3>
    {profile.chat_status?.can_chat ? (
      <Button onClick={() => navigate(`/chat/${profile.user_id}`)}>
        💬 Написати
      </Button>
    ) : (
      <Button onClick={() => openPaymentModal(profile)}>
        💰 Оплатити чат
      </Button>
    )}
  </div>
);
```

#### **4. NannyProfile.tsx / ParentProfile.tsx**
```typescript
// Додати стан для статусу чату
const [chatStatus, setChatStatus] = useState(null);

// Перевірити дозвіл на чат при завантаженні
useEffect(() => {
  if (nannyData?.user_id) {
    fastapi.request('GET', `/api/v1/chats/can-chat/${nannyData.user_id}`)
      .then(setChatStatus);
  }
}, [nannyData?.user_id]);

// Рендерити кнопки залежно від статусу
const renderActionButtons = () => {
  if (chatStatus?.can_chat) {
    return (
      <Button onClick={() => navigate(`/chat/${nannyData.user_id}`)}>
        💬 Написати
      </Button>
    );
  } else {
    return (
      <Button onClick={() => setShowPaymentModal(true)}>
        💰 Оплатити чат (50₴)
      </Button>
    );
  }
};
```

### **🔧 Нові хуки та утиліти:**

#### **useChatPermissions.ts**
```typescript
export const useChatPermissions = (targetUserId: string) => {
  const [chatStatus, setChatStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const checkPermissions = useCallback(async () => {
    if (!targetUserId) return;
    
    setLoading(true);
    try {
      const response = await fastapi.request('GET', `/api/v1/chats/can-chat/${targetUserId}`);
      setChatStatus(response);
    } catch (error) {
      console.error('Error checking chat permissions:', error);
    } finally {
      setLoading(false);
    }
  }, [targetUserId]);
  
  useEffect(() => {
    checkPermissions();
  }, [checkPermissions]);
  
  return { chatStatus, loading, refetch: checkPermissions };
};
```

#### **paymentService.ts**
```typescript
export const paymentService = {
  async payForChat(targetUserId: string, paymentData: any) {
    return await fastapi.request('POST', '/api/v1/chats/pay', {
      target_user_id: targetUserId,
      amount: 50,
      payment_data: paymentData
    });
  },
  
  async getMyPaidChats() {
    return await fastapi.request('GET', '/api/v1/chats/my-paid');
  }
};
```

---

## ✅ ГОТОВО ДО РЕАЛІЗАЦІЇ

Цей план покриває:
- ✅ **Повний аналіз наявної системи** - що є і що відсутнє
- ✅ **Детальну логіку оплачених чатів** - бізнес-процеси
- ✅ **Структуру бази даних** - нова таблиця paid_chats
- ✅ **API ендпоінти** - повний список з прикладами
- ✅ **Зміни на фронтенді** - конкретні файли та код
- ✅ **Покроковий план реалізації** - 6 етапів з деталями
- ✅ **План тестування** - всі сценарії використання

---

## ⚠️ ВИЯВЛЕНІ ПРОБЛЕМИ ТА НЕДОПРОДУМУВАННЯ

### **🔴 КРИТИЧНІ ПРОБЛЕМИ:**

#### **1. Дублювання чатів**
**Проблема:** Користувач може оплатити чат, а потім отримати взаємний лайк
```
Сценарій:
1. Батько лайкає няню → няня не лайкає
2. Батько оплачує чат → створюється чат з chat_type='paid'  
3. Няня потім лайкає батька → створюється match і новий чат?
```
**Рішення:** Перевіряти існуючі чати перед створенням нових

#### **2. Відсутність обмежень доступу**
**Проблема:** Хто може писати в оплаченому чаті?
- Тільки той хто оплатив?
- Обидва користувачі?
- Як це контролювати?

#### **3. Невизначеність з повідомленнями**
**Проблема:** Якщо чат оплачений односторонньо:
- Чи може цільовий користувач відповідати?
- Чи бачить він що чат оплачений?
- Як це відображається в UI?

### **🟡 АРХІТЕКТУРНІ НЕДОЛІКИ:**

#### **4. Складність перевірки дозволів**
**Проблема:** Для кожного профілю треба робити 3 запити:
1. Перевірити взаємний лайк в `swipes`
2. Перевірити існуючий чат в `chats`
3. Перевірити оплату в `orders`

#### **5. Неоптимальна структура orders**
**Проблема:** 
- `target_id` може бути NULL для деяких типів замовлень
- Немає валідації що `target_id` відповідає `order_type`
- Складно робити аналітику

### **🟢 ЗАПРОПОНОВАНІ ВИПРАВЛЕННЯ:**

#### **Виправлення 1: Унікальність чатів**
```sql
-- Додати унікальний індекс для чатів
ALTER TABLE chats ADD CONSTRAINT unique_chat_participants 
UNIQUE (LEAST(participant1_id, participant2_id), GREATEST(participant1_id, participant2_id));
```

#### **Виправлення 2: Права доступу до чату**
```sql
-- Додати поле для прав доступу
ALTER TABLE chats ADD COLUMN access_type VARCHAR(20) DEFAULT 'mutual';
-- Можливі значення: 'mutual' (обидва), 'payer_only' (тільки платник)
```

#### **Виправлення 3: Спрощена перевірка дозволів**
```sql
-- Створити VIEW для швидкої перевірки
CREATE VIEW user_chat_permissions AS
SELECT 
    c.id as chat_id,
    c.participant1_id,
    c.participant2_id,
    c.chat_type,
    c.access_type,
    o.user_id as payer_id
FROM chats c
LEFT JOIN orders o ON o.order_type = 'chat_access' 
    AND o.target_id IN (c.participant1_id, c.participant2_id)
    AND o.status = 'completed';
```

### **📋 ОНОВЛЕНИЙ ПЛАН ДІЙ:**

1. **Спочатку вирішити архітектурні питання**
2. **Визначити точні правила доступу до чатів**
3. **Створити оптимізовану схему БД**
4. **Тільки потім починати реалізацію**

---

## ✅ ГОТОВО ДО РЕАЛІЗАЦІЇ (ПІСЛЯ ВИПРАВЛЕНЬ)

**🚀 Наступний крок:** Обговорити та вирішити виявлені проблеми перед початком реалізації
