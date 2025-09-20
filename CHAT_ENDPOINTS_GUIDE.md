# 💬 **ЧАТИ - ІНСТРУКЦІЯ ДЛЯ ФРОНТЕНДУ**

## 🎯 **ПОЧАТОК ЧАТУ З ЛАЙКНУТИМИ ПРОФІЛЯМИ**

### **📋 1. Отримання списку чатів**
```javascript
GET /api/v1/conversations/{user_id}
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
[
  {
    "thread_id": "550e8400-e29b-41d4-a716-446655440010",
    "other_user_id": "550e8400-e29b-41d4-a716-446655440001", 
    "other_user_name": "Марія Іванова",
    "other_user_photo": "https://storage.url/photo.jpg",
    "last_message": "Привіт! Коли можемо зустрітися?",
    "last_message_at": "2025-01-20T15:30:00Z",
    "unread_count": 2,
    "chat_status": "active",  // "locked", "active"
    "created_at": "2025-01-20T10:00:00Z"
  }
]
```

### **💰 2. Розблокування чату (якщо потрібна оплата)**
```javascript
POST /api/v1/payments/chat-unlock
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "target_user_id": "550e8400-e29b-41d4-a716-446655440001"
}

// ✅ ВІДПОВІДЬ:
{
  "success": true,
  "message": "Оплата успішна! Чат розблоковано",
  "payment_id": "payment-uuid",
  "amount": 50.00,
  "target_user_id": "550e8400-e29b-41d4-a716-446655440001",
  "thread_id": "550e8400-e29b-41d4-a716-446655440010"
}
```

### **📤 3. Відправка повідомлення**
```javascript
POST /api/v1/chats/{thread_id}/messages
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "content": "Привіт! Як справи?"
}

// ✅ ВІДПОВІДЬ:
{
  "success": true,
  "message": {
    "message_id": "msg-uuid",
    "sender_user_id": "current-user-id",
    "content": "Привіт! Як справи?",
    "sent_at": "2025-01-20T16:00:00Z",
    "is_read": false
  }
}
```

### **💌 4. Отримання повідомлень чату**
```javascript
GET /api/v1/chats/{thread_id}/messages?limit=50&offset=0
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "messages": [
    {
      "message_id": "msg-uuid-1",
      "sender_user_id": "other-user-id",
      "content": "Привіт! Все добре, дякую!",
      "sent_at": "2025-01-20T16:05:00Z",
      "is_read": true
    },
    {
      "message_id": "msg-uuid-2", 
      "sender_user_id": "current-user-id",
      "content": "Привіт! Як справи?",
      "sent_at": "2025-01-20T16:00:00Z",
      "is_read": true
    }
  ],
  "has_more": false
}
```

### **✅ 5. Позначення повідомлень як прочитаних**
```javascript
POST /api/v1/chats/{thread_id}/mark-read
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "success": true,
  "message": "Повідомлення позначено як прочитані"
}
```

### **📊 6. Деталі чату**
```javascript
GET /api/v1/chats/{thread_id}/details
Authorization: Bearer {jwt_token}

// ✅ ВІДПОВІДЬ:
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440010",
  "other_user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Марія Іванова",
    "photo": "https://storage.url/photo.jpg",
    "role": "nanny"
  },
  "status": "active",
  "created_at": "2025-01-20T10:00:00Z",
  "total_messages": 15,
  "unread_count": 3
}
```

---

## 🔄 **ЛОГІКА ВИКОРИСТАННЯ У ФРОНТЕНДІ**

### **💬 Компонент списку чатів:**

