# 💕 СИСТЕМА МАТЧІВ, ЧАТІВ ТА ЛІЧИЛЬНИКІВ - ДОКУМЕНТАЦІЯ ДЛЯ ФРОНТЕНДУ

## 🎯 ЗАГАЛЬНИЙ ОПИС

Нова система включає:
- **Матчі** - взаємні лайки між користувачами
- **Чати** - повідомлення між користувачами після матчу
- **Платежі** - розблокування чатів через оплату
- **Лічильники** - статистика для дашборду
- **Збереження** - збереження/видалення профілів

## 🔄 СИСТЕМА СВАЙПІВ ТА МАТЧІВ

### 📱 Свайпи
```http
POST /api/v1/swipes
Authorization: Bearer {token}
Content-Type: application/json

{
  "target_user_id": "uuid-target-user",
  "swipe_type": "like"  // або "pass"
}
```

**Відповідь:**
```json
{
  "success": true,
  "swipe_id": "uuid-swipe-id",
  "match_created": true,  // true якщо створено матч
  "pair_id": "uuid-pair-id"  // якщо створено матч
}
```

### 💕 Отримання матчів
```http
GET /api/v1/matches
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "matches": [
    {
      "pair_id": "uuid-pair-id",
      "other_user_id": "uuid-other-user",
      "other_user_name": "Ім'я користувача",
      "other_user_photo": "url-to-photo",
      "matched_at": "2024-01-01T12:00:00Z",
      "chat_status": "locked",  // "locked", "unlocked", "active"
      "last_message": "Останнє повідомлення...",
      "last_message_at": "2024-01-01T12:30:00Z",
      "unread_count": 3
    }
  ]
}
```

## 💬 СИСТЕМА ЧАТІВ

### 📋 Отримання списку чатів
```http
GET /api/v1/chats
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "chats": [
    {
      "thread_id": "uuid-thread-id",
      "pair_id": "uuid-pair-id",
      "other_user_id": "uuid-other-user",
      "other_user_name": "Ім'я користувача",
      "other_user_photo": "url-to-photo",
      "status": "active",  // "locked", "active"
      "last_message": "Останнє повідомлення...",
      "last_message_at": "2024-01-01T12:30:00Z",
      "unread_count": 3,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### 💌 Отримання повідомлень чату
```http
GET /api/v1/chats/{thread_id}/messages?limit=50&offset=0
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "messages": [
    {
      "message_id": "uuid-message-id",
      "sender_user_id": "uuid-sender",
      "content": "Текст повідомлення",
      "sent_at": "2024-01-01T12:30:00Z",
      "is_read": true
    }
  ],
  "has_more": false
}
```

### 📤 Відправка повідомлення
```http
POST /api/v1/chats/{thread_id}/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Текст повідомлення"
}
```

**Відповідь:**
```json
{
  "success": true,
  "message": {
    "message_id": "uuid-message-id",
    "sender_user_id": "uuid-sender",
    "content": "Текст повідомлення",
    "sent_at": "2024-01-01T12:30:00Z",
    "is_read": false
  }
}
```

### ✅ Позначення повідомлень як прочитаних
```http
POST /api/v1/chats/{thread_id}/mark-read
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "success": true,
  "message": "Повідомлення позначено як прочитані"
}
```

### 📊 Деталі чату
```http
GET /api/v1/chats/{thread_id}/details
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "thread_id": "uuid-thread-id",
  "other_user": {
    "user_id": "uuid-user",
    "name": "Ім'я користувача",
    "photo": "url-to-photo",
    "role": "nanny"
  },
  "status": "active",
  "created_at": "2024-01-01T12:00:00Z",
  "total_messages": 15,
  "unread_count": 3
}
```

## 💳 СИСТЕМА ПЛАТЕЖІВ

### 💰 Створення платежу для розблокування чату
```http
POST /api/v1/payments/chat-unlock
Authorization: Bearer {token}
Content-Type: application/json

