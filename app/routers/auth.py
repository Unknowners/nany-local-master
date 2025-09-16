"""
Authentication endpoints router
Handles all auth-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from ..database import get_db
from ..schemas import *
from ..models import Profile
from ..sms import send_otp_sms, verify_otp, get_sms_balance
from ..auth_utils import hash_password, verify_password
from ..jwt_utils import create_access_token, create_refresh_token, verify_token, get_user_id_from_token

logger = logging.getLogger(__name__)
security = HTTPBearer()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# ===== Dependencies =====

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Profile:
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        user_id = get_user_id_from_token(token)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ===== Auth Endpoints =====

@router.get("/me", response_model=ProfileResponse)
async def get_current_user_profile(current_user: Profile = Depends(get_current_user)):
    """Get current user profile"""
    return ProfileResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        phone=current_user.phone,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None
    )

@router.post("/send-otp", response_model=OTPResponse)
async def send_otp(request: OTPRequest):
    """Send OTP to phone number"""
    try:
        logger.info(f"📱 Sending OTP to {request.phone} for {request.purpose}")
        
        # Send OTP via SMS
        success = send_otp_sms(request.phone, request.purpose)
        
        if success:
            logger.info(f"✅ OTP sent successfully to {request.phone}")
            return OTPResponse(
                success=True,
                message=f"OTP надіслано на номер {request.phone}"
            )
        else:
            logger.error(f"❌ Failed to send OTP to {request.phone}")
            raise HTTPException(status_code=500, detail="Не вдалося надіслати OTP")
            
    except Exception as e:
        logger.error(f"❌ Error sending OTP: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.post("/verify-otp", response_model=OTPVerifyResponse)
async def verify_otp_endpoint(request: OTPVerify):
    """Verify OTP code"""
    try:
        logger.info(f"🔐 Verifying OTP for {request.phone}")
        
        # Verify OTP
        is_valid = verify_otp(request.phone, request.code, request.purpose)
        
        if is_valid:
            logger.info(f"✅ OTP verified successfully for {request.phone}")
            return OTPVerifyResponse(
                success=True,
                message="OTP підтверджено успішно"
            )
        else:
            logger.warning(f"❌ Invalid OTP for {request.phone}")
            raise HTTPException(status_code=400, detail="Невірний або застарілий код")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error verifying OTP: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.post("/register")
async def register_user(request: dict, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        phone = request.get('phone')
        email = request.get('email')
        password = request.get('password')
        role = request.get('role', 'parent')
        
        logger.info(f"👤 Registering user: {phone}, role: {role}")
        
        # Check if user already exists
        existing_user = db.query(Profile).filter(
            (Profile.phone == phone) | (Profile.email == email)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Користувач вже існує")
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user profile
        import uuid
        user_id = str(uuid.uuid4())
        
        new_profile = Profile(
            user_id=user_id,
            phone=phone,
            email=email,
            password_hash=hashed_password,
            first_name=request.get('first_name', ''),
            last_name=request.get('last_name', '')
        )
        
        db.add(new_profile)
        
        # Add user role
        from ..models import UserRole
        user_role = UserRole(
            user_id=user_id,
            role=role
        )
        db.add(user_role)
        
        db.commit()
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user_id})
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        logger.info(f"✅ User registered successfully: {user_id}")
        
        return {
            "success": True,
            "user": {
                "id": user_id,
                "phone": phone,
                "email": email,
                "role": role
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка реєстрації")

@router.post("/login")
async def login_user(request: dict, db: Session = Depends(get_db)):
    """Login user"""
    try:
        email = request.get('email')
        password = request.get('password')
        
        logger.info(f"🔑 Login attempt for: {email}")
        
        # Find user
        user = db.query(Profile).filter(Profile.email == email).first()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Невірні дані для входу")
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user.user_id})
        refresh_token = create_refresh_token(data={"sub": user.user_id})
        
        logger.info(f"✅ Login successful for: {user.user_id}")
        
        return {
            "success": True,
            "user": {
                "id": user.user_id,
                "phone": user.phone,
                "email": user.email
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка входу")

@router.post("/update-password", response_model=UpdatePasswordResponse)
async def update_password(
    body: UpdatePasswordBody,
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user password"""
    try:
        logger.info(f"🔒 Updating password for user: {current_user.user_id}")
        
        # Verify current password
        if not verify_password(body.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Невірний поточний пароль")
        
        # Hash new password
        new_password_hash = hash_password(body.new_password)
        
        # Update password
        current_user.password_hash = new_password_hash
        db.commit()
        
        logger.info(f"✅ Password updated successfully for user: {current_user.user_id}")
        
        return UpdatePasswordResponse(
            success=True,
            message="Пароль успішно оновлено"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Password update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка оновлення паролю")