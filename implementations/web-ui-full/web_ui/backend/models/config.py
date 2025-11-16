"""
Pydantic models for Configuration
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class ConfigurationUpdate(BaseModel):
    """Request to update configuration"""
    config_data: Dict[str, Any] = Field(..., description="Configuration YAML as dict")
    backup: bool = Field(default=True, description="Create backup before update")

    class Config:
        json_schema_extra = {
            "example": {
                "config_data": {
                    "llm": {
                        "provider": "ollama",
                        "model": "llama3.1:8b"
                    }
                },
                "backup": True
            }
        }


class ConfigurationResponse(BaseModel):
    """Current configuration"""
    config_data: Dict[str, Any]
    last_modified: datetime
    version: str = "1.0.0"


class ConfigurationBackup(BaseModel):
    """Configuration backup record"""
    backup_id: str
    created_at: datetime
    config_data: Dict[str, Any]
    description: Optional[str] = None


class ConfigurationValidation(BaseModel):
    """Configuration validation result"""
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
