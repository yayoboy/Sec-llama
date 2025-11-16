"""
Configuration Management for Sec-Llama
Supports both YAML config files and environment variables with nested dataclasses
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


# ============================================================================
# NESTED CONFIGURATION DATACLASSES
# ============================================================================

@dataclass
class NetworkConfig:
    """Network scanning configuration"""
    default_timeout: int = 30
    max_concurrent_scans: int = 3
    scan_rate: int = 100  # packets per second
    interface: Optional[str] = None  # Network interface (auto-detect if None)


@dataclass
class ScanningConfig:
    """Port scanning and service detection configuration"""
    nmap_path: str = "nmap"  # Path to nmap binary
    masscan_path: str = "masscan"  # Path to masscan binary
    scan_profiles: Dict[str, Any] = field(default_factory=lambda: {
        "quick": "-T4 -F",
        "normal": "-T4 -p-",
        "thorough": "-T4 -p- -sV -sC -A",
        "stealth": "-T2 -sS -f"
    })
    max_ports: int = 65535
    service_detection: bool = True
    os_detection: bool = True


@dataclass
class WirelessConfig:
    """Wireless security scanning configuration"""
    interface: Optional[str] = None  # WiFi interface (auto-detect if None)
    monitor_mode: bool = False
    channel_hopping: bool = True
    scan_duration: int = 60  # seconds


@dataclass
class ReportingConfig:
    """Reporting and output configuration"""
    output_dir: str = "./reports"
    templates_dir: str = "./config/templates"
    pdf_enabled: bool = True
    html_enabled: bool = True
    json_enabled: bool = True
    include_screenshots: bool = False
    logo_path: Optional[str] = None


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    file: str = "./logs/sec-llama.log"
    json_format: bool = True
    rotation: str = "100 MB"
    retention: str = "30 days"


@dataclass
class SecurityConfig:
    """Application security configuration"""
    secret_key: str = "change-me-in-production"
    jwt_secret_key: str = "change-me-in-production"
    jwt_expiration_minutes: int = 1440  # 24 hours
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds


@dataclass
class LLMConfig:
    """LLM provider configuration"""
    provider: str = "ollama"  # ollama, lm-studio, openai, anthropic, etc.

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_timeout: int = 120

    # LM Studio
    lm_studio_host: str = "http://localhost:1234"
    lm_studio_model: str = "local-model"
    lm_studio_api_key: str = "not-needed"

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_base_url: Optional[str] = None

    # Anthropic
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"

    # Azure OpenAI
    azure_api_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    azure_deployment: Optional[str] = None

    # General
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "postgresql://sec_llama:sec_llama@localhost:5432/sec_llama"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class RedisConfig:
    """Redis cache configuration"""
    url: str = "redis://localhost:6379/0"
    password: Optional[str] = None
    max_connections: int = 50
    socket_timeout: int = 5


# ============================================================================
# MAIN CONFIG CLASS
# ============================================================================

@dataclass
class Config:
    """
    Main configuration class for Sec-Llama

    Organized with nested dataclasses for better structure
    """

    # Nested configurations
    llm: LLMConfig = field(default_factory=LLMConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)
    scanning: ScanningConfig = field(default_factory=ScanningConfig)
    wireless: WirelessConfig = field(default_factory=WirelessConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)

    # Application-level settings
    debug: bool = False
    app_name: str = "Sec-Llama"
    app_version: str = "2.0.0"

    # ========================================================================
    # BACKWARD COMPATIBILITY PROPERTIES
    # ========================================================================
    # These provide flat access for old code that hasn't been updated yet

    @property
    def llm_provider(self) -> str:
        """Backward compatibility"""
        return self.llm.provider

    @property
    def ollama_host(self) -> str:
        """Backward compatibility"""
        return self.llm.ollama_host

    @property
    def ollama_model(self) -> str:
        """Backward compatibility"""
        return self.llm.ollama_model

    @property
    def database_url(self) -> str:
        """Backward compatibility"""
        return self.database.url

    @property
    def redis_url(self) -> str:
        """Backward compatibility"""
        return self.redis.url

    @property
    def secret_key(self) -> str:
        """Backward compatibility"""
        return self.security.secret_key

    @property
    def jwt_secret_key(self) -> str:
        """Backward compatibility"""
        return self.security.jwt_secret_key

    @property
    def allowed_origins(self) -> List[str]:
        """Backward compatibility"""
        return self.security.allowed_origins

    @property
    def default_timeout(self) -> int:
        """Backward compatibility"""
        return self.network.default_timeout

    @property
    def max_concurrent_scans(self) -> int:
        """Backward compatibility"""
        return self.network.max_concurrent_scans

    @property
    def reports_dir(self) -> str:
        """Backward compatibility"""
        return self.reporting.output_dir

    @property
    def logs_dir(self) -> str:
        """Backward compatibility"""
        return self.logging.file.rsplit('/', 1)[0] if '/' in self.logging.file else "./logs"

    @property
    def log_level(self) -> str:
        """Backward compatibility"""
        return self.logging.level

    # ========================================================================
    # CLASS METHODS FOR LOADING CONFIG
    # ========================================================================

    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""

        # LLM Config
        llm_config = LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "ollama"),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            ollama_timeout=int(os.getenv("OLLAMA_TIMEOUT", "120")),
            lm_studio_host=os.getenv("LM_STUDIO_HOST", "http://localhost:1234"),
            lm_studio_model=os.getenv("LM_STUDIO_MODEL", "local-model"),
            lm_studio_api_key=os.getenv("LM_STUDIO_API_KEY", "not-needed"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
            openai_base_url=os.getenv("OPENAI_BASE_URL"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
            azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4096")),
            stream=os.getenv("LLM_STREAM", "false").lower() == "true",
        )

        # Network Config
        network_config = NetworkConfig(
            default_timeout=int(os.getenv("NETWORK_TIMEOUT", "30")),
            max_concurrent_scans=int(os.getenv("MAX_CONCURRENT_SCANS", "3")),
            scan_rate=int(os.getenv("NETWORK_SCAN_RATE", "100")),
            interface=os.getenv("NETWORK_INTERFACE"),
        )

        # Scanning Config
        scan_profiles_str = os.getenv("SCAN_PROFILES", "")
        scan_profiles = {}
        if scan_profiles_str:
            try:
                import json
                scan_profiles = json.loads(scan_profiles_str)
            except:
                pass

        scanning_config = ScanningConfig(
            nmap_path=os.getenv("NMAP_PATH", "nmap"),
            masscan_path=os.getenv("MASSCAN_PATH", "masscan"),
            scan_profiles=scan_profiles if scan_profiles else ScanningConfig().scan_profiles,
            max_ports=int(os.getenv("SCAN_MAX_PORTS", "65535")),
            service_detection=os.getenv("SCAN_SERVICE_DETECTION", "true").lower() == "true",
            os_detection=os.getenv("SCAN_OS_DETECTION", "true").lower() == "true",
        )

        # Wireless Config
        wireless_config = WirelessConfig(
            interface=os.getenv("WIRELESS_INTERFACE"),
            monitor_mode=os.getenv("WIRELESS_MONITOR_MODE", "false").lower() == "true",
            channel_hopping=os.getenv("WIRELESS_CHANNEL_HOPPING", "true").lower() == "true",
            scan_duration=int(os.getenv("WIRELESS_SCAN_DURATION", "60")),
        )

        # Reporting Config
        reporting_config = ReportingConfig(
            output_dir=os.getenv("REPORTS_DIR", "./reports"),
            templates_dir=os.getenv("REPORT_TEMPLATES_DIR", "./config/templates"),
            pdf_enabled=os.getenv("REPORT_PDF_ENABLED", "true").lower() == "true",
            html_enabled=os.getenv("REPORT_HTML_ENABLED", "true").lower() == "true",
            json_enabled=os.getenv("REPORT_JSON_ENABLED", "true").lower() == "true",
            include_screenshots=os.getenv("REPORT_SCREENSHOTS", "false").lower() == "true",
            logo_path=os.getenv("REPORT_LOGO_PATH"),
        )

        # Logging Config
        logging_config = LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file=os.getenv("LOG_FILE", "./logs/sec-llama.log"),
            json_format=os.getenv("LOG_JSON_FORMAT", "true").lower() == "true",
            rotation=os.getenv("LOG_ROTATION", "100 MB"),
            retention=os.getenv("LOG_RETENTION", "30 days"),
        )

        # Security Config
        allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
        allowed_origins = [o.strip() for o in allowed_origins_str.split(",")]

        security_config = SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
            jwt_secret_key=os.getenv("JWT_SECRET_KEY", "change-me-in-production"),
            jwt_expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "1440")),
            allowed_origins=allowed_origins,
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            rate_limit_window=int(os.getenv("RATE_LIMIT_WINDOW", "60")),
        )

        # Database Config
        database_config = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "postgresql://sec_llama:sec_llama@localhost:5432/sec_llama"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        )

        # Redis Config
        redis_config = RedisConfig(
            url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            password=os.getenv("REDIS_PASSWORD"),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
            socket_timeout=int(os.getenv("REDIS_SOCKET_TIMEOUT", "5")),
        )

        return cls(
            llm=llm_config,
            network=network_config,
            scanning=scanning_config,
            wireless=wireless_config,
            reporting=reporting_config,
            logging=logging_config,
            security=security_config,
            database=database_config,
            redis=redis_config,
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )

    @classmethod
    def from_yaml(cls, config_path: str) -> 'Config':
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        # Parse nested configs from YAML
        llm_data = data.get('llm', {})
        network_data = data.get('network', {})
        scanning_data = data.get('scanning', {})
        wireless_data = data.get('wireless', {})
        reporting_data = data.get('reporting', {})
        logging_data = data.get('logging', {})
        security_data = data.get('security', {})
        database_data = data.get('database', {})
        redis_data = data.get('redis', {})

        llm_config = LLMConfig(
            provider=llm_data.get('provider', 'ollama'),
            ollama_host=llm_data.get('ollama_host', 'http://localhost:11434'),
            ollama_model=llm_data.get('ollama_model', 'llama3.1:8b'),
            ollama_timeout=llm_data.get('ollama_timeout', 120),
            lm_studio_host=llm_data.get('lm_studio_host', 'http://localhost:1234'),
            lm_studio_model=llm_data.get('lm_studio_model', 'local-model'),
        )

        network_config = NetworkConfig(
            default_timeout=network_data.get('default_timeout', 30),
            max_concurrent_scans=network_data.get('max_concurrent_scans', 3),
        )

        scanning_config = ScanningConfig(
            nmap_path=scanning_data.get('nmap_path', 'nmap'),
            scan_profiles=scanning_data.get('scan_profiles', ScanningConfig().scan_profiles),
        )

        wireless_config = WirelessConfig(
            interface=wireless_data.get('interface'),
        )

        reporting_config = ReportingConfig(
            output_dir=reporting_data.get('output_dir', './reports'),
        )

        logging_config = LoggingConfig(
            level=logging_data.get('level', 'INFO'),
            file=logging_data.get('file', './logs/sec-llama.log'),
        )

        security_config = SecurityConfig(
            secret_key=security_data.get('secret_key', 'change-me'),
        )

        database_config = DatabaseConfig(
            url=database_data.get('url', 'sqlite:///./database/sec_llama.db'),
        )

        redis_config = RedisConfig(
            url=redis_data.get('url', 'redis://localhost:6379/0'),
        )

        return cls(
            llm=llm_config,
            network=network_config,
            scanning=scanning_config,
            wireless=wireless_config,
            reporting=reporting_config,
            logging=logging_config,
            security=security_config,
            database=database_config,
            redis=redis_config,
            debug=data.get('debug', False),
        )


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global configuration instance"""
    global _config

    if _config is None:
        # Try to load from environment first (Docker-friendly)
        _config = Config.from_env()

        # Try to load from YAML if exists (overrides env)
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


def set_config(config: Config):
    """Set configuration instance (useful for testing)"""
    global _config
    _config = config
