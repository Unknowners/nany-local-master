# 🔧 Виправлення CORS на продакшні

## 🎯 Проблема
Фронтенд на `https://www.proturbota.com` не може звернутися до API на `https://nany.datavertex.me` через CORS помилки:

```
Access to fetch at 'https://nany.datavertex.me/api/v1/profiles' from origin 'https://www.proturbota.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 🔧 Рішення

### 1. Оновлено Nginx конфігурацію
**Файл**: `nginx/nginx.conf`

**Додано CORS заголовки**:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH`
- `Access-Control-Allow-Headers: DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,Accept,Origin,X-Forwarded-For`
- `Access-Control-Allow-Credentials: true`

**Додано обробку preflight запитів**:
- OPTIONS запити повертають статус 204 з CORS заголовками
- Встановлено `Access-Control-Max-Age: 1728000` (20 днів)

## 🚀 Деплой на продакшн

### Варіант 1: Через Docker Compose
```bash
# Перезапуск Nginx контейнера
docker-compose restart nginx

# Або повний перезапуск
docker-compose down
docker-compose up -d
```

### Варіант 2: Через Makefile
```bash
# Якщо є команда для рестарту nginx
make prod-restart

# Або повний рестарт
make prod-down
make prod-up
```

### Варіант 3: Через Dockploy (якщо використовується)
1. Оновити конфігурацію в Dockploy
2. Перезапустити сервіс через веб-інтерфейс

## ✅ Перевірка після деплою

### 1. Тест CORS preflight
```bash
curl -X OPTIONS \
  -H "Origin: https://www.proturbota.com" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization" \
  -v https://nany.datavertex.me/api/v1/profiles
```

**Очікуваний результат**:
```
< HTTP/1.1 204 No Content
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
< Access-Control-Allow-Headers: DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,Accept,Origin,X-Forwarded-For
< Access-Control-Allow-Credentials: true
```

### 2. Тест реального API запиту
```bash
curl -X GET \
  -H "Origin: https://www.proturbota.com" \
  -H "Content-Type: application/json" \
  -v https://nany.datavertex.me/api/v1/onboarding_configs?target_role=nanny
```

**Очікуваний результат**:
- Статус 200 OK
- JSON відповідь з конфігураціями
- CORS заголовки присутні

## 🔍 Діагностика

### Якщо CORS все ще не працює:

1. **Перевірити логи Nginx**:
```bash
docker-compose logs nginx | tail -20
```

2. **Перевірити конфігурацію Nginx**:
```bash
docker-compose exec nginx nginx -t
```

3. **Перевірити, чи застосувалася конфігурація**:
```bash
docker-compose exec nginx cat /etc/nginx/nginx.conf | grep -A 10 "CORS"
```

## 📝 Додаткові налаштування

### Якщо потрібно обмежити домени (більш безпечно):
Замініть `'*'` на конкретні домени:
```nginx
add_header 'Access-Control-Allow-Origin' 'https://www.proturbota.com' always;
```

### Для кількох доменів:
```nginx
# В location блоці додати логіку
set $cors_origin "";
if ($http_origin ~ '^https://(www\.)?proturbota\.com$') {
    set $cors_origin $http_origin;
}
if ($http_origin ~ '^https://(www\.)?nany\.datavertex\.me$') {
    set $cors_origin $http_origin;
}
add_header 'Access-Control-Allow-Origin' $cors_origin always;
```

## 🎉 Результат

Після застосування виправлень:
- ✅ Фронтенд зможе робити запити до API
- ✅ Авторизація працюватиме
- ✅ Онбординг конфігурації завантажуватимуться
- ✅ Довідники будуть доступні

## 🛡️ Безпека

- CORS налаштовано на `*` для максимальної сумісності
- При потребі можна обмежити до конкретних доменів
- Credentials дозволені для передачі токенів авторизації
- Preflight запити обробляються коректно