"""
Onboarding endpoints router
Handles all onboarding-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from ..database import get_db
from ..services.onboarding_service import OnboardingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Onboarding"])

# ===== Supabase-like API endpoints for onboarding tables =====

@router.get("/onboarding_configs")
async def get_onboarding_configs(
    target_role: str = Query(None),
    is_default: bool = Query(None),
    is_active: bool = Query(None),
    db: Session = Depends(get_db)
):
    """Get onboarding configurations with Supabase-like filtering"""
    try:
        service = OnboardingService(db)
        return service.get_configs(target_role, is_default, is_active)
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding configs: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.get("/onboarding_steps")
async def get_onboarding_steps(
    config_id: str = Query(None),
    is_active: bool = Query(None),
    order_by: str = Query("step_number"),
    db: Session = Depends(get_db)
):
    """Get onboarding steps with Supabase-like filtering"""
    try:
        query = "SELECT * FROM onboarding_steps WHERE 1=1"
        params = {}
        
        if config_id is not None:
            query += " AND config_id = :config_id"
            params["config_id"] = config_id
            
        if is_active is not None:
            query += " AND is_active = :is_active"
            params["is_active"] = is_active
            
        if order_by:
            query += f" ORDER BY {order_by}"
        
        result = db.execute(text(query), params).fetchall()
        
        steps = []
        for row in result:
            steps.append({
                "id": str(row.id),
                "config_id": str(row.config_id),
                "step_number": row.step_number,
                "step_key": row.step_key,
                "title": row.title,
                "description": row.description,
                "is_required": row.is_required,
                "is_active": row.is_active,
                "created_at": row.created_at.isoformat() if row.created_at else None
            })
        
        return steps
        
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding steps: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.get("/onboarding_fields")
async def get_onboarding_fields(
    step_id: str = Query(None),
    is_active: bool = Query(None),
    order_by: str = Query("field_order"),
    db: Session = Depends(get_db)
):
    """Get onboarding fields with Supabase-like filtering"""
    try:
        query = "SELECT * FROM onboarding_fields WHERE 1=1"
        params = {}
        
        if step_id is not None:
            # Handle both single step_id and array of step_ids
            if "," in step_id:
                step_ids = [s.strip() for s in step_id.split(",")]
                placeholders = ",".join([f":step_id_{i}" for i in range(len(step_ids))])
                query += f" AND step_id IN ({placeholders})"
                for i, sid in enumerate(step_ids):
                    params[f"step_id_{i}"] = sid
            else:
                query += " AND step_id = :step_id"
                params["step_id"] = step_id
            
        if is_active is not None:
            query += " AND is_active = :is_active"
            params["is_active"] = is_active
            
        if order_by:
            query += f" ORDER BY {order_by}"
        
        result = db.execute(text(query), params).fetchall()
        
        fields = []
        for row in result:
            fields.append({
                "id": str(row.id),
                "step_id": str(row.step_id),
                "field_key": row.field_key,
                "field_type": row.field_type,
                "label": row.label,
                "description": row.description,
                "placeholder": row.placeholder,
                "help_text": row.help_text,
                "reference_category_code": row.reference_category_code,
                "is_required": row.is_required,
                "is_active": row.is_active,
                "field_order": row.field_order,
                "allow_custom_values": row.allow_custom_values,
                "validation_rules": row.validation_rules,
                "field_config": row.field_config,
                "group_id": str(row.group_id) if row.group_id else None,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None
            })
        
        return fields
        
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding fields: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

# ===== Legacy onboarding endpoints =====

@router.get("/onboarding/configs/{role}")
async def get_onboarding_config_by_role(
    role: str,
    db: Session = Depends(get_db)
):
    """Get onboarding configuration for a specific role"""
    try:
        query = text("""
            SELECT * FROM onboarding_configs 
            WHERE target_role = :role AND is_default = true AND is_active = true
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        result = db.execute(query, {"role": role}).fetchone()
        
        if not result:
            logger.warning(f"No onboarding configuration found for role: {role}")
            return []
        
        config = {
            "id": str(result.id),
            "target_role": result.target_role,
            "name": result.name,
            "is_default": result.is_default,
            "is_active": result.is_active,
            "version": result.version,
            "created_at": result.created_at.isoformat() if result.created_at else None,
            "updated_at": result.updated_at.isoformat() if result.updated_at else None
        }
        
        logger.info(f"✅ Found onboarding config for {role}: {config['name']}")
        return [config]  # Return as array to match frontend expectation
        
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding config: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.get("/onboarding/steps/{role}")
async def get_onboarding_steps_by_role(
    role: str,
    db: Session = Depends(get_db)
):
    """Get onboarding steps for a specific role"""
    try:
        query = text("""
            SELECT os.*, oc.name as config_name 
            FROM onboarding_steps os
            JOIN onboarding_configs oc ON os.config_id = oc.id
            WHERE oc.target_role = :role AND os.is_active = true
            ORDER BY os.step_number
        """)
        
        result = db.execute(query, {"role": role}).fetchall()
        
        steps = []
        for row in result:
            steps.append({
                "id": str(row.id),
                "config_id": str(row.config_id),
                "config_name": row.config_name,
                "step_key": row.step_key,
                "title": row.title,
                "description": row.description,
                "step_number": row.step_number,
                "is_required": row.is_required,
                "is_active": row.is_active,
                "created_at": row.created_at.isoformat() if row.created_at else None
            })
        
        return steps
        
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding steps: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")

@router.get("/onboarding/fields/{step_id}")
async def get_onboarding_fields_by_step(
    step_id: str,
    db: Session = Depends(get_db)
):
    """Get onboarding fields for a specific step"""
    try:
        query = text("""
            SELECT * FROM onboarding_fields 
            WHERE step_id = :step_id AND is_active = true
            ORDER BY field_order
        """)
        
        result = db.execute(query, {"step_id": step_id}).fetchall()
        
        fields = []
        for row in result:
            fields.append({
                "id": str(row.id),
                "step_id": str(row.step_id),
                "group_id": str(row.group_id) if row.group_id else None,
                "field_key": row.field_key,
                "label": row.label,
                "description": row.description,
                "placeholder": row.placeholder,
                "help_text": row.help_text,
                "field_type": row.field_type,
                "field_order": row.field_order,
                "is_required": row.is_required,
                "is_active": row.is_active,
                "reference_category_code": row.reference_category_code,
                "allow_custom_values": row.allow_custom_values,
                "validation_rules": row.validation_rules,
                "field_config": row.field_config,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None
            })
        
        return fields
        
    except Exception as e:
        logger.error(f"❌ Error fetching onboarding fields: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка сервера")