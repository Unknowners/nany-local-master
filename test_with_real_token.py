#!/usr/bin/env python3
"""
Тестування ендпоінту з реальним токеном
"""
import requests
import json

def test_with_token():
    """Тестує ендпоінт з реальним токеном"""
    
    BASE_URL = "https://nany.datavertex.me"
    
    print("🔐 Тестування з реальним токеном")
    print("Спочатку потрібно отримати токен через логін...")
    print()
    
    # Тестуємо логін ендпоінт
    print("1️⃣ Тест логін ендпоінту:")
    
    # Використовуємо тестовий номер телефону
    test_phone = "+380501234567"  # Замініть на реальний тестовий номер
    
    try:
        # Крок 1: Відправляємо OTP
        otp_response = requests.post(
            f"{BASE_URL}/api/v1/auth/send-otp",
            json={"phone": test_phone},
            timeout=10
        )
        
        print(f"   📱 OTP запит: {otp_response.status_code}")
        print(f"   📄 Відповідь: {otp_response.text[:200]}...")
        
        if otp_response.status_code == 200:
            otp_data = otp_response.json()
            print("   ✅ OTP відправлено успішно")
            
            # У DEV режимі OTP код може бути в відповіді
            if "OTP код:" in otp_data.get("message", ""):
                otp_code = otp_data["message"].split("OTP код: ")[1].split(" ")[0]
                print(f"   🔑 DEV OTP код: {otp_code}")
                
                # Крок 2: Верифікуємо OTP
                verify_response = requests.post(
                    f"{BASE_URL}/api/v1/auth/verify-otp",
                    json={
                        "phone": test_phone,
                        "otp_code": otp_code,
                        "otp_hash": otp_data.get("otp_hash", "")
                    },
                    timeout=10
                )
                
                print(f"   ✅ OTP верифікація: {verify_response.status_code}")
                print(f"   📄 Відповідь: {verify_response.text[:200]}...")
                
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    
                    if verify_data.get("verified"):
                        print("   🎉 OTP верифіковано успішно!")
                        
                        # Крок 3: Логін
                        login_response = requests.post(
                            f"{BASE_URL}/api/v1/auth/login",
                            json={"phone": test_phone},
                            timeout=10
                        )
                        
                        print(f"   🔐 Логін: {login_response.status_code}")
                        
                        if login_response.status_code == 200:
                            login_data = login_response.json()
                            access_token = login_data.get("data", {}).get("access_token")
                            
                            if access_token:
                                print(f"   🎯 Отримано токен: {access_token[:20]}...")
                                
                                # Тепер тестуємо search ендпоінт з реальним токеном
                                print()
                                print("2️⃣ Тест search ендпоінту з реальним токеном:")
                                
                                headers = {"Authorization": f"Bearer {access_token}"}
                                search_response = requests.get(
                                    f"{BASE_URL}/api/v1/search/nannies/complete?limit=5",
                                    headers=headers,
                                    timeout=10
                                )
                                
                                print(f"   📊 Status: {search_response.status_code}")
                                
                                if search_response.status_code == 200:
                                    print("   ✅ SUCCESS! Ендпоінт працює!")
                                    data = search_response.json()
                                    print(f"   📊 Знайдено нянь: {len(data.get('data', []))}")
                                    print(f"   📄 Структура відповіді: {list(data.keys())}")
                                elif search_response.status_code == 500:
                                    print("   ❌ ПОМИЛКА 500 - проблема на сервері!")
                                    print(f"   📄 Повна відповідь: {search_response.text}")
                                else:
                                    print(f"   ⚠️ Неочікуваний статус: {search_response.status_code}")
                                    print(f"   📄 Відповідь: {search_response.text}")
                            else:
                                print("   ❌ Токен не отримано")
                        else:
                            print(f"   ❌ Логін не вдався: {login_response.text}")
                    else:
                        print("   ❌ OTP не верифіковано")
                else:
                    print(f"   ❌ Помилка верифікації: {verify_response.text}")
            else:
                print("   ⚠️ OTP код не знайдено в відповіді (можливо production режим)")
        else:
            print(f"   ❌ Помилка відправки OTP: {otp_response.text}")
            
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print()
    print("3️⃣ Альтернативний тест - перевірка /api/v1/auth/me:")
    
    # Якщо у вас є збережений токен, можете його тут вставити для тестування
    saved_token = None  # Вставте сюди токен якщо є
    
    if saved_token:
        try:
            headers = {"Authorization": f"Bearer {saved_token}"}
            me_response = requests.get(
                f"{BASE_URL}/api/v1/auth/me",
                headers=headers,
                timeout=10
            )
            
            print(f"   📊 /auth/me Status: {me_response.status_code}")
            
            if me_response.status_code == 200:
                print("   ✅ Токен валідний!")
                
                # Тестуємо search з цим токеном
                search_response = requests.get(
                    f"{BASE_URL}/api/v1/search/nannies/complete?limit=5",
                    headers=headers,
                    timeout=10
                )
                
                print(f"   📊 Search Status: {search_response.status_code}")
                if search_response.status_code == 500:
                    print("   ❌ ПОМИЛКА 500 на search ендпоінті!")
                    print(f"   📄 Відповідь: {search_response.text}")
            else:
                print(f"   ❌ Токен невалідний: {me_response.text}")
                
        except Exception as e:
            print(f"   ❌ Помилка: {e}")
    else:
        print("   ⚠️ Немає збереженого токену для тестування")

if __name__ == "__main__":
    test_with_token()
