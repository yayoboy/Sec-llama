"""
Network Security Tools for MCP Server

Exposes network discovery, scanning, and vulnerability assessment tools
"""

import json
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.types as types

from modules.network.discovery.host_discovery import HostDiscovery
from modules.network.scanning.port_scanner import PortScanner


def register(server: Server):
    """Register network security tools"""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available network tools"""
        return [
            Tool(
                name="network_discover",
                description="Discover hosts in a network subnet using ARP, ICMP, or TCP methods. Returns list of active hosts with IP, MAC address, hostname, and vendor information.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "subnet": {
                            "type": "string",
                            "description": "Network subnet in CIDR notation (e.g., '192.168.1.0/24')"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["arp", "icmp", "tcp"],
                            "default": "arp",
                            "description": "Discovery method: 'arp' (fast, local), 'icmp' (ping), 'tcp' (port-based)"
                        }
                    },
                    "required": ["subnet"]
                }
            ),
            Tool(
                name="network_scan",
                description="Perform intelligent port scanning with AI analysis. Scans target host for open ports, detects services, versions, and provides security recommendations.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "host": {
                            "type": "string",
                            "description": "Target host IP address or hostname"
                        },
                        "ports": {
                            "type": "string",
                            "description": "Port range to scan (e.g., '1-1000', '22,80,443', or leave empty for default)"
                        },
                        "profile": {
                            "type": "string",
                            "enum": ["quick", "standard", "thorough", "stealth"],
                            "default": "standard",
                            "description": "Scan profile: 'quick' (common ports), 'standard' (1-10000), 'thorough' (all ports), 'stealth' (slow but evasive)"
                        },
                        "ai_analysis": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable AI-powered analysis of scan results"
                        }
                    },
                    "required": ["host"]
                }
            ),
            Tool(
                name="network_vuln_scan",
                description="Comprehensive vulnerability scan combining host discovery, port scanning, service detection, and CVE matching. Provides detailed security assessment of network.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "network": {
                            "type": "string",
                            "description": "Network range to scan in CIDR notation (e.g., '192.168.1.0/24')"
                        },
                        "depth": {
                            "type": "string",
                            "enum": ["quick", "standard", "full"],
                            "default": "standard",
                            "description": "Scan depth: 'quick' (discovery only), 'standard' (with port scan), 'full' (with vulnerability analysis)"
                        }
                    },
                    "required": ["network"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool execution"""

        if name == "network_discover":
            return await _network_discover(arguments)
        elif name == "network_scan":
            return await _network_scan(arguments)
        elif name == "network_vuln_scan":
            return await _network_vuln_scan(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")


async def _network_discover(args: dict) -> list[TextContent]:
    """Execute network discovery"""
    try:
        subnet = args["subnet"]
        method = args.get("method", "arp")

        discovery = HostDiscovery()
        hosts = discovery.discover_network(subnet, method)

        # Format results
        results = {
            "summary": {
                "total_hosts": len(hosts),
                "subnet": subnet,
                "method": method
            },
            "hosts": [
                {
                    "ip": h.ip,
                    "mac": h.mac,
                    "hostname": h.hostname,
                    "vendor": h.vendor,
                    "status": "active"
                }
                for h in hosts
            ]
        }

        output = f"# Network Discovery Results\n\n"
        output += f"**Subnet:** {subnet}\n"
        output += f"**Method:** {method}\n"
        output += f"**Hosts Found:** {len(hosts)}\n\n"

        if hosts:
            output += "## Active Hosts\n\n"
            for h in hosts:
                output += f"### {h.ip}\n"
                output += f"- **MAC:** {h.mac}\n"
                output += f"- **Hostname:** {h.hostname or 'N/A'}\n"
                output += f"- **Vendor:** {h.vendor or 'Unknown'}\n\n"
        else:
            output += "*No hosts found in this subnet.*\n"

        output += f"\n```json\n{json.dumps(results, indent=2)}\n```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"Network discovery failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]


