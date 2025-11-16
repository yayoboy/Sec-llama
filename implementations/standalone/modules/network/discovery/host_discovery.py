"""
Host Discovery Module
Network reconnaissance and host enumeration
"""

import subprocess
import ipaddress
import socket
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from scapy.all import ARP, Ether, srp, IP, ICMP, sr1
import concurrent.futures

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class DiscoveredHost:
    """Discovered host information"""
    ip: str
    mac: str = ""
    hostname: str = ""
    os_guess: str = ""
    open_ports: List[int] = None
    is_alive: bool = True
    response_time: float = 0.0

    def __post_init__(self):
        if self.open_ports is None:
            self.open_ports = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HostDiscovery:
    """Network host discovery and reconnaissance"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.timeout = self.config.network.default_timeout
        self.discovered_hosts: List[DiscoveredHost] = []

    def discover_network(self, network: str, method: str = "arp") -> List[DiscoveredHost]:
        """
        Discover hosts in a network

        Args:
            network: Network CIDR (e.g., "192.168.1.0/24")
            method: Discovery method (arp, icmp, tcp)

        Returns:
            List of discovered hosts
        """
        print(f"[*] Discovering hosts in {network} using {method} method...")

        if method == "arp":
            hosts = self._arp_scan(network)
        elif method == "icmp":
            hosts = self._icmp_scan(network)
        elif method == "tcp":
            hosts = self._tcp_scan(network)
        else:
            raise ValueError(f"Unknown discovery method: {method}")

        self.discovered_hosts.extend(hosts)

        # Get AI insights on discovered hosts
        if hosts:
            self._analyze_discovered_hosts(hosts)

        return hosts

    def _arp_scan(self, network: str) -> List[DiscoveredHost]:
        """ARP scan for local network"""
        print(f"[*] Running ARP scan on {network}...")

        try:
            # Create ARP request
            arp = ARP(pdst=network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether / arp

            # Send packets and receive responses
            result = srp(packet, timeout=self.timeout, verbose=False)[0]

            hosts = []
            for sent, received in result:
                host = DiscoveredHost(
                    ip=received.psrc,
                    mac=received.hwsrc,
                    is_alive=True,
                )
                # Try to resolve hostname
                try:
                    host.hostname = socket.gethostbyaddr(host.ip)[0]
                except (socket.herror, socket.gaierror):
                    host.hostname = ""

                hosts.append(host)
                print(f"[+] Found: {host.ip} ({host.mac}) - {host.hostname or 'Unknown'}")

            return hosts

        except PermissionError:
            print("[!] ARP scan requires root privileges. Falling back to ICMP...")
            return self._icmp_scan(network)
        except Exception as e:
            print(f"[!] ARP scan failed: {e}")
            return []

    def _icmp_scan(self, network: str) -> List[DiscoveredHost]:
        """ICMP ping scan"""
        print(f"[*] Running ICMP ping scan on {network}...")

        try:
            net = ipaddress.ip_network(network, strict=False)
            hosts = []

            def ping_host(ip: str) -> Optional[DiscoveredHost]:
                """Ping a single host"""
                try:
                    packet = IP(dst=str(ip)) / ICMP()
                    reply = sr1(packet, timeout=1, verbose=False)

                    if reply:
                        host = DiscoveredHost(ip=str(ip), is_alive=True)
                        try:
                            host.hostname = socket.gethostbyaddr(str(ip))[0]
                        except (socket.herror, socket.gaierror):
                            pass
                        return host
                except Exception:
                    pass
                return None

            # Parallel ping
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(ping_host, net.hosts())

            hosts = [h for h in results if h is not None]

            for host in hosts:
                print(f"[+] Host up: {host.ip} - {host.hostname or 'Unknown'}")

            return hosts

        except Exception as e:
            print(f"[!] ICMP scan failed: {e}")
            return []

    def _tcp_scan(self, network: str, ports: List[int] = None) -> List[DiscoveredHost]:
        """TCP SYN scan for host discovery"""
        if ports is None:
            ports = [80, 443, 22, 21, 3389]  # Common ports

        print(f"[*] Running TCP scan on {network} (ports: {ports})...")

        try:
            net = ipaddress.ip_network(network, strict=False)
            hosts = []

            def check_host(ip: str) -> Optional[DiscoveredHost]:
                """Check if host has any open ports"""
                for port in ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((str(ip), port))
                    sock.close()

                    if result == 0:
                        host = DiscoveredHost(ip=str(ip), is_alive=True)
                        host.open_ports.append(port)
                        try:
                            host.hostname = socket.gethostbyaddr(str(ip))[0]
                        except (socket.herror, socket.gaierror):
                            pass
                        return host
                return None

            # Parallel scanning
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(check_host, net.hosts())

            hosts = [h for h in results if h is not None]

            for host in hosts:
                print(f"[+] Host up: {host.ip} - Open ports: {host.open_ports}")

            return hosts

        except Exception as e:
            print(f"[!] TCP scan failed: {e}")
            return []

    def _analyze_discovered_hosts(self, hosts: List[DiscoveredHost]):
        """Use LLM to analyze discovered hosts"""
        print("\n[*] Analyzing discovered hosts with AI...")

        host_summary = "\n".join([
            f"- {h.ip} ({h.hostname or 'Unknown'}) - MAC: {h.mac} - Ports: {h.open_ports}"
            for h in hosts
        ])

        prompt = f"""Analyze the following discovered network hosts:

{host_summary}

Provide:
1. Network topology assessment
2. Device type identification (router, server, workstation, IoT, etc.)
3. Potential security concerns
4. Recommended next steps for security assessment

Be concise and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 60)
            print("AI ANALYSIS:")
            print("=" * 60)
            print(analysis)
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def fingerprint_os(self, ip: str) -> str:
        """
        OS fingerprinting using TTL and other techniques

        Args:
            ip: Target IP address

        Returns:
            OS guess
        """
        try:
            # Send ICMP packet and analyze TTL
            packet = IP(dst=ip) / ICMP()
            reply = sr1(packet, timeout=2, verbose=False)

            if reply:
                ttl = reply.ttl

                # Common TTL values
                if ttl <= 64:
                    os_guess = "Linux/Unix"
                elif ttl <= 128:
                    os_guess = "Windows"
                elif ttl <= 255:
                    os_guess = "Cisco/Network Device"
                else:
                    os_guess = "Unknown"

                return os_guess

        except Exception as e:
            print(f"[!] OS fingerprinting failed: {e}")

        return "Unknown"

    def get_network_topology(self) -> Dict[str, Any]:
        """
        Generate network topology map

        Returns:
            Dictionary representing network topology
        """
        if not self.discovered_hosts:
            return {"error": "No hosts discovered"}

        topology = {
            "total_hosts": len(self.discovered_hosts),
            "hosts": [h.to_dict() for h in self.discovered_hosts],
            "subnets": {},
        }

        # Group by subnet
        for host in self.discovered_hosts:
            try:
                ip_obj = ipaddress.ip_address(host.ip)
                # Assume /24 subnet
                subnet = str(ipaddress.ip_network(f"{host.ip}/24", strict=False))

                if subnet not in topology["subnets"]:
                    topology["subnets"][subnet] = []

                topology["subnets"][subnet].append(host.ip)
            except Exception:
                pass

        return topology

    def export_results(self, output_file: str, format: str = "json"):
        """Export discovery results"""
        import json

        if format == "json":
            data = {
                "total_hosts": len(self.discovered_hosts),
                "hosts": [h.to_dict() for h in self.discovered_hosts],
            }

            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)

            print(f"[+] Results exported to {output_file}")

        elif format == "csv":
            import csv

            with open(output_file, "w", newline="") as f:
                if not self.discovered_hosts:
                    return

                writer = csv.DictWriter(f, fieldnames=self.discovered_hosts[0].to_dict().keys())
                writer.writeheader()
                for host in self.discovered_hosts:
                    writer.writerow(host.to_dict())

            print(f"[+] Results exported to {output_file}")