```javascript
class ChatsList {
  constructor() {
    this.state = {
      chats: [],
      loading: false
    };
  }

  async componentDidMount() {
    await this.loadChats();
  }

  // 1. Завантаження списку чатів
  async loadChats() {
    this.setState({ loading: true });
    
    try {
      const currentUserId = getCurrentUserId(); // отримуємо з токену
      const chats = await fastapi.request(
        'GET', 
        `/api/v1/conversations/${currentUserId}`
      );
      
      this.setState({ 
        chats: chats || [],
        loading: false 
      });
    } catch (error) {
      console.error('Error loading chats:', error);
      this.setState({ loading: false });
    }
  }

  // 2. Розблокування чату
  async unlockChat(targetUserId) {
    try {
      const response = await fastapi.request(
        'POST',
        '/api/v1/payments/chat-unlock',
        { target_user_id: targetUserId }
      );

      if (response.success) {
        // Показуємо успішне повідомлення
        alert(`Чат розблоковано! Сплачено ${response.amount} грн`);
        
        // Оновлюємо список чатів
        await this.loadChats();
        
        // Переходимо до чату
        this.openChat(response.thread_id);
      }
    } catch (error) {
      console.error('Error unlocking chat:', error);
      alert('Помилка розблокування чату');
    }
  }

  // 3. Відкриття чату
  openChat(threadId) {
    // Переходимо на сторінку чату
    window.location.href = `/chat/${threadId}`;
  }

  // 4. Рендер списку чатів
  renderChats() {
    const { chats, loading } = this.state;

    if (loading) return <div>Завантаження чатів...</div>;
    if (!chats.length) return <div>Немає активних чатів</div>;

    return (
      <div className="chats-list">
        {chats.map((chat) => (
          <div key={chat.thread_id} className="chat-item">
            <img 
              src={chat.other_user_photo} 
              alt={chat.other_user_name}
              className="chat-avatar"
            />
            
            <div className="chat-info">
              <h3>{chat.other_user_name}</h3>
              {chat.last_message && (
                <p className="last-message">{chat.last_message}</p>
              )}
              <span className="last-time">
                {formatTime(chat.last_message_at)}
              </span>
            </div>

            {chat.unread_count > 0 && (
              <span className="unread-badge">{chat.unread_count}</span>
            )}

            <div className="chat-actions">
              {chat.chat_status === 'locked' ? (
                <button 
                  onClick={() => this.unlockChat(chat.other_user_id)}
                  className="unlock-btn"
                >
                  Розблокувати (50 грн)
                </button>
              ) : (
                <button 
                  onClick={() => this.openChat(chat.thread_id)}
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
  }
}
```

### **💌 Компонент чату:**

