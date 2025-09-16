# 🚨 Проблема скидання бази при білді

## 🎯 Проблема
База даних на продакшні скидається при кожному білді/деплої, що призводить до втрати:
- Конфігурацій онбордингу
- Кроків онбордингу  
- Довідкових даних
- Користувацьких даних

## 🔍 Можливі причини

### 1. 🚨 **Використання docker-compose down -v**
```bash
# ❌ НЕБЕЗПЕЧНА команда - видаляє volumes
docker-compose down -v

# ✅ БЕЗПЕЧНА команда - зберігає volumes  
docker-compose down
```

### 2. 🚨 **Видалення volumes вручну**
```bash
# ❌ НЕБЕЗПЕЧНІ команди
docker volume rm postgres_data
docker volume prune -f
docker system prune -a --volumes
```

### 3. 🚨 **Проблеми з CI/CD pipeline**
```yaml
# ❌ В CI/CD може бути:
- run: docker-compose down -v  # Видаляє дані!
- run: docker volume prune     # Видаляє volumes!
```

### 4. 🚨 **Seed data з DELETE командами**
```sql
-- В seed-data/03_onboarding_data.sql:
DELETE FROM onboarding_configs;  -- Видаляє дані!
DELETE FROM onboarding_steps;    -- Видаляє дані!
```

## 🔧 Рішення

### 1. **Перевірити команди деплою**
```bash
# На продакшн сервері перевірити історію команд:
history | grep "docker-compose down"
history | grep "volume"

# Перевірити CI/CD скрипти на наявність -v флагу
```

### 2. **Використовувати безпечні команди**
```bash
# ✅ Для оновлення без втрати даних:
docker-compose pull
docker-compose up -d --no-deps backend  # Тільки backend
docker-compose restart nginx             # Тільки nginx

# ❌ НЕ ВИКОРИСТОВУВАТИ:
docker-compose down -v    # Видаляє volumes!
docker-compose up --force-recreate  # Може пошкодити дані
```

### 3. **Створити безпечний seed data**
```sql
-- Замість DELETE використовувати INSERT ... ON CONFLICT:
INSERT INTO onboarding_configs (id, name, target_role, ...)
VALUES (...)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    updated_at = NOW();
```

### 4. **Backup перед деплоєм**
```bash
# Створити backup перед кожним деплоєм:
docker-compose exec postgres pg_dump -U app nanny_match_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 📊 Перевірка стану volumes

### Перевірити наявність volumes:
```bash
docker volume ls | grep postgres
docker volume inspect nanny-match-backend_postgres_data
```

### Перевірити розмір даних:
```bash
# Розмір volume
docker system df -v | grep postgres

# Кількість файлів в volume
docker run --rm -v nanny-match-backend_postgres_data:/data alpine find /data -type f | wc -l
```

## 🛡️ Захист від втрати даних

### 1. **Автоматичні backups**
```bash
# Додати в crontab:
0 2 * * * docker-compose exec postgres pg_dump -U app nanny_match_prod > /backups/daily_$(date +\%Y\%m\%d).sql
```

### 2. **Моніторинг volumes**
```bash
# Перевірка після кожного деплою:
docker volume ls | grep postgres_data || echo "⚠️ Volume missing!"
```

### 3. **Безпечні команди деплою**
```bash
# Створити аліаси для безпечного деплою:
alias prod-deploy="docker-compose pull && docker-compose up -d --no-deps backend"
alias prod-restart="docker-compose restart"
```

## 🎯 Негайні дії

### 1. **Перевірити поточний стан**
```bash
# Чи існує volume?
docker volume ls | grep postgres

# Чи є дані в volume?
docker run --rm -v postgres_data:/data alpine ls -la /data
```

### 2. **Створити backup зараз**
```bash
# Якщо є дані, створити backup:
docker-compose exec postgres pg_dump -U app nanny_match_prod > emergency_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 3. **Виправити seed data**
```bash
# Замінити DELETE команди на INSERT ... ON CONFLICT
# в файлі seed-data/03_onboarding_data.sql
```

## 🚨 **Критично важливо**

**НЕ ВИКОРИСТОВУВАТИ** команди з `-v` флагом на продакшні:
- `docker-compose down -v` ❌
- `docker volume prune` ❌  
- `docker system prune --volumes` ❌

**ЗАВЖДИ** робити backup перед деплоєм!