# 📋 СИСТЕМА ТЕГІВ КОРИСТУВАЧІВ - ДОКУМЕНТАЦІЯ ДЛЯ ФРОНТЕНДУ

## 🎯 ЗАГАЛЬНИЙ ОПИС

Система тегів дозволяє відстежувати стан користувачів (завершені туторіали, верифікація профілю, преміум статус тощо) через сервер замість localStorage. Це забезпечує персистентність даних між пристроями та сесіями.

## 🗄️ СТРУКТУРА ДАНИХ

- Теги зберігаються в полі `tags` профілю користувача як масив рядків
- Кожен тег має код (наприклад: `tutorial_nanny_search_completed`)
- Теги валідуються через довідник `user_tags`
- При логіні в відповіді `auth/login` тепер є поле `tags`

## 🔌 API ЕНДПОІНТИ

### 1️⃣ ОТРИМАННЯ ДОСТУПНИХ ТЕГІВ
```http
GET /api/v1/users/tags/available
```
**Повертає:** список всіх доступних тегів з описами

**Відповідь:**
```json
{
  "tags": [
    {
      "code": "tutorial_nanny_search_completed",
      "label": "Туторіал пошуку нянь завершено",
      "description": "Користувач завершив туторіал по пошуку нянь",
      "sort_order": 1
    }
  ],
  "success": true
}
```

### 2️⃣ ОТРИМАННЯ ТЕГІВ КОРИСТУВАЧА
```http
GET /api/v1/users/tags
Authorization: Bearer {token}
```
**Повертає:** масив тегів поточного користувача

**Відповідь:**
```json
{
  "tags": ["tutorial_nanny_search_completed", "profile_verified"],
  "success": true
}
```

### 3️⃣ ДОДАВАННЯ ТЕГУ
```http
POST /api/v1/users/tags/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "tag_code": "tutorial_nanny_search_completed"
}
```
**Повертає:** оновлений список тегів користувача

**Відповідь:**
```json
{
  "success": true,
  "message": "Тег успішно додано",
  "tags": ["tutorial_nanny_search_completed", "profile_verified"]
}
```

### 4️⃣ ВИДАЛЕННЯ ТЕГУ
```http
DELETE /api/v1/users/tags/{tag_code}
Authorization: Bearer {token}
```
**Повертає:** оновлений список тегів користувача

**Відповідь:**
```json
{
  "success": true,
  "message": "Тег успішно видалено",
  "tags": ["profile_verified"]
}
```

### 5️⃣ ПРОФІЛЬ З ТЕГАМИ
При логіні в відповіді `auth/login` тепер є поле `tags`:
```json
{
  "user_id": "...",
  "email": "...",
  "tags": ["tutorial_nanny_search_completed", "profile_verified"]
}
```

## 🏷️ ДОСТУПНІ ТЕГИ

### 📚 ТУТОРІАЛИ
- `tutorial_nanny_search_completed` - Туторіал пошуку нянь завершено
- `tutorial_parent_search_completed` - Туторіал пошуку батьків завершено  
- `tutorial_onboarding_completed` - Онбордінг завершено
- `tutorial_profile_setup_completed` - Налаштування профілю завершено

### 👑 АДМІН ФУНКЦІЇ
- `admin_panel_access` - Доступ до адмін панелі
- `admin_user_management` - Управління користувачами

### ⚙️ СИСТЕМНІ
- `profile_verified` - Профіль верифіковано
- `premium_user` - Преміум користувач

## 📝 ПРИКЛАДИ ВИКОРИСТАННЯ

### 🔍 1. ОТРИМАННЯ ДОСТУПНИХ ТЕГІВ
```javascript
const response = await fetch('/api/v1/users/tags/available');
const data = await response.json();
// data.tags = [{ code: 'tutorial_nanny_search_completed', label: 'Туторіал пошуку нянь завершено', ... }]
```

### 👤 2. ПЕРЕВІРКА ТЕГІВ КОРИСТУВАЧА
```javascript
const response = await fetch('/api/v1/users/tags', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
// data.tags = ['tutorial_nanny_search_completed', 'profile_verified']
```

### ➕ 3. ДОДАВАННЯ ТЕГУ (наприклад, після завершення туторіалу)
```javascript
const response = await fetch('/api/v1/users/tags/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ tag_code: 'tutorial_nanny_search_completed' })
});
const data = await response.json();
// data.tags = оновлений масив тегів
```

