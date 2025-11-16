"""
Security Dataset Manager
Collect, prepare, and manage training datasets for security-focused LLMs
"""

import json
import requests
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict

from core.config import get_config


class DatasetManager:
    """Manage security training datasets"""

    def __init__(self):
        self.config = get_config()
        self.dataset_dir = Path("database/datasets")
        self.dataset_dir.mkdir(parents=True, exist_ok=True)

    def collect_cve_dataset(self, max_items: int = 10000) -> str:
        """
        Collect CVE dataset from NVD

        Args:
            max_items: Maximum CVEs to collect

        Returns:
            Path to dataset file
        """
        print(f"[*] Collecting CVE dataset (max {max_items} items)...")

        dataset = []
        api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

        try:
            # Collect recent CVEs
            start_index = 0
            results_per_page = 2000

            while len(dataset) < max_items:
                print(f"[*] Fetching CVEs {start_index} to {start_index + results_per_page}...")

                response = requests.get(
                    api_url,
                    params={
                        "resultsPerPage": results_per_page,
                        "startIndex": start_index,
                    },
                    timeout=60,
                )

                if response.status_code != 200:
                    print(f"[!] API error: {response.status_code}")
                    break

                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])

                if not vulnerabilities:
                    break

                for vuln in vulnerabilities:
                    cve = vuln.get("cve", {})
                    cve_id = cve.get("id", "")
                    description = ""

                    # Get English description
                    descriptions = cve.get("descriptions", [])
                    for desc in descriptions:
                        if desc.get("lang") == "en":
                            description = desc.get("value", "")
                            break

                    # Extract CVSS score
                    metrics = cve.get("metrics", {})
                    cvss_score = 0.0
                    severity = "UNKNOWN"

                    if "cvssMetricV31" in metrics:
                        cvss_data = metrics["cvssMetricV31"][0]["cvssData"]
                        cvss_score = cvss_data.get("baseScore", 0.0)
                        severity = cvss_data.get("baseSeverity", "UNKNOWN")

                    # Create training example
                    dataset.append({
                        "instruction": f"Analyze CVE {cve_id} and provide security assessment",
                        "input": f"CVE ID: {cve_id}\nDescription: {description}",
                        "output": f"This vulnerability has a CVSS score of {cvss_score} ({severity}). {description[:200]}",
                        "metadata": {
                            "cve_id": cve_id,
                            "severity": severity,
                            "score": cvss_score,
                        }
                    })

                start_index += results_per_page

                if len(dataset) >= max_items:
                    break

            # Save dataset
            output_file = self.dataset_dir / f"cve_dataset_{datetime.now().strftime('%Y%m%d')}.json"

            with open(output_file, "w") as f:
                json.dump(dataset[:max_items], f, indent=2)

            print(f"[+] Collected {len(dataset)} CVE examples")
            print(f"[+] Dataset saved: {output_file}")

            return str(output_file)

        except Exception as e:
            print(f"[!] CVE collection failed: {e}")
            return ""

    def collect_exploit_dataset(self) -> str:
        """
        Collect exploit dataset from Exploit-DB

        Returns:
            Path to dataset file
        """
        print("[*] Collecting exploit dataset...")

        dataset = []

        # Note: This would require scraping exploit-db or using their API
        # For now, create template structure

        examples = [
            {
                "instruction": "Suggest exploits for Apache 2.4.49",
                "input": "Service: Apache HTTP Server\nVersion: 2.4.49\nPort: 80",
                "output": "Apache 2.4.49 is vulnerable to CVE-2021-41773 (Path Traversal). Available exploits:\n1. Manual: curl 'http://target/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd'\n2. Metasploit: exploit/multi/http/apache_normalize_path_rce\nSeverity: CRITICAL"
            },
            {
                "instruction": "Analyze vulnerability in Samba 4.2.3",
                "input": "Service: Samba\nVersion: 4.2.3\nPort: 445",
                "output": "Samba 4.2.3 has multiple known vulnerabilities including remote code execution. Recommend updating to latest version."
            },
        ]

        dataset.extend(examples)

        output_file = self.dataset_dir / f"exploit_dataset_{datetime.now().strftime('%Y%m%d')}.json"

        with open(output_file, "w") as f:
            json.dump(dataset, f, indent=2)

        print(f"[+] Created exploit dataset: {output_file}")
        return str(output_file)

    def collect_security_qa_dataset(self) -> str:
        """
        Collect security Q&A dataset

        Returns:
            Path to dataset file
        """
        print("[*] Creating security Q&A dataset...")

        dataset = [
            {
                "instruction": "Explain SQL injection",
                "input": "What is SQL injection and how does it work?",
                "output": "SQL injection is a code injection technique that exploits vulnerabilities in an application's database layer. Attackers insert malicious SQL statements into input fields, which are then executed by the database. Example: ' OR '1'='1 can bypass authentication. Prevention: Use parameterized queries and prepared statements."
            },
            {
                "instruction": "Explain XSS attack",
                "input": "What is Cross-Site Scripting (XSS)?",
                "output": "XSS is a vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users. Types: Reflected XSS, Stored XSS, DOM-based XSS. Prevention: Input validation, output encoding, Content Security Policy (CSP)."
            },
            {
                "instruction": "Explain CSRF",
                "input": "What is CSRF and how to prevent it?",
                "output": "CSRF (Cross-Site Request Forgery) tricks authenticated users into executing unwanted actions. Attackers craft malicious requests that appear legitimate. Prevention: Use CSRF tokens, SameSite cookies, verify origin headers."
            },
            {
                "instruction": "Network reconnaissance",
                "input": "What tools are used for network reconnaissance?",
                "output": "Common reconnaissance tools: Nmap (port scanning), Masscan (fast scanning), Wireshark (traffic analysis), Shodan (internet scanning), theHarvester (OSINT), Recon-ng (framework). Use nmap -sV -sC for service version detection."
            },
            {
                "instruction": "Privilege escalation",
                "input": "How to escalate privileges on Linux?",
                "output": "Linux privilege escalation techniques: 1. Kernel exploits (check with uname -a), 2. SUID binaries (find / -perm -4000), 3. Sudo misconfigurations (sudo -l), 4. Cron jobs (/etc/crontab), 5. Writable /etc/passwd, 6. Docker breakout if user in docker group."
            },
            {
                "instruction": "Windows privilege escalation",
                "input": "How to escalate privileges on Windows?",
                "output": "Windows privilege escalation: 1. Unquoted service paths, 2. AlwaysInstallElevated, 3. Stored credentials (cmdkey /list), 4. Token impersonation, 5. Vulnerable services, 6. DLL hijacking. Tools: WinPEAS, PowerUp, Watson."
            },
            {
                "instruction": "Secure coding",
                "input": "Best practices for secure coding?",
                "output": "Secure coding practices: 1. Input validation and sanitization, 2. Parameterized queries, 3. Principle of least privilege, 4. Error handling without info disclosure, 5. Secure session management, 6. HTTPS everywhere, 7. Regular security updates, 8. Code review and SAST tools."
            },
        ]

        output_file = self.dataset_dir / f"security_qa_{datetime.now().strftime('%Y%m%d')}.json"

        with open(output_file, "w") as f:
            json.dump(dataset, f, indent=2)

        print(f"[+] Created security Q&A dataset: {output_file}")
        print(f"[+] Total examples: {len(dataset)}")

        return str(output_file)

    def prepare_training_data(
        self,
        dataset_files: List[str],
        output_format: str = "alpaca"
    ) -> str:
        """
        Prepare and merge datasets for training

        Args:
            dataset_files: List of dataset file paths
            output_format: Output format (alpaca, sharegpt, etc.)

        Returns:
            Path to prepared dataset
        """
        print(f"[*] Preparing training data in {output_format} format...")

        combined_dataset = []

        for file_path in dataset_files:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    combined_dataset.extend(data)
                    print(f"[+] Loaded {len(data)} examples from {file_path}")
            except Exception as e:
                print(f"[!] Failed to load {file_path}: {e}")

        # Format conversion
        if output_format == "alpaca":
            # Already in Alpaca format (instruction, input, output)
            formatted_data = combined_dataset
        elif output_format == "sharegpt":
            # Convert to ShareGPT format
            formatted_data = []
            for item in combined_dataset:
                formatted_data.append({
                    "conversations": [
                        {"from": "human", "value": item.get("instruction", "") + "\n" + item.get("input", "")},
                        {"from": "gpt", "value": item.get("output", "")}
                    ]
                })
        else:
            formatted_data = combined_dataset

        # Save prepared dataset
        output_file = self.dataset_dir / f"training_data_{output_format}_{datetime.now().strftime('%Y%m%d')}.json"

        with open(output_file, "w") as f:
            json.dump(formatted_data, f, indent=2)

        print(f"[+] Prepared {len(formatted_data)} training examples")
        print(f"[+] Saved to: {output_file}")

        # Generate statistics
        self._print_dataset_stats(formatted_data)

        return str(output_file)

    def _print_dataset_stats(self, dataset: List[Dict]):
        """Print dataset statistics"""
        print("\n" + "=" * 60)
        print("DATASET STATISTICS")
        print("=" * 60)

        print(f"Total examples: {len(dataset)}")

        # Count by type (if metadata exists)
        types = defaultdict(int)
        for item in dataset:
            metadata = item.get("metadata", {})
            if "severity" in metadata:
                types[metadata["severity"]] += 1

        if types:
            print("\nBy severity:")
            for severity, count in sorted(types.items()):
                print(f"  {severity}: {count}")

        # Average lengths
        if dataset:
            avg_instruction = sum(len(item.get("instruction", "")) for item in dataset) / len(dataset)
            avg_input = sum(len(item.get("input", "")) for item in dataset) / len(dataset)
            avg_output = sum(len(item.get("output", "")) for item in dataset) / len(dataset)

            print(f"\nAverage lengths:")
            print(f"  Instruction: {avg_instruction:.0f} chars")
            print(f"  Input: {avg_input:.0f} chars")
            print(f"  Output: {avg_output:.0f} chars")

        print("=" * 60 + "\n")

    def create_custom_dataset(
        self,
        examples: List[Dict[str, str]],
        name: str = "custom"
    ) -> str:
        """
        Create custom dataset from examples

        Args:
            examples: List of training examples
            name: Dataset name

        Returns:
            Path to dataset file
        """
        print(f"[*] Creating custom dataset: {name}")

        output_file = self.dataset_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.json"

        with open(output_file, "w") as f:
            json.dump(examples, f, indent=2)

        print(f"[+] Created dataset with {len(examples)} examples")
        print(f"[+] Saved to: {output_file}")

        return str(output_file)

    def validate_dataset(self, dataset_file: str) -> Dict[str, Any]:
        """
        Validate dataset format and quality

        Args:
            dataset_file: Path to dataset file

        Returns:
            Validation results
        """
        print(f"[*] Validating dataset: {dataset_file}")

        try:
            with open(dataset_file, "r") as f:
                data = json.load(f)

            issues = []
            valid_count = 0

            for i, item in enumerate(data):
                # Check required fields
                if "instruction" not in item or "output" not in item:
                    issues.append(f"Item {i}: Missing required fields")
                    continue

                # Check empty fields
                if not item["instruction"].strip() or not item["output"].strip():
                    issues.append(f"Item {i}: Empty instruction or output")
                    continue

                # Check length
                if len(item["output"]) < 10:
                    issues.append(f"Item {i}: Output too short")

                valid_count += 1

            result = {
                "total_items": len(data),
                "valid_items": valid_count,
                "invalid_items": len(data) - valid_count,
                "issues": issues[:10],  # First 10 issues
                "is_valid": len(issues) == 0,
            }

            print(f"\n[+] Validation results:")
            print(f"    Total: {result['total_items']}")
            print(f"    Valid: {result['valid_items']}")
            print(f"    Invalid: {result['invalid_items']}")

            if issues:
                print(f"\n[!] Found {len(issues)} issues (showing first 10):")
                for issue in issues[:10]:
                    print(f"    - {issue}")

            return result

        except Exception as e:
            print(f"[!] Validation failed: {e}")
            return {"is_valid": False, "error": str(e)}

    def list_datasets(self) -> List[str]:
        """List available datasets"""
        datasets = list(self.dataset_dir.glob("*.json"))
        return [str(d) for d in datasets]
