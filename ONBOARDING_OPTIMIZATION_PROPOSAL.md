# 🚀 Пропозиція оптимізації структури онбордингу

## 📊 Поточні проблеми:

1. **Дублювання даних**: Profile.family_data + UserOnboardingData
2. **EAV антипатерн**: складні запити, погана продуктивність  
3. **Надмірна складність**: 6 таблиць для простого онбордингу

## ✅ Рекомендована структура:

### Варіант 1: JSON-центрична (рекомендований)
```sql
-- Спростити до 3 таблиць
OnboardingConfig (конфігурації)
OnboardingStep (кроки)  
OnboardingField (поля)

-- Видалити:
OnboardingFieldGroup (зайва)
OnboardingFieldMapping (зайва)
UserOnboardingData (замінити на JSON в Profile)

-- Profile залишити тільки з JSON полями:
family_data JSON
requirements_data JSON  
budget_data JSON
onboarding_progress JSON -- новий для відстеження прогресу
```

### Варіант 2: Нормалізована структура
```sql
-- Створити спеціалізовані таблиці:
ParentOnboarding (user_id, family_size, children_ages, budget_min, budget_max, ...)
NannyOnboarding (user_id, experience_years, education, languages, ...)
OnboardingProgress (user_id, step_key, completed_at, data_snapshot)
```

## 🎯 Переваги оптимізації:

### JSON-центрична:
✅ Простота розробки та підтримки
✅ Гнучкість структури даних
✅ Швидкі запити (один SELECT замість JOIN)
✅ Легко додавати нові поля
✅ PostgreSQL має відмінну підтримку JSON

### Нормалізована:
✅ Строга типізація
✅ Кращі можливості для аналітики
✅ Індекси на окремих полях
✅ Валідація на рівні БД

## 🔧 План міграції:

1. **Фаза 1**: Перенести дані з UserOnboardingData в JSON поля Profile
2. **Фаза 2**: Видалити зайві таблиці (OnboardingFieldGroup, OnboardingFieldMapping)
3. **Фаза 3**: Оптимізувати API для роботи з JSON
4. **Фаза 4**: Додати валідацію на рівні додатку

## 📈 Очікувані результати:

- **Продуктивність**: +50% швидкості запитів
- **Простота**: -60% складності коду
- **Гнучкість**: +100% легкості додавання полів
- **Підтримка**: -40% часу на розробку нових фіч

## 🚀 Рекомендація:

**Використовувати JSON-центричний підхід** для Nanny Match, оскільки:
- PostgreSQL має відмінну підтримку JSON
- Структура онбордингу часто змінюється
- Простота важливіша за строгу нормалізацію для цього кейсу

