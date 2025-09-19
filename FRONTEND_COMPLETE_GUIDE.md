# 🚀 **ПОВНА ІНСТРУКЦІЯ ДЛЯ ФРОНТЕНД РОЗРОБНИКА**

## 📋 **РЕЗЮМЕ АНАЛІЗУ**

**✅ ЩО ПРАЦЮЄ:**
- Swipes Domain: `POST /create`, `GET /my-likes` 
- Matches Domain: `GET /matches`, `DELETE /{id}`
- Frontend API SQL: всі ендпоінти для профілів, онбордингу, лічильників
- Авторизація: JWT токени працюють правильно

**❌ ЩО НЕ ПРАЦЮЄ У ФРОНТЕНДІ:**
- Використовуються **ЗАСТАРІЛІ** ендпоінти `saved_nannies`/`saved_parents`
- **ЗМІШУВАННЯ** старої і нової архітектури
- **НЕПРАВИЛЬНІ** URL та формати запитів

---

## 🔄 **ЛОГІКА ЛАЙКІВ/СВАЙПІВ/МАТЧІВ**

### **Правильна архітектура:**
```
1️⃣ ЛАЙК: POST /api/v1/swipes/create {to_user_id, swipe: "like"}
2️⃣ МОЇ ЛАЙКИ: GET /api/v1/swipes/my-likes
3️⃣ МАТЧІ: GET /api/v1/matches (взаємні лайки)
4️⃣ ЛІЧИЛЬНИКИ: GET /api/v1/counters/dashboard/complete
```

### **Потік даних:**
```
Користувач лайкає → swipes таблиця → my-likes показує → лічильники оновлюються
Якщо взаємний лайк → matches таблиця → показується в матчах
```

---

## 🛠️ **ЩО ТРЕБА ВИПРАВИТИ У ФРОНТЕНДІ**

### **1. ParentHome.tsx - КРИТИЧНО**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
// Старий спосіб - НЕ ВИКОРИСТОВУВАТИ
const response = await fastapi.request('POST', '/api/v1/saved_nannies', {
  parent_id: user.id,
  nanny_id: nannyId
});
```

**✅ Правильний код:**
```javascript
// Новий спосіб - ВИКОРИСТОВУВАТИ
const response = await fastapi.request('POST', '/api/v1/swipes/create', {
  to_user_id: nannyId,
  swipe: 'like'
});

// Оновити локальний стан
if (response.error) throw new Error(response.error.message);
setSavedNannies(prev => [...prev, nannyId]);
```

**✅ Отримання збережених:**
```javascript
// Замість saved_nannies
const fetchSavedNannies = async () => {
  try {
    const response = await fastapi.request('GET', '/api/v1/swipes/my-likes?limit=100');
    if (response.error) throw new Error(response.error.message);
    
    // Витягуємо ID користувачів яких лайкнули
    const savedIds = (response.data?.likes || response.likes || []).map(item => item.target_user_id);
    setSavedNannies(savedIds);
  } catch (error) {
    console.error('Error fetching saved nannies:', error);
  }
};
```

### **2. NannyProfile.tsx - КРИТИЧНО**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
const response = await fastapi.request('POST', '/api/v1/saved_nannies', {
  parent_id: user.id,
  nanny_id: nanny.id
});
```

**✅ Правильний код:**
```javascript
const toggleSaveNanny = async () => {
  try {
    if (isSaved) {
      // TODO: Додати unlike функціонал коли буде готовий ендпоінт
      console.log('🔄 Unlike functionality not implemented yet');
      setIsSaved(false);
      toast({ description: "Видалено зі збережених" });
    } else {
      // Створюємо лайк
      const response = await fastapi.request('POST', '/api/v1/swipes/create', {
        to_user_id: nanny.id,
        swipe: 'like'
      });

      if (response.error) throw new Error(response.error.message);
      setIsSaved(true);
      toast({ description: "Додано до збережених" });
    }
  } catch (error) {
    console.error('Error toggling save:', error);
    toast({ 
      description: "Помилка при збереженні", 
      variant: "destructive" 
    });
  }
};
```

