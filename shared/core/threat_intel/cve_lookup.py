"""
CVE Lookup and Analysis Module
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime

from core.config import get_config
from core.llm_interface import get_llm


class CVELookup:
    """CVE database lookup and analysis"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def lookup_cve(self, cve_id: str) -> Dict[str, Any]:
        """
        Lookup CVE information

        Args:
            cve_id: CVE ID (e.g., CVE-2024-1234)

        Returns:
            CVE information dictionary
        """
        print(f"[*] Looking up {cve_id}...")

        try:
            # Query NVD API
            response = requests.get(
                f"{self.nvd_api_url}",
                params={"cveId": cve_id},
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("vulnerabilities"):
                    cve_item = data["vulnerabilities"][0]["cve"]

                    cve_info = {
                        "id": cve_id,
                        "description": cve_item.get("descriptions", [{}])[0].get("value", ""),
                        "published": cve_item.get("published", ""),
                        "modified": cve_item.get("lastModified", ""),
                        "cvss_score": self._extract_cvss(cve_item),
                        "references": [ref.get("url") for ref in cve_item.get("references", [])],
                        "cpes": self._extract_cpes(cve_item),
                    }

                    # AI analysis
                    self._analyze_cve_with_ai(cve_info)

                    return cve_info

            print(f"[!] CVE not found: {cve_id}")
            return {}

        except requests.RequestException as e:
            print(f"[!] API request failed: {e}")
            return {}
        except Exception as e:
            print(f"[!] CVE lookup failed: {e}")
            return {}

    def _extract_cvss(self, cve_item: Dict) -> Dict[str, Any]:
        """Extract CVSS score"""
        metrics = cve_item.get("metrics", {})

        # Try CVSSv3 first
        if "cvssMetricV31" in metrics:
            cvss = metrics["cvssMetricV31"][0]["cvssData"]
            return {
                "version": "3.1",
                "score": cvss.get("baseScore", 0),
                "severity": cvss.get("baseSeverity", "UNKNOWN"),
                "vector": cvss.get("vectorString", ""),
            }
        elif "cvssMetricV30" in metrics:
            cvss = metrics["cvssMetricV30"][0]["cvssData"]
            return {
                "version": "3.0",
                "score": cvss.get("baseScore", 0),
                "severity": cvss.get("baseSeverity", "UNKNOWN"),
                "vector": cvss.get("vectorString", ""),
            }

        return {"version": "N/A", "score": 0, "severity": "UNKNOWN"}

    def _extract_cpes(self, cve_item: Dict) -> list:
        """Extract affected CPEs"""
        cpes = []
        configurations = cve_item.get("configurations", [])

        for config in configurations:
            for node in config.get("nodes", []):
                for cpe_match in node.get("cpeMatch", []):
                    if cpe_match.get("vulnerable"):
                        cpes.append(cpe_match.get("criteria", ""))

        return cpes

    def _analyze_cve_with_ai(self, cve_info: Dict[str, Any]):
        """Analyze CVE with AI"""
        print("\n[*] Analyzing CVE with AI...")

        from core.prompt_templates import PromptTemplates
        prompt = PromptTemplates.get_cve_analysis_prompt(cve_info["id"], cve_info)

        try:
            analysis = self.llm.generate(prompt)

            print("\n" + "=" * 80)
            print(f"CVE ANALYSIS: {cve_info['id']}")
            print("=" * 80)
            print(f"Score: {cve_info['cvss_score'].get('score')} ({cve_info['cvss_score'].get('severity')})")
            print(f"Published: {cve_info['published']}")
            print(f"\nDescription:\n{cve_info['description']}")
            print("\n" + "-" * 80)
            print("AI ANALYSIS:")
            print("-" * 80)
            print(analysis)
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def search_cves(
        self,
        keyword: str,
        max_results: int = 10,
    ) -> list:
        """
        Search CVEs by keyword

        Args:
            keyword: Search keyword
            max_results: Maximum results to return

        Returns:
            List of CVE IDs
        """
        print(f"[*] Searching CVEs for: {keyword}")

        try:
            response = requests.get(
                self.nvd_api_url,
                params={
                    "keywordSearch": keyword,
                    "resultsPerPage": max_results,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                cves = []

                for vuln in data.get("vulnerabilities", []):
                    cve = vuln["cve"]
                    cves.append({
                        "id": cve["id"],
                        "description": cve.get("descriptions", [{}])[0].get("value", "")[:200],
                        "published": cve.get("published", ""),
                    })

                print(f"[+] Found {len(cves)} CVEs")
                for cve in cves:
                    print(f"  - {cve['id']}: {cve['description']}...")

                return cves

            return []

        except Exception as e:
            print(f"[!] CVE search failed: {e}")
            return []
