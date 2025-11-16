"""
AI Configuration API Routes

Endpoints for managing AI/LLM configuration and models.
"""

import time
import asyncio
import os
from typing import List
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException
import httpx
import yaml

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.ai_config import (
    AIConfiguration,
    AIConfigurationUpdate,
    OllamaConfig,
    AIModel,
    ModelPullRequest,
    ModelPullProgress,
    ModelDeleteRequest,
    ConnectionTestRequest,
    ConnectionTestResponse,
    ModelGenerateRequest,
    ModelGenerateResponse
)

router = APIRouter()

# Configuration file path - use environment variable or relative path
CONFIG_DIR = Path(os.getenv("CONFIG_DIR", "./config"))
CONFIG_PATH = CONFIG_DIR / "mcp_server_config.yaml"

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load configuration from YAML"""
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def save_config(config: dict):
    """Save configuration to YAML"""
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)


def get_ollama_host() -> str:
    """Get Ollama host from config or environment"""
    import os
    config = load_config()
    return config.get('ollama', {}).get('host', os.getenv('OLLAMA_HOST', 'http://localhost:11434'))


@router.get("", response_model=AIConfiguration)
async def get_ai_configuration():
    """
    Get current AI configuration

    Returns:
        Current AI configuration including Ollama and provider settings
    """
    try:
        config = load_config()

        # Extract AI-related configuration
        ollama_config = config.get('ollama', {})

        ai_config = AIConfiguration(
            ollama=OllamaConfig(
                host=ollama_config.get('host', 'http://localhost:11434'),
                timeout=ollama_config.get('timeout', 120),
                enabled=ollama_config.get('enabled', True)
            ),
            default_model=ollama_config.get('model', 'llama3.1:8b'),
            providers=config.get('ai_providers', []),
            fallback_enabled=config.get('ai_fallback_enabled', False),
            temperature=ollama_config.get('temperature', 0.7),
            max_tokens=ollama_config.get('max_tokens', 2048)
        )

        return ai_config

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading AI configuration: {str(e)}")


@router.put("")
async def update_ai_configuration(update: AIConfigurationUpdate):
    """
    Update AI configuration

    Args:
        update: Configuration updates

    Returns:
        Success message
    """
    try:
        config = load_config()

        # Ensure ollama section exists
        if 'ollama' not in config:
            config['ollama'] = {}

        # Update Ollama configuration
        if update.ollama:
            config['ollama']['host'] = update.ollama.host
            config['ollama']['timeout'] = update.ollama.timeout
            config['ollama']['enabled'] = update.ollama.enabled

        # Update other AI settings
        if update.default_model:
            config['ollama']['model'] = update.default_model

        if update.providers is not None:
            config['ai_providers'] = [p.dict() for p in update.providers]

        if update.fallback_enabled is not None:
            config['ai_fallback_enabled'] = update.fallback_enabled

        if update.temperature is not None:
            config['ollama']['temperature'] = update.temperature

        if update.max_tokens is not None:
            config['ollama']['max_tokens'] = update.max_tokens

        # Save configuration
        save_config(config)

        return {
            "message": "AI configuration updated successfully",
            "restart_required": True
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating AI configuration: {str(e)}")


@router.get("/models", response_model=List[AIModel])
async def list_models():
    """
    List available AI models from Ollama

    Returns:
        List of available models
    """
    try:
        ollama_host = get_ollama_host()

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{ollama_host}/api/tags")
            response.raise_for_status()

            data = response.json()
            models = []

            for model_data in data.get('models', []):
                models.append(AIModel(
                    name=model_data.get('name'),
                    size=model_data.get('size'),
                    modified_at=model_data.get('modified_at'),
                    digest=model_data.get('digest'),
                    format=model_data.get('details', {}).get('format'),
                    family=model_data.get('details', {}).get('family'),
                    parameter_size=model_data.get('details', {}).get('parameter_size'),
                    quantization=model_data.get('details', {}).get('quantization_level')
                ))

            return models

    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Ollama server not available: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")


@router.post("/models/pull")
async def pull_model(request: ModelPullRequest):
    """
    Pull/download a model from Ollama registry

    Args:
        request: Model pull request

    Returns:
        Pull status
    """
    try:
        ollama_host = get_ollama_host()

        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{ollama_host}/api/pull",
                json={
                    "name": request.model_name,
                    "insecure": request.insecure
                }
            )
            response.raise_for_status()

            return {
                "message": f"Started pulling model: {request.model_name}",
                "model_name": request.model_name,
                "status": "pulling"
            }

    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Ollama server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error pulling model: {str(e)}")


@router.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a model from Ollama

    Args:
        model_name: Name of model to delete

    Returns:
        Deletion status
    """
    try:
        ollama_host = get_ollama_host()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(
                f"{ollama_host}/api/delete",
                json={"name": model_name}
            )
            response.raise_for_status()

            return {
                "message": f"Model deleted successfully: {model_name}",
                "model_name": model_name
            }

    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Ollama server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting model: {str(e)}")


