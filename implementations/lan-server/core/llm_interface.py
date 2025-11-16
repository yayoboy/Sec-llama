"""
LLM Interface for Remote Ollama and LM Studio
Supports both Ollama native API and OpenAI-compatible API (LM Studio)
"""

import requests
import json
from typing import Optional, Dict, Any, List
from .config import get_config


class LLMInterface:
    """Interface for communicating with remote LLM servers"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.provider = self.config.llm_provider.lower()

        if self.provider == "ollama":
            self.host = self.config.ollama_host
            self.model = self.config.ollama_model
            self.timeout = self.config.ollama_timeout
        elif self.provider == "lm-studio":
            self.host = self.config.lm_studio_host
            self.model = self.config.lm_studio_model
            self.api_key = self.config.lm_studio_api_key
            self.timeout = 120
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> str:
        """
        Generate text completion from prompt

        Args:
            prompt: Input prompt
            model: Override default model
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Stream response (not implemented yet)

        Returns:
            Generated text
        """
        model = model or self.model

        if self.provider == "ollama":
            return self._generate_ollama(prompt, model, temperature, max_tokens)
        elif self.provider == "lm-studio":
            return self._generate_lm_studio(prompt, model, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _generate_ollama(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Ollama native API"""
        url = f"{self.host}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.Timeout:
            raise Exception(f"Ollama request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to Ollama at {self.host}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {e}")

    def _generate_lm_studio(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using LM Studio (OpenAI-compatible API)"""
        url = f"{self.host}/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key and self.api_key != "not-needed":
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            raise Exception(f"LM Studio request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to LM Studio at {self.host}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"LM Studio API error: {e}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Chat completion with message history

        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            model: Override default model
            temperature: Sampling temperature
            max_tokens: Maximum tokens

        Returns:
            Assistant response
        """
        model = model or self.model

        if self.provider == "ollama":
            return self._chat_ollama(messages, model, temperature, max_tokens)
        elif self.provider == "lm-studio":
            return self._chat_lm_studio(messages, model, temperature, max_tokens)

    def _chat_ollama(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Chat using Ollama API"""
        url = f"{self.host}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]

        except Exception as e:
            raise Exception(f"Ollama chat error: {e}")

    def _chat_lm_studio(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Chat using LM Studio API"""
        url = f"{self.host}/v1/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.api_key and self.api_key != "not-needed":
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            raise Exception(f"LM Studio chat error: {e}")

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to LLM server

        Returns:
            Dict with status and info
        """
        try:
            if self.provider == "ollama":
                url = f"{self.host}/api/tags"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                models = response.json().get("models", [])

                return {
                    "status": "ok",
                    "provider": "ollama",
                    "host": self.host,
                    "models": [m["name"] for m in models],
                    "current_model": self.model,
                }

            elif self.provider == "lm-studio":
                url = f"{self.host}/v1/models"
                headers = {}
                if self.api_key and self.api_key != "not-needed":
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()
                models = response.json().get("data", [])

                return {
                    "status": "ok",
                    "provider": "lm-studio",
                    "host": self.host,
                    "models": [m["id"] for m in models],
                    "current_model": self.model,
                }

        except Exception as e:
            return {
                "status": "error",
                "provider": self.provider,
                "host": self.host,
                "error": str(e),
            }


# Global LLM instance
_llm: Optional[LLMInterface] = None


def get_llm() -> LLMInterface:
    """Get or create global LLM interface instance"""
    global _llm

    if _llm is None:
        _llm = LLMInterface()

    return _llm


def reload_llm():
    """Reload LLM interface (useful for config changes)"""
    global _llm
    _llm = None
    return get_llm()