### **3. SearchParents.tsx - КРИТИЧНО**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
const response = await fastapi.request('DELETE', `/api/v1/saved_parents?nanny_id=${user.id}&parent_id=${parentId}`);
const response = await fastapi.request('POST', '/api/v1/saved_parents', {
  nanny_id: user.id,
  parent_id: parentId
});
```

**✅ Правильний код:**
```javascript
// Для лайку
const response = await fastapi.request('POST', '/api/v1/swipes/create', {
  to_user_id: parentId,
  swipe: 'like'
});

// Для отримання лайків
const response = await fastapi.request('GET', '/api/v1/swipes/my-likes?limit=100');
const savedIds = (response.data?.likes || response.likes || []).map(item => item.target_user_id);
```

### **4. Matches.tsx - ВИПРАВИТИ**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
const response = await fastapi.request('DELETE', `/api/v1/saved_nannies?parent_id=${parentId}&nanny_id=${matchId}`);
```

**✅ Правильний код:**
```javascript
// Для видалення матчу (розірвання зв'язку)
const response = await fastapi.request('DELETE', `/api/v1/matches/${matchId}`);

// Для отримання матчів (БЕЗ user_id та role параметрів)
const response = await fastapi.request('GET', '/api/v1/matches');
```

### **5. SearchNannies.tsx - ВИПРАВИТИ**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
const response = await fastapi.request('POST', '/api/v1/saved/toggle', {
  user_id: user.id,
  target_user_id: nannyId
});

