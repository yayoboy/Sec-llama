"""
BloodHound Integration
Active Directory attack path analysis
"""

import json
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path

from core.config import get_config
from core.llm_interface import get_llm


class BloodHoundIntegration:
    """BloodHound integration for AD analysis"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()

    def run_sharphound(
        self,
        domain: str,
        username: str = None,
        password: str = None,
        collection_method: str = "All",
    ) -> Optional[str]:
        """
        Run SharpHound data collection

        Args:
            domain: Target domain
            username: Domain username
            password: Domain password
            collection_method: Collection method (All, DCOnly, etc.)

        Returns:
            Path to output ZIP file
        """
        print(f"[*] Running SharpHound on domain: {domain}")
        print(f"[*] Collection method: {collection_method}")

        try:
            cmd = [
                "SharpHound.exe",
                "-c", collection_method,
                "-d", domain,
                "--zipfilename", f"bloodhound_{domain}.zip",
            ]

            if username and password:
                cmd.extend(["--ldapusername", username, "--ldappassword", password])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes
            )

            if result.returncode == 0:
                # Find output file
                zip_file = f"bloodhound_{domain}.zip"
                if Path(zip_file).exists():
                    print(f"[+] Data collected: {zip_file}")
                    return zip_file

            print(f"[!] SharpHound failed: {result.stderr}")
            return None

        except FileNotFoundError:
            print("[!] SharpHound not found. Install from https://github.com/BloodHoundAD/SharpHound")
            return None
        except Exception as e:
            print(f"[!] SharpHound execution failed: {e}")
            return None

    def analyze_bloodhound_data(self, json_file: str) -> Dict[str, Any]:
        """
        Analyze BloodHound JSON data with AI

        Args:
            json_file: Path to BloodHound JSON file

        Returns:
            Analysis results
        """
        print(f"[*] Analyzing BloodHound data: {json_file}")

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Extract key information
            analysis = {
                "users": [],
                "computers": [],
                "groups": [],
                "domains": [],
                "attack_paths": [],
            }

            # Parse data based on type
            if isinstance(data, dict):
                if "data" in data:
                    items = data["data"]
                    for item in items:
                        props = item.get("Properties", {})
                        obj_type = props.get("objecttype", "")

                        if obj_type == "User":
                            analysis["users"].append({
                                "name": props.get("name", ""),
                                "enabled": props.get("enabled", False),
                                "admin": props.get("admincount", False),
                            })
                        elif obj_type == "Computer":
                            analysis["computers"].append({
                                "name": props.get("name", ""),
                                "os": props.get("operatingsystem", ""),
                            })
                        elif obj_type == "Group":
                            analysis["groups"].append({
                                "name": props.get("name", ""),
                                "highvalue": props.get("highvalue", False),
                            })

            # AI analysis
            self._ai_analyze_ad_environment(analysis)

            return analysis

        except Exception as e:
            print(f"[!] Analysis failed: {e}")
            return {}

    def _ai_analyze_ad_environment(self, analysis: Dict[str, Any]):
        """AI analysis of AD environment"""
        print("\n[*] Analyzing AD environment with AI...")

        summary = f"""Active Directory Environment Analysis:

Total Users: {len(analysis['users'])}
Total Computers: {len(analysis['computers'])}
Total Groups: {len(analysis['groups'])}

High-Value Targets:
- Admin users: {sum(1 for u in analysis['users'] if u.get('admin'))}
- High-value groups: {sum(1 for g in analysis['groups'] if g.get('highvalue'))}

Sample users: {', '.join([u['name'] for u in analysis['users'][:5]])}
Sample computers: {', '.join([c['name'] for c in analysis['computers'][:5]])}
Sample groups: {', '.join([g['name'] for g in analysis['groups'][:5]])}
"""

        prompt = f"""Analyze the following Active Directory environment:

{summary}

Provide:
1. **Attack Surface**: Key attack vectors in this environment
2. **High-Value Targets**: Which accounts/groups to target first
3. **Common Attack Paths**: Likely paths to Domain Admin
4. **Misconfigurations**: Potential security issues to exploit
5. **Recommendations**: Steps for privilege escalation

Focus on practical attack strategies."""

        try:
            ai_analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("AI AD ENVIRONMENT ANALYSIS:")
            print("=" * 80)
            print(ai_analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def find_attack_paths(
        self,
        start_node: str,
        end_node: str,
        relationship_type: str = "MemberOf",
    ) -> List[List[str]]:
        """
        Find attack paths between nodes

        Args:
            start_node: Starting node (e.g., user)
            end_node: Target node (e.g., "Domain Admins")
            relationship_type: Relationship to follow

        Returns:
            List of attack paths
        """
        print(f"[*] Finding paths from {start_node} to {end_node}")

        # This would typically query Neo4j database
        # Simplified example:

        paths = [
            [start_node, "Intermediate Group", end_node],
        ]

        if paths:
            print(f"[+] Found {len(paths)} potential attack paths")

            # AI analysis of paths
            self._ai_analyze_attack_paths(paths, start_node, end_node)

        return paths

    def _ai_analyze_attack_paths(
        self,
        paths: List[List[str]],
        start: str,
        end: str,
    ):
        """AI analysis of attack paths"""
        print("\n[*] Analyzing attack paths with AI...")

        paths_str = "\n".join([
            f"Path {i+1}: {' -> '.join(path)}"
            for i, path in enumerate(paths)
        ])

        prompt = f"""Analyze the following Active Directory attack paths:

Start: {start}
Target: {end}

Paths:
{paths_str}

Provide:
1. **Easiest Path**: Which path is easiest to exploit?
2. **Exploitation Steps**: Detailed steps for the easiest path
3. **Tools Required**: What tools/techniques to use
4. **Detection Risk**: Likelihood of detection for each path
5. **Alternatives**: If blocked, what are alternative approaches?

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("AI ATTACK PATH ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def suggest_kerberoast_targets(self, bloodhound_data: Dict[str, Any]) -> List[str]:
        """
        Suggest Kerberoasting targets

        Args:
            bloodhound_data: BloodHound data

        Returns:
            List of Kerberoastable accounts
        """
        print("[*] Identifying Kerberoast targets...")

        targets = []

        # Look for users with SPNs
        for user in bloodhound_data.get("users", []):
            if user.get("hasspn"):
                targets.append(user["name"])

        if targets:
            print(f"[+] Found {len(targets)} Kerberoastable accounts")
            for target in targets:
                print(f"  - {target}")

            # AI recommendations
            prompt = f"""The following accounts are Kerberoastable in the AD environment:

{', '.join(targets)}

Provide:
1. **Priority Targets**: Which accounts to Kerberoast first?
2. **Success Probability**: Likelihood of cracking the password
3. **Attack Steps**: Detailed Kerberoasting procedure
4. **Post-Exploitation**: What to do after obtaining credentials

Be practical and specific."""

            try:
                analysis = self.llm.generate(prompt)
                print("\n" + "=" * 80)
                print("KERBEROAST RECOMMENDATIONS:")
                print("=" * 80)
                print(analysis)
                print("=" * 80 + "\n")
            except Exception as e:
                print(f"[!] AI analysis failed: {e}")

        return targets
