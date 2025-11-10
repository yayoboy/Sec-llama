#!/usr/bin/env python3
"""
Sec-Llama Suite - Basic Usage Examples
"""

from core.config import load_config
from core.llm_interface import get_llm
from modules.network.discovery.host_discovery import HostDiscovery
from modules.network.scanning.port_scanner import PortScanner
from modules.vuln_scanner.code_scanner import CodeScanner
from modules.pentest_assistant.attack_planner import AttackPlanner
from modules.threat_intel.cve_lookup import CVELookup


def example_network_discovery():
    """Example: Network discovery"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Network Discovery")
    print("=" * 80)

    discovery = HostDiscovery()
    hosts = discovery.discover_network("192.168.1.0/24", method="arp")

    print(f"\nDiscovered {len(hosts)} hosts")


def example_port_scanning():
    """Example: Smart port scanning"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Smart Port Scanning")
    print("=" * 80)

    scanner = PortScanner()

    # Standard scan
    result = scanner.scan("192.168.1.1", ports="1-1000", scan_type="standard")

    # AI-suggested scan
    result = scanner.scan("192.168.1.1", ai_suggest=True)


def example_code_scanning():
    """Example: Code vulnerability scanning"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Code Vulnerability Scanning")
    print("=" * 80)

    scanner = CodeScanner()

    # Scan current directory
    vulns = scanner.scan_directory("./", language="python")

    scanner.print_report()


def example_attack_planning():
    """Example: AI-powered attack planning"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Attack Planning")
    print("=" * 80)

    planner = AttackPlanner()

    target_info = {
        "ip": "192.168.1.10",
        "hostname": "webserver01",
        "os": "Linux",
        "open_ports": [22, 80, 443],
        "services": {
            "22": "OpenSSH 7.4",
            "80": "Apache 2.4.6",
            "443": "Apache 2.4.6",
        },
    }

    plan = planner.plan_attack(
        target_info=target_info,
        objective="Gain root access",
        constraints=["No destructive actions", "Avoid detection"],
    )


def example_exploit_suggestions():
    """Example: Exploit suggestions"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Exploit Suggestions")
    print("=" * 80)

    planner = AttackPlanner()

    suggestions = planner.suggest_exploit(
        service="Apache",
        version="2.4.49",
        context="Publicly accessible web server",
    )


def example_cve_lookup():
    """Example: CVE lookup"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: CVE Lookup")
    print("=" * 80)

    lookup = CVELookup()

    # Lookup specific CVE
    cve = lookup.lookup_cve("CVE-2021-44228")  # Log4Shell

    # Search CVEs
    results = lookup.search_cves("apache", max_results=5)


def example_ai_analysis():
    """Example: Direct AI analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Direct AI Analysis")
    print("=" * 80)

    llm = get_llm()

    # Analyze scan results
    scan_data = """
    Host: 192.168.1.10
    Open ports: 22, 80, 445, 3389
    Services:
    - 22: OpenSSH 7.4
    - 80: Apache 2.4.6
    - 445: SMB (Samba 4.2.3)
    - 3389: RDP
    """

    analysis = llm.analyze_security(scan_data, analysis_type="network")
    print(analysis["analysis"])


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("SEC-LLAMA SUITE - USAGE EXAMPLES")
    print("=" * 80)

    # Load configuration
    config = load_config()
    print(f"Using LLM: {config.llm.model}")

    # Run examples (commented out to avoid actual scanning)
    # Uncomment to run specific examples

    # example_network_discovery()
    # example_port_scanning()
    # example_code_scanning()
    # example_attack_planning()
    # example_exploit_suggestions()
    # example_cve_lookup()
    # example_ai_analysis()

    print("\n✓ Examples loaded. Uncomment functions to run specific examples.")


if __name__ == "__main__":
    main()
