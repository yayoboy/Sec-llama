"""
API Fuzzer - REST/GraphQL API security testing
"""

import requests
import json
from typing import Dict, Any, List
from urllib.parse import urljoin

from core.llm_interface import get_llm


class APIFuzzer:
    """API security testing and fuzzing"""

    def __init__(self):
        self.llm = get_llm()
        self.session = requests.Session()

    def fuzz_endpoint(
        self,
        base_url: str,
        endpoint: str,
        method: str = "GET",
        payloads: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fuzz API endpoint

        Args:
            base_url: Base API URL
            endpoint: Endpoint path
            method: HTTP method
            payloads: Fuzzing payloads

        Returns:
            Fuzzing results
        """
        print(f"[*] Fuzzing endpoint: {method} {endpoint}")

        if payloads is None:
            payloads = self._get_default_payloads()

        url = urljoin(base_url, endpoint)
        results = []

        for payload in payloads:
            try:
                if method == "GET":
                    response = self.session.get(
                        url,
                        params={"input": payload},
                        timeout=5,
                    )
                elif method == "POST":
                    response = self.session.post(
                        url,
                        json={"input": payload},
                        timeout=5,
                    )

                result = {
                    "payload": payload,
                    "status_code": response.status_code,
                    "response_length": len(response.text),
                    "interesting": self._is_interesting_response(response),
                }

                results.append(result)

                if result["interesting"]:
                    print(f"[!] Interesting response: {payload} -> {response.status_code}")

            except Exception as e:
                results.append({
                    "payload": payload,
                    "error": str(e),
                })

        # AI analysis
        self._analyze_fuzzing_results(results, url)

        return results

    def _get_default_payloads(self) -> List[str]:
        """Get default fuzzing payloads"""
        return [
            "' OR '1'='1",  # SQL injection
            "<script>alert(1)</script>",  # XSS
            "../../../etc/passwd",  # Path traversal
            "${7*7}",  # SSTI
            "admin'--",  # SQL comment
            "1; DROP TABLE users--",  # SQL injection
            "{{7*7}}",  # Template injection
            "%00",  # Null byte
            "../../../../windows/system32/config/sam",  # Windows path traversal
        ]

    def _is_interesting_response(self, response: requests.Response) -> bool:
        """Check if response is interesting"""
        # Error messages
        error_indicators = ["error", "exception", "stack trace", "warning", "sql", "database"]

        if any(indicator in response.text.lower() for indicator in error_indicators):
            return True

        # Unusual status codes
        if response.status_code in [500, 403, 401]:
            return True

        return False

    def _analyze_fuzzing_results(self, results: List[Dict[str, Any]], url: str):
        """AI analysis of fuzzing results"""
        print("\n[*] Analyzing fuzzing results with AI...")

        interesting = [r for r in results if r.get("interesting")]

        if not interesting:
            print("[+] No interesting responses found")
            return

        prompt = f"""Analyze the following API fuzzing results:

URL: {url}
Total payloads tested: {len(results)}
Interesting responses: {len(interesting)}

Interesting results:
{json.dumps(interesting[:5], indent=2)}

Identify:
1. **Vulnerabilities**: What vulnerabilities might exist?
2. **Exploitation**: How to exploit these findings?
3. **Severity**: Risk level
4. **Next Steps**: Further testing recommendations

Be specific."""

        try:
            analysis = self.llm.generate(prompt)

            print("\n" + "=" * 80)
            print("API FUZZING ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def test_authentication(self, login_url: str) -> Dict[str, Any]:
        """Test authentication mechanisms"""
        print(f"[*] Testing authentication: {login_url}")

        tests = [
            {"username": "admin", "password": "admin"},
            {"username": "admin", "password": "password"},
            {"username": "' OR '1'='1", "password": "' OR '1'='1"},
        ]

        results = []

        for creds in tests:
            try:
                response = self.session.post(
                    login_url,
                    json=creds,
                    timeout=5,
                )

                results.append({
                    "credentials": creds,
                    "status": response.status_code,
                    "success": response.status_code == 200,
                })

            except Exception as e:
                results.append({
                    "credentials": creds,
                    "error": str(e),
                })

        return {"tests": results}
