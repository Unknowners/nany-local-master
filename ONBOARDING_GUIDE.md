# 📋 Онбординг - Повний гід

Детальний гід по системі онбордингу в Nanny Match Ukraine.

## 🌟 Огляд

Система онбордингу в Nanny Match Ukraine забезпечує плавний вхід нових користувачів у платформу з динамічною конфігурацією для різних ролей.

## 🏗️ Архітектура

### Компоненти системи
- **Backend**: FastAPI з PostgreSQL
- **Frontend**: React з TypeScript
- **Конфігурація**: Динамічна через базу даних
- **Валідація**: Zod схеми
- **Зберігання**: PostgreSQL + Redis

### Таблиці бази даних
- `onboarding_configs` - Конфігурації онбордингу
- `onboarding_steps` - Кроки онбордингу
- `onboarding_field_groups` - Групи полів
- `onboarding_fields` - Поля форм
- `user_onboarding_data` - Дані користувачів
- `onboarding_field_mappings` - Мапінг полів

## 👥 Ролі користувачів

### Батьки (parent)
**Мета**: Знайти відповідну няню для своїх дітей

**Кроки онбордингу:**
1. **Особиста інформація** - Базові дані про себе
2. **Інформація про сім'ю** - Дані про дітей
3. **Вимоги до няні** - Критерії пошуку
4. **Бюджет** - Фінансові рамки
5. **Додаткові налаштування** - Графік, локація

### Няні (nanny)
**Мета**: Створити привабливий профіль для роботи

**Кроки онбордингу:**
1. **Особиста інформація** - Базові дані про себе
2. **Досвід роботи** - Професійний досвід
3. **Послуги** - Типи послуг, які надає
4. **Розклад** - Доступність та графік
5. **Додаткові налаштування** - Навички, сертифікати

## 📊 Структура конфігурації

### onboarding_configs
```sql
CREATE TABLE onboarding_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    target_role user_role NOT NULL,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### onboarding_steps
```sql
CREATE TABLE onboarding_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_id UUID NOT NULL,
    step_key TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    step_number INTEGER NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (config_id) REFERENCES onboarding_configs(id)
);
```

### onboarding_fields
```sql
CREATE TABLE onboarding_fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    step_id UUID NOT NULL,
    group_id UUID,
    field_key TEXT NOT NULL,
    label TEXT NOT NULL,
    description TEXT,
    placeholder TEXT,
    help_text TEXT,
    field_type field_type NOT NULL,
    field_order INTEGER DEFAULT 0,
    is_required BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    reference_category_code TEXT,
    allow_custom_values BOOLEAN DEFAULT FALSE,
    validation_rules JSONB,
    field_config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (step_id) REFERENCES onboarding_steps(id),
    FOREIGN KEY (group_id) REFERENCES onboarding_field_groups(id)
);
```

## 🔧 Типи полів

### Підтримувані типи
- **text** - Текстове поле
- **email** - Email адреса
- **phone** - Номер телефону
- **number** - Числове поле
- **select** - Випадаючий список
- **multiselect** - Множинний вибір
- **textarea** - Багаторядкове поле
- **checkbox** - Чекбокс
- **radio** - Радіо кнопки
- **date** - Дата
- **time** - Час
- **file** - Файл
- **photo** - Фото
- **location** - Локація
- **slider** - Слайдер
- **rating** - Рейтинг
- **custom** - Кастомний компонент

### Приклад конфігурації поля
```json
{
  "field_key": "children_ages",
  "label": "Вік дітей",
  "field_type": "multiselect",
  "reference_category_code": "age_groups",
  "is_required": true,
  "validation_rules": {
    "min_selections": 1,
    "max_selections": 5
  },
  "field_config": {
    "placeholder": "Оберіть вікові групи",
    "help_text": "Можна обрати кілька варіантів"
  }
}
```

## 🗄️ Довідники

### Категорії довідників
- **gender** - Стать
- **age_groups** - Вікові групи
- **locations** - Локації
- **languages** - Мови
- **services** - Послуги
- **skills** - Навички
- **education_levels** - Рівні освіти
- **schedule_types** - Типи розкладу
- **experience_years** - Роки досвіду

### Приклад використання
```sql
-- Отримати всі послуги
SELECT rv.* FROM reference_values rv
JOIN data_categories dc ON rv.category_id = dc.id
WHERE dc.code = 'services' AND rv.is_active = true
ORDER BY rv.sort_order;
```

## 🎨 Frontend компоненти

### Основні компоненти
- **NewParentOnboarding.tsx** - Онбординг батьків
- **NewNannyOnboarding.tsx** - Онбординг нянь
- **DynamicOnboarding** - Динамічний онбординг
- **OnboardingStep** - Крок онбордингу
- **OnboardingField** - Поле форми

### Хуки
- **useDynamicOnboarding** - Динамічний онбординг
- **useReferenceData** - Довідники
- **useOnboardingData** - Дані онбордингу

### Приклад використання
```typescript
// Отримання конфігурації онбордингу
const { data: config } = useDynamicOnboarding('parent');

// Отримання довідників
const { data: services } = useReferenceData('services');

