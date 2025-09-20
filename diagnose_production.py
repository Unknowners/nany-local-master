#!/usr/bin/env python3
"""
Діагностика проблем на продакшн сервері
"""
import requests
import json

def diagnose_production():
    """Діагностує проблеми на продакшені"""
    
    BASE_URL = "https://nany.datavertex.me"
    
    print("🔍 ДІАГНОСТИКА ПРОДАКШН СЕРВЕРА")
    print(f"🌐 URL: {BASE_URL}")
    print("=" * 50)
    
    # 1. Перевірка базових ендпоінтів
    print("\n1️⃣ ПЕРЕВІРКА БАЗОВИХ ЕНДПОІНТІВ:")
    
    basic_endpoints = [
        ("/", "Головна сторінка"),
        ("/docs", "API документація"),
        ("/health", "Health check"),
        ("/api/v1/health", "API health check")
    ]
    
    for endpoint, description in basic_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            status = "✅" if response.status_code < 400 else "❌"
            print(f"   {status} {endpoint} ({description}): {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: ПОМИЛКА - {e}")
    
    # 2. Перевірка auth ендпоінтів
    print("\n2️⃣ ПЕРЕВІРКА AUTH ЕНДПОІНТІВ:")
    
    auth_endpoints = [
        ("/api/v1/auth/send-otp", "POST", {"phone": "+380501234567"}),
        ("/api/v1/auth/me", "GET", None),
    ]
    
    for endpoint, method, body in auth_endpoints:
        try:
            if method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=body, timeout=10)
            else:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            status = "✅" if response.status_code < 500 else "❌"
            print(f"   {status} {method} {endpoint}: {response.status_code}")
            
            if response.status_code >= 500:
                print(f"      🔥 SERVER ERROR: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: ПОМИЛКА - {e}")
    
    # 3. Перевірка search ендпоінтів без авторизації
    print("\n3️⃣ ПЕРЕВІРКА SEARCH ЕНДПОІНТІВ (без авторизації):")
    
    search_endpoints = [
        "/api/v1/search/nannies/complete",
        "/api/v1/search/parents/complete",
        "/api/v1/search/nannies",
        "/api/v1/search/parents"
    ]
    
    for endpoint in search_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}?limit=1", timeout=10)
            
            if response.status_code == 401 or response.status_code == 403:
                print(f"   ✅ {endpoint}: {response.status_code} (очікувано - потрібна авторизація)")
            elif response.status_code >= 500:
                print(f"   ❌ {endpoint}: {response.status_code} - SERVER ERROR!")
                print(f"      🔥 {response.text[:100]}...")
            else:
                print(f"   ⚠️ {endpoint}: {response.status_code} (неочікувано)")
                
        except Exception as e:
            print(f"   ❌ {endpoint}: ПОМИЛКА - {e}")
    
    # 4. Перевірка простих ендпоінтів
    print("\n4️⃣ ПЕРЕВІРКА ПРОСТИХ ЕНДПОІНТІВ:")
    
    simple_endpoints = [
        "/api/v1/simple/my-likes",
        "/api/v1/counters/dashboard/complete"
    ]
    
    for endpoint in simple_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 401 or response.status_code == 403:
                print(f"   ✅ {endpoint}: {response.status_code} (очікувано)")
            elif response.status_code >= 500:
                print(f"   ❌ {endpoint}: {response.status_code} - SERVER ERROR!")
            else:
                print(f"   ⚠️ {endpoint}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {endpoint}: ПОМИЛКА - {e}")
    
    # 5. Перевірка OpenAPI схеми
    print("\n5️⃣ АНАЛІЗ API СХЕМИ:")
    
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        
        if response.status_code == 200:
            print("   ✅ OpenAPI схема доступна")
            
            openapi_data = response.json()
            paths = openapi_data.get("paths", {})
            
            # Перевіряємо чи є наші ендпоінти в схемі
            target_paths = [
                "/api/v1/search/nannies/complete",
                "/api/v1/search/parents/complete",
                "/api/v1/auth/send-otp",
                "/api/v1/auth/verify-otp"
            ]
            
            print("   📋 Перевірка ендпоінтів в схемі:")
            for path in target_paths:
                if path in paths:
                    print(f"      ✅ {path}")
                else:
                    print(f"      ❌ {path} - ВІДСУТНІЙ!")
                    
        else:
            print(f"   ❌ OpenAPI схема недоступна: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Помилка отримання схеми: {e}")
    
    print("\n" + "=" * 50)
    print("📊 ВИСНОВКИ:")
    print("1. Якщо всі ендпоінти повертають 500 - проблема з базою даних або сервером")
    print("2. Якщо тільки деякі ендпоінти 500 - проблема в конкретному коді")
    print("3. Якщо 401/403 - сервер працює, проблема з авторизацією")
    print("4. Перевірте логи сервера для детальної інформації")

if __name__ == "__main__":
    diagnose_production()
