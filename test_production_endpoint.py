#!/usr/bin/env python3
"""
Тестування ендпоінту /api/v1/search/nannies/complete на продакшені
"""
import requests
import json
import sys

def test_search_endpoint():
    """Тестує ендпоінт пошуку нянь на продакшені"""
    
    # Базовий URL продакшн сервера
    BASE_URL = "https://nany.datavertex.me"
    
    print("🔍 Тестування ендпоінту /api/v1/search/nannies/complete")
    print(f"🌐 Сервер: {BASE_URL}")
    print()
    
    # Спочатку тестуємо без токену
    print("1️⃣ Тест без авторизації:")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/search/nannies/complete?limit=5",
            timeout=10
        )
        print(f"   📊 Status: {response.status_code}")
        print(f"   📄 Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ Очікувано - потрібна авторизація")
        else:
            print("   ⚠️ Неочікуваний статус")
            
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print()
    
    # Тестуємо з фейковим токеном
    print("2️⃣ Тест з фейковим токеном:")
    try:
        headers = {"Authorization": "Bearer fake-token-123"}
        response = requests.get(
            f"{BASE_URL}/api/v1/search/nannies/complete?limit=5",
            headers=headers,
            timeout=10
        )
        print(f"   📊 Status: {response.status_code}")
        print(f"   📄 Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ Очікувано - невалідний токен")
        elif response.status_code == 500:
            print("   ❌ ПОМИЛКА 500 - проблема на сервері!")
            print(f"   📄 Повна відповідь: {response.text}")
        else:
            print(f"   ⚠️ Неочікуваний статус: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print()
    
    # Перевіряємо інші ендпоінти для порівняння
    print("3️⃣ Тест інших ендпоінтів:")
    
    test_endpoints = [
        "/api/v1/search/nannies",
        "/api/v1/search/parents/complete", 
        "/api/v1/simple/my-likes",
        "/docs"  # OpenAPI документація
    ]
    
    for endpoint in test_endpoints:
        try:
            headers = {"Authorization": "Bearer fake-token-123"} if endpoint != "/docs" else {}
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                timeout=10
            )
            print(f"   📡 {endpoint}: {response.status_code}")
            
            if response.status_code == 500:
                print(f"      ❌ ПОМИЛКА 500 на {endpoint}!")
                
        except Exception as e:
            print(f"   ❌ {endpoint}: Помилка - {e}")
    
    print()
    print("4️⃣ Перевірка структури відповіді з документації:")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ Документація доступна")
            print(f"   🔗 Відкрийте: {BASE_URL}/docs")
        else:
            print(f"   ❌ Документація недоступна: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Помилка доступу до документації: {e}")

if __name__ == "__main__":
    test_search_endpoint()
