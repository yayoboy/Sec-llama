"""
Packet Analyzer - PCAP analysis with AI-powered insights
"""

import os
import subprocess
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import Counter
from scapy.all import rdpcap, IP, TCP, UDP, DNS, Raw, ARP, ICMP

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class PacketStats:
    """Packet statistics"""
    total_packets: int = 0
    protocols: Dict[str, int] = None
    src_ips: Dict[str, int] = None
    dst_ips: Dict[str, int] = None
    src_ports: Dict[int, int] = None
    dst_ports: Dict[int, int] = None
    dns_queries: List[str] = None
    suspicious_patterns: List[str] = None

    def __post_init__(self):
        if self.protocols is None:
            self.protocols = {}
        if self.src_ips is None:
            self.src_ips = {}
        if self.dst_ips is None:
            self.dst_ips = {}
        if self.src_ports is None:
            self.src_ports = {}
        if self.dst_ports is None:
            self.dst_ports = {}
        if self.dns_queries is None:
            self.dns_queries = []
        if self.suspicious_patterns is None:
            self.suspicious_patterns = []


class PacketAnalyzer:
    """Network traffic analyzer with AI insights"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.stats = PacketStats()

    def analyze_pcap(self, pcap_file: str, ai_analysis: bool = True) -> PacketStats:
        """
        Analyze PCAP file

        Args:
            pcap_file: Path to PCAP file
            ai_analysis: Use AI for advanced analysis

        Returns:
            PacketStats object
        """
        print(f"[*] Analyzing PCAP: {pcap_file}")

        if not os.path.exists(pcap_file):
            print(f"[!] File not found: {pcap_file}")
            return self.stats

        try:
            # Read PCAP
            packets = rdpcap(pcap_file)
            self.stats.total_packets = len(packets)

            print(f"[*] Loaded {len(packets)} packets")

            # Analyze packets
            self._analyze_packets(packets)

            # Print statistics
            self._print_stats()

            # AI analysis
            if ai_analysis:
                self._ai_analyze_traffic()

            return self.stats

        except Exception as e:
            print(f"[!] PCAP analysis failed: {e}")
            return self.stats

    def _analyze_packets(self, packets):
        """Analyze packet contents"""
        protocol_counter = Counter()
        src_ip_counter = Counter()
        dst_ip_counter = Counter()
        src_port_counter = Counter()
        dst_port_counter = Counter()

        for packet in packets:
            # Protocol analysis
            if IP in packet:
                protocol_counter[packet[IP].proto] += 1
                src_ip_counter[packet[IP].src] += 1
                dst_ip_counter[packet[IP].dst] += 1

                # TCP analysis
                if TCP in packet:
                    src_port_counter[packet[TCP].sport] += 1
                    dst_port_counter[packet[TCP].dport] += 1

                    # Check for suspicious patterns
                    self._check_suspicious_tcp(packet)

                # UDP analysis
                if UDP in packet:
                    src_port_counter[packet[UDP].sport] += 1
                    dst_port_counter[packet[UDP].dport] += 1

                # DNS analysis
                if DNS in packet and packet.haslayer(DNS):
                    self._analyze_dns(packet)

            # ARP analysis
            if ARP in packet:
                protocol_counter["ARP"] += 1
                self._check_arp_spoofing(packet)

            # Check for credentials in clear text
            if Raw in packet:
                self._check_credentials(packet)

        # Convert to dict
        self.stats.protocols = dict(protocol_counter)
        self.stats.src_ips = dict(src_ip_counter.most_common(20))
        self.stats.dst_ips = dict(dst_ip_counter.most_common(20))
        self.stats.src_ports = dict(src_port_counter.most_common(20))
        self.stats.dst_ports = dict(dst_port_counter.most_common(20))

    def _check_suspicious_tcp(self, packet):
        """Check for suspicious TCP patterns"""
        if TCP in packet:
            # Port scanning detection (SYN scan)
            if packet[TCP].flags == 2:  # SYN flag
                self.stats.suspicious_patterns.append(
                    f"Possible port scan: {packet[IP].src} -> {packet[IP].dst}:{packet[TCP].dport}"
                )

            # Suspicious ports
            suspicious_ports = [4444, 5555, 6666, 31337]  # Common backdoor ports
            if packet[TCP].dport in suspicious_ports or packet[TCP].sport in suspicious_ports:
                self.stats.suspicious_patterns.append(
                    f"Suspicious port: {packet[TCP].sport} -> {packet[TCP].dport}"
                )

    def _analyze_dns(self, packet):
        """Analyze DNS queries"""
        if packet.haslayer(DNS) and packet[DNS].qr == 0:  # Query
            qname = packet[DNS].qd.qname.decode('utf-8', errors='ignore')
            self.stats.dns_queries.append(qname)

            # Check for DNS tunneling (long subdomains)
            if len(qname) > 50:
                self.stats.suspicious_patterns.append(
                    f"Possible DNS tunneling: {qname}"
                )

    def _check_arp_spoofing(self, packet):
        """Detect ARP spoofing attempts"""
        if ARP in packet and packet[ARP].op == 2:  # ARP reply
            # This is a simplified check - in production, you'd track ARP cache
            self.stats.suspicious_patterns.append(
                f"ARP reply: {packet[ARP].psrc} is at {packet[ARP].hwsrc}"
            )

    def _check_credentials(self, packet):
        """Check for credentials in cleartext"""
        if Raw in packet:
            payload = packet[Raw].load

            # Convert to string (ignore errors)
            try:
                payload_str = payload.decode('utf-8', errors='ignore').lower()

                # Look for common credential patterns
                credential_keywords = ['password', 'passwd', 'pwd', 'user', 'login', 'auth']
                for keyword in credential_keywords:
                    if keyword in payload_str:
                        self.stats.suspicious_patterns.append(
                            f"Possible credentials in cleartext: {packet[IP].src} -> {packet[IP].dst}"
                        )
                        break
            except:
                pass

    def _print_stats(self):
        """Print traffic statistics"""
        print("\n" + "=" * 60)
        print("TRAFFIC STATISTICS")
        print("=" * 60)

        print(f"\nTotal packets: {self.stats.total_packets}")

        print("\nTop protocols:")
        for proto, count in sorted(self.stats.protocols.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - Protocol {proto}: {count} packets")

        print("\nTop source IPs:")
        for ip, count in list(self.stats.src_ips.items())[:10]:
            print(f"  - {ip}: {count} packets")

        print("\nTop destination IPs:")
        for ip, count in list(self.stats.dst_ips.items())[:10]:
            print(f"  - {ip}: {count} packets")

        print("\nTop destination ports:")
        for port, count in list(self.stats.dst_ports.items())[:10]:
            print(f"  - Port {port}: {count} packets")

        if self.stats.dns_queries:
            print(f"\nDNS queries found: {len(self.stats.dns_queries)}")
            print("Top DNS queries:")
            dns_counter = Counter(self.stats.dns_queries)
            for query, count in dns_counter.most_common(10):
                print(f"  - {query}: {count} times")

        if self.stats.suspicious_patterns:
            print(f"\n⚠️  Suspicious patterns detected: {len(self.stats.suspicious_patterns)}")
            for pattern in self.stats.suspicious_patterns[:20]:
                print(f"  - {pattern}")

        print("=" * 60 + "\n")

    def _ai_analyze_traffic(self):
        """AI-powered traffic analysis"""
        print("[*] Performing AI analysis of traffic patterns...")

        # Prepare summary for LLM
        summary = f"""Total packets: {self.stats.total_packets}

