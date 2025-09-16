"""
Development endpoints router
Only available in development environment
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
import io
import subprocess
import tempfile
import logging
from datetime import datetime

from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dev", tags=["Development"])

def check_dev_environment():
    """Check if this is a development environment"""
    current_env = os.getenv("ENVIRONMENT", "production").lower()
    is_dev = current_env in ["development", "dev", "local"]
    
    logger.info(f"Environment check: ENVIRONMENT={current_env}, is_dev={is_dev}")
    
    if not is_dev:
        raise HTTPException(
            status_code=404, 
            detail="Endpoint not found"
        )
    
    return True

@router.get("/export-database")
async def export_database(db: Session = Depends(get_db)):
    """
    Export database as SQL dump - only available in development environment
    """
    check_dev_environment()
    
    try:
        # Database connection parameters from environment
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "nanny_match")
        db_user = os.getenv("POSTGRES_USER", "app")
        db_password = os.getenv("POSTGRES_PASSWORD", "app")
        
        # Create temporary file for the dump
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.sql', delete=False) as temp_file:
            temp_path = temp_file.name
        
        # Run pg_dump command
        dump_command = [
            "pg_dump",
            f"--host={db_host}",
            f"--port={db_port}",
            f"--username={db_user}",
            f"--dbname={db_name}",
            "--no-password",
            "--verbose",
            "--clean",
            "--no-acl",
            "--no-owner",
            f"--file={temp_path}"
        ]
        
        # Set password via environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = db_password
        
        # Execute pg_dump
        result = subprocess.run(
            dump_command,
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode != 0:
            logger.error(f"pg_dump failed: {result.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Database export failed: {result.stderr}"
            )
        
        # Read the dump file
        with open(temp_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        # Generate filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"nanny_match_db_export_{timestamp}.sql"
        
        # Return as downloadable file
        return StreamingResponse(
            io.StringIO(sql_content),
            media_type="application/sql",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(sql_content.encode('utf-8')))
            }
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Database export timed out"
        )
    except Exception as e:
        logger.error(f"Database export error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database export failed: {str(e)}"
        )

@router.get("/database-info")
async def get_database_info():
    """
    Get database connection information - only available in development environment
    """
    check_dev_environment()
    
    try:
        # Database connection parameters from environment
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "nanny_match")
        db_user = os.getenv("POSTGRES_USER", "app")
        db_password = os.getenv("POSTGRES_PASSWORD", "app")
        
        # Get external host (Docker host IP or localhost)
        external_host = "localhost"  # For local development
        
        connection_info = {
            "host": external_host,
            "port": int(db_port),
            "database": db_name,
            "username": db_user,
            "password": db_password,
            "connection_string": f"postgresql://{db_user}:{db_password}@{external_host}:{db_port}/{db_name}",
            "psql_command": f"psql -h {external_host} -p {db_port} -U {db_user} -d {db_name}",
            "note": "Use PGPASSWORD environment variable or .pgpass file for password authentication"
        }
        
        return {
            "status": "success",
            "message": "Database connection information (development only)",
            "connection": connection_info,
            "security_warning": "⚠️  This endpoint is only available in development mode!"
        }
        
    except Exception as e:
        logger.error(f"Database info error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get database info: {str(e)}"
        )

@router.get("/database-test")
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Test database connection and show basic info - only available in development environment
    """
    check_dev_environment()
    
    try:
        # Test basic database queries
        result = db.execute(text("SELECT current_database(), current_user, version(), now()")).fetchone()
        
        # Count some tables
        tables_info = {}
        try:
            tables_info["profiles"] = db.execute(text("SELECT COUNT(*) FROM profiles")).scalar()
            tables_info["user_roles"] = db.execute(text("SELECT COUNT(*) FROM user_roles")).scalar()
            tables_info["onboarding_configs"] = db.execute(text("SELECT COUNT(*) FROM onboarding_configs")).scalar()
            tables_info["onboarding_steps"] = db.execute(text("SELECT COUNT(*) FROM onboarding_steps")).scalar()
            tables_info["onboarding_fields"] = db.execute(text("SELECT COUNT(*) FROM onboarding_fields")).scalar()
        except Exception as e:
            tables_info["error"] = f"Could not count tables: {str(e)}"
        
        return {
            "status": "success",
            "message": "Database connection test successful",
            "database_info": {
                "current_database": result[0],
                "current_user": result[1],
                "postgres_version": result[2].split(" on ")[0],  # Clean version string
                "current_time": result[3].isoformat()
            },
            "tables_count": tables_info,
            "connection_status": "✅ Connected successfully!",
            "security_warning": "⚠️  This endpoint is only available in development mode!"
        }
        
    except Exception as e:
        logger.error(f"Database test error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection test failed: {str(e)}"
        )