# 🚀 **ПОВНА ІНСТРУКЦІЯ ДЛЯ ФРОНТЕНДУ - API ЕНДПОІНТИ**

## 📋 **СТОРІНКА ПОШУКУ НЯНЬ (/search-nannies)**

### **1. 👩‍🍼 Завантаження рекомендованих нянь (не лайкнутих)**
```javascript
GET /api/v1/search/nannies/complete?limit=20
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "data": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "first_name": "Марія",
      "last_name": "Іванова",
      "phone": "+380501234567",
      "email": "maria@example.com",
      "location": "Київ",
      "onboarding_completed": true,
      "age": 25,
      "hourly_rate": 150.0,
      "experience_years": 3,
      "about_me": "Досвідчена няня з педагогічною освітою...",
      "education_level": "Вища",
      "languages_spoken": ["українська", "англійська"],
      "certifications": ["Перша допомога", "Педагогіка"],
      "services_offered": ["babysitting", "tutoring", "cooking"],
      "avatar_url": "https://storage.url/photo.jpg", // ⭐ ФОТО!
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-15T14:30:00Z"
    }
  ],
  "total": 150,
  "has_more": true
}
```

### **2. 💖 Лайк няні (переміщення в збережені)**
```javascript
POST /api/v1/simple/swipes
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "target_user_id": "550e8400-e29b-41d4-a716-446655440001"
}

// ✅ ВІДПОВІДЬ:
{
  "success": true,
  "swipe": {
    "swipe_id": "123e4567-e89b-12d3-a456-426614174000",
    "from_user_id": "current-user-id",
    "to_user_id": "550e8400-e29b-41d4-a716-446655440001",
    "swipe": "like",
    "created_at": "2025-01-20T15:30:00Z"
  },
  "is_match": false  // true якщо взаємний лайк
}
```

### **3. 📊 Завантаження збережених нянь та матчів**
```javascript
GET /api/v1/simple/my-likes?limit=100
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "likes": [
    {
      "swipe_id": "123e4567-e89b-12d3-a456-426614174000",
      "target_user_id": "550e8400-e29b-41d4-a716-446655440001",
      "swiped_at": "2025-01-20T15:30:00Z",
      "first_name": "Марія",
      "last_name": "Іванова",
      "role": "nanny",
      "is_mutual": true  // ⭐ true = матч, false = тільки мій лайк
    },
    {
      "swipe_id": "123e4567-e89b-12d3-a456-426614174002",
      "target_user_id": "550e8400-e29b-41d4-a716-446655440002",
      "swiped_at": "2025-01-19T10:15:00Z",
      "first_name": "Олена",
      "last_name": "Петренко",
      "role": "nanny",
      "is_mutual": false  // тільки мій лайк
    }
  ],
  "total": 5,
  "has_more": false
}
```

### **4. 🗑️ Відміна лайку (повернення в рекомендовані)**
```javascript
DELETE /api/v1/simple/swipes/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "success": true,
  "message": "Swipe deleted successfully",
  "deleted_swipe": {
    "swipe_id": "123e4567-e89b-12d3-a456-426614174000",
    "from_user_id": "current-user-id",
    "to_user_id": "550e8400-e29b-41d4-a716-446655440001",
    "swipe": "like",
    "created_at": "2025-01-20T15:30:00Z"
  }
}
```

---

## 👨‍👩‍👧‍👦 **СТОРІНКА ПОШУКУ БАТЬКІВ (/search-parents)**

### **1. 👪 Завантаження рекомендованих батьків (не лайкнутих)**
```javascript
GET /api/v1/search/parents/complete?limit=20
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "data": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440010",
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "first_name": "Олена",
      "last_name": "Петренко",
      "phone": "+380509876543",
      "email": "olena@example.com",
      "location": "Київ",
      "onboarding_completed": true,
      "about_me": "Шукаю няню для двох дітей...",
      "children_count": 2,
      "children_ages": "3, 7 років",
      "budget_min": 100.0,
      "budget_max": 200.0,
      "preferred_languages": ["українська", "англійська"],
      "special_requirements": "Знання англійської мови",
      "avatar_url": "https://storage.url/parent-photo.jpg", // ⭐ ФОТО!
      "created_at": "2025-01-05T09:00:00Z",
      "updated_at": "2025-01-18T11:20:00Z"
    }
  ],
  "total": 80,
  "has_more": true
}
```

### **2-4. Лайк, збережені, відміна лайку**
*Використовують ті ж ендпоінти що і для нянь*

---

## 📊 **ЛІЧИЛЬНИКИ ДЛЯ ТАБІВ**
```javascript
GET /api/v1/counters/dashboard/complete
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "counters": {
    "available_nannies": 150,     // для батьків
    "available_parents": 80,      // для нянь  
    "saved_profiles": 5,          // загальна кількість лайків
    "matches": 2,                 // кількість взаємних матчів
    "messages": 1                 // непрочитані повідомлення
  },
  "user_id": "current-user-id",
  "role": "parent"
}
```

---

## 🎯 **ЛОГІКА ВИКОРИСТАННЯ У ФРОНТЕНДІ**

### **📱 Компонент пошуку нянь:**

