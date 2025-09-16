#!/usr/bin/env python3
"""
Скрипт для автоматичного проставляння імен профайлам з null значеннями
"""
import psycopg2
import random
from datetime import datetime

# Підключення до продакшн БД
LOCAL_DB_CONFIG = {
    "host": "localhost", 
    "port": "5432", 
    "database": "app",
    "user": "app",
    "password": "app"
}

# Списки імен для генерації
FIRST_NAMES_MALE = [
    "Сергій", "Олександр", "Андрій", "Володимир", "Дмитро", "Максим", 
    "Віталій", "Роман", "Богдан", "Тарас", "Ігор", "Павло", "Олег"
]

FIRST_NAMES_FEMALE = [
    "Олена", "Світлана", "Наталія", "Ольга", "Тетяна", "Марія", 
    "Катерина", "Анна", "Юлія", "Ірина", "Віктория", "Людмила"
]

LAST_NAMES = [
    "Петренко", "Іваненко", "Коваленко", "Бойко", "Мельник", "Гріщенко",
    "Ткаченко", "Кравченко", "Морозенко", "Полтавченко", "Савченко", "Лисенко"
]

def generate_name():
    """Генерує випадкове ім'я та прізвище"""
    # Випадково вибираємо чоловіче чи жіноче ім'я
    if random.choice([True, False]):
        first_name = random.choice(FIRST_NAMES_FEMALE)
    else:
        first_name = random.choice(FIRST_NAMES_MALE)
    
    last_name = random.choice(LAST_NAMES)
    return first_name, last_name

def main():
    try:
        # Підключення до БД
        print("🔌 Підключаємось до локальної БД...")
        conn = psycopg2.connect(**LOCAL_DB_CONFIG)
        cursor = conn.cursor()
        
        # Знаходимо профайли з null іменами
        print("🔍 Шукаємо профайли з NULL іменами...")
        cursor.execute("""
            SELECT user_id, first_name, last_name, role, created_at
            FROM profiles 
            WHERE first_name IS NULL OR last_name IS NULL OR first_name = '' OR last_name = ''
            ORDER BY created_at DESC
        """)
        
        null_profiles = cursor.fetchall()
        
        if not null_profiles:
            print("✅ Всі профайли вже мають імена!")
            return
            
        print(f"📊 Знайдено {len(null_profiles)} профайлів з відсутніми іменами")
        
        counter = 1
        updated_count = 0
        
        for user_id, first_name, last_name, role, created_at in null_profiles:
            print(f"\n🔧 #{counter}: {user_id} - '{first_name}' '{last_name}' ({role})")
            
            # Генеруємо нові імена
            new_first_name, new_last_name = generate_name()
            
            # Додаємо номер для унікальності
            new_first_name = f"{new_first_name} {counter:02d}"
            
            print(f"   → Нові імена: '{new_first_name}' '{new_last_name}'")
            
            # Оновлюємо профайл
            cursor.execute("""
                UPDATE profiles 
                SET first_name = %s, last_name = %s, updated_at = NOW()
                WHERE user_id = %s
            """, (new_first_name, new_last_name, user_id))
            
            updated_count += 1
            counter += 1
            
        # Підтверджуємо зміни
        conn.commit()
        print(f"\n✅ ГОТОВО! Оновлено {updated_count} профайлів")
        
        # Перевіряємо результат
        cursor.execute("""
            SELECT COUNT(*) FROM profiles 
            WHERE first_name IS NULL OR last_name IS NULL OR first_name = '' OR last_name = ''
        """)
        remaining_null = cursor.fetchone()[0]
        
        print(f"📊 Залишилось профайлів з NULL: {remaining_null}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ПОМИЛКА: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("🚀 Початок обробки NULL профайлів...")
    main()
    print("🏁 Завершено!")