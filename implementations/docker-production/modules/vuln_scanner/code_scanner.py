"""
Code Vulnerability Scanner (SAST)
Static Application Security Testing with AI
"""

import os
import subprocess
import json
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class Vulnerability:
    """Code vulnerability"""
    file: str
    line: int
    severity: str
    title: str
    description: str
    cwe: str = ""
    recommendation: str = ""
    code_snippet: str = ""


class CodeScanner:
    """Static code analysis for security vulnerabilities"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.vulnerabilities: List[Vulnerability] = []

    def scan_directory(self, path: str, language: str = "auto") -> List[Vulnerability]:
        """
        Scan directory for vulnerabilities

        Args:
            path: Directory path to scan
            language: Programming language (auto-detect if "auto")

        Returns:
            List of vulnerabilities found
        """
        print(f"[*] Scanning {path} for vulnerabilities...")

        if language == "auto":
            language = self._detect_language(path)

        print(f"[*] Detected language: {language}")

        # Run appropriate scanner
        if language == "python":
            self._scan_python(path)
        elif language == "javascript":
            self._scan_javascript(path)
        else:
            print(f"[!] Language {language} not fully supported, using generic analysis")
            self._scan_generic(path)

        # AI-enhanced analysis
        if self.vulnerabilities:
            self._ai_enhance_findings()

        return self.vulnerabilities

    def _detect_language(self, path: str) -> str:
        """Auto-detect primary programming language"""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.php': 'php',
            '.rb': 'ruby',
        }

        file_counts = {}
        for ext, lang in extensions.items():
            count = len(list(Path(path).rglob(f'*{ext}')))
            if count > 0:
                file_counts[lang] = count

        if file_counts:
            return max(file_counts.items(), key=lambda x: x[1])[0]

        return "unknown"

    def _scan_python(self, path: str):
        """Scan Python code with Bandit"""
        print("[*] Running Bandit scanner...")

        try:
            cmd = ["bandit", "-r", path, "-f", "json", "-o", "/tmp/bandit_results.json"]
            subprocess.run(cmd, capture_output=True, timeout=300)

            # Parse results
            if os.path.exists("/tmp/bandit_results.json"):
                with open("/tmp/bandit_results.json", "r") as f:
                    data = json.load(f)

                for result in data.get("results", []):
                    vuln = Vulnerability(
                        file=result.get("filename", ""),
                        line=result.get("line_number", 0),
                        severity=result.get("issue_severity", "MEDIUM"),
                        title=result.get("test_name", ""),
                        description=result.get("issue_text", ""),
                        cwe=result.get("test_id", ""),
                        code_snippet=result.get("code", ""),
                    )
                    self.vulnerabilities.append(vuln)

                print(f"[+] Found {len(self.vulnerabilities)} potential vulnerabilities")

        except FileNotFoundError:
            print("[!] Bandit not found. Install with: pip install bandit")
        except Exception as e:
            print(f"[!] Bandit scan failed: {e}")

    def _scan_javascript(self, path: str):
        """Scan JavaScript code"""
        print("[*] Scanning JavaScript code...")

        # Use semgrep if available
        try:
            cmd = ["semgrep", "--config=auto", "--json", path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                data = json.loads(result.stdout)

                for finding in data.get("results", []):
                    vuln = Vulnerability(
                        file=finding.get("path", ""),
                        line=finding.get("start", {}).get("line", 0),
                        severity=finding.get("extra", {}).get("severity", "MEDIUM"),
                        title=finding.get("check_id", ""),
                        description=finding.get("extra", {}).get("message", ""),
                        code_snippet=finding.get("extra", {}).get("lines", ""),
                    )
                    self.vulnerabilities.append(vuln)

                print(f"[+] Found {len(self.vulnerabilities)} potential vulnerabilities")

        except FileNotFoundError:
            print("[!] Semgrep not found. Install with: pip install semgrep")
        except Exception as e:
            print(f"[!] JavaScript scan failed: {e}")

    def _scan_generic(self, path: str):
        """Generic scan using pattern matching"""
        print("[*] Running generic vulnerability scan...")

        dangerous_patterns = {
            "eval(": "Code injection risk",
            "exec(": "Command injection risk",
            "system(": "Command injection risk",
            "shell_exec": "Command injection risk",
            "md5(": "Weak cryptography",
            "sha1(": "Weak cryptography",
            "SELECT * FROM": "Possible SQL injection",
            "innerHTML": "XSS risk",
            "document.write": "XSS risk",
        }

        for file_path in Path(path).rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.php', '.java']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):
                        for pattern, description in dangerous_patterns.items():
                            if pattern in line:
                                vuln = Vulnerability(
                                    file=str(file_path),
                                    line=line_num,
                                    severity="MEDIUM",
                                    title=f"Dangerous pattern: {pattern}",
                                    description=description,
                                    code_snippet=line.strip(),
                                )
                                self.vulnerabilities.append(vuln)

                except Exception:
                    pass

        print(f"[+] Found {len(self.vulnerabilities)} potential issues")

    def _ai_enhance_findings(self):
        """Use AI to enhance vulnerability findings"""
        print("\n[*] Enhancing findings with AI...")

        for vuln in self.vulnerabilities[:10]:  # Analyze top 10
            prompt = f"""Analyze this security vulnerability:

