"""
Configuration Management for Sec-Llama
Supports both YAML config files and environment variables
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration class for Sec-Llama"""

    # LLM Configuration
    llm_provider: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_timeout: int = 120

    lm_studio_host: str = "http://localhost:1234"
    lm_studio_model: str = "local-model"
    lm_studio_api_key: str = "not-needed"

    # Database
    database_url: str = "sqlite:///./database/sec_llama.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Application
    secret_key: str = "change-me-in-production"
    jwt_secret_key: str = "change-me-in-production"
    debug: bool = False
    log_level: str = "INFO"

    # Security
    allowed_origins: list = field(default_factory=lambda: ["*"])
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # Network Settings
    max_concurrent_scans: int = 3
    default_timeout: int = 30

    # Reporting
    reports_dir: str = "./reports"
    logs_dir: str = "./logs"

    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        return cls(
            # LLM
            llm_provider=os.getenv("LLM_PROVIDER", "ollama"),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            ollama_timeout=int(os.getenv("OLLAMA_TIMEOUT", "120")),

            lm_studio_host=os.getenv("LM_STUDIO_HOST", "http://localhost:1234"),
            lm_studio_model=os.getenv("LM_STUDIO_MODEL", "local-model"),
            lm_studio_api_key=os.getenv("LM_STUDIO_API_KEY", "not-needed"),

            # Database & Redis
            database_url=os.getenv("DATABASE_URL", "sqlite:///./database/sec_llama.db"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),

            # Application
            secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
            jwt_secret_key=os.getenv("JWT_SECRET_KEY", "change-me-in-production"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),

            # Security
            allowed_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            rate_limit_window=int(os.getenv("RATE_LIMIT_WINDOW", "60")),

            # Network
            max_concurrent_scans=int(os.getenv("MAX_CONCURRENT_SCANS", "3")),
            default_timeout=int(os.getenv("DEFAULT_TIMEOUT", "30")),

            # Paths
            reports_dir=os.getenv("REPORTS_DIR", "./reports"),
            logs_dir=os.getenv("LOGS_DIR", "./logs"),
        )

    @classmethod
    def from_yaml(cls, config_path: str) -> 'Config':
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(
            llm_provider=data.get('llm', {}).get('provider', 'ollama'),
            ollama_host=data.get('llm', {}).get('base_url', 'http://localhost:11434'),
            ollama_model=data.get('llm', {}).get('model', 'llama3.1:8b'),
            ollama_timeout=data.get('llm', {}).get('timeout', 120),

            database_url=data.get('database', {}).get('url', 'sqlite:///./database/sec_llama.db'),

            secret_key=data.get('security', {}).get('secret_key', 'change-me'),
            debug=data.get('advanced', {}).get('debug_mode', False),
            log_level=data.get('logging', {}).get('level', 'INFO'),

            reports_dir=data.get('reporting', {}).get('output_dir', './reports'),
            logs_dir=data.get('logging', {}).get('file', './logs/sec-llama.log'),
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global configuration instance"""
    global _config

    if _config is None:
        # Try to load from environment first (Docker-friendly)
        _config = Config.from_env()

        # Try to load from YAML if exists
        config_path = Path("./config/config.yaml")
        if config_path.exists():
            try:
                _config = Config.from_yaml(str(config_path))
                print(f"[+] Loaded configuration from {config_path}")
            except Exception as e:
                print(f"[!] Failed to load YAML config: {e}")
                print("[*] Using environment variables")

    return _config


def reload_config():
    """Reload configuration (useful for testing)"""
    global _config
    _config = None
    return get_config()