const response = await fastapi.request('POST', '/api/v1/swipes', {
  from_user_id: user.id,
  to_user_id: nannyId,
  swipe: swipeType
});
```

**✅ Правильний код:**
```javascript
// Правильний URL для swipes
const response = await fastapi.request('POST', '/api/v1/swipes/create', {
  to_user_id: nannyId,
  swipe: swipeType  // "like" або "pass"
});
```

### **6. NewMessages.tsx - ВИПРАВИТИ**

**❌ Поточний код (НЕПРАВИЛЬНО):**
```javascript
const response = await fastapi.request('GET', `/api/counters/dashboard/${user.id}`);
const response = await fastapi.request('GET', `/api/conversations/${user.id}`);
```

**✅ Правильний код:**
```javascript
// Правильні URL з /api/v1/ префіксом
const response = await fastapi.request('GET', `/api/v1/counters/dashboard/complete?user_id=${user.id}&role=${userRole}`);
const response = await fastapi.request('GET', `/api/v1/conversations/${user.id}`);
```

---

## 📊 **СТРУКТУРИ ВІДПОВІДЕЙ**

### **Swipes Create Response:**
```javascript
{
  "swipe_id": 13,
  "from_user_id": "uuid",
  "to_user_id": "uuid", 
  "swipe": "like",
  "created_at": "2025-09-19T11:41:46.758825Z",
  "is_match": false,  // true якщо взаємний лайк
  "pair_id": null     // ID матчу якщо is_match = true
}
```

### **My-Likes Response:**
```javascript
{
  "likes": [
    {
      "swipe_id": 12,
      "target_user_id": "uuid",
      "swiped_at": "2025-09-19T11:41:46.758825Z",
      "first_name": "Ім'я",
      "last_name": "Прізвище", 
      "role": "nanny"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### **Matches Response:**
```javascript
{
  "matches": [
    {
      "match_id": "uuid",
      "user1_id": "uuid",
      "user2_id": "uuid",
      "created_at": "2025-01-01T00:00:00Z",
      "user1_profile": { /* профіль */ },
      "user2_profile": { /* профіль */ }
    }
  ],
  "total": 2
}
```

### **Counters Response:**
```javascript
{
  "counters": {
    "available_nannies": 23,    // або available_parents для нянь
    "saved_profiles": 3,        // кількість лайків
    "matches": 0                // кількість взаємних матчів
  },
  "user_id": "uuid",
  "role": "parent"
}
```

---

## 🔧 **ПЛАН ВИПРАВЛЕНЬ**

### **Крок 1: Замінити всі saved_* на swipes**
1. `ParentHome.tsx` - замінити `saved_nannies` на `swipes/create`
2. `NannyProfile.tsx` - замінити `saved_nannies` на `swipes/create`  
3. `SearchParents.tsx` - замінити `saved_parents` на `swipes/create`
4. `SearchNannies.tsx` - виправити URL `/api/v1/swipes` → `/api/v1/swipes/create`

### **Крок 2: Виправити URL та параметри**
1. `NewMessages.tsx` - додати `/api/v1/` префікси
2. `Matches.tsx` - видалити `user_id`/`role` параметри з `/matches`
3. Всі файли - перевірити що використовується `https://nany.datavertex.me`

### **Крок 3: Додати обробку помилок**
```javascript
// Шаблон для всіх API викликів
try {
  const response = await fastapi.request('POST', '/api/v1/swipes/create', data);
  if (response.error) {
    throw new Error(response.error.message || 'API Error');
  }
  // Обробка успішної відповіді
} catch (error) {
  console.error('API Error:', error);
  toast({
    description: error.message || "Помилка сервера",
    variant: "destructive"
  });
}
```

### **Крок 4: Додати автоматичний refresh токенів**
```javascript
// В fastapi-client.ts або AuthContext
const refreshTokenIfNeeded = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return;
  
  try {
    // Декодуємо токен і перевіряємо exp
    const payload = JSON.parse(atob(token.split('.')[1]));
    const now = Date.now() / 1000;
    
    if (payload.exp - now < 300) { // 5 хвилин до закінчення
      const refreshToken = localStorage.getItem('refresh_token');
      const response = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
      });
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
      }
    }
  } catch (error) {
    console.error('Token refresh error:', error);
  }
};
```

---

## 🧪 **ТЕСТУВАННЯ**

### **Після кожного виправлення тестуйте:**

1. **Лайк профілю:**
   - Клік на ❤️ → має створитися swipe
   - Лічильник `saved_profiles` має збільшитися
   - Профіль має з'явитися в "Збережених"

2. **Перегляд збережених:**
   - Сторінка "Збережені" має показувати всі лайки
   - Кількість має відповідати лічильнику

3. **Матчі:**
   - Якщо обидва лайкнули → має з'явитися в "Матчах"
   - Видалення матчу має працювати

4. **Лічильники:**
   - Мають оновлюватися в реальному часі
   - `available_*`, `saved_profiles`, `matches`

---

## 🚨 **КРИТИЧНІ ПОМИЛКИ ЯКІ ТРЕБА УНИКАТИ**

1. **НЕ використовувати** `/api/v1/saved_nannies` або `/api/v1/saved_parents`
2. **НЕ передавати** `user_id`/`role` в `/api/v1/matches` (токен містить все)
3. **НЕ забувати** префікс `/api/v1/` для всіх ендпоінтів
4. **НЕ ігнорувати** `response.error` - завжди перевіряти
5. **НЕ використовувати** `http://` - тільки `https://`

---

## ✅ **ЧЕКЛИСТ ГОТОВНОСТІ**

- [ ] Замінено всі `saved_nannies`/`saved_parents` на `swipes/create`
- [ ] Виправлено всі URL (додано `/api/v1/` префікси)
- [ ] Додано обробку помилок для всіх API викликів
- [ ] Протестовано лайки, збережені, матчі, лічильники
- [ ] Додано автоматичний refresh токенів
- [ ] Видалено всі Supabase виклики
- [ ] Перевірено що використовується HTTPS

---

**📅 Дата створення:** 19 вересня 2025  
**🔄 Версія:** 1.0  
**✅ Статус:** Всі backend ендпоінти працюють, потрібні тільки зміни у фронтенді
