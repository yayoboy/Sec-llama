"""
API Keys Management Routes

Provides endpoints for managing MCP server API keys.
"""

from datetime import datetime
from typing import List, Optional
import sys
import os
from pathlib import Path
import secrets
import hashlib
import json

from fastapi import APIRouter, HTTPException

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.api_key import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyCreateResponse,
    APIKeyUpdate,
    APIKeyUsageStats
)

router = APIRouter()

# API Keys database file (simple JSON for now) - use environment variable or relative path
DB_DIR = Path(os.getenv("DATABASE_DIR", "./database"))
KEYS_DB_PATH = DB_DIR / "api_keys.json"

# Ensure database directory exists
DB_DIR.mkdir(parents=True, exist_ok=True)


def load_keys_db() -> dict:
    """Load API keys database"""
    if not KEYS_DB_PATH.exists():
        KEYS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return {"keys": {}, "usage": {}}

    with open(KEYS_DB_PATH, 'r') as f:
        return json.load(f)


def save_keys_db(db: dict) -> None:
    """Save API keys database"""
    KEYS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(KEYS_DB_PATH, 'w') as f:
        json.dump(db, f, indent=2, default=str)


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()


def generate_api_key() -> str:
    """Generate a new API key"""
    return secrets.token_urlsafe(32)


