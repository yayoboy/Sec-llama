"""
Log Parser - Multi-format log analysis with AI
"""

import re
from datetime import datetime
from typing import List, Dict, Any
from collections import Counter

from core.config import get_config
from core.llm_interface import get_llm


class LogParser:
    """Parse and analyze security logs"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.parsed_logs: List[Dict[str, Any]] = []

    def parse_log_file(self, file_path: str, log_type: str = "auto") -> List[Dict[str, Any]]:
        """
        Parse log file

        Args:
            file_path: Path to log file
            log_type: Log type (apache, nginx, syslog, auth, auto)

        Returns:
            Parsed log entries
        """
        print(f"[*] Parsing log file: {file_path}")

        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        if log_type == "auto":
            log_type = self._detect_log_type(lines[:10])

        print(f"[*] Detected log type: {log_type}")

        if log_type == "apache":
            self.parsed_logs = self._parse_apache_logs(lines)
        elif log_type == "nginx":
            self.parsed_logs = self._parse_nginx_logs(lines)
        elif log_type == "auth":
            self.parsed_logs = self._parse_auth_logs(lines)
        else:
            self.parsed_logs = self._parse_generic_logs(lines)

        print(f"[+] Parsed {len(self.parsed_logs)} log entries")

        # AI analysis
        self._analyze_logs_with_ai()

        return self.parsed_logs

    def _detect_log_type(self, sample_lines: List[str]) -> str:
        """Auto-detect log type"""
        sample = '\n'.join(sample_lines)

        if 'GET' in sample or 'POST' in sample:
            if 'nginx' in sample.lower():
                return "nginx"
            return "apache"
        elif 'sshd' in sample or 'sudo' in sample:
            return "auth"

        return "generic"

    def _parse_apache_logs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse Apache access logs"""
        logs = []
        pattern = r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\S+)'

        for line in lines:
            match = re.match(pattern, line)
            if match:
                logs.append({
                    "ip": match.group(1),
                    "timestamp": match.group(2),
                    "method": match.group(3),
                    "path": match.group(4),
                    "protocol": match.group(5),
                    "status": int(match.group(6)),
                    "size": match.group(7),
                })

        return logs

    def _parse_nginx_logs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse Nginx access logs"""
        return self._parse_apache_logs(lines)  # Similar format

    def _parse_auth_logs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse authentication logs"""
        logs = []

        for line in lines:
            logs.append({
                "raw": line.strip(),
                "timestamp": datetime.now(),
                "message": line.strip(),
            })

        return logs

    def _parse_generic_logs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse generic logs"""
        return [{"raw": line.strip()} for line in lines if line.strip()]

    def _analyze_logs_with_ai(self):
        """AI analysis of logs"""
        print("\n[*] Analyzing logs with AI...")

        # Get statistics
        stats = self.get_statistics()

        prompt = f"""Analyze the following security log statistics:

Total entries: {stats.get('total_entries', 0)}
Unique IPs: {stats.get('unique_ips', 0)}
Top IPs: {stats.get('top_ips', [])}
HTTP methods: {stats.get('methods', {})}
Status codes: {stats.get('status_codes', {})}

Identify:
1. **Suspicious Activity**: Unusual patterns or behavior
2. **Attack Indicators**: Signs of attacks (SQL injection, XSS, brute force, etc.)
3. **Anomalies**: Deviations from normal behavior
4. **Recommendations**: Actions to take

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("LOG ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get log statistics"""
        stats = {
            "total_entries": len(self.parsed_logs),
            "unique_ips": 0,
            "top_ips": [],
            "methods": {},
            "status_codes": {},
        }

        ips = []
        methods = []
        status_codes = []

        for log in self.parsed_logs:
            if "ip" in log:
                ips.append(log["ip"])
            if "method" in log:
                methods.append(log["method"])
            if "status" in log:
                status_codes.append(log["status"])

        stats["unique_ips"] = len(set(ips))
        stats["top_ips"] = [ip for ip, count in Counter(ips).most_common(10)]
        stats["methods"] = dict(Counter(methods))
        stats["status_codes"] = dict(Counter(status_codes))

        return stats

    def find_attacks(self) -> List[Dict[str, Any]]:
        """Find potential attacks in logs"""
        attacks = []

        attack_patterns = {
            "sql_injection": r"(union|select|insert|update|delete|drop|exec)",
            "xss": r"(<script|javascript:|onerror=)",
            "lfi": r"(\.\./|/etc/passwd|/etc/shadow)",
            "rfi": r"(http://|https://|ftp://)",
        }

        for log in self.parsed_logs:
            path = log.get("path", "").lower()

            for attack_type, pattern in attack_patterns.items():
                if re.search(pattern, path, re.IGNORECASE):
                    attacks.append({
                        "type": attack_type,
                        "log": log,
                    })

        print(f"[!] Found {len(attacks)} potential attack attempts")
        return attacks