// Збереження даних онбордингу
const { saveOnboardingData } = useOnboardingData();
```

## 🔄 API Endpoints

### Отримання конфігурації
```http
GET /api/v1/onboarding/configs
GET /api/v1/onboarding/steps/{role}
GET /api/v1/onboarding/fields/{step_id}
```

### Робота з даними
```http
POST /api/v1/onboarding/data
PUT /api/v1/onboarding/data/{id}
GET /api/v1/onboarding/data/{user_id}
```

### Довідники
```http
GET /api/v1/reference/categories
GET /api/v1/reference/values/{category}
```

## 📱 Процес онбордингу

### 1. Реєстрація
- Користувач реєструється з телефоном
- Отримує SMS з OTP кодом
- Підтверджує номер телефону

### 2. Вибір ролі
- Обирає роль: батько або няня
- Система завантажує відповідну конфігурацію

### 3. Проходження кроків
- Користувач проходить кроки послідовно
- Дані зберігаються в `user_onboarding_data`
- Валідація відбувається на frontend та backend

### 4. Завершення
- Після завершення всіх кроків
- `onboarding_completed` встановлюється в `true`
- Користувач перенаправляється на головну сторінку

## 🛡️ Валідація

### Frontend валідація (Zod)
```typescript
const onboardingSchema = z.object({
  first_name: z.string().min(2, 'Мінімум 2 символи'),
  last_name: z.string().min(2, 'Мінімум 2 символи'),
  phone: z.string().regex(/^\+380\d{9}$/, 'Невірний формат телефону'),
  children_ages: z.array(z.string()).min(1, 'Оберіть хоча б одну вікову групу')
});
```

### Backend валідація (Pydantic)
```python
class OnboardingDataCreate(BaseModel):
    step_key: str
    field_key: str
    text_value: Optional[str] = None
    number_value: Optional[float] = None
    boolean_value: Optional[bool] = None
    json_value: Optional[dict] = None
```

## 🔧 Налаштування

### Створення нової конфігурації
```sql
-- Створення конфігурації для нової ролі
INSERT INTO onboarding_configs (name, target_role, is_default) 
VALUES ('Нова роль', 'new_role', true);

-- Додавання кроків
INSERT INTO onboarding_steps (config_id, step_key, title, step_number) 
SELECT id, 'step1', 'Перший крок', 1 
FROM onboarding_configs WHERE target_role = 'new_role';
```

### Додавання нових полів
```sql
-- Додавання поля до кроку
INSERT INTO onboarding_fields (step_id, field_key, label, field_type, is_required) 
SELECT id, 'new_field', 'Нове поле', 'text', true 
FROM onboarding_steps WHERE step_key = 'step1';
```

## 🧪 Тестування

### Тестування конфігурації
```bash
# Перевірка конфігурації онбордингу
curl http://localhost:8000/api/v1/onboarding/configs

# Перевірка кроків для ролі
curl http://localhost:8000/api/v1/onboarding/steps/parent
```

### Тестування даних
```bash
# Збереження тестових даних
curl -X POST http://localhost:8000/api/v1/onboarding/data \
  -H "Content-Type: application/json" \
  -d '{"step_key": "personal_info", "field_key": "first_name", "text_value": "Тест"}'
```

## 🚨 Troubleshooting

### Проблеми з конфігурацією
```sql
-- Перевірка активних конфігурацій
SELECT * FROM onboarding_configs WHERE is_active = true;

-- Перевірка кроків
SELECT * FROM onboarding_steps WHERE is_active = true ORDER BY step_number;
```

### Проблеми з даними
```sql
-- Перевірка даних користувача
SELECT * FROM user_onboarding_data WHERE user_id = 'user-id';

-- Перевірка завершення онбордингу
SELECT onboarding_completed, onboarding_step FROM profiles WHERE id = 'user-id';
```

### Frontend проблеми
```typescript
// Перевірка завантаження конфігурації
console.log('Onboarding config:', config);

// Перевірка валідації
console.log('Validation errors:', errors);
```

## 📈 Моніторинг

### Метрики
- **Відсоток завершення** - Скільки користувачів завершують онбординг
- **Час проходження** - Середній час на крок
- **Популярні поля** - Які поля заповнюються найчастіше
- **Помилки валідації** - Найпоширеніші помилки

### Логування
```python
# Логування прогресу онбордингу
logger.info(f"User {user_id} completed step {step_key}")

# Логування помилок валідації
logger.warning(f"Validation error for user {user_id}: {error}")
```

## 🔮 Майбутні покращення

### Заплановані функції
- **Умовна логіка** - Поля, що з'являються залежно від попередніх відповідей
- **Прогрес бар** - Візуальний індикатор прогресу
- **Збереження чернеток** - Автоматичне збереження введених даних
- **Аналітика** - Детальна аналітика проходження онбордингу
- **A/B тестування** - Різні варіанти онбордингу

### Технічні покращення
- **Кешування** - Кешування конфігурації онбордингу
- **Оптимізація** - Оптимізація завантаження даних
- **Мобільна версія** - Покращена мобільна версія
- **Доступність** - Покращення доступності

---

**📋 Онбординг - це ключовий етап успіху платформи. Правильна настройка забезпечує плавний вхід користувачів та збільшує конверсію!**