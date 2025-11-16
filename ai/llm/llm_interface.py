"""
LLM Interface for Sec-Llama Suite
Supports Ollama, OpenAI-compatible APIs, and local models
"""

import os
import json
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain_community.llms import Ollama
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from .config import Config, get_config


class BaseLLM(ABC):
    """Base LLM interface"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt"""
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM is available"""
        pass


class OllamaLLM(BaseLLM):
    """Ollama LLM implementation"""

    def __init__(self, config: Config):
        self.config = config
        self.model = config.llm.model
        self.base_url = config.llm.base_url
        self.temperature = config.llm.temperature
        self.client = None

        if OLLAMA_AVAILABLE:
            # Use ollama Python library
            self.client = ollama.Client(host=self.base_url)
        else:
            raise ImportError("Ollama library not installed. Run: pip install ollama")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt"""
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": kwargs.get("temperature", self.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.llm.max_tokens),
                },
            )
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion"""
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": kwargs.get("temperature", self.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.llm.max_tokens),
                },
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama chat failed: {e}")

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List available models"""
        try:
            models = self.client.list()
            return [model["name"] for model in models["models"]]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            self.client.pull(model_name)
            return True
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False


class LangChainLLM(BaseLLM):
    """LangChain-based LLM implementation"""

    def __init__(self, config: Config):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed. Run: pip install langchain langchain-community")

        self.config = config
        self.llm = Ollama(
            model=config.llm.model,
            base_url=config.llm.base_url,
            temperature=config.llm.temperature,
        )

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from prompt"""
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            raise RuntimeError(f"LangChain generation failed: {e}")

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion (convert to prompt)"""
        # Convert messages to single prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return self.generate(prompt, **kwargs)

    def is_available(self) -> bool:
        """Check if LLM is available"""
        try:
            self.llm.invoke("test")
            return True
        except Exception:
            return False

    def create_chain(self, template: str) -> LLMChain:
        """Create a LangChain chain"""
        prompt = PromptTemplate.from_template(template)
        return LLMChain(llm=self.llm, prompt=prompt)


class LLMInterface:
    """Main LLM Interface"""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        self.llm = self._init_llm()

    def _init_llm(self) -> BaseLLM:
        """Initialize LLM based on configuration"""
        provider = self.config.llm.provider.lower()

        if provider == "ollama":
            return OllamaLLM(self.config)
        elif provider == "langchain":
            return LangChainLLM(self.config)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion"""
        return self.llm.generate(prompt, **kwargs)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion"""
        return self.llm.chat(messages, **kwargs)

    def analyze_security(self, data: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze security data with LLM

        Args:
            data: Data to analyze (code, logs, scan results, etc.)
            analysis_type: Type of analysis (vulnerability, threat, log, etc.)

        Returns:
            Dictionary with analysis results
        """
        from .prompt_templates import PromptTemplates

        prompt_template = PromptTemplates.get_security_analysis_prompt(analysis_type)
        prompt = prompt_template.format(data=data)

        response = self.generate(prompt)

        return {
            "analysis_type": analysis_type,
            "input_data": data[:500] + "..." if len(data) > 500 else data,
            "analysis": response,
            "model": self.config.llm.model,
        }

    def suggest_exploit(self, service: str, version: str, context: str = "") -> Dict[str, Any]:
        """
        Suggest exploits for a service/version

        Args:
            service: Service name
            version: Service version
            context: Additional context (network, permissions, etc.)

        Returns:
            Dictionary with exploit suggestions
        """
        from .prompt_templates import PromptTemplates

        prompt = PromptTemplates.get_exploit_suggestion_prompt(service, version, context)
        response = self.generate(prompt)

        return {
            "service": service,
            "version": version,
            "context": context,
            "suggestions": response,
        }

    def plan_attack(self, target_info: Dict[str, Any], objective: str) -> str:
        """
        Plan an attack chain based on target information

        Args:
            target_info: Information about the target (services, vulnerabilities, etc.)
            objective: Attack objective (e.g., "gain domain admin")

        Returns:
            Attack plan as string
        """
        from .prompt_templates import PromptTemplates

        prompt = PromptTemplates.get_attack_planning_prompt(target_info, objective)
        return self.generate(prompt)

    def analyze_vulnerability(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code for vulnerabilities

        Args:
            code: Source code to analyze
            language: Programming language

        Returns:
            Dictionary with vulnerability analysis
        """
        from .prompt_templates import PromptTemplates

        prompt = PromptTemplates.get_code_vulnerability_prompt(code, language)
        response = self.generate(prompt)

        return {
            "language": language,
            "code_snippet": code[:200] + "..." if len(code) > 200 else code,
            "vulnerabilities": response,
        }

    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.llm.is_available()


# Global LLM instance
_llm_instance: Optional[LLMInterface] = None


def get_llm(config: Optional[Config] = None) -> LLMInterface:
    """Get global LLM instance (singleton)"""
    global _llm_instance
    if _llm_instance is None or config:
        _llm_instance = LLMInterface(config)
    return _llm_instance
