# 🪟 Запуск проекту на Windows

## 🚀 ВАРІАНТ 1: Git Bash (Рекомендовано)

### 1️⃣ Встанови Git for Windows:
- Завантаж з https://git-scm.com/download/win  
- При інсталяції вибери "Git Bash" та "Git GUI"

### 2️⃣ Відкрий Git Bash:
- Правий клік в папці проекту → "Git Bash Here"
- АБО Пуск → "Git Bash"

### 3️⃣ Запусти команди:
```bash
# Перейди в папку проекту
cd /c/Users/YourName/Desktop/nany

# Надай права доступу
chmod +x restart-all.sh

# Запусти скрипт  
./restart-all.sh

# Вибери: 2) Хмарний backend
```

---

## 🚀 ВАРІАНТ 2: WSL (Windows Subsystem for Linux)

### 1️⃣ Встанови WSL:
```powershell
# Відкрий PowerShell як адміністратор
wsl --install
# Перезавантаж комп'ютер
```

### 2️⃣ Запусти WSL:
```bash
# У WSL терміналі
cd /mnt/c/Users/YourName/Desktop/nany
chmod +x restart-all.sh
./restart-all.sh
```

---

## 🚀 ВАРІАНТ 3: Ручний запуск (якщо bash не працює)

### Backend (хмарний - найпростіше):
✅ **НЕ ПОТРІБНО!** Використовуй https://nany.datavertex.me/

### Frontend (User):
```cmd
cd nanny-match-ukraine
npm install
npm run dev
```
Відкриється: http://localhost:8080

### Frontend (Admin):  
```cmd
cd nanny-match-ukraine-adminfront
npm install
npm run dev
```
Відкриється: http://localhost:8081

---

## 🛠️ Встановлення залежностей для Windows:

### Node.js:
- Завантаж з https://nodejs.org/ (LTS версія)
- Встанови з усіма дефолтними налаштуваннями

### Docker (опціонально):
- Завантаж Docker Desktop for Windows
- Потрібно лише для локального backend

---

## ⚡ ШВИДКИЙ СТАРТ:

1. **Встанови Git for Windows**
2. **Відкрий Git Bash в папці проекту**  
3. **Запусти:**
   ```bash
   chmod +x restart-all.sh
   ./restart-all.sh
   ```
4. **Вибери опцію 2 (Хмарний backend)**
5. **Чекай поки запуститься!**

---

## ❗ Часті проблеми Windows:

### "bash не розпізнається"
- Встанови Git for Windows
- Використовуй Git Bash замість CMD

### "Permission denied"  
```bash
chmod +x restart-all.sh
```

### "Docker не знайдено"
- Вибери хмарний backend (опція 2)
- АБО встанови Docker Desktop

### Порти зайняті:
```cmd
# Перевір які процеси використовують порти
netstat -ano | findstr :8080
netstat -ano | findstr :8081

# Вбий процес (замість PID вставь номер процесу)
taskkill /PID номер_процесу /F
```
