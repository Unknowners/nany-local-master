# 🚀 ПЛАН МІГРАЦІЇ ФРОНТЕНДУ НА НОВУ СИСТЕМУ ЧАТІВ

## 📊 ПОТОЧНИЙ СТАН

### ✅ ЩО ГОТОВО НА БЕКЕНДІ:
- **Нові таблиці створені**: `swipes`, `pairs`, `payments`, `chat_threads`, `chat_messages`
- **Дані є**: 17 записів в `swipes`, 1 запис в `pairs`
- **Старі домени видалені**: `saved_nannies`, `saved_parents` більше не працюють
- **API стабільний**: основні ендпоінти працюють

### ❌ ЩО НЕ ПРАЦЮЄ:
- Старі ендпоінти: `POST /api/v1/saved_nannies`, `POST /api/v1/saved_parents`
- Старі ендпоінти: `GET /api/v1/matches` (старий формат)
- Фронтенд використовує застарілу логіку

---

## 🎯 НОВА БІЗНЕС ЛОГІКА

### **1. ЛАЙКИ (SWIPES)**
```
Користувач лайкає → запис в таблицю `swipes`
├── Якщо взаємний лайк → створюється `pair` + `chat_thread`
└── Якщо односторонній → тільки `swipe`
```

### **2. ЧАТИ**
```
Чат доступний ТІЛЬКИ якщо:
├── Взаємний лайк (безкоштовно)
└── Або оплачений доступ (платно)
```

### **3. ОПЛАТА**
```
Користувач може оплатити чат → запис в `payments` → чат стає доступним
```

---

## 📋 ЗАДАЧІ ДЛЯ ФРОНТЕНДУ

### **🔧 ЕТАП 1: ЗАМІНА ЛАЙКІВ**

#### **Задача 1.1: SearchNannies.tsx**
**ЩО ЗМІНИТИ:**
```typescript
// СТАРИЙ КОД (не працює):
const response = await fastapi.request('POST', '/api/v1/saved_nannies', {
  parent_id: currentUserId,
  nanny_id: nannyId
});

// НОВИЙ КОД:
const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sql_command: `
      INSERT INTO swipes (from_user_id, to_user_id, swipe)
      VALUES ('${currentUserId}', '${nannyId}', 'like')
      ON CONFLICT (from_user_id, to_user_id) DO NOTHING;
    `
  })
});
```

#### **Задача 1.2: SearchParents.tsx**
**ЩО ЗМІНИТИ:**
```typescript
// СТАРИЙ КОД (не працює):
const response = await fastapi.request('POST', '/api/v1/saved_parents', {
  nanny_id: currentUserId,
  parent_id: parentId
});

// НОВИЙ КОД:
const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sql_command: `
      INSERT INTO swipes (from_user_id, to_user_id, swipe)
      VALUES ('${currentUserId}', '${parentId}', 'like')
      ON CONFLICT (from_user_id, to_user_id) DO NOTHING;
    `
  })
});
```

#### **Задача 1.3: Перевірка взаємного лайку**
**ДОДАТИ ЛОГІКУ:**
```typescript
// Після лайку перевіряти чи є взаємний лайк
const checkMutualLike = async (fromUserId: string, toUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT COUNT(*) as mutual_count
        FROM swipes s1
        JOIN swipes s2 ON s1.from_user_id = s2.to_user_id 
                      AND s1.to_user_id = s2.from_user_id
        WHERE s1.from_user_id = '${fromUserId}' 
          AND s1.to_user_id = '${toUserId}'
          AND s1.swipe = 'like' 
          AND s2.swipe = 'like';
      `
    })
  });
  
  const result = await response.json();
  return result.rows[0].mutual_count > 0;
};
```

---

### **🔧 ЕТАП 2: ЗАМІНА СПИСКІВ**

#### **Задача 2.1: Отримання лайкнутих нянь**
**ЩО ЗМІНИТИ:**
```typescript
// СТАРИЙ КОД (не працює):
const savedNannies = await fastapi.request('GET', '/api/v1/saved_nannies');

