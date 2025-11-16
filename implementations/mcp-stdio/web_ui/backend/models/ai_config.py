"""
AI Configuration Models

Pydantic models for AI/LLM configuration management.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class OllamaConfig(BaseModel):
    """Ollama server configuration"""
    host: str = Field(..., description="Ollama server host (e.g., http://localhost:11434)")
    timeout: int = Field(default=120, description="Request timeout in seconds")
    enabled: bool = Field(default=True, description="Enable Ollama integration")


class AIModel(BaseModel):
    """AI Model information"""
    name: str = Field(..., description="Model name")
    size: Optional[int] = Field(None, description="Model size in bytes")
    modified_at: Optional[datetime] = Field(None, description="Last modification time")
    digest: Optional[str] = Field(None, description="Model digest/hash")
    format: Optional[str] = Field(None, description="Model format")
    family: Optional[str] = Field(None, description="Model family")
    parameter_size: Optional[str] = Field(None, description="Parameter size (e.g., 8B, 70B)")
    quantization: Optional[str] = Field(None, description="Quantization level")


class ModelPullRequest(BaseModel):
    """Request to pull/download a model"""
    model_name: str = Field(..., description="Model name to pull (e.g., llama3.1:8b)")
    insecure: bool = Field(default=False, description="Allow insecure connections")


class ModelPullProgress(BaseModel):
    """Model pull progress information"""
    status: str = Field(..., description="Current status")
    digest: Optional[str] = None
    total: Optional[int] = None
    completed: Optional[int] = None


class ModelDeleteRequest(BaseModel):
    """Request to delete a model"""
    model_name: str = Field(..., description="Model name to delete")


class AIProviderConfig(BaseModel):
    """External AI provider configuration"""
    provider_type: str = Field(..., description="Provider type (openai, anthropic, cohere, etc.)")
    api_key: Optional[str] = Field(None, description="API key for the provider")
    api_url: Optional[str] = Field(None, description="Custom API URL")
    model: Optional[str] = Field(None, description="Default model to use")
    enabled: bool = Field(default=False, description="Enable this provider")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional parameters")


class AIConfiguration(BaseModel):
    """Complete AI configuration"""
    ollama: OllamaConfig
    default_model: str = Field(default="llama3.1:8b", description="Default model to use")
    providers: List[AIProviderConfig] = Field(default_factory=list, description="External AI providers")
    fallback_enabled: bool = Field(default=False, description="Enable fallback to external providers")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Default temperature")
    max_tokens: int = Field(default=2048, gt=0, description="Maximum tokens to generate")


class AIConfigurationUpdate(BaseModel):
    """Update AI configuration"""
    ollama: Optional[OllamaConfig] = None
    default_model: Optional[str] = None
    providers: Optional[List[AIProviderConfig]] = None
    fallback_enabled: Optional[bool] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)


class ConnectionTestRequest(BaseModel):
    """Test connection to AI service"""
    host: str = Field(..., description="Host to test")
    timeout: int = Field(default=10, description="Timeout in seconds")


class ConnectionTestResponse(BaseModel):
    """Connection test result"""
    success: bool
    message: str
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    models_available: Optional[int] = Field(None, description="Number of models available")
    version: Optional[str] = Field(None, description="Server version")


class ModelGenerateRequest(BaseModel):
    """Test model generation"""
    model: str = Field(..., description="Model to test")
    prompt: str = Field(default="Hello, how are you?", description="Test prompt")
    max_tokens: int = Field(default=50, description="Maximum tokens to generate")


class ModelGenerateResponse(BaseModel):
    """Model generation result"""
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    duration: Optional[float] = Field(None, description="Generation time in seconds")
    tokens: Optional[int] = Field(None, description="Tokens generated")
