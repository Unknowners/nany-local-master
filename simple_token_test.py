#!/usr/bin/env python3
"""
Простий тест з готовим токеном
Вставте сюди валідний токен з браузера
"""
import requests
import json

def test_with_browser_token():
    """Тестує з токеном отриманим з браузера"""
    
    BASE_URL = "https://nany.datavertex.me"
    
    print("🔑 ТЕСТ З ТОКЕНОМ З БРАУЗЕРА")
    print("=" * 40)
    print()
    print("📋 ІНСТРУКЦІЯ:")
    print("1. Відкрийте https://nany.datavertex.me в браузері")
    print("2. Увійдіть в систему")
    print("3. Відкрийте Developer Tools (F12)")
    print("4. Перейдіть на вкладку Application/Storage")
    print("5. Знайдіть localStorage -> access_token")
    print("6. Скопіюйте значення токену")
    print("7. Вставте його нижче в код")
    print()
    
    # 🔑 ВСТАВТЕ ТОКЕН СЮДИ:
    browser_token = None  # Наприклад: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    
    if not browser_token:
        print("❌ Токен не вставлено!")
        print("💡 Вставте токен в змінну browser_token")
        return
    
    print(f"🔍 Тестуємо з токеном: {browser_token[:30]}...")
    print()
    
    headers = {"Authorization": f"Bearer {browser_token}"}
    
    # 1. Спочатку перевіряємо валідність токену
    print("1️⃣ Перевірка валідності токену:")
    try:
        me_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers, timeout=10)
        print(f"   📊 /auth/me Status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print("   ✅ Токен валідний!")
            print(f"   👤 Користувач: {user_data.get('id', 'N/A')}")
            print(f"   📧 Email: {user_data.get('email', 'N/A')}")
            print(f"   🎭 Роль: {user_data.get('role', 'N/A')}")
        else:
            print("   ❌ Токен невалідний!")
            print(f"   📄 Відповідь: {me_response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
        return
    
    # 2. Тестуємо search ендпоінт
    print("\n2️⃣ Тестування search ендпоінту:")
    
    search_tests = [
        ("Базовий запит", "/api/v1/search/nannies/complete?limit=3"),
        ("З exclude_saved=true", "/api/v1/search/nannies/complete?limit=3&exclude_saved=true"),
        ("Простий ендпоінт", "/api/v1/search/nannies?limit=3"),
    ]
    
    for test_name, endpoint in search_tests:
        print(f"\n   📡 {test_name}:")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=15)
            print(f"      📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("      ✅ SUCCESS!")
                
                data = response.json()
                print(f"      📊 Ключі відповіді: {list(data.keys())}")
                
                if 'data' in data:
                    nannies = data['data']
                    print(f"      👩‍🍼 Знайдено нянь: {len(nannies)}")
                    
                    if nannies:
                        first_nanny = nannies[0]
                        print(f"      📋 Поля няні: {list(first_nanny.keys())}")
                        print(f"      👤 Ім'я: {first_nanny.get('first_name', 'N/A')} {first_nanny.get('last_name', '')}")
                        print(f"      📍 Локація: {first_nanny.get('location', 'N/A')}")
                        print(f"      📸 Фото: {'✅' if first_nanny.get('avatar_url') else '❌'}")
                        print(f"      💰 Ставка: {first_nanny.get('hourly_rate', 'N/A')}")
                else:
                    print(f"      📊 Повна відповідь: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    
            elif response.status_code == 500:
                print("      ❌ SERVER ERROR 500!")
                error_text = response.text
                print(f"      🔥 Помилка: {error_text}")
                
                # Аналіз помилки
                if "relation" in error_text and "does not exist" in error_text:
                    print("      💡 ПРОБЛЕМА: Таблиця не існує в базі даних!")
                elif "column" in error_text and "does not exist" in error_text:
                    print("      💡 ПРОБЛЕМА: Колонка не існує в таблиці!")
                elif "database" in error_text.lower():
                    print("      💡 ПРОБЛЕМА: Проблема з підключенням до бази даних!")
                elif "syntax error" in error_text.lower():
                    print("      💡 ПРОБЛЕМА: Синтаксична помилка в SQL запиті!")
                else:
                    print("      💡 ПРОБЛЕМА: Невідома помилка сервера")
                    
            else:
                print(f"      ⚠️ Неочікуваний статус: {response.status_code}")
                print(f"      📄 Відповідь: {response.text[:200]}...")
                
        except Exception as e:
            print(f"      ❌ Помилка запиту: {e}")
    
    # 3. Тестуємо інші ендпоінти для порівняння
    print("\n3️⃣ Тестування інших ендпоінтів:")
    
    other_tests = [
        ("Лайки", "/api/v1/simple/my-likes"),
        ("Лічильники", "/api/v1/counters/dashboard/complete"),
    ]
    
    for test_name, endpoint in other_tests:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            status_icon = "✅" if response.status_code == 200 else "❌" if response.status_code >= 500 else "⚠️"
            print(f"   {status_icon} {test_name}: {response.status_code}")
            
            if response.status_code >= 500:
                print(f"      🔥 {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ {test_name}: Помилка - {e}")

if __name__ == "__main__":
    test_with_browser_token()