File: {vuln.file}
Line: {vuln.line}
Severity: {vuln.severity}
Issue: {vuln.title}
Description: {vuln.description}

Code:
```
{vuln.code_snippet}
```

Provide:
1. **Detailed Explanation**: How this vulnerability works
2. **Exploitation**: How could an attacker exploit this?
3. **Impact**: What's the potential impact?
4. **Fix**: Specific code fix recommendation

Be concise and actionable."""

            try:
                analysis = self.llm.generate(prompt)
                vuln.recommendation = analysis
            except Exception as e:
                print(f"[!] AI enhancement failed for {vuln.file}:{vuln.line}: {e}")

    def print_report(self):
        """Print vulnerability report"""
        if not self.vulnerabilities:
            print("\n[+] No vulnerabilities found!")
            return

        print("\n" + "=" * 80)
        print("VULNERABILITY REPORT")
        print("=" * 80)

        # Group by severity
        critical = [v for v in self.vulnerabilities if v.severity == "CRITICAL"]
        high = [v for v in self.vulnerabilities if v.severity == "HIGH"]
        medium = [v for v in self.vulnerabilities if v.severity == "MEDIUM"]
        low = [v for v in self.vulnerabilities if v.severity == "LOW"]

        print(f"\n📊 Summary:")
        print(f"   CRITICAL: {len(critical)}")
        print(f"   HIGH: {len(high)}")
        print(f"   MEDIUM: {len(medium)}")
        print(f"   LOW: {len(low)}")

        # Print details
        for severity, vulns in [("CRITICAL", critical), ("HIGH", high), ("MEDIUM", medium)]:
            if vulns:
                print(f"\n{'=' * 80}")
                print(f"{severity} SEVERITY")
                print('=' * 80)

                for vuln in vulns[:5]:  # Show top 5 per severity
                    print(f"\n🔴 {vuln.title}")
                    print(f"   File: {vuln.file}:{vuln.line}")
                    print(f"   Description: {vuln.description}")
                    if vuln.code_snippet:
                        print(f"   Code: {vuln.code_snippet[:100]}...")
                    if vuln.recommendation:
                        print(f"   Recommendation: {vuln.recommendation[:200]}...")

        print("\n" + "=" * 80)

    def export_json(self, output_file: str):
        """Export results as JSON"""
        data = {
            "total": len(self.vulnerabilities),
            "by_severity": {
                "CRITICAL": len([v for v in self.vulnerabilities if v.severity == "CRITICAL"]),
                "HIGH": len([v for v in self.vulnerabilities if v.severity == "HIGH"]),
                "MEDIUM": len([v for v in self.vulnerabilities if v.severity == "MEDIUM"]),
                "LOW": len([v for v in self.vulnerabilities if v.severity == "LOW"]),
            },
            "vulnerabilities": [asdict(v) for v in self.vulnerabilities],
        }

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"[+] Results exported to {output_file}")
