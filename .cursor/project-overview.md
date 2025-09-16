# Nanny Match - Complete Project Overview

## 🎯 Project Mission
**Nanny Match Ukraine** is a comprehensive platform connecting families with qualified nannies across Ukraine. The platform provides secure authentication, detailed onboarding, profile management, and matching services with integrated SMS notifications and file storage.

## 🏗️ Architecture Overview

### Technology Stack
```
Frontend (Local)     Backend (Docker)      Infrastructure (Docker)
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐
│ React 18        │  │ FastAPI         │  │ PostgreSQL 15           │
│ TypeScript      │◄─┤ Python 3.11     │◄─┤ Redis 7                 │
│ Vite            │  │ Uvicorn         │  │ Docker Containers       │
│ Tailwind CSS    │  │ Pydantic        │  │ PgAdmin (dev)          │
│ Shadcn/ui       │  │ SQLAlchemy      │  │                        │
└─────────────────┘  │ Alembic         │  └─────────────────────────┘
                     │ JWT Auth        │
                     │ TurboSMS        │
                     │ S3 Storage      │
                     └─────────────────┘
```

### Service Distribution
- **Local Development**: Frontend (React + Vite)
- **Docker Containers**: Backend, Database, Cache
- **External Services**: SMS (TurboSMS), Storage (S3-compatible)

## 📊 Core Features

### 👥 User Management
- **Dual Role System**: Parents & Nannies
- **Secure Authentication**: JWT tokens, SMS OTP verification
- **Profile Management**: Comprehensive user profiles with photos
- **Dynamic Onboarding**: Role-specific registration flows

### 🔐 Security Features
- **Password Hashing**: bcrypt implementation
- **SMS Verification**: TurboSMS integration for OTP
- **JWT Tokens**: Access & refresh token system
- **Input Validation**: Pydantic models throughout

### 📱 Communication
- **SMS Integration**: OTP codes, notifications
- **Real-time Updates**: WebSocket support
- **Email System**: Planned integration
- **Push Notifications**: Future enhancement

### 🗄️ Data Management
- **PostgreSQL Database**: Primary data store
- **Redis Cache**: Session management, OTP storage
- **S3 Storage**: Photos, documents, media files
- **Database Migrations**: Alembic-managed schema evolution

## 🌐 API Architecture

### Backend Endpoints
```
Authentication:
POST /auth/register          # User registration
POST /auth/login            # User login  
POST /auth/refresh          # Token refresh
POST /auth/logout           # User logout
POST /auth/forgot-password  # Password reset
POST /auth/verify-otp       # OTP verification

User Management:
GET  /users/profile         # Get user profile
PUT  /users/profile         # Update profile
POST /users/upload-photo    # Profile photo upload
GET  /users/me              # Current user info

Nanny Services:
GET  /nannies              # Search nannies
GET  /nannies/{id}         # Nanny details
POST /nannies/favorites    # Add to favorites

Reference Data:
GET  /categories           # Service categories
GET  /skills              # Available skills
GET  /locations           # Supported locations

System:
GET  /health              # Health check
GET  /docs                # API documentation
```

### Frontend Architecture
```
src/
├── pages/                 # Route components
├── components/           # Reusable UI components
│   ├── ui/              # Shadcn components
│   ├── onboarding/      # Registration flows
│   └── admin/           # Admin interface
├── contexts/            # React contexts (Auth, etc.)
├── hooks/               # Custom React hooks
├── integrations/        # Backend adapters
│   ├── supabase/       # Supabase client
│   └── fastapi/        # FastAPI client
└── lib/                 # Utilities, validations
```

## 🔄 Development Workflow

### Local Development Setup
```bash
# 1. Start all services
./restart-all.sh

# 2. Services will be available at:
# - Frontend: http://localhost:8080
# - Backend:  http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - PgAdmin:  http://localhost:5050
```

### Docker Services
- **PostgreSQL**: Database server with health checks
- **Redis**: Cache and session store
- **Backend**: FastAPI application with auto-reload
- **PgAdmin**: Database management interface (dev only)

### Development Tools
- **Hot Reload**: Both frontend (Vite) and backend (Uvicorn)
- **Type Safety**: TypeScript frontend, Pydantic backend
- **Code Formatting**: Prettier, Black, ESLint
- **API Testing**: Built-in Swagger UI at `/docs`

## 📋 Data Models

### Core Entities
```python
User:
- id, email, phone, password_hash
- role (parent/nanny), status, created_at
- profile data, preferences

Nanny:
- user_id, experience_years, hourly_rate
- services, skills, availability
- location, bio, photos

Parent:
- user_id, children_count, budget_range
- location, requirements, preferences

Booking:
- parent_id, nanny_id, date_time
- duration, status, total_cost
- special_requirements, notes
```

### Reference Data
- **Categories**: Childcare service types
- **Skills**: Nanny capabilities and certifications  
- **Locations**: Supported cities and regions
- **Services**: Available service offerings

## 🔧 Configuration Management

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://app:app@localhost:5432/app
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=dev-secret-key
TURBOSMS_API_TOKEN=your-token
EXTERNAL_STORAGE_*=s3-config

# Frontend (.env)
VITE_BACKEND_KIND=fastapi
VITE_FASTAPI_BASE_URL=http://localhost:8000
```

### Backend Switching
The frontend supports multiple backend types:
- **FastAPI**: Local/remote FastAPI servers
- **Supabase**: Cloud-based backend alternative
- **Runtime Switching**: Change backends without rebuild

## 🚀 Deployment Architecture

### Production Stack
- **Backend**: Docker containers with orchestration
- **Database**: Managed PostgreSQL service
- **Cache**: Redis cluster
- **Frontend**: CDN deployment (Vercel/Netlify)
- **Storage**: S3-compatible object storage

### Scaling Considerations
- **Horizontal Scaling**: Multiple backend containers
- **Database Optimization**: Connection pooling, read replicas
- **Caching Strategy**: Redis for sessions, API responses
- **CDN Integration**: Static asset delivery

## 📈 Monitoring & Maintenance

### Health Checks
- **Backend**: `/health` endpoint with service status
- **Database**: Connection and query performance
- **Cache**: Redis connectivity and memory usage
- **External Services**: SMS and storage availability

### Logging Strategy
- **Application Logs**: Structured JSON logging
- **Access Logs**: Request/response tracking
- **Error Tracking**: Exception monitoring
- **Performance Metrics**: Response times, throughput

## 🔒 Security Considerations

### Authentication Flow
1. User registration with phone verification
2. SMS OTP validation
3. JWT token issuance (access + refresh)
4. Token-based API authentication
5. Automatic token refresh

### Data Protection
- **Password Security**: bcrypt hashing with salt
- **Input Sanitization**: Pydantic validation
- **SQL Injection Prevention**: ORM parameter binding
- **File Upload Security**: Type validation, size limits

## 🎯 Future Enhancements

### Planned Features
- **Real-time Chat**: In-app messaging system
- **Video Calls**: Integrated video interviews
- **Payment Processing**: Stripe/PayPal integration
- **Review System**: Ratings and feedback
- **Mobile Apps**: React Native applications
- **Advanced Matching**: AI-powered recommendations

### Technical Improvements
- **Microservices**: Service decomposition
- **Event Sourcing**: Audit trail and rollback
- **GraphQL**: Alternative API layer
- **Kubernetes**: Container orchestration
- **CI/CD Pipeline**: Automated testing and deployment

---

**This project represents a production-ready platform with modern architecture, comprehensive security, and scalable design patterns.**