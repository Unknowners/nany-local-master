# 📋 Шаблони коду для швидкої розробки

## 🔧 FastAPI Роутер

```python
"""
{Feature} endpoints router
Handles all {feature}-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..database import get_db
from ..services.{feature}_service import {Feature}Service
from ..schemas.{feature} import {Feature}Create, {Feature}Response, {Feature}Update
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/{features}", tags=["{Features}"])

@router.get("/", response_model=List[{Feature}Response])
async def get_{features}(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: {Feature}Service = Depends(get_{feature}_service)
) -> List[{Feature}Response]:
    """Отримати список {features}"""
    try:
        return await service.get_{features}(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"❌ Error fetching {features}: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.get("/{{{feature}_id}}", response_model={Feature}Response)
async def get_{feature}(
    {feature}_id: str,
    service: {Feature}Service = Depends(get_{feature}_service)
) -> {Feature}Response:
    """Отримати {feature} за ID"""
    try:
        return await service.get_{feature}({feature}_id)
    except {Feature}NotFoundError:
        raise HTTPException(status_code=404, detail="{Feature} не знайдено")
    except Exception as e:
        logger.error(f"❌ Error fetching {feature}: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.post("/", response_model={Feature}Response, status_code=201)
async def create_{feature}(
    {feature}_data: {Feature}Create,
    service: {Feature}Service = Depends(get_{feature}_service),
    current_user = Depends(get_current_user)
) -> {Feature}Response:
    """Створити новий {feature}"""
    try:
        return await service.create_{feature}({feature}_data, current_user.id)
    except Exception as e:
        logger.error(f"❌ Error creating {feature}: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка створення")

@router.put("/{{{feature}_id}}", response_model={Feature}Response)
async def update_{feature}(
    {feature}_id: str,
    {feature}_data: {Feature}Update,
    service: {Feature}Service = Depends(get_{feature}_service),
    current_user = Depends(get_current_user)
) -> {Feature}Response:
    """Оновити {feature}"""
    try:
        return await service.update_{feature}({feature}_id, {feature}_data, current_user.id)
    except {Feature}NotFoundError:
        raise HTTPException(status_code=404, detail="{Feature} не знайдено")
    except Exception as e:
        logger.error(f"❌ Error updating {feature}: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка оновлення")

@router.delete("/{{{feature}_id}}", status_code=204)
async def delete_{feature}(
    {feature}_id: str,
    service: {Feature}Service = Depends(get_{feature}_service),
    current_user = Depends(get_current_user)
):
    """Видалити {feature}"""
    try:
        await service.delete_{feature}({feature}_id, current_user.id)
    except {Feature}NotFoundError:
        raise HTTPException(status_code=404, detail="{Feature} не знайдено")
    except Exception as e:
        logger.error(f"❌ Error deleting {feature}: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка видалення")

# Dependency
def get_{feature}_service(db: Session = Depends(get_db)) -> {Feature}Service:
    return {Feature}Service(db)
```

## 🔧 Сервіс

