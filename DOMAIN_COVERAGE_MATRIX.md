# 📊 Матриця покриття старих роутерів новими доменами

## 🔐 AUTH Роутер

### ✅ Покрито новим AUTH доменом:
- `POST /send-otp` ✅
- `POST /verify-otp` ✅  
- `POST /login` ✅
- `POST /register` ✅
- `GET /me` ✅
- `POST /logout` ✅

### ❌ НЕ покрито (потрібно додати):
- `POST /admin-login` ❌
- `POST /refresh` ❌
- `POST /update-password` ❌

## 👶 ONBOARDING Роутер

### ✅ Покрито новим ONBOARDING доменом:
- Всі основні ендпоінти покрито ✅
- Legacy сумісність забезпечена ✅

## 💬 CHATS Роутер

### ✅ Покрито новим CHATS доменом:
- Основна функціональність покрита ✅
- Потрібно перевірити повне покриття ❓

## 🔍 SEARCH Роутер (search_optimized)

### ✅ Покрито новим SEARCH доменом:
- Пошук нянь ✅
- Пошук батьків ✅
- Лічильники ✅

## 📊 ADMIN Роутер

### ✅ Покрито новим ADMIN доменом:
- Dashboard ✅
- Користувачі ✅
- Статистика ✅
- Дії з користувачами ✅

## 🚫 НЕ ПОКРИТО (окремі системи):

### 📁 FILES - залишається
- Завантаження файлів
- Управління зображеннями

### 💳 PAYMENTS - залишається  
- Платіжна система
- Обробка платежів

### 📚 COURSES - залишається
- Система курсів
- Управління навчанням

### 📅 BOOKINGS - залишається
- Система бронювання
- Календар

### ⭐ REVIEWS - залишається
- Система відгуків
- Рейтинги

### 📋 REFERENCE_DATA - залишається
- Довідкові дані
- Категорії та значення

### 🏷️ USER_TAGS - залишається
- Система тегів користувачів

### 👤 PROFILES - залишається
- Управління профілями

## 🎯 ПЛАН ДІЙ:

### 1. Доповнити AUTH домен:
- Додати `POST /admin-login`
- Додати `POST /refresh` 
- Додати `POST /update-password`

### 2. Перевірити повне покриття CHATS

### 3. Після доповнення - видалити старі роутери:
- ❌ `auth.router` 
- ❌ `onboarding.router`
- ❌ `chats_router` 
- ❌ `search_optimized_router`
- ❌ `admin.router`

### 4. Залишити системні роутери:
- ✅ `files_router`
- ✅ `payments_router` 
- ✅ `courses_router`
- ✅ `bookings_router`
- ✅ `reviews_router`
- ✅ `reference_data_router`
- ✅ `user_tags_router`
- ✅ `profiles_router`