### 🗑️ 4. ВИДАЛЕННЯ ТЕГУ
```javascript
const response = await fetch('/api/v1/users/tags/tutorial_nanny_search_completed', {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
// data.tags = оновлений масив тегів без видаленого тегу
```

## 🔧 ІНТЕГРАЦІЯ З AuthContext

### 📝 ОНОВЛЕННЯ User ІНТЕРФЕЙСУ
```typescript
interface User {
  id: string;
  email?: string;
  phone?: string;
  role?: string;
  tags: string[];  // ← НОВЕ ПОЛЕ
  // ... інші поля
}
```

### 🔄 МЕТОДИ ДЛЯ AuthContext
```typescript
const AuthContext = createContext({
  user: null,
  // ... існуючі методи
  addTag: async (tagCode: string) => {
    const response = await fastapi.request('POST', '/api/v1/users/tags/add', {
      tag_code: tagCode
    });
    setUser(prev => ({ ...prev, tags: response.tags }));
  },
  removeTag: async (tagCode: string) => {
    const response = await fastapi.request('DELETE', `/api/v1/users/tags/${tagCode}`);
    setUser(prev => ({ ...prev, tags: response.tags }));
  },
  hasTag: (tagCode: string) => user?.tags?.includes(tagCode) || false
});
```

## 🎯 ПРАКТИЧНІ ПРИКЛАДИ

### 1️⃣ ЗАМІНА localStorage В ТУТОРІАЛАХ

#### ❌ СТАРИЙ СПОСІБ (localStorage):
```javascript
// Перевірка
const tutorialCompleted = localStorage.getItem('tutorial_nanny_search') === 'completed';

// Збереження
localStorage.setItem('tutorial_nanny_search', 'completed');
```

#### ✅ НОВИЙ СПОСІБ (теги):
```javascript
// Перевірка
const { user, hasTag } = useAuth();
const tutorialCompleted = hasTag('tutorial_nanny_search_completed');

// Збереження
const { addTag } = useAuth();
await addTag('tutorial_nanny_search_completed');
```

### 2️⃣ ХУК ДЛЯ ТУТОРІАЛІВ
```typescript
const useTutorial = (tutorialType: string) => {
  const { user, hasTag, addTag } = useAuth();
  const tagCode = `tutorial_${tutorialType}_completed`;

  return {
    isCompleted: hasTag(tagCode),
    markCompleted: () => addTag(tagCode)
  };
};

// Використання:
const { isCompleted, markCompleted } = useTutorial('nanny_search');
if (!isCompleted) {
  showTutorial();
}
```

### 3️⃣ УМОВНИЙ РЕНДЕРИНГ
```jsx
const { hasTag } = useAuth();

return (
  <div>
    {!hasTag('tutorial_nanny_search_completed') && (
      <TutorialOverlay onComplete={() => addTag('tutorial_nanny_search_completed')} />
    )}
    
    {hasTag('premium_user') && (
      <PremiumFeatures />
    )}
    
    {hasTag('profile_verified') && (
      <VerifiedBadge />
    )}
  </div>
);
```

## 💡 ПЕРЕВАГИ НОВОЇ СИСТЕМИ

1. **Персистентність** - дані зберігаються на сервері, доступні з будь-якого пристрою
2. **Централізованість** - всі теги в одному місці, легко управляти
3. **Валідація** - теги валідуються через довідник
4. **Розширюваність** - легко додавати нові типи тегів
5. **Аналітика** - можна відстежувати статистику по тегах в адмін панелі

## 🚨 ВАЖЛИВІ МОМЕНТИ

1. **Авторизація** - всі операції з тегами потребують авторизації
2. **Валідація** - можна додавати тільки теги з довідника `user_tags`
3. **Дублікати** - система автоматично запобігає дублюванню тегів
4. **Помилки** - обробляйте помилки API (неіснуючі теги, проблеми з авторизацією)

## 🔄 МІГРАЦІЯ З localStorage

Для міграції існуючих даних з localStorage на теги:

```javascript
const migrateFromLocalStorage = async () => {
  const { addTag } = useAuth();
  
  // Перевіряємо старі ключі localStorage
  const migrations = [
    { key: 'tutorial_nanny_search', tag: 'tutorial_nanny_search_completed' },
    { key: 'tutorial_parent_search', tag: 'tutorial_parent_search_completed' },
    { key: 'onboarding_completed', tag: 'tutorial_onboarding_completed' }
  ];
  
  for (const { key, tag } of migrations) {
    if (localStorage.getItem(key) === 'completed') {
      await addTag(tag);
      localStorage.removeItem(key); // Очищаємо старі дані
    }
  }
};
```