```python
"""
{Feature} business logic service
Handles all {feature}-related business operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import uuid

from ..repositories.{feature}_repository import {Feature}Repository
from ..schemas.{feature} import {Feature}Create, {Feature}Update
from ..models.{feature} import {Feature}
from ..exceptions import {Feature}NotFoundError, {Feature}AlreadyExistsError

logger = logging.getLogger(__name__)

class {Feature}Service:
    """Service class for {feature} operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = {Feature}Repository(db)
    
    async def get_{features}(
        self, 
        limit: int = 10, 
        offset: int = 0,
        user_id: Optional[str] = None
    ) -> List[{Feature}]:
        """Get list of {features} with pagination"""
        try:
            return self.repository.get_all(
                limit=limit, 
                offset=offset,
                filters={"user_id": user_id} if user_id else None
            )
        except Exception as e:
            logger.error(f"❌ Error fetching {features}: {str(e)}")
            raise
    
    async def get_{feature}(self, {feature}_id: str) -> {Feature}:
        """Get {feature} by ID"""
        try:
            {feature} = self.repository.get_by_id({feature}_id)
            if not {feature}:
                raise {Feature}NotFoundError(f"{Feature} {{{feature}_id}} not found")
            return {feature}
        except {Feature}NotFoundError:
            raise
        except Exception as e:
            logger.error(f"❌ Error fetching {feature}: {str(e)}")
            raise
    
    async def create_{feature}(self, {feature}_data: {Feature}Create, user_id: str) -> {Feature}:
        """Create new {feature}"""
        try:
            # Check if {feature} already exists (if needed)
            # existing = self.repository.get_by_field("name", {feature}_data.name)
            # if existing:
            #     raise {Feature}AlreadyExistsError(f"{Feature} already exists")
            
            {feature}_dict = {feature}_data.dict()
            {feature}_dict["id"] = str(uuid.uuid4())
            {feature}_dict["user_id"] = user_id
            
            {feature} = self.repository.create({feature}_dict)
            
            logger.info(f"✅ {Feature} created: {{{feature}.id}}")
            return {feature}
            
        except {Feature}AlreadyExistsError:
            raise
        except Exception as e:
            logger.error(f"❌ Error creating {feature}: {str(e)}")
            raise
    
    async def update_{feature}(
        self, 
        {feature}_id: str, 
        {feature}_data: {Feature}Update,
        user_id: str
    ) -> {Feature}:
        """Update {feature}"""
        try:
            {feature} = await self.get_{feature}({feature}_id)
            
            # Check permissions (if needed)
            # if {feature}.user_id != user_id:
            #     raise PermissionDeniedError("Access denied")
            
            update_data = {feature}_data.dict(exclude_unset=True)
            updated_{feature} = self.repository.update({feature}_id, update_data)
            
            logger.info(f"✅ {Feature} updated: {{{feature}_id}}")
            return updated_{feature}
            
        except {Feature}NotFoundError:
            raise
        except Exception as e:
            logger.error(f"❌ Error updating {feature}: {str(e)}")
            raise
    
    async def delete_{feature}(self, {feature}_id: str, user_id: str) -> None:
        """Delete {feature}"""
        try:
            {feature} = await self.get_{feature}({feature}_id)
            
            # Check permissions (if needed)
            # if {feature}.user_id != user_id:
            #     raise PermissionDeniedError("Access denied")
            
            self.repository.delete({feature}_id)
            
            logger.info(f"✅ {Feature} deleted: {{{feature}_id}}")
            
        except {Feature}NotFoundError:
            raise
        except Exception as e:
            logger.error(f"❌ Error deleting {feature}: {str(e)}")
            raise
```

## 🔧 Pydantic Схеми

```python
"""
{Feature} Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class {Feature}Base(BaseModel):
    """Base {feature} schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Назва {feature}")
    description: Optional[str] = Field(None, max_length=500, description="Опис {feature}")
    is_active: bool = Field(True, description="Чи активний {feature}")

class {Feature}Create({Feature}Base):
    """Schema for creating new {feature}"""
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class {Feature}Update(BaseModel):
    """Schema for updating {feature} (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v

class {Feature}Response({Feature}Base):
    """Schema for {feature} response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class {Feature}List(BaseModel):
    """Schema for paginated {feature} list"""
    items: List[{Feature}Response]
    total: int
    limit: int
    offset: int
    has_more: bool
```

## 🔧 SQLAlchemy Модель

```python
"""
{Feature} SQLAlchemy model
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class {Feature}(BaseModel):
    """SQLAlchemy model for {feature}"""
    __tablename__ = "{features}"
    
    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Foreign keys
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="{features}")
    
    def __repr__(self):
        return f"<{Feature}(id={self.id}, name={self.name})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
```

## 🔧 Репозиторій

```python
"""
{Feature} repository for database operations
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .base_repository import BaseRepository
from ..models.{feature} import {Feature}

class {Feature}Repository(BaseRepository[{Feature}]):
    """Repository for {feature} database operations"""
    
    def __init__(self, db: Session):
        super().__init__(db, {Feature})
    
    def get_by_name(self, name: str) -> Optional[{Feature}]:
        """Get {feature} by name"""
        return self.db.query(self.model).filter(
            self.model.name == name
        ).first()
    
    def get_by_user_id(self, user_id: str) -> List[{Feature}]:
        """Get all {features} for a user"""
        return self.db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()
    
    def get_active(self) -> List[{Feature}]:
        """Get all active {features}"""
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).all()
    
    def search(self, query: str) -> List[{Feature}]:
        """Search {features} by name or description"""
        search_filter = or_(
            self.model.name.ilike(f"%{query}%"),
            self.model.description.ilike(f"%{query}%")
        )
        return self.db.query(self.model).filter(search_filter).all()
```

