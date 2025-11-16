"""
Configuration API Routes

Provides endpoints for managing MCP server configuration.
"""

from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path
import shutil
import yaml

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.config import (
    ConfigurationResponse,
    ConfigurationUpdate,
    ConfigurationBackup,
    ConfigurationValidation
)

router = APIRouter()

# Configuration file path
CONFIG_PATH = Path("/home/user/Sec-llama/config/mcp_server_config.yaml")
BACKUP_DIR = Path("/home/user/Sec-llama/config/backups")


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def save_config(config_data: Dict[str, Any], create_backup: bool = True) -> None:
    """Save configuration to YAML file"""
    if create_backup:
        create_config_backup()

    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)


def create_config_backup() -> str:
    """Create backup of current configuration"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"config_backup_{timestamp}.yaml"

    shutil.copy2(CONFIG_PATH, backup_file)

    return str(backup_file)


def validate_config(config_data: Dict[str, Any]) -> ConfigurationValidation:
    """Validate configuration data"""
    errors = []
    warnings = []

    # Check required sections
    required_sections = ["server", "transport", "auth", "security"]
    for section in required_sections:
        if section not in config_data:
            errors.append(f"Missing required section: {section}")

    # Validate server section
    if "server" in config_data:
        if "name" not in config_data["server"]:
            errors.append("Missing server.name")
        if "version" not in config_data["server"]:
            warnings.append("Missing server.version")

    # Validate transport section
    if "transport" in config_data:
        transport = config_data["transport"]

        if "stdio" not in transport and "http" not in transport:
            errors.append("At least one transport (stdio or http) must be configured")

        if "http" in transport:
            http_config = transport["http"]
            if http_config.get("enabled", False):
                if "host" not in http_config:
                    warnings.append("Missing transport.http.host")
                if "port" not in http_config:
                    warnings.append("Missing transport.http.port")

    # Validate auth section
    if "auth" in config_data:
        auth = config_data["auth"]

        if auth.get("type") == "api_key":
            if "api_keys" not in auth or not auth["api_keys"]:
                warnings.append("API key authentication enabled but no keys configured")

    # Validate security section
    if "security" in config_data:
        security = config_data["security"]

        if "allowed_networks" in security:
            networks = security["allowed_networks"]
            if not isinstance(networks, list):
                errors.append("security.allowed_networks must be a list")

    return ConfigurationValidation(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


@router.get("", response_model=ConfigurationResponse)
async def get_configuration():
    """
    Get current configuration

    Returns:
        Current configuration data
    """
    try:
        config_data = load_config()

        # Get file modification time
        last_modified = datetime.fromtimestamp(CONFIG_PATH.stat().st_mtime)

        return ConfigurationResponse(
            config_data=config_data,
            last_modified=last_modified,
            file_path=str(CONFIG_PATH)
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading configuration: {str(e)}")


@router.put("")
async def update_configuration(update: ConfigurationUpdate):
    """
    Update configuration

    Args:
        update: Configuration update data

    Returns:
        Success message with validation results
    """
    try:
        # Validate new configuration
        validation = validate_config(update.config_data)

        if not validation.valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid configuration",
                    "errors": validation.errors,
                    "warnings": validation.warnings
                }
            )

        # Save configuration
        save_config(update.config_data, create_backup=update.backup)

        return {
            "message": "Configuration updated successfully",
            "validation": validation.dict(),
            "backup_created": update.backup
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating configuration: {str(e)}")


@router.post("/validate", response_model=ConfigurationValidation)
async def validate_configuration(config_data: Dict[str, Any]):
    """
    Validate configuration without saving

    Args:
        config_data: Configuration to validate

    Returns:
        Validation results
    """
    try:
        validation = validate_config(config_data)
        return validation

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating configuration: {str(e)}")


@router.post("/backup", response_model=ConfigurationBackup)
async def create_backup():
    """
    Create backup of current configuration

    Returns:
        Backup information
    """
    try:
        backup_path = create_config_backup()
        created_at = datetime.utcnow()

        return ConfigurationBackup(
            backup_id=Path(backup_path).stem,
            file_path=backup_path,
            created_at=created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating backup: {str(e)}")


@router.get("/backups")
async def list_backups():
    """
    List all configuration backups

    Returns:
        List of backup files
    """
    try:
        if not BACKUP_DIR.exists():
            return []

        backups = []
        for backup_file in sorted(BACKUP_DIR.glob("config_backup_*.yaml"), reverse=True):
            created_at = datetime.fromtimestamp(backup_file.stat().st_mtime)
            backups.append({
                "backup_id": backup_file.stem,
                "file_path": str(backup_file),
                "created_at": created_at.isoformat(),
                "size_bytes": backup_file.stat().st_size
            })

        return backups

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing backups: {str(e)}")


@router.post("/restore/{backup_id}")
async def restore_backup(backup_id: str):
    """
    Restore configuration from backup

    Args:
        backup_id: Backup ID to restore

    Returns:
        Success message
    """
    try:
        backup_file = BACKUP_DIR / f"{backup_id}.yaml"

        if not backup_file.exists():
            raise HTTPException(status_code=404, detail=f"Backup '{backup_id}' not found")

        # Create backup of current config before restoring
        current_backup = create_config_backup()

        # Restore from backup
        shutil.copy2(backup_file, CONFIG_PATH)

        return {
            "message": f"Configuration restored from backup '{backup_id}'",
            "previous_backup": current_backup
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restoring backup: {str(e)}")


@router.get("/download")
async def download_configuration():
    """
    Download current configuration file

    Returns:
        Configuration file
    """
    try:
        if not CONFIG_PATH.exists():
            raise HTTPException(status_code=404, detail="Configuration file not found")

        return FileResponse(
            path=CONFIG_PATH,
            media_type="application/x-yaml",
            filename="mcp_server_config.yaml"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading configuration: {str(e)}")


@router.get("/schema")
async def get_configuration_schema():
    """
    Get configuration schema/template

    Returns:
        Configuration schema with descriptions
    """
    return {
        "server": {
            "name": "sec-llama",
            "version": "1.0.0",
            "_description": "Server identification"
        },
        "transport": {
            "stdio": {
                "enabled": True,
                "_description": "Standard I/O transport for local usage"
            },
            "http": {
                "enabled": True,
                "host": "0.0.0.0",
                "port": 8765,
                "_description": "HTTP/SSE transport for LAN usage"
            }
        },
        "auth": {
            "type": "api_key",
            "api_keys": [
                {
                    "name": "admin",
                    "key": "your_api_key_here",
                    "permissions": ["*"]
                }
            ],
            "_description": "Authentication configuration"
        },
        "rate_limiting": {
            "enabled": True,
            "default_limit": "100/hour",
            "tool_limits": {},
            "_description": "Rate limiting for tool execution"
        },
        "security": {
            "require_confirmation": True,
            "allowed_networks": ["192.168.0.0/16", "10.0.0.0/8"],
            "blocked_ips": [],
            "_description": "Security and access control"
        },
        "ollama": {
            "host": "http://localhost:11434",
            "model": "llama3.1:8b",
            "timeout": 120,
            "_description": "Ollama LLM configuration"
        }
    }
