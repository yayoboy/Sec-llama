"""
WiFi Security Auditing Module
"""

import subprocess
import re
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class WiFiNetwork:
    """WiFi network information"""
    ssid: str
    bssid: str
    channel: int
    encryption: str
    signal_strength: int
    clients: int = 0
    vulnerabilities: List[str] = None

    def __post_init__(self):
        if self.vulnerabilities is None:
            self.vulnerabilities = []


class WiFiAuditor:
    """WiFi security auditor"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.interface = self.config.get("wireless.interface", "wlan0")

    def scan_networks(self) -> List[WiFiNetwork]:
        """Scan for WiFi networks"""
        print(f"[*] Scanning WiFi networks on {self.interface}...")

        networks = []

        try:
            # Use iwlist for scanning
            cmd = ["iwlist", self.interface, "scan"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                print(f"[!] Scan failed: {result.stderr}")
                return networks

            # Parse output
            networks = self._parse_iwlist_output(result.stdout)

            # Analyze security
            self._analyze_network_security(networks)

            return networks

        except FileNotFoundError:
            print("[!] iwlist not found. Install wireless-tools")
            return []
        except Exception as e:
            print(f"[!] WiFi scan failed: {e}")
            return []

    def _parse_iwlist_output(self, output: str) -> List[WiFiNetwork]:
        """Parse iwlist output"""
        networks = []
        current = {}

        for line in output.split('\n'):
            line = line.strip()

            if 'ESSID:' in line:
                match = re.search(r'ESSID:"([^"]+)"', line)
                if match:
                    current['ssid'] = match.group(1)

            elif 'Address:' in line and 'Cell' in line:
                match = re.search(r'Address: ([0-9A-Fa-f:]+)', line)
                if match:
                    current['bssid'] = match.group(1)

            elif 'Channel:' in line:
                match = re.search(r'Channel:(\d+)', line)
                if match:
                    current['channel'] = int(match.group(1))

            elif 'Encryption key:' in line:
                if 'on' in line:
                    current['encryption'] = 'WPA/WPA2'  # Simplified
                else:
                    current['encryption'] = 'OPEN'

            elif 'Signal level=' in line:
                match = re.search(r'Signal level=(-?\d+)', line)
                if match:
                    current['signal_strength'] = int(match.group(1))

                    # Complete network info
                    if 'ssid' in current and 'bssid' in current:
                        network = WiFiNetwork(
                            ssid=current.get('ssid', ''),
                            bssid=current.get('bssid', ''),
                            channel=current.get('channel', 0),
                            encryption=current.get('encryption', 'Unknown'),
                            signal_strength=current.get('signal_strength', 0),
                        )
                        networks.append(network)
                        current = {}

        return networks

    def _analyze_network_security(self, networks: List[WiFiNetwork]):
        """Analyze network security with AI"""
        print("\n[*] Analyzing WiFi security...")

        for network in networks:
            # Check for common vulnerabilities
            if network.encryption == 'OPEN':
                network.vulnerabilities.append("Open network - no encryption")

            if 'WEP' in network.encryption:
                network.vulnerabilities.append("WEP encryption - easily crackable")

            if network.ssid.lower() in ['default', 'linksys', 'netgear', 'dlink']:
                network.vulnerabilities.append("Default SSID - possible default configuration")

        # AI analysis
        network_summary = "\n".join([
            f"- {n.ssid} ({n.bssid}): {n.encryption}, Channel {n.channel}, Signal {n.signal_strength}"
            for n in networks
        ])

        prompt = f"""Analyze the following WiFi networks for security issues:

{network_summary}

Provide:
1. Security assessment for each network
2. Vulnerabilities identified
3. Attack vectors
4. Recommendations for secure configuration

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 60)
            print("AI WIFI SECURITY ANALYSIS:")
            print("=" * 60)
            print(analysis)
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

        # Print results
        for network in networks:
            print(f"\n[+] {network.ssid}")
            print(f"    BSSID: {network.bssid}")
            print(f"    Channel: {network.channel}")
            print(f"    Encryption: {network.encryption}")
            print(f"    Signal: {network.signal_strength} dBm")
            if network.vulnerabilities:
                print(f"    ⚠️ Vulnerabilities: {', '.join(network.vulnerabilities)}")
