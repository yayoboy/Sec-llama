"""
Burp Suite Integration
Web application security testing
"""

import requests
import json
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin

from core.config import get_config
from core.llm_interface import get_llm


class BurpSuiteIntegration:
    """Burp Suite Professional API integration"""

    def __init__(self, api_url: str = "http://localhost:1337", api_key: str = None):
        """
        Initialize Burp Suite integration

        Args:
            api_url: Burp Suite REST API URL
            api_key: API key (if authentication enabled)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.config = get_config()
        self.llm = get_llm()
        self.headers = {}

        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def start_scan(
        self,
        target_url: str,
        scan_type: str = "active",
    ) -> Optional[str]:
        """
        Start Burp Suite scan

        Args:
            target_url: Target URL to scan
            scan_type: Scan type (active, passive, crawl)

        Returns:
            Task ID
        """
        print(f"[*] Starting Burp Suite {scan_type} scan on {target_url}")

        try:
            endpoint = f"{self.api_url}/v0.1/scan"

            data = {
                "scan_configurations": [
                    {
                        "type": scan_type,
                        "name": f"Sec-Llama {scan_type} scan",
                    }
                ],
                "urls": [target_url],
            }

            response = requests.post(
                endpoint,
                headers=self.headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 201:
                task_id = response.headers.get("Location", "").split("/")[-1]
                print(f"[+] Scan started: Task ID {task_id}")
                return task_id
            else:
                print(f"[!] Scan failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"[!] Burp Suite scan failed: {e}")
            return None

    def get_scan_status(self, task_id: str) -> Dict[str, Any]:
        """Get scan status"""
        try:
            endpoint = f"{self.api_url}/v0.1/scan/{task_id}"
            response = requests.get(endpoint, headers=self.headers, timeout=30)

            if response.status_code == 200:
                return response.json()
            return {}

        except Exception as e:
            print(f"[!] Failed to get scan status: {e}")
            return {}

    def get_scan_results(self, task_id: str) -> List[Dict[str, Any]]:
        """
        Get scan results

        Args:
            task_id: Scan task ID

        Returns:
            List of vulnerabilities found
        """
        print(f"[*] Retrieving scan results for task {task_id}")

        try:
            # Get scan issues
            endpoint = f"{self.api_url}/v0.1/scan/{task_id}/issues"
            response = requests.get(endpoint, headers=self.headers, timeout=30)

            if response.status_code == 200:
                issues = response.json().get("issues", [])
                print(f"[+] Found {len(issues)} issues")

                # AI analysis
                if issues:
                    self._ai_analyze_issues(issues)

                return issues
            else:
                print(f"[!] Failed to get results: {response.status_code}")
                return []

        except Exception as e:
            print(f"[!] Failed to retrieve results: {e}")
            return []

    def _ai_analyze_issues(self, issues: List[Dict[str, Any]]):
        """AI analysis of Burp Suite findings"""
        print("\n[*] Analyzing findings with AI...")

        # Group by severity
        critical = [i for i in issues if i.get("severity") == "high"]
        high = [i for i in issues if i.get("severity") == "medium"]

        summary = f"""Found {len(issues)} total issues:
- Critical/High: {len(critical)}
- Medium: {len(high)}

Top issues:
"""
        for issue in issues[:5]:
            summary += f"- {issue.get('name')}: {issue.get('severity')}\n"

        prompt = f"""Analyze the following web application vulnerabilities found by Burp Suite:

{summary}

Provide:
1. **Critical Findings**: Most severe issues to fix immediately
2. **Exploitation Risk**: How easily can these be exploited?
3. **Business Impact**: Potential impact on the application
4. **Remediation Priority**: What to fix first and why
5. **Quick Wins**: Easy fixes with high security impact

Be concise and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("AI ANALYSIS OF WEB VULNERABILITIES:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def export_report(self, task_id: str, output_file: str, format: str = "html"):
        """
        Export scan report

        Args:
            task_id: Scan task ID
            output_file: Output file path
            format: Report format (html, xml)
        """
        print(f"[*] Exporting report to {output_file}")

        try:
            endpoint = f"{self.api_url}/v0.1/scan/{task_id}/report"

            params = {"format": format}

            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=60,
            )

            if response.status_code == 200:
                with open(output_file, "w") as f:
                    f.write(response.text)
                print(f"[+] Report saved to {output_file}")
            else:
                print(f"[!] Export failed: {response.status_code}")

        except Exception as e:
            print(f"[!] Report export failed: {e}")

    def spider_url(self, target_url: str) -> List[str]:
        """
        Spider/crawl a URL

        Args:
            target_url: Target URL

        Returns:
            List of discovered URLs
        """
        print(f"[*] Spidering {target_url}")

        try:
            endpoint = f"{self.api_url}/v0.1/spider"

            data = {"base_url": target_url}

            response = requests.post(
                endpoint,
                headers=self.headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 201:
                task_id = response.headers.get("Location", "").split("/")[-1]

                # Wait for spider to complete (simplified)
                import time
                time.sleep(10)

                # Get results
                result_endpoint = f"{self.api_url}/v0.1/spider/{task_id}"
                result_response = requests.get(
                    result_endpoint,
                    headers=self.headers,
                    timeout=30,
                )

                if result_response.status_code == 200:
                    urls = result_response.json().get("urls", [])
                    print(f"[+] Discovered {len(urls)} URLs")
                    return urls

            return []

        except Exception as e:
            print(f"[!] Spidering failed: {e}")
            return []

    def passive_scan_item(self, url: str, method: str = "GET") -> Dict[str, Any]:
        """
        Send item for passive scanning

        Args:
            url: URL to scan
            method: HTTP method

        Returns:
            Scan result
        """
        try:
            endpoint = f"{self.api_url}/v0.1/scan/passive"

            data = {
                "url": url,
                "method": method,
            }

            response = requests.post(
                endpoint,
                headers=self.headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 200:
                return response.json()

            return {}

        except Exception as e:
            print(f"[!] Passive scan failed: {e}")
            return {}