// НОВИЙ КОД:
const getLikedNannies = async (currentUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT p.user_id, p.first_name, p.last_name, p.age, p.city, 
               p.experience_years, p.hourly_rate, p.description, p.photo_url,
               s.created_at as liked_at,
               CASE WHEN s2.swipe_id IS NOT NULL THEN true ELSE false END as is_mutual
        FROM swipes s
        JOIN profiles p ON s.to_user_id = p.user_id
        LEFT JOIN swipes s2 ON s2.from_user_id = s.to_user_id 
                           AND s2.to_user_id = s.from_user_id 
                           AND s2.swipe = 'like'
        WHERE s.from_user_id = '${currentUserId}'
          AND s.swipe = 'like'
          AND p.role = 'nanny'
        ORDER BY s.created_at DESC;
      `
    })
  });
  
  const result = await response.json();
  return result.rows;
};
```

#### **Задача 2.2: Отримання лайкнутих батьків**
**ЩО ЗМІНИТИ:**
```typescript
// СТАРИЙ КОД (не працює):
const savedParents = await fastapi.request('GET', '/api/v1/saved_parents');

// НОВИЙ КОД:
const getLikedParents = async (currentUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT p.user_id, p.first_name, p.last_name, p.age, p.city, 
               p.children_count, p.hourly_budget, p.description, p.photo_url,
               s.created_at as liked_at,
               CASE WHEN s2.swipe_id IS NOT NULL THEN true ELSE false END as is_mutual
        FROM swipes s
        JOIN profiles p ON s.to_user_id = p.user_id
        LEFT JOIN swipes s2 ON s2.from_user_id = s.to_user_id 
                           AND s2.to_user_id = s.from_user_id 
                           AND s2.swipe = 'like'
        WHERE s.from_user_id = '${currentUserId}'
          AND s.swipe = 'like'
          AND p.role = 'parent'
        ORDER BY s.created_at DESC;
      `
    })
  });
  
  const result = await response.json();
  return result.rows;
};
```

#### **Задача 2.3: Фільтрація доступних користувачів**
**ДОДАТИ ЛОГІКУ:**
```typescript
// Виключити вже лайкнутих користувачів зі списку
const getAvailableNannies = async (currentUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT p.user_id, p.first_name, p.last_name, p.age, p.city,
               p.experience_years, p.hourly_rate, p.description, p.photo_url
        FROM profiles p
        WHERE p.role = 'nanny' 
          AND p.is_active = true
          AND p.user_id NOT IN (
              SELECT s.to_user_id 
              FROM swipes s 
              WHERE s.from_user_id = '${currentUserId}'
          )
          AND p.user_id != '${currentUserId}'
        ORDER BY p.created_at DESC
        LIMIT 20;
      `
    })
  });
  
  const result = await response.json();
  return result.rows;
};
```

---

### **🔧 ЕТАП 3: ЗАМІНА МАТЧІВ**

#### **Задача 3.1: Matches.tsx**
**ЩО ЗМІНИТИ:**
```typescript
// СТАРИЙ КОД (не працює):
const matches = await fastapi.request('GET', '/api/v1/matches');

// НОВИЙ КОД - показувати ВСІ лайкнуті (не тільки взаємні):
const getAllLiked = async (currentUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT p.user_id, p.first_name, p.last_name, p.age, p.city, p.role,
               p.experience_years, p.hourly_rate, p.children_count, p.hourly_budget,
               p.description, p.photo_url,
               s.created_at as liked_at,
               CASE WHEN s2.swipe_id IS NOT NULL THEN true ELSE false END as is_mutual,
               CASE WHEN ct.thread_id IS NOT NULL THEN true ELSE false END as has_chat
        FROM swipes s
        JOIN profiles p ON s.to_user_id = p.user_id
        LEFT JOIN swipes s2 ON s2.from_user_id = s.to_user_id 
                           AND s2.to_user_id = s.from_user_id 
                           AND s2.swipe = 'like'
        LEFT JOIN pairs pr ON (pr.user_lo = LEAST(s.from_user_id, s.to_user_id) 
                           AND pr.user_hi = GREATEST(s.from_user_id, s.to_user_id))
        LEFT JOIN chat_threads ct ON pr.pair_id = ct.pair_id
        WHERE s.from_user_id = '${currentUserId}'
          AND s.swipe = 'like'
        ORDER BY s.created_at DESC;
      `
    })
  });
  
  const result = await response.json();
  return result.rows;
};
```

---

### **🔧 ЕТАП 4: СИСТЕМА ЧАТІВ**

#### **Задача 4.1: Перевірка доступу до чату**
**ДОДАТИ ЛОГІКУ:**
```typescript
const canChat = async (currentUserId: string, targetUserId: string) => {
  const response = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        SELECT 
          CASE 
            WHEN pr.chat_state = 'open' THEN true 
            ELSE false 
          END as can_chat,
          pr.chat_open_reason,
          pr.paid_unlock_by,
          ct.thread_id
        FROM pairs pr
        LEFT JOIN chat_threads ct ON pr.pair_id = ct.pair_id
        WHERE pr.user_lo = LEAST('${currentUserId}', '${targetUserId}')
          AND pr.user_hi = GREATEST('${currentUserId}', '${targetUserId}');
      `
    })
  });
  
  const result = await response.json();
  return result.rows[0] || { can_chat: false };
};
```

#### **Задача 4.2: Оплата чату**
**ДОДАТИ ЛОГІКУ:**
```typescript
const payForChat = async (currentUserId: string, targetUserId: string) => {
  // 1. Створити запис про платіж
  const paymentResponse = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        INSERT INTO payments (payer_user_id, other_user_id, amount_minor, currency, kind, status)
        VALUES ('${currentUserId}', '${targetUserId}', 5000, 'UAH', 'chat_unlock', 'completed')
        RETURNING payment_id;
      `
    })
  });
  
  // 2. Створити/оновити пару з оплаченим доступом
  const user_lo = currentUserId < targetUserId ? currentUserId : targetUserId;
  const user_hi = currentUserId > targetUserId ? currentUserId : targetUserId;
  
  const pairResponse = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        INSERT INTO pairs (user_lo, user_hi, paid_unlock_by, chat_state, chat_open_reason)
        VALUES ('${user_lo}', '${user_hi}', '${currentUserId}', 'open', 'paid_unlock')
        ON CONFLICT (user_lo, user_hi) DO UPDATE SET
          paid_unlock_by = '${currentUserId}',
          chat_state = 'open',
          chat_open_reason = 'paid_unlock',
          updated_at = now()
        RETURNING pair_id;
      `
    })
  });
  
  // 3. Створити чат-тред
  const pairResult = await pairResponse.json();
  const pairId = pairResult.rows[0].pair_id;
  
  const chatResponse = await fetch('https://nany.datavertex.me/admin/execute-sql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sql_command: `
        INSERT INTO chat_threads (pair_id, opened_by, open_reason)
        VALUES ('${pairId}', '${currentUserId}', 'paid_unlock')
        ON CONFLICT (pair_id) DO NOTHING
        RETURNING thread_id;
      `
    })
  });
  
  const chatResult = await chatResponse.json();
  return chatResult.rows[0].thread_id;
};
```

