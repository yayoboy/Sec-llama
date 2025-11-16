"""
Docker Security Scanner
Scan Docker images and containers for vulnerabilities
"""

import subprocess
import json
from typing import Dict, Any, List

from core.llm_interface import get_llm


class DockerScanner:
    """Docker security scanner"""

    def __init__(self):
        self.llm = get_llm()

    def scan_image(self, image_name: str) -> Dict[str, Any]:
        """
        Scan Docker image for vulnerabilities

        Args:
            image_name: Docker image name

        Returns:
            Scan results
        """
        print(f"[*] Scanning Docker image: {image_name}")

        results = {
            "image": image_name,
            "vulnerabilities": [],
            "secrets": [],
            "misconfigurations": [],
        }

        # Check image history
        results["history"] = self._check_image_history(image_name)

        # Scan with Trivy (if available)
        trivy_results = self._scan_with_trivy(image_name)
        if trivy_results:
            results["vulnerabilities"] = trivy_results

        # AI analysis
        self._analyze_image_with_ai(results)

        return results

    def _check_image_history(self, image_name: str) -> List[str]:
        """Check image build history"""
        try:
            cmd = ["docker", "history", "--no-trunc", image_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return result.stdout.split('\n')[:10]  # Top 10 layers

            return []

        except Exception as e:
            print(f"[!] History check failed: {e}")
            return []

    def _scan_with_trivy(self, image_name: str) -> List[Dict[str, Any]]:
        """Scan with Trivy"""
        try:
            cmd = ["trivy", "image", "--format", "json", image_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                # Extract vulnerabilities
                vulns = []
                for result_item in data.get("Results", []):
                    for vuln in result_item.get("Vulnerabilities", []):
                        vulns.append({
                            "id": vuln.get("VulnerabilityID"),
                            "severity": vuln.get("Severity"),
                            "package": vuln.get("PkgName"),
                            "version": vuln.get("InstalledVersion"),
                        })
                return vulns

        except FileNotFoundError:
            print("[!] Trivy not found. Install: https://github.com/aquasecurity/trivy")
        except Exception as e:
            print(f"[!] Trivy scan failed: {e}")

        return []

    def _analyze_image_with_ai(self, results: Dict[str, Any]):
        """AI analysis of Docker image"""
        print("\n[*] Analyzing image with AI...")

        prompt = f"""Analyze this Docker image security scan:

Image: {results['image']}
Vulnerabilities found: {len(results['vulnerabilities'])}

Top vulnerabilities:
{json.dumps(results['vulnerabilities'][:5], indent=2)}

Provide:
1. **Risk Assessment**: Overall security risk
2. **Critical Issues**: Most important issues to fix
3. **Best Practices**: Docker security best practices violated
4. **Remediation**: Specific steps to fix issues

Be actionable."""

        try:
            analysis = self.llm.generate(prompt)

            print("\n" + "=" * 80)
            print("DOCKER IMAGE ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def scan_running_containers(self) -> List[Dict[str, Any]]:
        """Scan all running containers"""
        print("[*] Scanning running containers...")

        try:
            cmd = ["docker", "ps", "--format", "{{.Names}}"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                containers = result.stdout.strip().split('\n')
                results = []

                for container in containers:
                    if container:
                        results.append(self._scan_container(container))

                return results

            return []

        except Exception as e:
            print(f"[!] Container scan failed: {e}")
            return []

    def _scan_container(self, container_name: str) -> Dict[str, Any]:
        """Scan single container"""
        print(f"[*] Scanning container: {container_name}")

        return {
            "name": container_name,
            "status": "scanned",
        }
