"""
Sec-Llama Core Module
Provides core functionality for LLM integration, configuration, and prompts
"""

from .config import get_config, Config
from .llm_interface import get_llm, LLMInterface
from .prompt_templates import PromptTemplates

__all__ = [
    'get_config',
    'Config',
    'get_llm',
    'LLMInterface',
    'PromptTemplates',
]
