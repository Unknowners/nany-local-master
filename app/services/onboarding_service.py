"""
Onboarding business logic service
Handles all onboarding-related business operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Optional, Any
import logging
import uuid

logger = logging.getLogger(__name__)

class OnboardingService:
    """Service class for onboarding operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_configs(
        self, 
        target_role: Optional[str] = None,
        is_default: Optional[bool] = None,
        is_active: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Get onboarding configurations with filtering"""
        try:
            query = "SELECT * FROM onboarding_configs WHERE 1=1"
            params = {}
            
            if target_role is not None:
                query += " AND target_role = :target_role"
                params["target_role"] = target_role
                
            if is_default is not None:
                query += " AND is_default = :is_default"
                params["is_default"] = is_default
                
            if is_active is not None:
                query += " AND is_active = :is_active"
                params["is_active"] = is_active
                
            query += " ORDER BY created_at DESC"
            
            result = self.db.execute(text(query), params).fetchall()
            
            configs = []
            for row in result:
                configs.append({
                    "id": str(row.id),
                    "target_role": row.target_role,
                    "name": row.name,
                    "is_default": row.is_default,
                    "is_active": row.is_active,
                    "version": row.version,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None
                })
            
            return configs
            
        except Exception as e:
            logger.error(f"❌ Error fetching onboarding configs: {str(e)}")
            raise
    
    def get_steps(
        self,
        config_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: str = "step_number"
    ) -> List[Dict[str, Any]]:
        """Get onboarding steps with filtering"""
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
            
            result = self.db.execute(text(query), params).fetchall()
            
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
            raise
    
    def get_fields(
        self,
        step_id: Optional[str] = None,
        step_ids: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
        order_by: str = "field_order"
    ) -> List[Dict[str, Any]]:
        """Get onboarding fields with filtering"""
        try:
            query = "SELECT * FROM onboarding_fields WHERE 1=1"
            params = {}
            
            if step_id is not None:
                query += " AND step_id = :step_id"
                params["step_id"] = step_id
            elif step_ids is not None:
                placeholders = ",".join([f":step_id_{i}" for i in range(len(step_ids))])
                query += f" AND step_id IN ({placeholders})"
                for i, sid in enumerate(step_ids):
                    params[f"step_id_{i}"] = sid
                
            if is_active is not None:
                query += " AND is_active = :is_active"
                params["is_active"] = is_active
                
            if order_by:
                query += f" ORDER BY {order_by}"
            
            result = self.db.execute(text(query), params).fetchall()
            
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
            raise
    
    def get_config_by_role(self, role: str) -> Optional[Dict[str, Any]]:
        """Get default active onboarding configuration for a specific role"""
        try:
            query = text("""
                SELECT * FROM onboarding_configs 
                WHERE target_role = :role AND is_default = true AND is_active = true
                ORDER BY created_at DESC
                LIMIT 1
            """)
            
            result = self.db.execute(query, {"role": role}).fetchone()
            
            if not result:
                logger.warning(f"No onboarding configuration found for role: {role}")
                return None
            
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
            return config
            
        except Exception as e:
            logger.error(f"❌ Error fetching onboarding config by role: {str(e)}")
            raise
    
    def get_steps_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get onboarding steps for a specific role"""
        try:
            query = text("""
                SELECT os.*, oc.name as config_name 
                FROM onboarding_steps os
                JOIN onboarding_configs oc ON os.config_id = oc.id
                WHERE oc.target_role = :role AND os.is_active = true
                ORDER BY os.step_number
            """)
            
            result = self.db.execute(query, {"role": role}).fetchall()
            
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
            logger.error(f"❌ Error fetching onboarding steps by role: {str(e)}")
            raise
    
    def save_user_data(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save onboarding data for a user"""
        try:
            # Insert or update onboarding data
            query = text("""
                INSERT INTO user_onboarding_data 
                (id, user_id, config_id, step_key, field_key, text_value, number_value, 
                 boolean_value, date_value, time_value, json_value, custom_values, 
                 is_completed, created_at, updated_at)
                VALUES (:id, :user_id, :config_id, :step_key, :field_key, :text_value, 
                        :number_value, :boolean_value, :date_value, :time_value, 
                        :json_value, :custom_values, :is_completed, NOW(), NOW())
                ON CONFLICT (user_id, config_id, step_key, field_key)
                DO UPDATE SET
                    text_value = EXCLUDED.text_value,
                    number_value = EXCLUDED.number_value,
                    boolean_value = EXCLUDED.boolean_value,
                    date_value = EXCLUDED.date_value,
                    time_value = EXCLUDED.time_value,
                    json_value = EXCLUDED.json_value,
                    custom_values = EXCLUDED.custom_values,
                    is_completed = EXCLUDED.is_completed,
                    updated_at = NOW()
            """)
            
            data_id = str(uuid.uuid4())
            params = {
                "id": data_id,
                "user_id": user_id,
                "config_id": data.get("config_id"),
                "step_key": data.get("step_key"),
                "field_key": data.get("field_key"),
                "text_value": data.get("text_value"),
                "number_value": data.get("number_value"),
                "boolean_value": data.get("boolean_value"),
                "date_value": data.get("date_value"),
                "time_value": data.get("time_value"),
                "json_value": data.get("json_value"),
                "custom_values": data.get("custom_values"),
                "is_completed": data.get("is_completed", False)
            }
            
            self.db.execute(query, params)
            self.db.commit()
            
            return {"success": True, "message": "Onboarding data saved successfully"}
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error saving onboarding data: {str(e)}")
            raise
    
    def get_user_data(self, user_id: str, config_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get onboarding data for a user"""
        try:
            query = "SELECT * FROM user_onboarding_data WHERE user_id = :user_id"
            params = {"user_id": user_id}
            
            if config_id:
                query += " AND config_id = :config_id"
                params["config_id"] = config_id
            
            query += " ORDER BY created_at"
            
            result = self.db.execute(text(query), params).fetchall()
            
            data = []
            for row in result:
                data.append({
                    "id": str(row.id),
                    "user_id": str(row.user_id),
                    "config_id": str(row.config_id),
                    "step_key": row.step_key,
                    "field_key": row.field_key,
                    "text_value": row.text_value,
                    "number_value": row.number_value,
                    "boolean_value": row.boolean_value,
                    "date_value": row.date_value.isoformat() if row.date_value else None,
                    "time_value": row.time_value.isoformat() if row.time_value else None,
                    "json_value": row.json_value,
                    "custom_values": row.custom_values,
                    "is_completed": row.is_completed,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None
                })
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error fetching user onboarding data: {str(e)}")
            raise