## 🔧 Кастомні винятки

```python
"""
{Feature} custom exceptions
"""

class {Feature}Error(Exception):
    """Base exception for {feature} operations"""
    pass

class {Feature}NotFoundError({Feature}Error):
    """Raised when {feature} is not found"""
    pass

class {Feature}AlreadyExistsError({Feature}Error):
    """Raised when {feature} already exists"""
    pass

class {Feature}ValidationError({Feature}Error):
    """Raised when {feature} validation fails"""
    pass

class {Feature}PermissionError({Feature}Error):
    """Raised when user doesn't have permission for {feature} operation"""
    pass
```

## 🧪 Тести - ОБОВ'ЯЗКОВО для кожної функції!

### ❗ Правило: Кожен API endpoint ОБОВ'ЯЗКОВО має тести

### API тест (позитивний + негативний)
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_item_success():
    """Тест успішного створення елементу"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        item_data = {
            "name": "Test Item", 
            "description": "Test Description"
        }
        
        response = await client.post(
            "/api/v1/items",
            json=item_data,
            headers={"Authorization": "Bearer valid_token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == item_data["name"]
        assert "id" in data

@pytest.mark.asyncio
async def test_create_item_unauthorized():
    """Тест створення без авторизації"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/items", json={})
        assert response.status_code == 401

@pytest.mark.asyncio  
async def test_create_item_invalid_data():
    """Тест з невалідними даними"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/items",
            json={"invalid": "data"},
            headers={"Authorization": "Bearer valid_token"}
        )
        assert response.status_code == 422
```

### Сервіс тест
```python
"""
Tests for {feature} functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services.{feature}_service import {Feature}Service
from app.schemas.{feature} import {Feature}Create, {Feature}Update
from app.exceptions import {Feature}NotFoundError

class Test{Feature}Service:
    """Test {feature} service operations"""
    
    def test_create_{feature}_success(self, db_session: Session):
        # Arrange
        service = {Feature}Service(db_session)
        {feature}_data = {Feature}Create(
            name="Test {Feature}",
            description="Test description"
        )
        
        # Act
        result = service.create_{feature}({feature}_data, "user123")
        
        # Assert
        assert result.name == "Test {Feature}"
        assert result.user_id == "user123"
        assert result.id is not None
    
    def test_get_{feature}_not_found(self, db_session: Session):
        # Arrange
        service = {Feature}Service(db_session)
        
        # Act & Assert
        with pytest.raises({Feature}NotFoundError):
            service.get_{feature}("nonexistent_id")
    
    def test_update_{feature}_success(self, db_session: Session, sample_{feature}):
        # Arrange
        service = {Feature}Service(db_session)
        update_data = {Feature}Update(name="Updated Name")
        
        # Act
        result = service.update_{feature}(sample_{feature}.id, update_data, sample_{feature}.user_id)
        
        # Assert
        assert result.name == "Updated Name"
        assert result.id == sample_{feature}.id

class Test{Feature}API:
    """Test {feature} API endpoints"""
    
    def test_create_{feature}_endpoint(self, client: TestClient, auth_headers):
        # Arrange
        {feature}_data = {
            "name": "Test {Feature}",
            "description": "Test description"
        }
        
        # Act
        response = client.post(
            "/api/v1/{features}/",
            json={feature}_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test {Feature}"
        assert "id" in data
    
    def test_get_{feature}_endpoint(self, client: TestClient, sample_{feature}):
        # Act
        response = client.get(f"/api/v1/{features}/{sample_{feature}.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_{feature}.id
        assert data["name"] == sample_{feature}.name
```

---

## 📝 Як використовувати шаблони

1. **Замініть плейсхолдери**:
   - `{Feature}` → `User`, `Order`, `Product` (PascalCase)
   - `{feature}` → `user`, `order`, `product` (snake_case)
   - `{features}` → `users`, `orders`, `products` (множина)

2. **Адаптуйте під потреби**:
   - Додайте специфічні поля
   - Змініть валідацію
   - Додайте бізнес-логіку

3. **Тестуйте поступово**:
   - Спочатку модель та схеми
   - Потім репозиторій та сервіс
   - Нарешті роутер та API