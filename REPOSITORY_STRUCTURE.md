# 🏗️ Структура репозиторіїв проекту Nanny Match

## 📦 Чотири незалежні Git репозиторії:

### 1. **Головний репозиторій** (`nany/`)
- **Призначення**: Загальні конфігурації та координація
- **Вміст**:
  - `restart-all.sh` - основний скрипт запуску всієї системи
  - `start-dev.sh` - скрипт для розробки
  - `Makefile` - команди для управління проектом
  - Документація проекту (README.md, QUICK_START.md, etc.)
  - `app/` - спільний код (роутери, сервіси)
  - `archive/` - застарілі файли для історії

### 2. **Backend репозиторій** (`nanny-match-backend/`)
- **Призначення**: FastAPI додаток та API
- **Технології**: Python, FastAPI, PostgreSQL, Redis
- **Вміст**:
  - `app/` - основний код додатку
  - `alembic/` - міграції бази даних
  - `tests/` - тести
  - `scripts/` - утиліти та seed data
  - `docker-compose.yml` - конфігурація Docker
  - Власна документація та конфігурації

### 3. **Користувацький Frontend репозиторій** (`nanny-match-ukraine/`)
- **Призначення**: React додаток для користувачів (батьки та няні)
- **Технології**: React, Vite, TypeScript, Tailwind CSS
- **Порт**: 8080
- **Вміст**:
  - `src/` - вихідний код React додатку
  - `public/` - статичні файли
  - `vite.config.ts` - конфігурація Vite
  - Власна документація та конфігурації

### 4. **Адмін Frontend репозиторій** (`nanny-match-ukraine-adminfront/`)
- **Призначення**: React додаток для адміністрування системи
- **Технології**: React, Vite, TypeScript, Tailwind CSS
- **Порт**: 8081
- **Вміст**:
  - `src/` - вихідний код React додатку адмінки
  - `components/` - UI компоненти
  - `public/` - статичні файли
  - `vite.config.ts` - конфігурація Vite
  - Власна документація та конфігурації

## ⚠️ ВАЖЛИВО: Правила комітів

**ОБОВ'ЯЗКОВО** робити коміти окремо для кожного репозиторію:

```bash
# Для змін в головному репозиторії
cd /Users/anton/Desktop/nany
git add .
git commit -m "..."
git push

# Для змін в backend
cd /Users/anton/Desktop/nany/nanny-match-backend
git add .
git commit -m "..."
git push

# Для змін в користувацькому frontend
cd /Users/anton/Desktop/nany/nanny-match-ukraine
git add .
git commit -m "..."
git push

# Для змін в адмін frontend
cd /Users/anton/Desktop/nany/nanny-match-ukraine-adminfront
git add .
git commit -m "..."
git push
```

**НІКОЛИ** не комітити зміни з кореневого каталогу для backend/frontend файлів!

## 🚀 Запуск системи

Використовуйте головний скрипт:
```bash
./restart-all.sh
```

Він автоматично:
1. Зупинить всі попередні процеси
2. Запитає про тип backend (локальний/хмарний)
3. Запустить backend (якщо локальний)
4. Запустить користувацький frontend на порту 8080
5. Запустить адмін frontend на порту 8081

### Результат запуску:
- **Backend**: http://localhost:8000 (локальний) або https://nany.datavertex.me (хмарний)
- **Користувацький додаток**: http://localhost:8080
- **Адмін панель**: http://localhost:8081