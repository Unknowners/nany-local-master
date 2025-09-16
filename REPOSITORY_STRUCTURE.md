# 🏗️ Структура репозиторіїв проекту Nanny Match

## 📦 Три незалежні Git репозиторії:

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

### 3. **Frontend репозиторій** (`nanny-match-ukraine/`)
- **Призначення**: React додаток
- **Технології**: React, Vite, TypeScript, Tailwind CSS
- **Вміст**:
  - `src/` - вихідний код React додатку
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

# Для змін в frontend
cd /Users/anton/Desktop/nany/nanny-match-ukraine
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
1. Зупинить старі процеси
2. Запустить Docker контейнери (PostgreSQL, Redis)
3. Запустить Backend на http://localhost:8000
4. Запустить Frontend на http://localhost:8080