```javascript
class ChatComponent {
  constructor(props) {
    super(props);
    this.state = {
      messages: [],
      newMessage: '',
      loading: false,
      chatDetails: null
    };
    this.messagesEndRef = React.createRef();
  }

  async componentDidMount() {
    await this.loadChatDetails();
    await this.loadMessages();
    await this.markAsRead();
    
    // Автоматично прокручуємо до низу
    this.scrollToBottom();
  }

  // 1. Завантаження деталей чату
  async loadChatDetails() {
    try {
      const details = await fastapi.request(
        'GET',
        `/api/v1/chats/${this.props.threadId}/details`
      );
      this.setState({ chatDetails: details });
    } catch (error) {
      console.error('Error loading chat details:', error);
    }
  }

  // 2. Завантаження повідомлень
  async loadMessages() {
    this.setState({ loading: true });
    
    try {
      const response = await fastapi.request(
        'GET',
        `/api/v1/chats/${this.props.threadId}/messages?limit=100`
      );
      
      // Сортуємо повідомлення за часом (старіші спочатку)
      const sortedMessages = response.messages.sort(
        (a, b) => new Date(a.sent_at) - new Date(b.sent_at)
      );
      
      this.setState({ 
        messages: sortedMessages,
        loading: false 
      });
      
      this.scrollToBottom();
    } catch (error) {
      console.error('Error loading messages:', error);
      this.setState({ loading: false });
    }
  }

  // 3. Відправка повідомлення
  async sendMessage() {
    const { newMessage } = this.state;
    if (!newMessage.trim()) return;

    try {
      const response = await fastapi.request(
        'POST',
        `/api/v1/chats/${this.props.threadId}/messages`,
        { content: newMessage }
      );

      // Додаємо нове повідомлення до списку
      this.setState(prev => ({
        messages: [...prev.messages, response.message],
        newMessage: ''
      }));

      this.scrollToBottom();
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Помилка відправки повідомлення');
    }
  }

  // 4. Позначення як прочитані
  async markAsRead() {
    try {
      await fastapi.request(
        'POST',
        `/api/v1/chats/${this.props.threadId}/mark-read`
      );
    } catch (error) {
      console.error('Error marking as read:', error);
    }
  }

  // 5. Прокрутка до низу
  scrollToBottom() {
    setTimeout(() => {
      this.messagesEndRef.current?.scrollIntoView({ 
        behavior: 'smooth' 
      });
    }, 100);
  }

  // 6. Обробка натискання Enter
  handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.sendMessage();
    }
  }

  // 7. Рендер чату
  render() {
    const { messages, newMessage, loading, chatDetails } = this.state;
    const currentUserId = getCurrentUserId();

    if (loading) return <div>Завантаження чату...</div>;

    return (
      <div className="chat-container">
        {/* Заголовок чату */}
        {chatDetails && (
          <div className="chat-header">
            <img 
              src={chatDetails.other_user.photo} 
              alt={chatDetails.other_user.name}
              className="header-avatar"
            />
            <h2>{chatDetails.other_user.name}</h2>
            <span className="user-role">{chatDetails.other_user.role}</span>
          </div>
        )}

        {/* Список повідомлень */}
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.message_id}
              className={`message ${
                message.sender_user_id === currentUserId ? 'own' : 'other'
              }`}
            >
              <div className="message-content">
                {message.content}
              </div>
              <div className="message-time">
                {formatTime(message.sent_at)}
                {message.sender_user_id === currentUserId && (
                  <span className={`read-status ${message.is_read ? 'read' : 'unread'}`}>
                    {message.is_read ? '✓✓' : '✓'}
                  </span>
                )}
              </div>
            </div>
          ))}
          <div ref={this.messagesEndRef} />
        </div>

        {/* Поле вводу */}
        <div className="message-input-container">
          <textarea
            value={newMessage}
            onChange={(e) => this.setState({ newMessage: e.target.value })}
            onKeyPress={(e) => this.handleKeyPress(e)}
            placeholder="Введіть повідомлення..."
            className="message-input"
            rows="2"
          />
          <button 
            onClick={() => this.sendMessage()}
            disabled={!newMessage.trim()}
            className="send-button"
          >
            Відправити
          </button>
        </div>
      </div>
    );
  }
}
```

---

## 🔄 **ІНТЕГРАЦІЯ З ОСНОВНИМИ СТОРІНКАМИ**

### **📱 Додавання кнопки "Написати" на сторінці збережених:**

```javascript
// У компоненті SavedNannies.tsx або SavedParents.tsx
class SavedProfiles {
  
  // Функція для початку чату
  async startChat(targetUserId) {
    try {
      // Спочатку перевіряємо чи є вже чат
      const currentUserId = getCurrentUserId();
      const chats = await fastapi.request(
        'GET', 
        `/api/v1/conversations/${currentUserId}`
      );
      
      // Шукаємо існуючий чат з цим користувачем
      const existingChat = chats.find(
        chat => chat.other_user_id === targetUserId
      );
      
      if (existingChat) {
        // Якщо чат вже є - відкриваємо його
        if (existingChat.chat_status === 'locked') {
          // Потрібна оплата
          await this.unlockAndOpenChat(targetUserId);
        } else {
          // Чат вже активний
          window.location.href = `/chat/${existingChat.thread_id}`;
        }
      } else {
        // Якщо чату немає - створюємо через оплату
        await this.unlockAndOpenChat(targetUserId);
      }
      
    } catch (error) {
      console.error('Error starting chat:', error);
      alert('Помилка початку чату');
    }
  }

  async unlockAndOpenChat(targetUserId) {
    try {
      const response = await fastapi.request(
        'POST',
        '/api/v1/payments/chat-unlock',
        { target_user_id: targetUserId }
      );

      if (response.success) {
        alert(`Чат розблоковано! Сплачено ${response.amount} грн`);
        window.location.href = `/chat/${response.thread_id}`;
      }
    } catch (error) {
      console.error('Error unlocking chat:', error);
      alert('Помилка розблокування чату');
    }
  }

  // У рендері профілю додаємо кнопку
  renderProfile(profile) {
    return (
      <div className="profile-card">
        {/* ... інша інформація профілю ... */}
        
        <div className="profile-actions">
          <button 
            onClick={() => this.unlikeProfile(profile.swipe_id)}
            className="unlike-btn"
          >
            💔 Прибрати з збережених
          </button>
          
          {/* ⭐ НОВА КНОПКА ДЛЯ ЧАТУ */}
          <button 
            onClick={() => this.startChat(profile.target_user_id)}
            className="chat-btn"
          >
            💬 Написати
          </button>
        </div>
      </div>
    );
  }
}
```

