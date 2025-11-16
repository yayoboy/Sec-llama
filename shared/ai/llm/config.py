"""
Configuration management for Sec-Llama Suite
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    """LLM Configuration"""
    provider: str = "ollama"
    model: str = "llama3.1:8b"
    base_url: str = "http://localhost:11434"
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 120


@dataclass
class NetworkConfig:
    """Network Security Configuration"""
    default_timeout: int = 30
    max_threads: int = 10
    stealth_mode: bool = False
    interface: str = "eth0"
    scan_profiles: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class ScanningConfig:
    """Scanning Tools Configuration"""
    nmap_path: str = "/usr/bin/nmap"
    nmap_default_args: str = "-sV -sC --open"
    masscan_path: str = "/usr/bin/masscan"
    masscan_rate: int = 1000
    nuclei_path: str = "/usr/bin/nuclei"
    nuclei_templates_path: str = "/usr/share/nuclei-templates"


@dataclass
class ReportingConfig:
    """Reporting Configuration"""
    output_dir: str = "./reports"
    format: str = "pdf"
    include_screenshots: bool = True
    executive_summary: bool = True
    severity_threshold: str = "MEDIUM"


@dataclass
class DatabaseConfig:
    """Database Configuration"""
    type: str = "sqlite"
    path: str = "./database"


@dataclass
class LoggingConfig:
    """Logging Configuration"""
    level: str = "INFO"
    file: str = "./logs/sec-llama.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Config:
    """Main configuration class"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration"""
        self.config_path = config_path or self._find_config()
        self.data = self._load_config()

        # Initialize sub-configs
        self.llm = self._init_llm_config()
        self.network = self._init_network_config()
        self.scanning = self._init_scanning_config()
        self.reporting = self._init_reporting_config()
        self.database = self._init_database_config()
        self.logging = self._init_logging_config()

    def _find_config(self) -> str:
        """Find configuration file"""
        possible_paths = [
            "./config/config.yaml",
            "./config.yaml",
            os.path.expanduser("~/.sec-llama/config.yaml"),
            "/etc/sec-llama/config.yaml",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        # If no config found, use example config
        return "./config/config.example.yaml"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Warning: Config file not found: {self.config_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return {}

    def _init_llm_config(self) -> LLMConfig:
        """Initialize LLM configuration"""
        llm_data = self.data.get("llm", {})
        return LLMConfig(
            provider=llm_data.get("provider", "ollama"),
            model=llm_data.get("model", "llama3.1:8b"),
            base_url=llm_data.get("base_url", "http://localhost:11434"),
            api_key=llm_data.get("api_key"),
            temperature=llm_data.get("temperature", 0.7),
            max_tokens=llm_data.get("max_tokens", 4096),
            timeout=llm_data.get("timeout", 120),
        )

    def _init_network_config(self) -> NetworkConfig:
        """Initialize network configuration"""
        net_data = self.data.get("network", {})
        return NetworkConfig(
            default_timeout=net_data.get("default_timeout", 30),
            max_threads=net_data.get("max_threads", 10),
            stealth_mode=net_data.get("stealth_mode", False),
            interface=net_data.get("interface", "eth0"),
            scan_profiles=net_data.get("scan_profiles", {}),
        )

    def _init_scanning_config(self) -> ScanningConfig:
        """Initialize scanning configuration"""
        scan_data = self.data.get("scanning", {})
        nmap_data = scan_data.get("nmap", {})
        masscan_data = scan_data.get("masscan", {})
        nuclei_data = scan_data.get("nuclei", {})

        return ScanningConfig(
            nmap_path=nmap_data.get("path", "/usr/bin/nmap"),
            nmap_default_args=nmap_data.get("default_args", "-sV -sC --open"),
            masscan_path=masscan_data.get("path", "/usr/bin/masscan"),
            masscan_rate=masscan_data.get("rate", 1000),
            nuclei_path=nuclei_data.get("path", "/usr/bin/nuclei"),
            nuclei_templates_path=nuclei_data.get(
                "templates_path", "/usr/share/nuclei-templates"
            ),
        )

    def _init_reporting_config(self) -> ReportingConfig:
        """Initialize reporting configuration"""
        report_data = self.data.get("reporting", {})
        return ReportingConfig(
            output_dir=report_data.get("output_dir", "./reports"),
            format=report_data.get("format", "pdf"),
            include_screenshots=report_data.get("include_screenshots", True),
            executive_summary=report_data.get("executive_summary", True),
            severity_threshold=report_data.get("severity_threshold", "MEDIUM"),
        )

    def _init_database_config(self) -> DatabaseConfig:
        """Initialize database configuration"""
        db_data = self.data.get("database", {})
        return DatabaseConfig(
            type=db_data.get("type", "sqlite"),
            path=db_data.get("path", "./database"),
        )

    def _init_logging_config(self) -> LoggingConfig:
        """Initialize logging configuration"""
        log_data = self.data.get("logging", {})
        return LoggingConfig(
            level=log_data.get("level", "INFO"),
            file=log_data.get("file", "./logs/sec-llama.log"),
            format=log_data.get(
                "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split(".")
        value = self.data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value


# Global config instance
_config: Optional[Config] = None


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration (singleton)"""
    global _config
    if _config is None or config_path:
        _config = Config(config_path)
    return _config


def get_config() -> Config:
    """Get current configuration"""
    global _config
    if _config is None:
        _config = load_config()
    return _config
