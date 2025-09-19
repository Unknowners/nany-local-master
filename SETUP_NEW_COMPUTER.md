# 🖥️ Налаштування проекту на новому комп'ютері

## 📋 Швидкий чек-лист

### 1. Встановити необхідні інструменти:
```bash
# Перевірити що встановлено:
node --version     # Потрібно v16+
docker --version   # Потрібно для локального backend
python3 --version  # Потрібно v3.8+
git --version      # Потрібно для клонування
```

### 2. Клонувати всі репозиторії:
```bash
# Головний репозиторій
git clone https://github.com/your-org/nany.git
cd nany

# Backend
git clone https://github.com/Unknowners/nanny-match-backend.git

# User Frontend  
git clone https://github.com/Unknowners/nanny-match-ukraine.git

# Admin Frontend
git clone https://github.com/Unknowners/nanny-match-ukraine-adminfront.git
```

### 3. Налаштувати .env файли:
```bash
# Backend
cp nanny-match-backend/.env.example nanny-match-backend/.env

# User Frontend
cp nanny-match-ukraine/.env.example nanny-match-ukraine/.env

# Admin Frontend  
cp nanny-match-ukraine-adminfront/.env.example nanny-match-ukraine-adminfront/.env
```

### 4. Надати права доступу:
```bash
chmod +x restart-all.sh
chmod +x restart-all-local.sh
```

### 5. Запустити проект:
```bash
# Вибрати хмарний backend (простіше)
./restart-all.sh
# Коли запитає тип backend - вибери: 2) Хмарний

# АБО локальний backend (потребує Docker)
./restart-all.sh  
# Коли запитає тип backend - вибери: 1) Локальний
```

## ❗ Часті проблеми:

### Проблема: "Permission denied"
```bash
chmod +x restart-all.sh
```

### Проблема: "Docker not found"
- Встанови Docker Desktop
- АБО вибери хмарний backend (option 2)

### Проблема: "Node not found"  
```bash
# Встанови Node.js v18+
brew install node  # на macOS
# або завантаж з nodejs.org
```

### Проблема: Скрипт зависає
- Перевір інтернет з'єднання
- Спробуй хмарний backend (швидше)

## 🚀 Швидкий старт (рекомендовано):
```bash
# 1. Клонуй проект
git clone ваш-репозиторій
cd nany

# 2. Запусти з хмарним backend
./restart-all.sh
# Вибери: 2) Хмарний backend

# 3. Чекай поки все запуститься
# Frontend: http://localhost:8080
# Admin: http://localhost:8081
```
