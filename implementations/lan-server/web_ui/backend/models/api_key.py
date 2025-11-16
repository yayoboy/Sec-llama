"""
Pydantic models for API Keys
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    """Request to create new API key"""
    name: str = Field(..., description="Friendly name for the API key")
    description: Optional[str] = Field(None, description="Description of key purpose")
    permissions: List[str] = Field(default=["*"], description="List of allowed tools")
    expires_at: Optional[datetime] = Field(None, description="Expiration date (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "scanner-bot",
                "description": "Automated scanning key",
                "permissions": ["network_*", "code_scan"],
                "expires_at": None
            }
        }


class APIKeyResponse(BaseModel):
    """API key information (without secret)"""
    key_id: str
    name: str
    description: Optional[str]
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    usage_count: int = 0
    is_active: bool = True


class APIKeyCreateResponse(BaseModel):
    """Response when creating new API key (includes secret once)"""
    key_id: str
    name: str
    api_key: str = Field(..., description="The actual API key - save this, it won't be shown again!")
    created_at: datetime


class APIKeyUsageStats(BaseModel):
    """Usage statistics for an API key"""
    key_id: str
    name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    last_used: Optional[datetime]
    most_used_tools: List[Dict[str, Any]] = Field(default_factory=list)