{
  "other_user_id": "uuid-other-user"
}
```

**Відповідь:**
```json
{
  "payment_id": "uuid-payment-id",
  "amount_minor": 5000,  // 50.00 грн в копійках
  "currency": "UAH",
  "status": "pending",
  "external_id": "external-payment-id",
  "expires_at": "2024-01-01T13:00:00Z"
}
```

### ✅ Завершення платежу (фейкове для тестування)
```http
POST /api/v1/payments/{payment_id}/fake-complete
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "success": true,
  "payment": {
    "payment_id": "uuid-payment-id",
    "status": "completed",
    "completed_at": "2024-01-01T12:45:00Z"
  },
  "chat_unlocked": true,
  "thread_id": "uuid-thread-id"
}
```

### 📋 Історія платежів користувача
```http
GET /api/v1/payments/user
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "payments": [
    {
      "payment_id": "uuid-payment-id",
      "other_user_id": "uuid-other-user",
      "amount_minor": 5000,
      "currency": "UAH",
      "kind": "chat_unlock",
      "status": "completed",
      "created_at": "2024-01-01T12:30:00Z",
      "completed_at": "2024-01-01T12:45:00Z"
    }
  ]
}
```

## 📊 ОПТИМІЗОВАНІ ЛІЧИЛЬНИКИ

### 🎯 Лічильники дашборду
```http
GET /api/v1/counters/dashboard/complete?exclude_saved=true
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "recommended": 25,      // Рекомендовані профілі
  "matches": 8,          // Кількість матчів
  "messages": 12,        // Непрочитані повідомлення
  "mutual_matches": 3,   // Взаємні матчі
  "new_profiles": 5,     // Нові профілі за тиждень
  "total_available": 150 // Загальна кількість доступних профілів
}
```

## 🔍 ОПТИМІЗОВАНИЙ ПОШУК

### 👩‍🍼 Пошук нянь з повними даними
```http
GET /api/v1/search/nannies/complete?limit=20&offset=0&exclude_saved=true
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "data": [
    {
      "id": "uuid-nanny-id",
      "user_id": "uuid-user-id",
      "profile": {
        "first_name": "Марія",
        "last_name": "Іванова",
        "location": "Київ",
        "onboarding_completed": true
      },
      "photos": [
        {
          "id": "uuid-photo-id",
          "file_url": "https://storage.url/photo.jpg",
          "is_primary": true
        }
      ],
      "services": [
        {
          "service_type": "babysitting",
          "hourly_rate": 150,
          "currency": "UAH"
        }
      ],
      "skills": ["cooking", "first_aid"],
      "languages": ["ukrainian", "english"],
      "education": [
        {
          "degree": "Педагогічна освіта",
          "institution": "КНУ"
        }
      ],
      "age_experience": {
        "min_age": 1,
        "max_age": 10,
        "years_experience": 5
      },
      "rating": {
        "average_rating": 4.8,
        "total_reviews": 15
      },
      "is_saved": false
    }
  ],
  "total": 150,
  "has_more": true
}
```

### 👨‍👩‍👧‍👦 Пошук батьків з повними даними
```http
GET /api/v1/search/parents/complete?limit=20&offset=0&exclude_saved=true
Authorization: Bearer {token}
```

**Відповідь:**
```json
{
  "data": [
    {
      "id": "uuid-parent-id",
      "user_id": "uuid-user-id",
      "profile": {
        "first_name": "Олександр",
        "last_name": "Петров",
        "location": "Львів"
      },
      "photos": [
        {
          "id": "uuid-photo-id",
          "file_url": "https://storage.url/photo.jpg",
          "is_primary": true
        }
      ],
      "children": [
        {
          "age": 5,
          "gender": "boy",
          "special_needs": false
        }
      ],
      "requirements": [
        {
          "requirement_type": "experience",
          "value": "3+ years"
        }
      ],
      "rating": {
        "average_rating": 4.5,
        "total_reviews": 8
      },
      "is_saved": false
    }
  ],
  "total": 85,
  "has_more": true
}
```

## 💾 СИСТЕМА ЗБЕРЕЖЕННЯ

### 🔄 Універсальне збереження/видалення
```http
POST /api/v1/saved/toggle
Authorization: Bearer {token}
Content-Type: application/json

