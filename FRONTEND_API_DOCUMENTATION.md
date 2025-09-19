# 🌐 **ПОВНА ДОКУМЕНТАЦІЯ API ДЛЯ ФРОНТЕНД РОЗРОБНИКА**

## 📋 **ЗМІСТ**
1. [Авторизація](#авторизація)
2. [Профілі користувачів](#профілі-користувачів)
3. [Онбординг](#онбординг)
4. [Пошук і каталог](#пошук-і-каталог)
5. [Лайки і Свайпи](#лайки-і-свайпи)
6. [Матчі](#матчі)
7. [Лічильники](#лічильники)
8. [Відгуки](#відгуки)
9. [Повідомлення](#повідомлення)
10. [Довідкові дані](#довідкові-дані)
11. [Проблемні ендпоінти](#проблемні-ендпоінти)

---

## 🔐 **АВТОРИЗАЦІЯ**

### Заголовки для всіх запитів:
```javascript
headers: {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${access_token}`
}
```

### Реєстрація/Логін:
```javascript
// Реєстрація
POST /api/v1/auth/register
{
  "phone": "+380999999999",
  "password": "password123",
  "role": "parent" | "nanny"
}

// Логін
POST /api/v1/auth/login
{
  "phone": "+380999999999", 
  "password": "password123"
}

// Відповідь:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "phone": "+380999999999",
    "roles": ["parent"]
  }
}
```

---

## 👤 **ПРОФІЛІ КОРИСТУВАЧІВ**

### Отримання профілю:
```javascript
GET /api/v1/profiles?user_id={user_id}
// Відповідь: масив профілів
[{
  "id": "uuid",
  "user_id": "uuid", 
  "first_name": "Ім'я",
  "last_name": "Прізвище",
  "email": "email@example.com",
  "phone": "+380999999999",
  "role": "parent" | "nanny",
  "onboarding_completed": true,
  "created_at": "2025-01-01T00:00:00Z"
}]
```

### Оновлення профілю:
```javascript
// Новий формат (використовується в онбордингу)
PATCH /api/v1/profiles
{
  "values": {
    "onboarding_completed": true,
    "first_name": "Нове ім'я"
  },
  "filters": {
    "user_id": "uuid"
  }
}

// Старий формат (також підтримується)
PATCH /api/v1/profiles  
{
  "onboarding_completed": true,
  "first_name": "Нове ім'я"
}
```

---

## 🎯 **ОНБОРДИНГ**

### Конфігурація онбордингу:
```javascript
GET /api/v1/onboarding_configs?role={role}
// Відповідь: конфігурація кроків онбордингу
```

### Кроки онбордингу:
```javascript
GET /api/v1/onboarding_steps?config_id={id}
// Відповідь: список кроків
```

### Поля кроків:
```javascript
GET /api/v1/onboarding_fields?step_id={id}
// Відповідь: поля для заповнення
```

### Збереження даних кроку:
```javascript
POST /api/v1/user-onboarding-data
{
  "field_key": "first_name",
  "value": "Значення", // автоматично визначається тип
  "step_key": "personal_info"
}
```

### Отримання збережених даних:
```javascript
GET /api/v1/user_onboarding_data?user_id={user_id}
// Відповідь: масив збережених даних користувача
```

### Завершення онбордингу:
```javascript
POST /api/v1/onboarding/complete
{
  "final_step": 4,
  "role": "parent"
}
```

---

## 🔍 **ПОШУК І КАТАЛОГ**

### Пошук батьків (для нянь):
```javascript
GET /api/v1/search/parents?user_id={user_id}&exclude_saved=true&limit=20
// Відповідь: масив профілів батьків
```

### Список нянь:
```javascript
GET /api/v1/nannies?user_id={user_id}&limit=20
// Відповідь: 
{
  "data": [/* масив профілів нянь */],
  "total": 50
}
```

---

## 💖 **ЛАЙКИ І СВАЙПИ**

### ⚠️ **ВАЖЛИВО: АРХІТЕКТУРА ЗМІНИЛАСЯ!**

**Старі ендпоінти (НЕ ВИКОРИСТОВУВАТИ):**
- ❌ `POST /api/v1/saved_nannies` 
- ❌ `DELETE /api/v1/saved_nannies`
- ❌ `POST /api/v1/saved_parents`

**Нові ендпоінти (ВИКОРИСТОВУВАТИ):**

### Створення лайку:
```javascript
POST /api/v1/swipes/create
{
  "to_user_id": "uuid_няні_або_батька",
  "swipe": "like" | "pass"
}
```

### Отримання моїх лайків:
```javascript
GET /api/v1/swipes/my-likes?limit=100
// Відповідь:
{
  "likes": [{
    "id": "uuid",
    "from_user_id": "uuid",
    "to_user_id": "uuid", 
    "swipe": "like",
    "created_at": "2025-01-01T00:00:00Z"
  }],
  "total": 5
}
```

---

## 🤝 **МАТЧІ**

### Отримання матчів:
```javascript
GET /api/v1/matches
// Відповідь: взаємні лайки (коли обидва лайкнули)
{
  "matches": [/* масив матчів */],
  "total": 3
}
```

### Видалення матчу:
```javascript
DELETE /api/v1/matches/{match_id}
```

---

## 📊 **ЛІЧИЛЬНИКИ**

### Лічильники для дашборду:
```javascript
GET /api/v1/counters/dashboard/complete?user_id={user_id}&role={role}&exclude_saved=true
// Відповідь:
{
  "counters": {
    "available_nannies": 23,    // або available_parents для нянь
    "saved_profiles": 5,        // кількість лайків
    "matches": 2                // кількість взаємних матчів
  },
  "user_id": "uuid",
  "role": "parent"
}
```

---

## ⭐ **ВІДГУКИ**

### Отримання відгуків няні:
```javascript
GET /api/v1/reviews?nanny_user_id={nanny_id}
// Відповідь:
{
  "data": [{
    "id": "uuid",
    "rating": 4.5,
    "comment": "Текст відгуку",
    "punctuality_rating": 5.0,
    "reliability_rating": 4.0,
    "communication_rating": 5.0,
    "professionalism_rating": 4.0,
    "created_at": "2025-01-01T00:00:00Z",
    "reviewer_name": "Ім'я Прізвище"
  }],
  "total": 10
}
```

### Створення відгуку:
```javascript
POST /api/v1/reviews
{
  "nanny_user_id": "uuid",
  "rating": 4.5,
  "comment": "Відмінна няня!",
  "punctuality": 5,
  "reliability": 4, 
  "communication": 5,
  "professionalism": 4,
  "review_type": "public" | "admin_only"
}
```

### Агреговані рейтинги няні:
```javascript
GET /api/v1/nannies/{nanny_user_id}/rating
// Відповідь:
{
  "overall": 4.2,
  "total_reviews": 15,
  "punctuality": 4.5,
  "reliability": 4.0,
  "communication": 4.3,
  "professionalism": 4.1
}
```

---

## 💬 **ПОВІДОМЛЕННЯ**

### Отримання чатів:
```javascript
GET /api/v1/conversations/{user_id}
// Alias для /api/v1/chats/
```

### Деталі чату:
```javascript
GET /api/v1/chats/{thread_id}/details
```

---

## 📚 **ДОВІДКОВІ ДАНІ**

### Категорії:
```javascript
GET /api/v1/reference/categories
// Відповідь: масив категорій
```

### Значення категорії:
```javascript
GET /api/v1/reference/values/{category}?is_active=true
// Відповідь: масив значень для категорії
```

### Для адмін панелі:
```javascript
GET /api/v1/data-categories
GET /api/v1/reference-values
```

---

## ⚠️ **ПРОБЛЕМНІ ЕНДПОІНТИ**

### Ендпоінти що НЕ ПРАЦЮЮТЬ або ЗАСТАРІЛІ:

#### 1. Swipes Domain (проблема з авторизацією):
- ❌ `POST /api/v1/swipes/create` - повертає 403
- ❌ `GET /api/v1/swipes/my-likes` - повертає 403

#### 2. Matches Domain (проблема з авторизацією):
- ❌ `GET /api/v1/matches` - повертає 403
- ❌ `DELETE /api/v1/matches/{id}` - повертає 403

#### 3. Застарілі ендпоінти у фронтенді:
```javascript
// ❌ НЕ ВИКОРИСТОВУВАТИ:
POST /api/v1/saved/toggle          // SearchNannies.tsx:203
POST /api/v1/swipes               // SearchNannies.tsx:327 (неправильний URL)
DELETE /api/v1/saved_parents      // SearchParents.tsx:255,394
POST /api/v1/saved_parents        // SearchParents.tsx:274
GET /api/v1/parents               // Matches.tsx:323,343
```

---

## 🔧 **РЕКОМЕНДАЦІЇ ДЛЯ ФРОНТЕНД РОЗРОБНИКА**

### 1. **Негайно виправити:**
```javascript
// Замінити всі saved_nannies/saved_parents на:
POST /api/v1/swipes/create {to_user_id, swipe: "like"}

// Замінити всі отримання збережених на:
GET /api/v1/swipes/my-likes
```

### 2. **Проблема з авторизацією:**
- Swipes і Matches домени використовують іншу авторизацію
- Потрібно виправити авторизацію в цих доменах
- Або перенести функціонал в frontend_api_sql.py

### 3. **Структура відповідей:**
- Завжди перевіряйте `response.error` 
- Дані можуть бути в `response.data` або прямо в `response`
- Масиви часто в полі `data` з `total`

### 4. **Токени:**
- Токени протермінуються через 30 хвилин
- Потрібно додати автоматичний refresh
- Зберігайте refresh_token для оновлення

---

## 🎯 **ПРІОРИТЕТИ ВИПРАВЛЕНЬ**

### Високий пріоритет:
1. ✅ Виправити авторизацію в swipes/matches доменах
2. ✅ Замінити всі saved_* на swipes у фронтенді  
3. ✅ Додати автоматичний refresh токенів

### Середній пріоритет:
1. Додати unlike функціонал (DELETE swipe)
2. Виправити неправильні URL у фронтенді
3. Уніфікувати структури відповідей

### Низький пріоритет:
1. Видалити застарілі ендпоінти
2. Додати валідацію на фронтенді
3. Покращити обробку помилок

---

**📅 Дата створення:** 19 вересня 2025  
**🔄 Версія API:** v1  
**🌐 Base URL:** https://nany.datavertex.me
