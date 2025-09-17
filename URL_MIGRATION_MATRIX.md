# 🔄 Матриця переходів URL-ів: Старі → Нові домени

## 📋 Загальна інформація
- **Дата створення**: 2025-09-17
- **Статус**: В процесі міграції
- **Мета**: Перехід від монолітних роутерів до доменної архітектури

---

## 🔐 AUTH домен (✅ ГОТОВО)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `POST /api/v1/auth/send-otp` | `POST /api/v1/auth/send-otp` | ✅ Готово | Новий домен |
| `POST /api/v1/auth/verify-otp` | `POST /api/v1/auth/verify-otp` | ✅ Готово | Новий домен |
| `POST /api/v1/auth/register` | `POST /api/v1/auth/register` | ✅ Готово | Новий домен |
| `POST /api/v1/auth/login` | `POST /api/v1/auth/login` | ✅ Готово | Новий домен |
| `GET /api/v1/auth/me` | `GET /api/v1/auth/me` | ✅ Готово | Новий домен |

---

## 🔄 SWIPES домен (✅ ГОТОВО)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `POST /api/v1/swipes` | `POST /api/v1/swipes/create` | ✅ Готово | Новий домен |
| `GET /api/v1/swipes/my-likes` | `GET /api/v1/swipes/my-likes` | ✅ Готово | Новий домен |
| `GET /api/v1/swipes/received-likes` | `GET /api/v1/swipes/received-likes` | ✅ Готово | Новий домен |
| `GET /api/v1/swipes/status/{user_id}` | `GET /api/v1/swipes/status/{user_id}` | ✅ Готово | Новий домен |

---

## 🤝 MATCHES домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/matches` | `GET /api/v1/matches/list` | 📋 Планується | Список матчів |
| `GET /api/v1/matches/{match_id}` | `GET /api/v1/matches/details/{match_id}` | 📋 Планується | Деталі матчу |
| `POST /api/v1/matches/{match_id}/chat` | `POST /api/v1/matches/start-chat/{match_id}` | 📋 Планується | Початок чату |

---

## 🔍 SEARCH домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/search/nannies` | `GET /api/v1/search/nannies` | 📋 Планується | Простий пошук нянь |
| `GET /api/v1/search/nannies/complete` | `GET /api/v1/search/nannies/complete` | 📋 Планується | Повний пошук нянь |
| `GET /api/v1/search/parents` | `GET /api/v1/search/parents` | 📋 Планується | Пошук батьків |
| `GET /api/v1/search/dashboard` | `GET /api/v1/search/dashboard` | 📋 Планується | Дашборд статистики |

---

## 👶 ONBOARDING домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/onboarding/configs` | `GET /api/v1/onboarding/configs` | 📋 Планується | Конфігурації онбордингу |
| `POST /api/v1/onboarding/save-simple` | `POST /api/v1/onboarding/save-simple` | 📋 Планується | Збереження даних |
| `GET /api/v1/user_onboarding_data` | `GET /api/v1/onboarding/user-data` | 📋 Планується | Дані користувача |
| `POST /api/v1/onboarding/complete` | `POST /api/v1/onboarding/complete` | 📋 Планується | Завершення онбордингу |

---

## 💬 CHATS домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/chats` | `GET /api/v1/chats/list` | 📋 Планується | Список чатів |
| `GET /api/v1/chats/{chat_id}/messages` | `GET /api/v1/chats/messages/{chat_id}` | 📋 Планується | Повідомлення чату |
| `POST /api/v1/chats/{chat_id}/messages` | `POST /api/v1/chats/send-message/{chat_id}` | 📋 Планується | Відправка повідомлення |
| `PUT /api/v1/chats/{chat_id}/read` | `PUT /api/v1/chats/mark-read/{chat_id}` | 📋 Планується | Позначити як прочитане |

---