@router.post("/test-connection", response_model=ConnectionTestResponse)
async def test_connection(request: ConnectionTestRequest):
    """
    Test connection to AI service

    Args:
        request: Connection test request

    Returns:
        Connection test result
    """
    try:
        start_time = time.time()

        async with httpx.AsyncClient(timeout=request.timeout) as client:
            response = await client.get(f"{request.host}/api/tags")
            response.raise_for_status()

            response_time = time.time() - start_time
            data = response.json()

            # Try to get version
            version = None
            try:
                version_response = await client.get(f"{request.host}/api/version")
                if version_response.status_code == 200:
                    version = version_response.json().get('version')
            except:
                pass

            return ConnectionTestResponse(
                success=True,
                message="Connection successful",
                response_time=response_time,
                models_available=len(data.get('models', [])),
                version=version
            )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message=f"Connection timeout after {request.timeout}s"
        )
    except httpx.HTTPError as e:
        return ConnectionTestResponse(
            success=False,
            message=f"Connection failed: {str(e)}"
        )
    except Exception as e:
        return ConnectionTestResponse(
            success=False,
            message=f"Unexpected error: {str(e)}"
        )


@router.post("/test-generation", response_model=ModelGenerateResponse)
async def test_generation(request: ModelGenerateRequest):
    """
    Test model generation

    Args:
        request: Generation test request

    Returns:
        Generation test result
    """
    try:
        ollama_host = get_ollama_host()
        start_time = time.time()

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ollama_host}/api/generate",
                json={
                    "model": request.model,
                    "prompt": request.prompt,
                    "stream": False,
                    "options": {
                        "num_predict": request.max_tokens
                    }
                }
            )
            response.raise_for_status()

            duration = time.time() - start_time
            data = response.json()

            return ModelGenerateResponse(
                success=True,
                response=data.get('response', ''),
                duration=duration,
                tokens=data.get('eval_count', 0)
            )

    except httpx.HTTPError as e:
        return ModelGenerateResponse(
            success=False,
            error=f"Generation failed: {str(e)}"
        )
    except Exception as e:
        return ModelGenerateResponse(
            success=False,
            error=f"Unexpected error: {str(e)}"
        )


@router.get("/models/{model_name}/info")
async def get_model_info(model_name: str):
    """
    Get detailed information about a specific model

    Args:
        model_name: Model name

    Returns:
        Model details
    """
    try:
        ollama_host = get_ollama_host()

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ollama_host}/api/show",
                json={"name": model_name}
            )
            response.raise_for_status()

            data = response.json()

            return {
                "model_name": model_name,
                "modelfile": data.get('modelfile'),
                "parameters": data.get('parameters'),
                "template": data.get('template'),
                "details": data.get('details'),
                "model_info": data.get('model_info')
            }

    except httpx.HTTPError as e:
        raise HTTPException(status_code=404, detail=f"Model not found or error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model info: {str(e)}")


@router.get("/status")
async def get_ai_status():
    """
    Get AI service status

    Returns:
        Status of all AI services
    """
    try:
        ollama_host = get_ollama_host()

        # Test Ollama
        ollama_status = "offline"
        ollama_models = 0
        ollama_error = None

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{ollama_host}/api/tags")
                if response.status_code == 200:
                    ollama_status = "online"
                    data = response.json()
                    ollama_models = len(data.get('models', []))
        except Exception as e:
            ollama_error = str(e)

        return {
            "ollama": {
                "status": ollama_status,
                "host": ollama_host,
                "models_available": ollama_models,
                "error": ollama_error
            },
            "providers": [],  # TODO: Check external providers
            "overall_status": ollama_status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking AI status: {str(e)}")