```javascript
class NannySearchPage {
  constructor() {
    this.state = {
      recommendedNannies: [],     // Таб "Рекомендовані"
      savedNannies: [],          // Таб "Збережені" 
      matches: [],               // Таб "Матчі"
      counters: {},
      loading: false
    };
  }

  async componentDidMount() {
    await this.loadAllData();
  }

  async loadAllData() {
    this.setState({ loading: true });
    
    try {
      // Паралельно завантажуємо всі дані
      const [recommended, saved, counters] = await Promise.all([
        this.loadRecommendedNannies(),
        this.loadSavedNannies(), 
        this.loadCounters()
      ]);

      this.setState({
        recommendedNannies: recommended.data,
        savedNannies: saved.nannies,
        matches: saved.matches,
        counters: counters.counters,
        loading: false
      });
    } catch (error) {
      console.error('Error loading data:', error);
      this.setState({ loading: false });
    }
  }

  // 1. Завантаження рекомендованих нянь
  async loadRecommendedNannies() {
    return await fastapi.request('GET', '/api/v1/search/nannies/complete?limit=20');
  }

  // 2. Завантаження збережених нянь та матчів
  async loadSavedNannies() {
    const response = await fastapi.request('GET', '/api/v1/simple/my-likes?limit=100');
    
    // Фільтруємо тільки нянь
    const nannies = response.likes.filter(like => like.role === 'nanny');
    
    return {
      nannies: nannies.filter(like => !like.is_mutual),  // Тільки збережені
      matches: nannies.filter(like => like.is_mutual)    // Тільки матчі
    };
  }

  // 3. Завантаження лічильників
  async loadCounters() {
    return await fastapi.request('GET', '/api/v1/counters/dashboard/complete');
  }

  // 4. Лайк няні
  async likeNanny(nannyId) {
    try {
      const response = await fastapi.request('POST', '/api/v1/simple/swipes', {
        target_user_id: nannyId
      });

      // Показуємо модал матчу якщо потрібно
      if (response.is_match) {
        this.showMatchModal(nannyId);
      }

      // Переміщуємо няню з рекомендованих в збережені
      this.setState(prev => ({
        recommendedNannies: prev.recommendedNannies.filter(n => n.user_id !== nannyId),
        counters: {
          ...prev.counters,
          available_nannies: prev.counters.available_nannies - 1,
          saved_profiles: prev.counters.saved_profiles + 1,
          matches: response.is_match ? prev.counters.matches + 1 : prev.counters.matches
        }
      }));

      // Перезавантажуємо збережених
      const saved = await this.loadSavedNannies();
      this.setState(prev => ({
        ...prev,
        savedNannies: saved.nannies,
        matches: saved.matches
      }));

    } catch (error) {
      console.error('Error liking nanny:', error);
    }
  }

  // 5. Відміна лайку
  async unlikeNanny(swipeId, nannyId) {
    try {
      await fastapi.request('DELETE', `/api/v1/simple/swipes/${swipeId}`);

      // Перезавантажуємо рекомендованих (няня повернеться)
      const recommended = await this.loadRecommendedNannies();
      const saved = await this.loadSavedNannies();
      const counters = await this.loadCounters();

      this.setState({
        recommendedNannies: recommended.data,
        savedNannies: saved.nannies,
        matches: saved.matches,
        counters: counters.counters
      });

    } catch (error) {
      console.error('Error unliking nanny:', error);
    }
  }

  // 6. Рендер табів
  renderTabs() {
    const { recommendedNannies, savedNannies, matches, counters } = this.state;

    return (
      <div className="tabs">
        <Tab 
          title={`Рекомендовані (${counters.available_nannies || 0})`}
          content={recommendedNannies}
          onLike={this.likeNanny}
        />
        <Tab 
          title={`Збережені (${counters.saved_profiles || 0})`}
          content={savedNannies}
          onUnlike={this.unlikeNanny}
        />
        <Tab 
          title={`Матчі (${counters.matches || 0})`}
          content={matches}
          onUnlike={this.unlikeNanny}
        />
      </div>
    );
  }
}
```

### **🔄 Логіка для сторінки батьків:**
*Аналогічна, тільки замінити `nannies` на `parents` та відповідні ендпоінти*

---

## ✅ **ПІДСУМОК ЕНДПОІНТІВ**

| Призначення | Ендпоінт | Відповідь |
|-------------|----------|-----------|
| 📋 Рекомендовані няні | `GET /api/v1/search/nannies/complete` | `{data: [...], total, has_more}` |
| 👪 Рекомендовані батьки | `GET /api/v1/search/parents/complete` | `{data: [...], total, has_more}` |
| 💖 Лайк | `POST /api/v1/simple/swipes` | `{success, swipe, is_match}` |
| 📊 Збережені + матчі | `GET /api/v1/simple/my-likes` | `{likes: [...], total, has_more}` |
| 🗑️ Відміна лайку | `DELETE /api/v1/simple/swipes/{id}` | `{success, deleted_swipe}` |
| 🔢 Лічильники | `GET /api/v1/counters/dashboard/complete` | `{counters: {...}}` |

---

## 🎯 **КЛЮЧОВІ ОСОБЛИВОСТІ**

### **✅ ЩО ПРАЦЮЄ:**
- **Фото профілів** - повертається `avatar_url` в пошукових ендпоінтах
- **Автоматичне виключення** - пошук за замовчуванням показує тільки не лайкнутих
- **Один ендпоінт для лайків і матчів** - `/simple/my-likes` з полем `is_mutual`
- **Відміна лайків** - профіль повертається в рекомендовані

### **❌ ЩО НЕ ВИКОРИСТОВУВАТИ:**
- ❌ `POST /api/v1/saved_nannies` - застарілий
- ❌ `POST /api/v1/saved_parents` - застарілий  
- ❌ `GET /api/v1/simple/matches` - видалений (використовуйте my-likes)
- ❌ Параметр `swipe_type: "pass"` - не потрібен

### **🔄 ЛОГІКА ТАБІВ:**
1. **Рекомендовані** - `search/nannies/complete` (exclude_saved=true за замовчуванням)
2. **Збережені** - `my-likes` фільтровані по `is_mutual: false`
3. **Матчі** - `my-likes` фільтровані по `is_mutual: true`

**Всі ендпоінти готові до використання! 🚀**