## 💳 PAYMENTS домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `POST /api/v1/payments/create` | `POST /api/v1/payments/create` | 📋 Планується | Створення платежу |
| `GET /api/v1/payments/{payment_id}` | `GET /api/v1/payments/details/{payment_id}` | 📋 Планується | Деталі платежу |
| `PUT /api/v1/payments/{payment_id}/status` | `PUT /api/v1/payments/update-status/{payment_id}` | 📋 Планується | Оновлення статусу |

---

## 👤 PROFILES домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/profiles` | `GET /api/v1/profiles/list` | 📋 Планується | Список профілів |
| `PUT /api/v1/profiles/` | `PUT /api/v1/profiles/update` | 📋 Планується | Оновлення профілю |
| `PATCH /api/v1/profiles/` | `PATCH /api/v1/profiles/update` | 📋 Планується | Часткове оновлення |

---

## 🏷️ TAGS домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/users/profile` | `GET /api/v1/tags/user-profile` | 📋 Планується | Профіль з тегами |
| `POST /api/v1/users/tags/add` | `POST /api/v1/tags/add` | 📋 Планується | Додавання тегу |
| `DELETE /api/v1/users/tags/{tag_code}` | `DELETE /api/v1/tags/remove/{tag_code}` | 📋 Планується | Видалення тегу |

---

## 🗄️ REFERENCE домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/reference-values` | `GET /api/v1/reference/values` | 📋 Планується | Довідкові значення |
| `GET /api/v1/reference/categories` | `GET /api/v1/reference/categories` | 📋 Планується | Категорії довідника |
| `GET /api/v1/reference/values/{category}` | `GET /api/v1/reference/values/{category}` | 📋 Планується | Значення по категорії |

---

## 👑 ADMIN домен (📋 ПЛАНУЄТЬСЯ)

| Старий URL | Новий URL | Статус | Примітки |
|------------|-----------|--------|----------|
| `GET /api/v1/admin/onboarding-configs` | `GET /api/v1/admin/onboarding/configs` | 📋 Планується | Адмін конфігурації |
| `POST /api/v1/admin/onboarding-configs` | `POST /api/v1/admin/onboarding/configs` | 📋 Планується | Створення конфігурації |
| `GET /api/v1/admin/chats` | `GET /api/v1/admin/chats/list` | 📋 Планується | Адмін чати |
| `GET /api/v1/admin/payments` | `GET /api/v1/admin/payments/list` | 📋 Планується | Адмін платежі |

---

## 📱 Інструкції для фронтенду

### 🔄 Поетапна міграція
1. **Фаза 1**: AUTH домен (✅ готово)
2. **Фаза 2**: SWIPES домен (🚧 в процесі)
3. **Фаза 3**: MATCHES + SEARCH домени
4. **Фаза 4**: ONBOARDING + CHATS домени
5. **Фаза 5**: ADMIN + інші домени

### 🛠️ Як оновлювати URL-и:

#### Frontend (nanny-match-ukraine):
```typescript
// Старий спосіб
await fastapi.request('POST', '/api/v1/swipes', data);

// Новий спосіб
await fastapi.request('POST', '/api/v1/swipes/create', data);
```

#### Admin Frontend (nanny-match-ukraine-adminfront):
```typescript
// Старий спосіб
await fastapi.request('GET', '/api/v1/admin/chats');

// Новий спосіб
await fastapi.request('GET', '/api/v1/admin/chats/list');
```

---

## ⚠️ Важливі примітки

1. **Зворотна сумісність**: Старі URL-и будуть працювати до завершення міграції
2. **Тестування**: Кожен новий домен тестується перед переходом
3. **Документація**: Оновлюється після кожної фази
4. **Логування**: Всі зміни логуються для відстеження

---

## 📊 Прогрес міграції

- ✅ **AUTH домен**: 100% (5/5 ендпоінтів)
- ✅ **SWIPES домен**: 100% (4/4 ендпоінтів)
- 📋 **MATCHES домен**: 0% (0/3 ендпоінтів)
- 📋 **SEARCH домен**: 0% (0/4 ендпоінтів)
- 📋 **Інші домени**: 0% (0/20+ ендпоінтів)

**Загальний прогрес**: 21% (9/42 ендпоінтів)