### **💕 Додавання кнопки "Написати" на сторінці матчів:**

```javascript
// У компоненті для відображення матчів
class MatchesPage {
  
  renderMatch(match) {
    return (
      <div className="match-card">
        <img src={match.avatar_url} alt={match.first_name} />
        
        <div className="match-info">
          <h3>{match.first_name} {match.last_name}</h3>
          <p>Взаємний лайк! 💕</p>
        </div>

        <div className="match-actions">
          <button 
            onClick={() => this.startChat(match.target_user_id)}
            className="chat-btn primary"
          >
            💬 Написати
          </button>
          
          <button 
            onClick={() => this.unlikeProfile(match.swipe_id)}
            className="unlike-btn secondary"
          >
            💔 Прибрати
          </button>
        </div>
      </div>
    );
  }

  // Використовуємо ту ж логіку startChat що і вище
  async startChat(targetUserId) {
    // ... аналогічна логіка ...
  }
}
```

---

## 📊 **ПІДСУМОК ЕНДПОІНТІВ ДЛЯ ЧАТІВ**

| Призначення | Ендпоінт | Відповідь |
|-------------|----------|-----------|
| 📋 Список чатів | `GET /api/v1/conversations/{user_id}` | `[{thread_id, other_user_name, ...}]` |
| 💰 Розблокування чату | `POST /api/v1/payments/chat-unlock` | `{success, thread_id, amount}` |
| 📤 Відправка повідомлення | `POST /api/v1/chats/{thread_id}/messages` | `{success, message}` |
| 💌 Отримання повідомлень | `GET /api/v1/chats/{thread_id}/messages` | `{messages: [...], has_more}` |
| ✅ Позначити як прочитані | `POST /api/v1/chats/{thread_id}/mark-read` | `{success, message}` |
| 📊 Деталі чату | `GET /api/v1/chats/{thread_id}/details` | `{thread_id, other_user, status}` |

---

## 🎯 **ЛОГІКА РОБОТИ**

### **🔄 Послідовність дій для початку чату:**

1. **Користувач натискає "Написати"** на збереженому профілі або матчі
2. **Перевіряємо існуючі чати** через `GET /api/v1/conversations/{user_id}`
3. **Якщо чат існує:**
   - `chat_status: "active"` → відкриваємо чат
   - `chat_status: "locked"` → пропонуємо оплату
4. **Якщо чату немає** → створюємо через оплату `POST /api/v1/payments/chat-unlock`
5. **Після оплати** → переходимо до чату з `thread_id`

### **💡 Важливі моменти:**

- **Оплата потрібна тільки один раз** для кожної пари користувачів
- **Взаємні лайки (матчі)** можуть мати безкоштовні чати (залежить від бізнес-логіки)
- **Всі повідомлення зберігаються** навіть після відміни лайку
- **Непрочитані повідомлення** відображаються в лічильниках

**Готово для імплементації! 💬🚀**