{
  "target_id": "uuid-target-user",
  "target_type": "nanny"  // або "parent"
}
```

**Відповідь:**
```json
{
  "success": true,
  "action": "added",  // "added" або "removed"
  "message": "Профіль додано до збережених"
}
```

## 📱 ПРИКЛАДИ ВИКОРИСТАННЯ НА ФРОНТЕНДІ

### 🎯 1. Компонент дашборду з лічильниками
```typescript
import { useEffect, useState } from 'react';
import { fastapi } from '@/integrations/fastapi/fastapi-client';

interface DashboardCounters {
  recommended: number;
  matches: number;
  messages: number;
  mutual_matches: number;
  new_profiles: number;
  total_available: number;
}

const Dashboard = () => {
  const [counters, setCounters] = useState<DashboardCounters | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadCounters = async () => {
      try {
        const response = await fastapi.request(
          'GET', 
          '/api/v1/counters/dashboard/complete?exclude_saved=true'
        );
        setCounters(response);
      } catch (error) {
        console.error('Помилка завантаження лічильників:', error);
      } finally {
        setLoading(false);
      }
    };

    loadCounters();
  }, []);

  if (loading) return <div>Завантаження...</div>;

  return (
    <div className="dashboard">
      <div className="counters-grid">
        <div className="counter-card">
          <h3>Рекомендовані</h3>
          <span className="count">{counters?.recommended || 0}</span>
        </div>
        <div className="counter-card">
          <h3>Матчі</h3>
          <span className="count">{counters?.matches || 0}</span>
        </div>
        <div className="counter-card">
          <h3>Повідомлення</h3>
          <span className="count">{counters?.messages || 0}</span>
        </div>
      </div>
    </div>
  );
};
```

### 💕 2. Компонент списку матчів
```typescript
import { useEffect, useState } from 'react';
import { fastapi } from '@/integrations/fastapi/fastapi-client';

interface Match {
  pair_id: string;
  other_user_id: string;
  other_user_name: string;
  other_user_photo: string;
  matched_at: string;
  chat_status: 'locked' | 'unlocked' | 'active';
  last_message?: string;
  last_message_at?: string;
  unread_count: number;
}