Top protocols: {', '.join([f"{p}:{c}" for p, c in list(self.stats.protocols.items())[:5]])}

Top source IPs: {', '.join([f"{ip}({c})" for ip, c in list(self.stats.src_ips.items())[:5]])}

Top destination IPs: {', '.join([f"{ip}({c})" for ip, c in list(self.stats.dst_ips.items())[:5]])}

Top destination ports: {', '.join([f"{p}:{c}" for p, c in list(self.stats.dst_ports.items())[:10]])}

DNS queries: {len(self.stats.dns_queries)}
Sample queries: {', '.join(self.stats.dns_queries[:10])}

Suspicious patterns detected: {len(self.stats.suspicious_patterns)}
{chr(10).join(self.stats.suspicious_patterns[:10]) if self.stats.suspicious_patterns else "None"}
"""

        from core.prompt_templates import PromptTemplates
        prompt = PromptTemplates.get_traffic_analysis_prompt(summary)

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 60)
            print("AI TRAFFIC ANALYSIS:")
            print("=" * 60)
            print(analysis)
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def capture_live(
        self,
        interface: str,
        duration: int = 60,
        output_file: str = "capture.pcap",
    ) -> str:
        """
        Capture live traffic

        Args:
            interface: Network interface (e.g., eth0, wlan0)
            duration: Capture duration in seconds
            output_file: Output PCAP file

        Returns:
            Path to captured PCAP file
        """
        print(f"[*] Capturing traffic on {interface} for {duration} seconds...")

        try:
            # Use tcpdump for capture
            cmd = [
                "tcpdump",
                "-i", interface,
                "-w", output_file,
                "-G", str(duration),
                "-W", "1",
            ]

            subprocess.run(cmd, timeout=duration + 10, check=True)

            print(f"[+] Capture saved to {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            print(f"[!] Capture failed: {e}")
            return ""
        except FileNotFoundError:
            print("[!] tcpdump not found. Install with: apt install tcpdump")
            return ""

    def find_credentials(self, pcap_file: str) -> List[Dict[str, str]]:
        """
        Search for credentials in PCAP

        Args:
            pcap_file: Path to PCAP file

        Returns:
            List of potential credentials found
        """
        print(f"[*] Searching for credentials in {pcap_file}...")

        credentials = []

        try:
            packets = rdpcap(pcap_file)

            for packet in packets:
                if Raw in packet:
                    payload = packet[Raw].load

                    try:
                        payload_str = payload.decode('utf-8', errors='ignore')

                        # HTTP Basic Auth
                        if 'Authorization: Basic' in payload_str:
                            credentials.append({
                                "type": "HTTP Basic Auth",
                                "source": packet[IP].src if IP in packet else "Unknown",
                                "data": payload_str[:200],
                            })

                        # FTP credentials
                        if payload_str.startswith('USER ') or payload_str.startswith('PASS '):
                            credentials.append({
                                "type": "FTP",
                                "source": packet[IP].src if IP in packet else "Unknown",
                                "data": payload_str.strip(),
                            })

                        # SMTP/POP3/IMAP
                        if any(keyword in payload_str for keyword in ['AUTH LOGIN', 'AUTH PLAIN']):
                            credentials.append({
                                "type": "Email Auth",
                                "source": packet[IP].src if IP in packet else "Unknown",
                                "data": payload_str[:200],
                            })

                    except:
                        pass

            if credentials:
                print(f"[!] Found {len(credentials)} potential credential leaks!")
                for cred in credentials[:10]:  # Show first 10
                    print(f"  - {cred['type']} from {cred['source']}")
            else:
                print("[+] No obvious credential leaks found")

            return credentials

        except Exception as e:
            print(f"[!] Credential search failed: {e}")
            return []

    def export_report(self, output_file: str):
        """Export analysis report"""
        import json

        report = {
            "total_packets": self.stats.total_packets,
            "protocols": self.stats.protocols,
            "top_src_ips": dict(list(self.stats.src_ips.items())[:20]),
            "top_dst_ips": dict(list(self.stats.dst_ips.items())[:20]),
            "top_dst_ports": {str(k): v for k, v in list(self.stats.dst_ports.items())[:20]},
            "dns_queries_count": len(self.stats.dns_queries),
            "suspicious_patterns": self.stats.suspicious_patterns,
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"[+] Report saved to {output_file}")