async def _network_scan(args: dict) -> list[TextContent]:
    """Execute port scanning"""
    try:
        host = args["host"]
        ports = args.get("ports")
        profile = args.get("profile", "standard")
        ai_analysis = args.get("ai_analysis", True)

        scanner = PortScanner()
        result = scanner.scan(
            target=host,
            ports=ports,
            scan_type=profile,
            ai_suggest=ai_analysis
        )

        # Format results
        output = f"# Port Scan Results\n\n"
        output += f"**Target:** {host}\n"
        output += f"**Profile:** {profile}\n"
        output += f"**Scan Time:** {result.scan_time:.2f}s\n\n"

        if result.services:
            output += f"## Open Ports ({len(result.services)})\n\n"

            for service in result.services:
                output += f"### Port {service.port}/{service.protocol}\n"
                output += f"- **Service:** {service.name}\n"
                output += f"- **Version:** {service.version or 'Unknown'}\n"
                output += f"- **State:** {service.state}\n"

                if service.cve_matches:
                    output += f"- **⚠️ CVE Matches:** {', '.join(service.cve_matches)}\n"

                output += "\n"

            # AI Analysis summary
            if ai_analysis and hasattr(result, 'ai_summary'):
                output += f"## AI Analysis\n\n{result.ai_summary}\n\n"

        else:
            output += "*No open ports found.*\n"

        # JSON details
        result_dict = {
            "host": host,
            "scan_time": result.scan_time,
            "open_ports": len(result.services),
            "services": [
                {
                    "port": s.port,
                    "protocol": s.protocol,
                    "service": s.name,
                    "version": s.version,
                    "cve_matches": s.cve_matches
                }
                for s in result.services
            ]
        }

        output += f"\n```json\n{json.dumps(result_dict, indent=2)}\n```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"Port scan failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]


async def _network_vuln_scan(args: dict) -> list[TextContent]:
    """Execute comprehensive vulnerability scan"""
    try:
        network = args["network"]
        depth = args.get("depth", "standard")

        output = f"# Comprehensive Network Vulnerability Scan\n\n"
        output += f"**Network:** {network}\n"
        output += f"**Depth:** {depth}\n\n"

        # Phase 1: Discovery
        output += "## Phase 1: Host Discovery\n\n"
        discovery = HostDiscovery()
        hosts = discovery.discover_network(network)
        output += f"✓ Found {len(hosts)} active hosts\n\n"

        if not hosts:
            return [TextContent(type="text", text=output + "*No active hosts found.*\n")]

        # Phase 2: Port Scanning (if depth >= standard)
        if depth in ["standard", "full"]:
            output += "## Phase 2: Port Scanning\n\n"
            scanner = PortScanner()
            scan_results = []

            for host in hosts[:5]:  # Limit to first 5 hosts for performance
                result = scanner.scan(
                    target=host.ip,
                    scan_type="quick" if depth == "standard" else "standard",
                    ai_suggest=True
                )
                scan_results.append((host, result))

                output += f"### {host.ip}\n"
                output += f"- Open ports: {len(result.services)}\n"

                if result.services:
                    for svc in result.services[:3]:  # Show top 3
                        output += f"  - Port {svc.port}: {svc.name} {svc.version or ''}\n"

                output += "\n"

            # Phase 3: Vulnerability Analysis (if depth == full)
            if depth == "full":
                output += "## Phase 3: Vulnerability Analysis\n\n"
                total_vulns = 0

                for host, result in scan_results:
                    for service in result.services:
                        if service.cve_matches:
                            total_vulns += len(service.cve_matches)
                            output += f"⚠️ **{host.ip}:{service.port}** - {', '.join(service.cve_matches)}\n"

                output += f"\n**Total vulnerabilities found:** {total_vulns}\n\n"

        # Summary
        output += "## Summary\n\n"
        output += f"- Hosts scanned: {len(hosts)}\n"
        output += f"- Scan depth: {depth}\n"
        output += f"- Status: ✓ Complete\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"Vulnerability scan failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]
