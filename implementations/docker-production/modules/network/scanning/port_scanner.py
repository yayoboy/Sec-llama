"""
Smart Port Scanner with AI-powered analysis
Integrates with nmap and provides intelligent insights
"""

import subprocess
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import socket

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class ServiceInfo:
    """Service information"""
    port: int
    protocol: str
    state: str
    service: str
    version: str = ""
    product: str = ""
    extra_info: str = ""
    cpes: List[str] = None
    vulnerabilities: List[str] = None

    def __post_init__(self):
        if self.cpes is None:
            self.cpes = []
        if self.vulnerabilities is None:
            self.vulnerabilities = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScanResult:
    """Port scan result"""
    host: str
    hostname: str = ""
    state: str = "unknown"
    os_guess: str = ""
    services: List[ServiceInfo] = None
    scan_stats: Dict[str, Any] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []
        if self.scan_stats is None:
            self.scan_stats = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "host": self.host,
            "hostname": self.hostname,
            "state": self.state,
            "os_guess": self.os_guess,
            "services": [s.to_dict() for s in self.services],
            "scan_stats": self.scan_stats,
        }


class PortScanner:
    """Smart port scanner with AI analysis"""

    def __init__(self):
        self.config = get_config()
        self.llm = get_llm()
        self.nmap_path = self.config.scanning.nmap_path
        self.results: List[ScanResult] = []

    def scan(
        self,
        target: str,
        ports: str = None,
        scan_type: str = "standard",
        ai_suggest: bool = False,
    ) -> ScanResult:
        """
        Scan a target with intelligent port selection

        Args:
            target: Target IP or hostname
            ports: Port specification (e.g., "1-1000", "22,80,443")
            scan_type: Scan profile (quick, standard, thorough, stealth)
            ai_suggest: Use AI to suggest optimal scan strategy

        Returns:
            ScanResult object
        """
        print(f"[*] Scanning target: {target}")

        # AI-powered scan strategy
        if ai_suggest:
            ports, scan_args = self._ai_suggest_scan_strategy(target)
        else:
            # Use profile from config
            profile = self.config.network.scan_profiles.get(scan_type, {})
            ports = ports or profile.get("ports", "1-1000")
            scan_args = [f"-T{profile.get('timing', '3')}"]

        # Run nmap scan
        result = self._run_nmap(target, ports, scan_args)

        # AI analysis of results
        if result.services:
            self._ai_analyze_services(result)

        self.results.append(result)
        return result

    def _ai_suggest_scan_strategy(self, target: str) -> tuple:
        """Use AI to suggest optimal scanning strategy"""
        print("[*] Consulting AI for optimal scan strategy...")

        # Get initial info about target
        try:
            hostname = socket.gethostbyaddr(target)[0]
        except:
            hostname = "Unknown"

        prompt = f"""As a network reconnaissance expert, suggest an optimal nmap scanning strategy for:

Target: {target}
Hostname: {hostname}

Provide:
1. **Port Selection**: Which specific ports to scan (format: "22,80,443,3389" or "1-1000")
2. **Scan Arguments**: Additional nmap arguments
3. **Reasoning**: Why this strategy?

Format your response as:
PORTS: <port list>
ARGS: <nmap arguments>
REASONING: <explanation>"""

        try:
            response = self.llm.generate(prompt)

            # Parse response
            ports = "1-1000"  # default
            args = ["-T3"]  # default

            for line in response.split("\n"):
                if line.startswith("PORTS:"):
                    ports = line.split("PORTS:")[1].strip()
                elif line.startswith("ARGS:"):
                    args_str = line.split("ARGS:")[1].strip()
                    args = args_str.split() if args_str else ["-T3"]

            print(f"[+] AI suggests: Ports={ports}, Args={args}")
            return ports, args

        except Exception as e:
            print(f"[!] AI suggestion failed: {e}. Using defaults.")
            return "1-1000", ["-T3"]

    def _run_nmap(
        self,
        target: str,
        ports: str,
        additional_args: List[str] = None,
    ) -> ScanResult:
        """Run nmap scan"""
        if additional_args is None:
            additional_args = []

        # Build nmap command
        cmd = [
            self.nmap_path,
            "-p", ports,
            "-sV",  # Version detection
            "-sC",  # Default scripts
            "--open",  # Only show open ports
            "-oX", "-",  # XML output to stdout
        ]
        cmd.extend(additional_args)
        cmd.append(target)

        print(f"[*] Running: {' '.join(cmd)}")

        try:
            # Run nmap
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if process.returncode != 0:
                print(f"[!] Nmap error: {process.stderr}")
                return ScanResult(host=target, state="error")

            # Parse XML output
            result = self._parse_nmap_xml(process.stdout)
            return result

        except subprocess.TimeoutExpired:
            print(f"[!] Scan timeout for {target}")
            return ScanResult(host=target, state="timeout")
        except FileNotFoundError:
            print(f"[!] Nmap not found at {self.nmap_path}")
            return ScanResult(host=target, state="error")
        except Exception as e:
            print(f"[!] Scan failed: {e}")
            return ScanResult(host=target, state="error")

    def _parse_nmap_xml(self, xml_output: str) -> ScanResult:
        """Parse nmap XML output"""
        try:
            root = ET.fromstring(xml_output)

            # Get host info
            host_elem = root.find(".//host")
            if host_elem is None:
                return ScanResult(host="Unknown", state="down")

            # IP address
            addr_elem = host_elem.find(".//address[@addrtype='ipv4']")
            ip = addr_elem.get("addr") if addr_elem is not None else "Unknown"

            # Hostname
            hostname_elem = host_elem.find(".//hostname")
            hostname = hostname_elem.get("name") if hostname_elem is not None else ""

            # Host state
            state_elem = host_elem.find(".//status")
            state = state_elem.get("state") if state_elem is not None else "unknown"

            # OS detection
            os_guess = ""
            osmatch_elem = host_elem.find(".//osmatch")
            if osmatch_elem is not None:
                os_guess = osmatch_elem.get("name", "")

            # Parse services
            services = []
            for port_elem in host_elem.findall(".//port"):
                port = int(port_elem.get("portid"))
                protocol = port_elem.get("protocol")

                state_elem = port_elem.find("state")
                port_state = state_elem.get("state") if state_elem is not None else "unknown"

                service_elem = port_elem.find("service")
                if service_elem is not None:
                    service = ServiceInfo(
                        port=port,
                        protocol=protocol,
                        state=port_state,
                        service=service_elem.get("name", ""),
                        version=service_elem.get("version", ""),
                        product=service_elem.get("product", ""),
                        extra_info=service_elem.get("extrainfo", ""),
                    )

                    # Get CPEs
                    for cpe_elem in service_elem.findall("cpe"):
                        service.cpes.append(cpe_elem.text)

                    services.append(service)

            result = ScanResult(
                host=ip,
                hostname=hostname,
                state=state,
                os_guess=os_guess,
                services=services,
            )

            # Print results
            print(f"\n[+] Scan complete for {ip}")
            print(f"    Hostname: {hostname or 'Unknown'}")
            print(f"    State: {state}")
            print(f"    OS: {os_guess or 'Unknown'}")
            print(f"    Open ports: {len(services)}")

            for service in services:
                version_info = f"{service.product} {service.version}".strip()
                print(f"    - {service.port}/{service.protocol}: {service.service} {version_info}")

            return result

        except ET.ParseError as e:
            print(f"[!] XML parse error: {e}")
            return ScanResult(host="Unknown", state="error")

    def _ai_analyze_services(self, result: ScanResult):
        """AI analysis of discovered services"""
        print("\n[*] Analyzing services with AI...")

        services_summary = "\n".join([
            f"- Port {s.port}/{s.protocol}: {s.service} {s.product} {s.version}"
            for s in result.services
        ])

        prompt = f"""Analyze the following services found on {result.host}:

{services_summary}

Hostname: {result.hostname}
OS: {result.os_guess}

Provide:
1. **Security Assessment**: Vulnerabilities and security concerns for each service
2. **CVE Lookup**: Known CVEs for these service versions
3. **Attack Vectors**: Potential ways to exploit these services
4. **Risk Rating**: Overall risk level (CRITICAL/HIGH/MEDIUM/LOW)
5. **Next Steps**: Recommended follow-up scans or tests

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            print("\n" + "=" * 60)
            print("AI SECURITY ANALYSIS:")
            print("=" * 60)
            print(analysis)
            print("=" * 60 + "\n")

            # Store analysis in result
            result.scan_stats["ai_analysis"] = analysis

        except Exception as e:
            print(f"[!] AI analysis failed: {e}")

    def scan_multiple(
        self,
        targets: List[str],
        ports: str = None,
        scan_type: str = "standard",
    ) -> List[ScanResult]:
        """Scan multiple targets"""
        results = []
        for target in targets:
            result = self.scan(target, ports, scan_type)
            results.append(result)
        return results

    def export_results(self, output_file: str, format: str = "json"):
        """Export scan results"""
        if format == "json":
            data = {
                "total_hosts": len(self.results),
                "results": [r.to_dict() for r in self.results],
            }

            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)

            print(f"[+] Results exported to {output_file}")

        elif format == "html":
            # Simple HTML report
            html = self._generate_html_report()
            with open(output_file, "w") as f:
                f.write(html)
            print(f"[+] HTML report saved to {output_file}")

    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Sec-Llama Scan Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        .critical { color: red; font-weight: bold; }
        .high { color: orange; font-weight: bold; }
        .medium { color: #FFA500; }
        .low { color: green; }
    </style>
</head>
<body>
    <h1>Sec-Llama Network Scan Report</h1>
"""

        for result in self.results:
            html += f"""
    <h2>Host: {result.host}</h2>
    <p><strong>Hostname:</strong> {result.hostname or 'Unknown'}</p>
    <p><strong>State:</strong> {result.state}</p>
    <p><strong>OS:</strong> {result.os_guess or 'Unknown'}</p>

    <h3>Open Ports</h3>
    <table>
        <tr>
            <th>Port</th>
            <th>Protocol</th>
            <th>Service</th>
            <th>Version</th>
        </tr>
"""

            for service in result.services:
                version = f"{service.product} {service.version}".strip()
                html += f"""
        <tr>
            <td>{service.port}</td>
            <td>{service.protocol}</td>
            <td>{service.service}</td>
            <td>{version or 'Unknown'}</td>
        </tr>
"""

            html += """
    </table>
"""

        html += """
</body>
</html>
"""
        return html
