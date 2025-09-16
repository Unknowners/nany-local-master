# 💻 Безпечне використання терміналу

## ❗ КРИТИЧНЕ ПРАВИЛО: НЕ використовувати команди які можуть зависнути

### 🚫 **ЗАБОРОНЕНІ команди (можуть зависнути):**

#### HTTP запити без таймаутів
```bash
# ❌ НЕБЕЗПЕЧНО - може зависнути назавжди
curl http://localhost:8080
curl https://api.example.com
wget http://slow-server.com

# ✅ БЕЗПЕЧНО - з таймаутами
curl -s -f -m 5 http://localhost:8080/health
curl -s -I -m 3 http://localhost:8080  # тільки заголовки
curl -s --max-time 5 https://api.example.com
```

#### Інтерактивні процеси
```bash  
# ❌ НЕБЕЗПЕЧНО - інтерактивні
npm run dev
npm start
python manage.py runserver
uvicorn app:main

# ✅ БЕЗПЕЧНО - у фоні або з обмеженнями
npm run dev > /dev/null 2>&1 &
npm start &
python manage.py runserver > /dev/null &
uvicorn app:main --host 0.0.0.0 --port 8000 &
```

#### Читання великих даних
```bash
# ❌ НЕБЕЗПЕЧНО - може повернути гігабайти
cat large_file.log
docker logs container_name
psql -c "SELECT * FROM big_table"
tail -f logfile.log

# ✅ БЕЗПЕЧНО - з обмеженнями
head -20 large_file.log
tail -10 large_file.log
docker logs container_name --tail=10 --since=1h
psql -c "SELECT * FROM table LIMIT 5"
timeout 5 tail -f logfile.log
```

#### Команди які чекають вводу
```bash
# ❌ НЕБЕЗПЕЧНО - чекають вводу
rm file.txt                    # може запитати підтвердження
docker exec -it container bash # інтерактивний режим
psql database_name             # інтерактивна консоль

# ✅ БЕЗПЕЧНО - неінтерактивні
rm -f file.txt                 # без підтвердження
docker exec container_name command  # одна команда
psql database_name -c "SELECT 1"   # одна команда
```

### 🛡️ **ОБОВ'ЯЗКОВІ параметри безпеки:**

#### Для HTTP запитів
- **`-m 5`** або **`--max-time 5`** - таймаут 5 секунд
- **`-s`** або **`--silent`** - без прогрес-бару  
- **`-f`** або **`--fail`** - швидкий fail при помилках
- **`-I`** - тільки заголовки, не тіло відповіді

#### Для баз даних
- **`LIMIT 10`** - обмежити результат
- **`-t`** - тільки дані, без форматування
- **`--timeout=5`** - таймаут для з'єднання

#### Для Docker
- **`--tail=10`** - тільки останні рядки логів
- **`--since=1h`** - тільки останні години
- **`--format`** - структурований вивід

#### Для файлів
- **`head -10`** - тільки перші рядки
- **`tail -5`** - тільки останні рядки  
- **`wc -l`** - тільки кількість рядків

### ⚡ **Швидкі перевірки стану:**

```bash
# Перевірка портів (швидко)
lsof -ti :8000 && echo "Port busy" || echo "Port free"
netstat -an | grep :8080 | head -1

# Перевірка процесів (швидко)  
pgrep -f "npm run dev" && echo "Running" || echo "Stopped"
ps aux | grep "docker" | head -3

# Перевірка сервісів (з таймаутом)
curl -s -f -m 3 http://localhost:8000/health | jq '.status' 2>/dev/null || echo "Down"

# Перевірка Docker (швидко)
docker ps --filter "name=nanny" --format "{{.Names}}: {{.Status}}"
docker-compose ps --format "table {{.Name}}\t{{.State}}"

# Перевірка логів (обмежено)
docker logs container_name --tail=5 --since=5m
tail -10 backend.log | grep ERROR
```

### 🔍 **Діагностика проблем:**

```bash
# Замість довгих логів
docker logs backend --tail=10 | grep ERROR
grep -n "ERROR" backend.log | tail -5

# Замість інтерактивного psql
docker exec container psql -U user -d db -c "SELECT COUNT(*) FROM table"
docker exec container pg_isready -U user -d db

# Замість curl до HTML сторінок
curl -s -I -m 3 http://localhost:3000 | head -1
curl -s -m 3 http://localhost:3000 | grep -o "<title>.*</title>"
```

### 🎯 **Золоті правила:**

1. **Завжди використовувати таймаути** (`-m 5`, `--timeout=5`)
2. **Обмежувати вивід** (`LIMIT`, `--tail`, `| head`)
3. **Перевіряти статус швидко** (`lsof`, `pgrep`, `docker ps`)
4. **Фонові процеси** для довготривалих команд (`&`)
5. **Неінтерактивний режим** (`-y`, `--yes`, `-f`)

### ⚠️ **Якщо команда зависла:**
- Натисніть `Ctrl+C` для переривання
- Використовуйте `timeout` команду: `timeout 10 your_command`
- Перевіряйте процеси: `ps aux | grep command_name`