const MatchesList = () => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const response = await fastapi.request('GET', '/api/v1/matches');
        setMatches(response.matches);
      } catch (error) {
        console.error('Помилка завантаження матчів:', error);
      } finally {
        setLoading(false);
      }
    };

    loadMatches();
  }, []);

  const handleChatUnlock = async (otherUserId: string) => {
    try {
      // Створюємо платіж
      const paymentResponse = await fastapi.request(
        'POST', 
        '/api/v1/payments/chat-unlock',
        { other_user_id: otherUserId }
      );

      // Фейкове завершення платежу для тестування
      const completeResponse = await fastapi.request(
        'POST', 
        `/api/v1/payments/${paymentResponse.payment_id}/fake-complete`
      );

      if (completeResponse.chat_unlocked) {
        // Оновлюємо список матчів
        loadMatches();
        // Переходимо до чату
        window.location.href = `/chat/${completeResponse.thread_id}`;
      }
    } catch (error) {
      console.error('Помилка розблокування чату:', error);
    }
  };

  return (
    <div className="matches-list">
      {matches.map((match) => (
        <div key={match.pair_id} className="match-card">
          <img src={match.other_user_photo} alt={match.other_user_name} />
          <div className="match-info">
            <h3>{match.other_user_name}</h3>
            {match.last_message && (
              <p className="last-message">{match.last_message}</p>
            )}
            {match.unread_count > 0 && (
              <span className="unread-badge">{match.unread_count}</span>
            )}
          </div>
          <div className="match-actions">
            {match.chat_status === 'locked' ? (
              <button 
                onClick={() => handleChatUnlock(match.other_user_id)}
                className="unlock-chat-btn"
              >
                Розблокувати чат (50 грн)
              </button>
            ) : (
              <button 
                onClick={() => window.location.href = `/chat/${match.pair_id}`}
                className="open-chat-btn"
              >
                Відкрити чат
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
```

### 💬 3. Компонент чату
```typescript
import { useEffect, useState, useRef } from 'react';
import { fastapi } from '@/integrations/fastapi/fastapi-client';

interface Message {
  message_id: string;
  sender_user_id: string;
  content: string;
  sent_at: string;
  is_read: boolean;
}

interface ChatProps {
  threadId: string;
  currentUserId: string;
}

const Chat = ({ threadId, currentUserId }: ChatProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadMessages();
    markMessagesAsRead();
  }, [threadId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadMessages = async () => {
    try {
      const response = await fastapi.request(
        'GET', 
        `/api/v1/chats/${threadId}/messages?limit=100`
      );
      setMessages(response.messages.reverse()); // Реверсуємо для правильного порядку
    } catch (error) {
      console.error('Помилка завантаження повідомлень:', error);
    } finally {
      setLoading(false);
    }
  };

  const markMessagesAsRead = async () => {
    try {
      await fastapi.request('POST', `/api/v1/chats/${threadId}/mark-read`);
    } catch (error) {
      console.error('Помилка позначення як прочитані:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      const response = await fastapi.request(
        'POST',
        `/api/v1/chats/${threadId}/messages`,
        { content: newMessage }
      );

      setMessages(prev => [...prev, response.message]);
      setNewMessage('');
    } catch (error) {
      console.error('Помилка відправки повідомлення:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (loading) return <div>Завантаження чату...</div>;

  return (
    <div className="chat-container">
      <div className="messages-list">
        {messages.map((message) => (
          <div
            key={message.message_id}
            className={`message ${
              message.sender_user_id === currentUserId ? 'own' : 'other'
            }`}
          >
            <div className="message-content">{message.content}</div>
            <div className="message-time">
              {new Date(message.sent_at).toLocaleTimeString()}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="message-input">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Введіть повідомлення..."
        />
        <button onClick={sendMessage}>Відправити</button>
      </div>
    </div>
  );
};
```

### 🔍 4. Компонент пошуку з свайпами
```typescript
import { useEffect, useState } from 'react';
import { fastapi } from '@/integrations/fastapi/fastapi-client';

interface Profile {
  id: string;
  user_id: string;
  profile: {
    first_name: string;
    last_name: string;
    location: string;
  };
  photos: Array<{
    file_url: string;
    is_primary: boolean;
  }>;
  is_saved: boolean;
}

const SearchNannies = () => {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      const response = await fastapi.request(
        'GET', 
        '/api/v1/search/nannies/complete?limit=20&exclude_saved=true'
      );
      setProfiles(response.data);
    } catch (error) {
      console.error('Помилка завантаження профілів:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSwipe = async (swipeType: 'like' | 'pass') => {
    const currentProfile = profiles[currentIndex];
    if (!currentProfile) return;

    try {
      const response = await fastapi.request(
        'POST',
        '/api/v1/swipes',
        {
          target_user_id: currentProfile.user_id,
          swipe_type: swipeType
        }
      );

      if (response.match_created) {
        alert('Новий матч! 💕');
        // Можна показати модальне вікно або перенаправити до матчів
      }

      // Переходимо до наступного профілю
      setCurrentIndex(prev => prev + 1);
      
      // Якщо профілі закінчилися, завантажуємо нові
      if (currentIndex >= profiles.length - 3) {
        loadProfiles();
      }
    } catch (error) {
      console.error('Помилка свайпу:', error);
    }
  };

  const handleSaveToggle = async () => {
    const currentProfile = profiles[currentIndex];
    if (!currentProfile) return;

    try {
      const response = await fastapi.request(
        'POST',
        '/api/v1/saved/toggle',
        {
          target_id: currentProfile.user_id,
          target_type: 'nanny'
        }
      );

      // Оновлюємо стан збереження
      setProfiles(prev => prev.map((profile, index) => 
        index === currentIndex 
          ? { ...profile, is_saved: response.action === 'added' }
          : profile
      ));
    } catch (error) {
      console.error('Помилка збереження:', error);
    }
  };

  if (loading) return <div>Завантаження...</div>;

  const currentProfile = profiles[currentIndex];
  if (!currentProfile) return <div>Немає більше профілів</div>;

  return (
    <div className="search-container">
      <div className="profile-card">
        <img 
          src={currentProfile.photos.find(p => p.is_primary)?.file_url} 
          alt={`${currentProfile.profile.first_name} ${currentProfile.profile.last_name}`}
        />
        <div className="profile-info">
          <h2>{currentProfile.profile.first_name} {currentProfile.profile.last_name}</h2>
          <p>{currentProfile.profile.location}</p>
        </div>
      </div>
      
      <div className="action-buttons">
        <button 
          onClick={() => handleSwipe('pass')}
          className="pass-btn"
        >
          ❌ Пропустити
        </button>
        
        <button 
          onClick={handleSaveToggle}
          className={`save-btn ${currentProfile.is_saved ? 'saved' : ''}`}
        >
          {currentProfile.is_saved ? '💙 Збережено' : '🤍 Зберегти'}
        </button>
        
        <button 
          onClick={() => handleSwipe('like')}
          className="like-btn"
        >
          💚 Подобається
        </button>
      </div>
    </div>
  );
};
```

## 🔄 РЕАЛТАЙМ ОНОВЛЕННЯ

### WebSocket підключення (рекомендовано)
```typescript
const useRealtimeUpdates = (userId: string) => {
  useEffect(() => {
    // Підключення до WebSocket для реалтайм оновлень
    const ws = new WebSocket(`wss://nany.datavertex.me/ws/${userId}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'new_message':
          // Оновити список чатів
          updateChatsList();
          break;
        case 'new_match':
          // Показати сповіщення про новий матч
          showMatchNotification(data.match);
          break;
        case 'payment_completed':
          // Оновити статус чату
          updateChatStatus(data.thread_id);
          break;
      }
    };

    return () => ws.close();
  }, [userId]);
};
```

### Polling (альтернатива)
```typescript
const usePollingUpdates = () => {
  useEffect(() => {
    const interval = setInterval(async () => {
      // Оновлюємо лічильники кожні 30 секунд
      await updateCounters();
      // Оновлюємо список чатів кожні 10 секунд
      await updateChats();
    }, 30000);

    return () => clearInterval(interval);
  }, []);
};
```

## 🚨 ОБРОБКА ПОМИЛОК

```typescript
const handleApiError = (error: any) => {
  switch (error.status) {
    case 401:
      // Перенаправити на логін
      window.location.href = '/login';
      break;
    case 403:
      alert('Недостатньо прав для цієї дії');
      break;
    case 404:
      alert('Ресурс не знайдено');
      break;
    case 500:
      alert('Помилка сервера. Спробуйте пізніше');
      break;
    default:
      alert('Невідома помилка');
  }
};

// Використання
try {
  const response = await fastapi.request('GET', '/api/v1/matches');
} catch (error) {
  handleApiError(error);
}
```

## 💡 ОПТИМІЗАЦІЯ ПРОДУКТИВНОСТІ

### 1. Кешування даних
```typescript
const useCache = <T>(key: string, fetcher: () => Promise<T>, ttl = 5 * 60 * 1000) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cached = localStorage.getItem(key);
    if (cached) {
      const { data: cachedData, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp < ttl) {
        setData(cachedData);
        setLoading(false);
        return;
      }
    }

    fetcher().then(result => {
      setData(result);
      localStorage.setItem(key, JSON.stringify({
        data: result,
        timestamp: Date.now()
      }));
      setLoading(false);
    });
  }, [key]);

  return { data, loading };
};
```

### 2. Пагінація
```typescript
const useInfiniteScroll = (endpoint: string) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);

  const loadMore = async () => {
    if (loading || !hasMore) return;
    
    setLoading(true);
    try {
      const response = await fastapi.request(
        'GET', 
        `${endpoint}?limit=20&offset=${offset}`
      );
      
      setItems(prev => [...prev, ...response.data]);
      setOffset(prev => prev + 20);
      setHasMore(response.has_more);
    } catch (error) {
      console.error('Помилка завантаження:', error);
    } finally {
      setLoading(false);
    }
  };

  return { items, loading, hasMore, loadMore };
};
```

## 🎯 КЛЮЧОВІ ОСОБЛИВОСТІ

1. **Оптимізовані запити** - всі дані завантажуються одним запитом
2. **Реалтайм оновлення** - WebSocket або polling для актуальних даних
3. **Кешування** - зменшення навантаження на сервер
4. **Обробка помилок** - коректна обробка всіх можливих помилок
5. **Пагінація** - ефективне завантаження великих списків
6. **Типізація** - повна підтримка TypeScript

Ця система забезпечує повний функціонал матчингу, чатів та платежів з оптимальною продуктивністю та користувацьким досвідом.
