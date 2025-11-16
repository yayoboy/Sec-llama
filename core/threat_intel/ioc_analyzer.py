"""
IOC (Indicator of Compromise) Analyzer
"""

import re
import socket
from typing import Dict, Any

from core.config import get_config
from core.llm_interface import get_llm
from core.prompt_templates import PromptTemplates


class IOCAnalyzer:
    """Analyze Indicators of Compromise"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()

    def analyze_ioc(self, ioc: str, ioc_type: str = "auto") -> Dict[str, Any]:
        """
        Analyze an IOC

        Args:
            ioc: The indicator (IP, domain, hash, etc.)
            ioc_type: Type of IOC (auto-detect if "auto")

        Returns:
            Analysis results
        """
        if ioc_type == "auto":
            ioc_type = self._detect_ioc_type(ioc)

        print(f"[*] Analyzing IOC: {ioc} (Type: {ioc_type})")

        # Get basic info
        info = self._get_ioc_info(ioc, ioc_type)

        # AI analysis
        analysis = self._ai_analyze_ioc(ioc, ioc_type, info)

        result = {
            "ioc": ioc,
            "type": ioc_type,
            "info": info,
            "analysis": analysis,
        }

        self._print_results(result)

        return result

    def _detect_ioc_type(self, ioc: str) -> str:
        """Auto-detect IOC type"""
        # IP address
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if re.match(ip_pattern, ioc):
            return "ip"

        # Domain
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if re.match(domain_pattern, ioc):
            return "domain"

        # MD5 hash
        if re.match(r'^[a-fA-F0-9]{32}$', ioc):
            return "md5"

        # SHA256 hash
        if re.match(r'^[a-fA-F0-9]{64}$', ioc):
            return "sha256"

        # URL
        if ioc.startswith(('http://', 'https://')):
            return "url"

        return "unknown"

    def _get_ioc_info(self, ioc: str, ioc_type: str) -> Dict[str, Any]:
        """Get basic information about IOC"""
        info = {}

        if ioc_type == "ip":
            try:
                # Reverse DNS lookup
                hostname = socket.gethostbyaddr(ioc)
                info["hostname"] = hostname[0]
            except:
                info["hostname"] = "Unknown"

            # Check if private IP
            octets = list(map(int, ioc.split('.')))
            if octets[0] == 10 or (octets[0] == 172 and 16 <= octets[1] <= 31) or (octets[0] == 192 and octets[1] == 168):
                info["is_private"] = True
            else:
                info["is_private"] = False

        elif ioc_type == "domain":
            try:
                # DNS lookup
                ip = socket.gethostbyname(ioc)
                info["ip"] = ip
            except:
                info["ip"] = "Unable to resolve"

        return info

    def _ai_analyze_ioc(self, ioc: str, ioc_type: str, info: Dict[str, Any]) -> str:
        """AI analysis of IOC"""
        print("[*] Performing AI analysis...")

        prompt = PromptTemplates.get_ioc_analysis_prompt(ioc, ioc_type)

        # Add context
        if info:
            context = "\n".join([f"{k}: {v}" for k, v in info.items()])
            prompt += f"\n\nAdditional context:\n{context}"

        try:
            analysis = self.llm.generate(prompt)
            return analysis
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")
            return "Analysis unavailable"

    def _print_results(self, result: Dict[str, Any]):
        """Print analysis results"""
        print("\n" + "=" * 80)
        print(f"IOC ANALYSIS: {result['ioc']}")
        print("=" * 80)
        print(f"Type: {result['type']}")

        if result['info']:
            print("\nBasic Information:")
            for k, v in result['info'].items():
                print(f"  - {k}: {v}")

        print("\n" + "-" * 80)
        print("AI ANALYSIS:")
        print("-" * 80)
        print(result['analysis'])
        print("=" * 80 + "\n")
