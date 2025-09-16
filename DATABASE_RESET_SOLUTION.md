# 🔧 РІШЕННЯ: База скидається при білді

## 🎯 Проблема знайдена!
База даних на продакшні скидається при кожному білді через **DELETE команди** в seed файлах.

## 🚨 Корінь проблеми

### В файлі `seed-data/03_onboarding_data.sql`:
```sql
-- ❌ ЦІ КОМАНДИ ВИДАЛЯЮТЬ ВСІ ДАНІ:
DELETE FROM user_onboarding_data;
DELETE FROM onboarding_fields;
DELETE FROM onboarding_field_groups;  
DELETE FROM onboarding_steps;
DELETE FROM onboarding_configs;
```

### Що відбувається:
1. **При білді** - seed скрипт виконується
2. **DELETE команди** - видаляють всі дані онбордингу
3. **INSERT команди** - додають нові дані
4. **Результат** - втрачаються користувацькі дані та налаштування

## ✅ Рішення застосовано

### 1. **Створено безпечну версію seed файлу**
**Файл**: `seed-data/03_onboarding_data_safe.sql`
- 🚫 **Немає DELETE команд**
- ✅ **Використовує INSERT ... ON CONFLICT**
- ✅ **Зберігає існуючі дані**

### 2. **Оновлено seed скрипт**
**Файл**: `scripts/seed_data_complete.py`
- Спочатку спробує безпечну версію
- Fallback до звичайної версії

### 3. **Приклад безпечної команди**
```sql
-- ✅ БЕЗПЕЧНА версія:
INSERT INTO onboarding_configs (id, name, target_role, version, is_active, is_default) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Онбординг батьків', 'parent', 1, true, true)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    version = EXCLUDED.version,
    updated_at = NOW();
```

## 🚀 Деплой рішення

### 1. **Закомітити зміни**
```bash
git add .
git commit -m "Fix database reset issue - use safe seed data without DELETE commands"
git push
```

### 2. **Деплой на продакшн**
```bash
# Безпечний деплой без втрати даних:
docker-compose pull
docker-compose up -d --no-deps backend
```

### 3. **Запустити безпечний seed**
```bash
docker-compose exec backend python scripts/seed_data_complete.py
```

## 🛡️ Захист від майбутніх проблем

### 1. **Заборонити небезпечні команди**
```bash
# ❌ НЕ ВИКОРИСТОВУВАТИ на продакшні:
docker-compose down -v           # Видаляє volumes!
docker volume prune             # Видаляє volumes!
docker system prune --volumes   # Видаляє volumes!

# ✅ БЕЗПЕЧНІ альтернативи:
docker-compose down             # Зберігає volumes
docker-compose restart         # Безпечний рестарт
docker-compose up -d --no-deps backend  # Оновити тільки backend
```

### 2. **Автоматичні backups**
```bash
# Додати в CI/CD pipeline:
# Перед кожним деплоєм:
docker-compose exec postgres pg_dump -U app nanny_match_prod > backup_pre_deploy.sql
```

### 3. **Моніторинг даних**
```bash
# Перевірка після деплою:
curl "https://nany.datavertex.me/api/v1/onboarding_configs" | jq '. | length'
# Має бути: 2 (не 0!)
```

## 📊 Очікуваний результат

Після застосування рішення:
- ✅ **Дані НЕ видаляються** при білді
- ✅ **Seed data оновлює** існуючі записи
- ✅ **Користувацькі дані зберігаються**
- ✅ **Онбординг працює** після кожного деплою

## 🎯 Негайні дії

1. **Деплой** виправленого коду
2. **Запустити** безпечний seed скрипт
3. **Перевірити** що дані не зникають після деплою
4. **Додати** автоматичні backups

**Це має остаточно вирішити проблему скидання бази!**