@router.get("", response_model=List[APIKeyResponse])
async def list_api_keys():
    """
    List all API keys (without revealing the actual keys)

    Returns:
        List of API key metadata
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        response = []
        for key_id, key_data in keys.items():
            response.append(APIKeyResponse(
                key_id=key_id,
                name=key_data["name"],
                description=key_data.get("description"),
                permissions=key_data["permissions"],
                created_at=datetime.fromisoformat(key_data["created_at"]),
                expires_at=datetime.fromisoformat(key_data["expires_at"]) if key_data.get("expires_at") else None,
                last_used_at=datetime.fromisoformat(key_data["last_used_at"]) if key_data.get("last_used_at") else None,
                is_active=key_data["is_active"]
            ))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing API keys: {str(e)}")


@router.post("", response_model=APIKeyCreateResponse)
async def create_api_key(key_create: APIKeyCreate):
    """
    Create a new API key

    Args:
        key_create: API key creation data

    Returns:
        Created API key (only time the key is shown!)
    """
    try:
        db = load_keys_db()

        # Generate new API key
        api_key = generate_api_key()
        key_hash = hash_api_key(api_key)
        key_id = secrets.token_urlsafe(16)

        # Create key data
        key_data = {
            "name": key_create.name,
            "description": key_create.description,
            "key_hash": key_hash,
            "permissions": key_create.permissions,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": key_create.expires_at.isoformat() if key_create.expires_at else None,
            "last_used_at": None,
            "is_active": True
        }

        # Save to database
        if "keys" not in db:
            db["keys"] = {}
        db["keys"][key_id] = key_data

        # Initialize usage stats
        if "usage" not in db:
            db["usage"] = {}
        db["usage"][key_id] = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "last_24h_requests": 0
        }

        save_keys_db(db)

        return APIKeyCreateResponse(
            key_id=key_id,
            api_key=api_key,
            name=key_create.name,
            description=key_create.description,
            permissions=key_create.permissions,
            created_at=datetime.utcnow(),
            expires_at=key_create.expires_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating API key: {str(e)}")


@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(key_id: str):
    """
    Get API key information

    Args:
        key_id: API key ID

    Returns:
        API key metadata
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        key_data = keys[key_id]

        return APIKeyResponse(
            key_id=key_id,
            name=key_data["name"],
            description=key_data.get("description"),
            permissions=key_data["permissions"],
            created_at=datetime.fromisoformat(key_data["created_at"]),
            expires_at=datetime.fromisoformat(key_data["expires_at"]) if key_data.get("expires_at") else None,
            last_used_at=datetime.fromisoformat(key_data["last_used_at"]) if key_data.get("last_used_at") else None,
            is_active=key_data["is_active"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching API key: {str(e)}")


@router.patch("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(key_id: str, update: APIKeyUpdate):
    """
    Update API key

    Args:
        key_id: API key ID
        update: Update data

    Returns:
        Updated API key metadata
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        key_data = keys[key_id]

        # Update fields
        if update.name is not None:
            key_data["name"] = update.name
        if update.description is not None:
            key_data["description"] = update.description
        if update.permissions is not None:
            key_data["permissions"] = update.permissions
        if update.expires_at is not None:
            key_data["expires_at"] = update.expires_at.isoformat()
        if update.is_active is not None:
            key_data["is_active"] = update.is_active

        save_keys_db(db)

        return APIKeyResponse(
            key_id=key_id,
            name=key_data["name"],
            description=key_data.get("description"),
            permissions=key_data["permissions"],
            created_at=datetime.fromisoformat(key_data["created_at"]),
            expires_at=datetime.fromisoformat(key_data["expires_at"]) if key_data.get("expires_at") else None,
            last_used_at=datetime.fromisoformat(key_data["last_used_at"]) if key_data.get("last_used_at") else None,
            is_active=key_data["is_active"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating API key: {str(e)}")


@router.delete("/{key_id}")
async def delete_api_key(key_id: str):
    """
    Delete an API key

    Args:
        key_id: API key ID

    Returns:
        Success message
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        # Remove key and usage stats
        del keys[key_id]
        if "usage" in db and key_id in db["usage"]:
            del db["usage"][key_id]

        save_keys_db(db)

        return {
            "message": f"API key '{key_id}' deleted successfully",
            "key_id": key_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting API key: {str(e)}")


@router.post("/{key_id}/revoke")
async def revoke_api_key(key_id: str):
    """
    Revoke an API key (disable without deleting)

    Args:
        key_id: API key ID

    Returns:
        Success message
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        keys[key_id]["is_active"] = False
        save_keys_db(db)

        return {
            "message": f"API key '{key_id}' revoked successfully",
            "key_id": key_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error revoking API key: {str(e)}")


@router.post("/{key_id}/activate")
async def activate_api_key(key_id: str):
    """
    Activate a revoked API key

    Args:
        key_id: API key ID

    Returns:
        Success message
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        keys[key_id]["is_active"] = True
        save_keys_db(db)

        return {
            "message": f"API key '{key_id}' activated successfully",
            "key_id": key_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error activating API key: {str(e)}")


@router.get("/{key_id}/usage", response_model=APIKeyUsageStats)
async def get_api_key_usage(key_id: str):
    """
    Get usage statistics for an API key

    Args:
        key_id: API key ID

    Returns:
        Usage statistics
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})
        usage = db.get("usage", {})

        if key_id not in keys:
            raise HTTPException(status_code=404, detail=f"API key '{key_id}' not found")

        if key_id not in usage:
            usage[key_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "last_24h_requests": 0
            }

        usage_data = usage[key_id]

        return APIKeyUsageStats(
            key_id=key_id,
            total_requests=usage_data["total_requests"],
            successful_requests=usage_data["successful_requests"],
            failed_requests=usage_data["failed_requests"],
            last_24h_requests=usage_data["last_24h_requests"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching usage stats: {str(e)}")


@router.post("/verify")
async def verify_api_key(api_key: str):
    """
    Verify if an API key is valid

    Args:
        api_key: API key to verify

    Returns:
        Verification result
    """
    try:
        db = load_keys_db()
        keys = db.get("keys", {})

        key_hash = hash_api_key(api_key)

        # Find matching key
        for key_id, key_data in keys.items():
            if key_data["key_hash"] == key_hash:
                # Check if active
                if not key_data["is_active"]:
                    return {
                        "valid": False,
                        "reason": "API key is revoked"
                    }

                # Check if expired
                if key_data.get("expires_at"):
                    expires_at = datetime.fromisoformat(key_data["expires_at"])
                    if datetime.utcnow() > expires_at:
                        return {
                            "valid": False,
                            "reason": "API key has expired"
                        }

                return {
                    "valid": True,
                    "key_id": key_id,
                    "name": key_data["name"],
                    "permissions": key_data["permissions"]
                }

        return {
            "valid": False,
            "reason": "API key not found"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying API key: {str(e)}")
