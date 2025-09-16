# 🚀 Nanny Match - Інструкція для розробки

## ⚠️ ВАЖЛИВО: Завжди очищуйте старі процеси!

Перед запуском ЗАВЖДИ виконайте очищення:

```bash
# Зупинити ВСІ старі процеси
pkill -f "npm.*dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true  
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
pkill -f "python.*uvicorn" 2>/dev/null || true

# Очистити порти примусово
lsof -ti :8080 | xargs -r kill -9 2>/dev/null || true
lsof -ti :8000 | xargs -r kill -9 2>/dev/null || true
```

## 🎯 Правильні порти (НЕ ЗМІНЮВАТИ):

- **Фронтенд**: http://localhost:8080 (ЗАВЖДИ)
- **Бекенд**: http://localhost:8000 (ЗАВЖДИ)

## 📜 Готові скрипти:

### 1. Повне очищення + запуск:
```bash
./restart-clean.sh
```

### 2. Запуск з меню:
```bash
./start-dev.sh
```

### 3. Запуск обох сервісів:
```bash
./start-both.sh
```

## 🔄 Перемикання бекендів:

### Через URL (рекомендовано):
- **Supabase**: http://localhost:8080?backend=supabase
- **FastAPI локальний**: http://localhost:8080?backend=fastapi-local  
- **FastAPI віддалений**: http://localhost:8080?backend=fastapi-remote

### Через перемикач в інтерфейсі:
- У правому верхньому куті є кнопки перемикання

## 📱 Тестування SMS з FastAPI:

1. Перейдіть на: http://localhost:8080?backend=fastapi-local
2. Перевірте в куті: "Backend: fastapi-local"
3. Перейдіть на /forgot-password
4. Введіть номер: +380663556014
5. SMS код з'явиться в логах бекенду (тестовий режим)

## 📝 Моніторинг логів:

```bash
# У новому терміналі
cd nanny-match-backend && tail -f debug.log
```

## ❌ ЩО НЕ РОБИТИ:

- ❌ НЕ запускати кілька npm/vite процесів
- ❌ НЕ змінювати порти без очищення
- ❌ НЕ залишати завислі процеси
- ❌ НЕ перезапускати без потреби

## ✅ ЩО РОБИТИ:

- ✅ Завжди очищати процеси перед запуском
- ✅ Використовувати порти 8080/8000
- ✅ Перемикати бекенди через URL
- ✅ Читати логи для діагностики