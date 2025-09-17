# 🏗️ Правильна архітектура Profile vs Nanny/Parent

## 🎯 Принципи правильної архітектури:

### Profile - тільки ЗАГАЛЬНІ поля:
```sql
class Profile(Base):
    id = Column(String, primary_key=True)
    user_id = Column(String, unique=True)
    phone = Column(String, unique=True)
    password_hash = Column(String)
    email = Column(String, unique=True)  -- загальний email
    first_name = Column(String)          -- загальне ім'я
    last_name = Column(String)           -- загальне прізвище
    location = Column(String)            -- загальна локація
    
    -- Онбординг статус (загальний для всіх)
    onboarding_completed = Column(Boolean, default=False)
    onboarding_step = Column(Integer, default=1)
    
    -- Системні поля
    approved = Column(Boolean, default=True)
    is_test_data = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    -- ВИДАЛИТИ ці поля (вони специфічні):
    -- family_data = Column(JSON)      ❌ Тільки для батьків
    -- requirements_data = Column(JSON) ❌ Тільки для батьків  
    -- budget_data = Column(JSON)      ❌ Тільки для батьків
```

### Nanny - специфічні поля нянь:
```sql
class Nanny(Base):
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("profiles.user_id"))
    
    -- НЕ дублювати загальні поля з Profile:
    -- first_name ❌ (є в Profile)
    -- last_name ❌ (є в Profile)  
    -- email ❌ (є в Profile)
    -- phone ❌ (є в Profile)
    -- location ❌ (є в Profile)
    
    -- Тільки специфічні для нянь:
    age = Column(Integer)
    hourly_rate = Column(Numeric(10, 2))
    experience_years = Column(Integer)
    about_me = Column(Text)
    professional_experience = Column(Text)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    transportation = Column(String)
    rating = Column(Numeric(3, 2))
    
    -- Онбординг дані нянь (замість JSON):
    education_level = Column(String)
    languages_spoken = Column(String)  -- або окрема таблиця
    certifications = Column(Text)      -- або окрема таблиця
    age_groups_experience = Column(String)
    services_offered = Column(String)  -- або окрема таблиця
```

### Parent - специфічні поля батьків:
```sql
class Parent(Base):
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("profiles.user_id"))
    
    -- НЕ дублювати загальні поля з Profile:
    -- first_name ❌ (є в Profile)
    -- last_name ❌ (є в Profile)
    -- email ❌ (є в Profile)
    -- phone ❌ (є в Profile)
    -- location ❌ (є в Profile)
    
    -- Тільки специфічні для батьків:
    about_me = Column(Text)
    children_count = Column(Integer)
    household_type = Column(String)
    home_environment = Column(String)
    schedule_flexibility = Column(String)
    preferred_start_date = Column(Date)
    rating = Column(Numeric(3, 2))
    
    -- Онбординг дані батьків (замість JSON):
    budget_min = Column(Numeric(10, 2))
    budget_max = Column(Numeric(10, 2))
    preferred_nanny_age_min = Column(Integer)
    preferred_nanny_age_max = Column(Integer)
    required_experience_years = Column(Integer)
    preferred_languages = Column(String)
    special_requirements = Column(Text)
```

## 🔄 План міграції:

### Крок 1: Очистити Profile
```sql
-- Видалити специфічні поля з Profile:
ALTER TABLE profiles DROP COLUMN family_data;
ALTER TABLE profiles DROP COLUMN requirements_data;
ALTER TABLE profiles DROP COLUMN budget_data;

-- Видалити дублюючі поля з Nanny та Parent:
ALTER TABLE nannies DROP COLUMN first_name;
ALTER TABLE nannies DROP COLUMN last_name;
ALTER TABLE nannies DROP COLUMN email;
ALTER TABLE nannies DROP COLUMN phone;
ALTER TABLE nannies DROP COLUMN location;

ALTER TABLE parents DROP COLUMN first_name;
ALTER TABLE parents DROP COLUMN last_name;
ALTER TABLE parents DROP COLUMN email;
ALTER TABLE parents DROP COLUMN phone;
ALTER TABLE parents DROP COLUMN location;
```

### Крок 2: Додати онбординг поля
```sql
-- Додати специфічні онбординг поля в Nanny:
ALTER TABLE nannies ADD COLUMN education_level VARCHAR(100);
ALTER TABLE nannies ADD COLUMN languages_spoken TEXT;
ALTER TABLE nannies ADD COLUMN age_groups_experience TEXT;

-- Додати специфічні онбординг поля в Parent:
ALTER TABLE parents ADD COLUMN budget_min DECIMAL(10,2);
ALTER TABLE parents ADD COLUMN budget_max DECIMAL(10,2);
ALTER TABLE parents ADD COLUMN preferred_nanny_age_min INTEGER;
ALTER TABLE parents ADD COLUMN preferred_nanny_age_max INTEGER;
```

### Крок 3: Мігрувати дані
```python
# Перенести дані з JSON полів Profile в нормалізовані поля Nanny/Parent
# Видалити UserOnboardingData таблицю (замінити на поля в Nanny/Parent)
```

## ✅ Переваги правильної архітектури:

1. **Чистота**: Profile містить тільки загальні поля
2. **Без дублювання**: Кожне поле в одному місці
3. **Типізація**: Замість JSON - конкретні типи полів
4. **Продуктивність**: Індекси на конкретних полях
5. **Валідація**: На рівні БД та додатку
6. **Простота**: Прості SELECT замість JSON запитів

## 🎯 Результат:

```sql
-- Отримати повну інформацію про няню:
SELECT p.*, n.* 
FROM profiles p 
JOIN nannies n ON p.user_id = n.user_id 
WHERE p.user_id = ?

-- Отримати повну інформацію про батька:
SELECT p.*, pr.* 
FROM profiles p 
JOIN parents pr ON p.user_id = pr.user_id 
WHERE p.user_id = ?
```

**Простіше, швидше, зрозуміліше!**