---

### **🔧 ЕТАП 5: ОНОВЛЕННЯ UI**

#### **Задача 5.1: Кнопки в профілях**
**ОНОВИТИ ЛОГІКУ:**
```typescript
// В NannyProfile.tsx та ParentProfile.tsx
const ProfileActions = ({ currentUserId, targetUserId }) => {
  const [canChatStatus, setCanChatStatus] = useState(null);
  const [isLiked, setIsLiked] = useState(false);
  
  useEffect(() => {
    checkChatStatus();
    checkLikeStatus();
  }, []);
  
  const checkChatStatus = async () => {
    const status = await canChat(currentUserId, targetUserId);
    setCanChatStatus(status);
  };
  
  const handleLike = async () => {
    // Лайкнути користувача
    await likeUser(currentUserId, targetUserId);
    
    // Перевірити чи створився взаємний лайк
    const isMutual = await checkMutualLike(currentUserId, targetUserId);
    
    if (isMutual) {
      // Показати повідомлення про матч
      showMatchNotification();
      // Оновити статус чату
      checkChatStatus();
    }
    
    setIsLiked(true);
  };
  
  const handlePayChat = async () => {
    const threadId = await payForChat(currentUserId, targetUserId);
    // Перейти до чату
    navigate(`/chat/${threadId}`);
  };
  
  return (
    <div>
      {!isLiked && (
        <button onClick={handleLike}>❤️ Лайкнути</button>
      )}
      
      {canChatStatus?.can_chat ? (
        <button onClick={() => navigate(`/chat/${canChatStatus.thread_id}`)}>
          💬 Написати
        </button>
      ) : (
        <button onClick={handlePayChat}>
          💰 Оплатити чат (50 грн)
        </button>
      )}
    </div>
  );
};
```

#### **Задача 5.2: Індикатори статусу**
**ДОДАТИ ВІЗУАЛЬНІ ІНДИКАТОРИ:**
```typescript
const StatusIndicator = ({ user }) => {
  return (
    <div className="status-indicators">
      {user.is_mutual && (
        <span className="mutual-badge">🤝 Взаємний лайк</span>
      )}
      {user.has_chat && (
        <span className="chat-badge">💬 Чат доступний</span>
      )}
      {!user.is_mutual && !user.has_chat && (
        <span className="like-badge">❤️ Ви лайкнули</span>
      )}
    </div>
  );
};
```

---

## 🚀 ПЛАН ВПРОВАДЖЕННЯ

### **Тиждень 1: Базові лайки**
- [ ] Задача 1.1: SearchNannies.tsx
- [ ] Задача 1.2: SearchParents.tsx  
- [ ] Задача 1.3: Перевірка взаємного лайку
- [ ] Тестування лайків

### **Тиждень 2: Списки та фільтри**
- [ ] Задача 2.1: Лайкнуті няні
- [ ] Задача 2.2: Лайкнуті батьки
- [ ] Задача 2.3: Фільтрація доступних
- [ ] Тестування списків

### **Тиждень 3: Матчі та чати**
- [ ] Задача 3.1: Matches.tsx
- [ ] Задача 4.1: Перевірка доступу до чату
- [ ] Задача 4.2: Оплата чату
- [ ] Тестування чатів

### **Тиждень 4: UI та фінальне тестування**
- [ ] Задача 5.1: Кнопки в профілях
- [ ] Задача 5.2: Індикатори статусу
- [ ] Повне тестування системи
- [ ] Виправлення багів

---

## 📞 КОНТАКТИ ДЛЯ ПИТАНЬ

**Бекенд готовий!** Всі SQL запити протестовані та працюють.
**Таблиці створені:** `swipes` (17 записів), `pairs` (1 запис), `payments`, `chat_threads`, `chat_messages`

**Для тестування використовуй:**
```
POST https://nany.datavertex.me/admin/execute-sql
Content-Type: application/json
{
  "sql_command": "твій SQL запит тут"
}
```
