#!/usr/bin/env python3
"""
Тестування search ендпоінту з валідним токеном
"""
import requests
import json

def get_valid_token():
    """Отримує валідний токен через процес авторизації"""
    
    BASE_URL = "https://nany.datavertex.me"
    test_phone = "+380501234567"
    
    print("🔐 Отримання валідного токену...")
    
    try:
        # Крок 1: Відправляємо OTP
        print("   📱 Відправка OTP...")
        otp_response = requests.post(
            f"{BASE_URL}/api/v1/auth/send-otp",
            json={"phone": test_phone},
            timeout=10
        )
        
        if otp_response.status_code != 200:
            print(f"   ❌ Помилка відправки OTP: {otp_response.status_code}")
            return None
            
        otp_data = otp_response.json()
        
        # Витягуємо OTP код з DEV режиму
        if "OTP код:" in otp_data.get("message", ""):
            otp_code = otp_data["message"].split("OTP код: ")[1].split(" ")[0]
            print(f"   🔑 OTP код: {otp_code}")
            
            # Крок 2: Верифікуємо OTP (пропускаємо через помилку 500)
            print("   ✅ Пропускаємо верифікацію (через помилку 500)")
            
            # Крок 3: Спробуємо прямий логін
            print("   🔐 Спроба логіну...")
            login_response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json={"phone": test_phone},
                timeout=10
            )
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                access_token = login_data.get("data", {}).get("access_token")
                
                if access_token:
                    print(f"   ✅ Токен отримано: {access_token[:20]}...")
                    return access_token
                else:
                    print("   ❌ Токен не знайдено в відповіді")
            else:
                print(f"   ❌ Помилка логіну: {login_response.status_code}")
                print(f"       {login_response.text}")
        else:
            print("   ❌ OTP код не знайдено в відповіді")
            
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    return None

def test_search_endpoint(token):
    """Тестує search ендпоінт з валідним токеном"""
    
    BASE_URL = "https://nany.datavertex.me"
    
    print("\n🔍 Тестування search ендпоінту...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Тестуємо різні варіанти запиту
    test_cases = [
        ("Базовий запит", "/api/v1/search/nannies/complete?limit=5"),
        ("З exclude_saved=true", "/api/v1/search/nannies/complete?limit=5&exclude_saved=true"),
        ("З exclude_saved=false", "/api/v1/search/nannies/complete?limit=5&exclude_saved=false"),
        ("Простий ендпоінт", "/api/v1/search/nannies?limit=5"),
    ]
    
    for test_name, endpoint in test_cases:
        try:
            print(f"\n   📡 {test_name}:")
            print(f"      URL: {BASE_URL}{endpoint}")
            
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                timeout=15
            )
            
            print(f"      📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("      ✅ SUCCESS!")
                
                try:
                    data = response.json()
                    print(f"      📊 Структура відповіді: {list(data.keys())}")
                    
                    if 'data' in data:
                        nannies = data['data']
                        print(f"      👩‍🍼 Знайдено нянь: {len(nannies)}")
                        
                        if nannies:
                            first_nanny = nannies[0]
                            print(f"      📋 Поля першої няні: {list(first_nanny.keys())}")
                            print(f"      👤 Ім'я: {first_nanny.get('first_name', 'N/A')}")
                            print(f"      📸 Фото: {'Є' if first_nanny.get('avatar_url') else 'Немає'}")
                    else:
                        print(f"      📊 Відповідь: {str(data)[:200]}...")
                        
                except json.JSONDecodeError:
                    print(f"      📄 Текстова відповідь: {response.text[:200]}...")
                    
            elif response.status_code == 500:
                print("      ❌ SERVER ERROR 500!")
                print(f"      🔥 Помилка: {response.text}")
                
                # Спробуємо зрозуміти причину
                if "database" in response.text.lower():
                    print("      💡 Можлива проблема з базою даних")
                elif "table" in response.text.lower():
                    print("      💡 Можлива проблема з таблицями")
                elif "column" in response.text.lower():
                    print("      💡 Можлива проблема зі структурою таблиць")
                    
            elif response.status_code == 401:
                print("      ❌ Токен невалідний або прострочений")
            elif response.status_code == 403:
                print("      ❌ Недостатньо прав доступу")
            else:
                print(f"      ⚠️ Неочікуваний статус: {response.status_code}")
                print(f"      📄 Відповідь: {response.text[:200]}...")
                
        except Exception as e:
            print(f"      ❌ Помилка запиту: {e}")

def main():
    """Головна функція"""
    
    print("🚀 ТЕСТУВАННЯ SEARCH ЕНДПОІНТУ З ВАЛІДНИМ ТОКЕНОМ")
    print("=" * 60)
    
    # Спробуємо використати збережений токен якщо є
    saved_token = None  # Можете вставити токен сюди для швидкого тестування
    
    if saved_token:
        print("🔑 Використовуємо збережений токен...")
        token = saved_token
    else:
        token = get_valid_token()
    
    if token:
        test_search_endpoint(token)
    else:
        print("\n❌ Не вдалося отримати валідний токен")
        print("💡 Спробуйте:")
        print("   1. Перевірити чи працює база даних")
        print("   2. Перевірити логи сервера")
        print("   3. Вставити валідний токен в код")

if __name__ == "__main__":
    main()
