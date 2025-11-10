#!/usr/bin/env python3
"""
Sec-Llama Suite - Main CLI Entry Point
"""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🛡️  Sec-Llama Suite - Local LLM-Powered Cybersecurity Testing

    A comprehensive security testing suite powered by local LLMs (Ollama).
    """
    pass


# ==================== Network Commands ====================

@cli.group()
def network():
    """Network security testing commands"""
    pass


@network.command("discover")
@click.option("--subnet", required=True, help="Network subnet (e.g., 192.168.1.0/24)")
@click.option("--method", default="arp", type=click.Choice(["arp", "icmp", "tcp"]), help="Discovery method")
@click.option("--output", help="Output file")
def network_discover(subnet, method, output):
    """Discover hosts in a network"""
    from modules.network.discovery.host_discovery import HostDiscovery

    console.print(f"[bold green]🔍 Discovering hosts in {subnet}...[/bold green]")

    discovery = HostDiscovery()
    hosts = discovery.discover_network(subnet, method)

    if output:
        discovery.export_results(output, "json")

    console.print(f"\n[bold green]✓ Found {len(hosts)} hosts[/bold green]")


@network.command("scan")
@click.option("--host", required=True, help="Target host IP or hostname")
@click.option("--ports", default=None, help="Ports to scan (e.g., '1-1000' or '22,80,443')")
@click.option("--profile", default="standard", type=click.Choice(["quick", "standard", "thorough", "stealth"]))
@click.option("--ai-suggest", is_flag=True, help="Use AI to suggest optimal scan strategy")
@click.option("--output", help="Output file")
def network_scan(host, ports, profile, ai_suggest, output):
    """Smart port scanning with AI analysis"""
    from modules.network.scanning.port_scanner import PortScanner

    console.print(f"[bold green]🔍 Scanning {host}...[/bold green]")

    scanner = PortScanner()
    result = scanner.scan(host, ports, profile, ai_suggest)

    if output:
        scanner.export_results(output, "json")


@network.command("vuln-scan")
@click.option("--network", required=True, help="Network to scan")
@click.option("--depth", default="standard", type=click.Choice(["quick", "standard", "full"]))
def network_vuln_scan(network, depth):
    """Comprehensive vulnerability scan"""
    console.print(f"[bold green]🔍 Vulnerability scanning {network}...[/bold green]")
    console.print("[yellow]This will perform discovery + port scan + vulnerability analysis[/yellow]")

    from modules.network.discovery.host_discovery import HostDiscovery
    from modules.network.scanning.port_scanner import PortScanner

    # Discovery
    discovery = HostDiscovery()
    hosts = discovery.discover_network(network)

    # Scan each host
    scanner = PortScanner()
    for host in hosts:
        scanner.scan(host.ip, scan_type=depth, ai_suggest=True)


# ==================== Traffic Analysis Commands ====================

@cli.group()
def traffic():
    """Network traffic analysis commands"""
    pass


@traffic.command("analyze")
@click.option("--pcap", required=True, help="PCAP file to analyze")
@click.option("--ai", is_flag=True, default=True, help="Use AI analysis")
@click.option("--output", help="Output report file")
def traffic_analyze(pcap, ai, output):
    """Analyze PCAP file"""
    from modules.network.traffic.packet_analyzer import PacketAnalyzer

    console.print(f"[bold green]📊 Analyzing {pcap}...[/bold green]")

    analyzer = PacketAnalyzer()
    stats = analyzer.analyze_pcap(pcap, ai)

    if output:
        analyzer.export_report(output)


@traffic.command("capture")
@click.option("--interface", required=True, help="Network interface")
@click.option("--duration", default=60, help="Capture duration in seconds")
@click.option("--output", default="capture.pcap", help="Output PCAP file")
def traffic_capture(interface, duration, output):
    """Capture live network traffic"""
    from modules.network.traffic.packet_analyzer import PacketAnalyzer

    console.print(f"[bold green]📡 Capturing traffic on {interface}...[/bold green]")

    analyzer = PacketAnalyzer()
    pcap_file = analyzer.capture_live(interface, duration, output)

    if pcap_file:
        console.print(f"[green]✓ Capture saved to {pcap_file}[/green]")


@traffic.command("find-creds")
@click.option("--pcap", required=True, help="PCAP file to analyze")
def traffic_find_creds(pcap):
    """Search for credentials in PCAP"""
    from modules.network.traffic.packet_analyzer import PacketAnalyzer

    console.print(f"[bold yellow]🔑 Searching for credentials in {pcap}...[/bold yellow]")

    analyzer = PacketAnalyzer()
    creds = analyzer.find_credentials(pcap)

    if creds:
        console.print(f"[bold red]⚠️  Found {len(creds)} potential credential leaks![/bold red]")


# ==================== Wireless Commands ====================

@cli.group()
def wireless():
    """Wireless security testing commands"""
    pass


@wireless.command("scan")
@click.option("--interface", help="Wireless interface (default from config)")
def wireless_scan(interface):
    """Scan for WiFi networks"""
    from modules.network.wireless.wifi_audit import WiFiAuditor

    console.print("[bold green]📡 Scanning WiFi networks...[/bold green]")

    auditor = WiFiAuditor()
    if interface:
        auditor.interface = interface

    networks = auditor.scan_networks()
    console.print(f"\n[green]✓ Found {len(networks)} networks[/green]")


# ==================== Code Security Commands ====================

@cli.group()
def code():
    """Code security analysis commands"""
    pass


@code.command("scan")
@click.option("--path", required=True, help="Directory or file to scan")
@click.option("--language", default="auto", help="Programming language")
@click.option("--output", help="Output file (JSON)")
def code_scan(path, language, output):
    """Scan code for vulnerabilities (SAST)"""
    from modules.vuln_scanner.code_scanner import CodeScanner

    console.print(f"[bold green]🔍 Scanning {path} for vulnerabilities...[/bold green]")

    scanner = CodeScanner()
    vulns = scanner.scan_directory(path, language)

    scanner.print_report()

    if output:
        scanner.export_json(output)


# ==================== Penetration Testing Commands ====================

@cli.group()
def pentest():
    """Penetration testing commands"""
    pass


@pentest.command("attack-plan")
@click.option("--target", required=True, help="Target (IP or hostname)")
@click.option("--objective", required=True, help="Attack objective")
def pentest_attack_plan(target, objective):
    """Generate AI-powered attack plan"""
    from modules.pentest_assistant.attack_planner import AttackPlanner

    console.print(f"[bold green]🎯 Planning attack on {target}...[/bold green]")

    planner = AttackPlanner()

    # Get target info (simplified - would normally scan first)
    target_info = {
        "target": target,
        "services": "Unknown - run scan first",
    }

    plan = planner.plan_attack(target_info, objective)


@pentest.command("exploit")
@click.option("--service", required=True, help="Service name")
@click.option("--version", required=True, help="Service version")
@click.option("--context", default="", help="Additional context")
def pentest_exploit(service, version, context):
    """Suggest exploits for a service"""
    from modules.pentest_assistant.attack_planner import AttackPlanner

    console.print(f"[bold green]💥 Finding exploits for {service} {version}...[/bold green]")

    planner = AttackPlanner()
    suggestions = planner.suggest_exploit(service, version, context)


@pentest.command("payload")
@click.option("--type", required=True, help="Payload type (reverse_shell, bind_shell, etc.)")
@click.option("--os", required=True, help="Target OS (windows, linux, etc.)")
def pentest_payload(type, os):
    """Generate custom payload"""
    from modules.pentest_assistant.attack_planner import AttackPlanner

    console.print(f"[bold green]🔨 Generating {type} payload for {os}...[/bold green]")

    planner = AttackPlanner()
    payload = planner.generate_payload(type, os)


# ==================== Threat Intelligence Commands ====================

@cli.group()
def threat():
    """Threat intelligence commands"""
    pass


@threat.command("cve")
@click.option("--id", required=True, help="CVE ID (e.g., CVE-2024-1234)")
def threat_cve(id):
    """Lookup CVE information"""
    from modules.threat_intel.cve_lookup import CVELookup

    console.print(f"[bold green]🔍 Looking up {id}...[/bold green]")

    lookup = CVELookup()
    cve_info = lookup.lookup_cve(id)


@threat.command("cve-search")
@click.option("--keyword", required=True, help="Search keyword")
@click.option("--max", default=10, help="Maximum results")
def threat_cve_search(keyword, max):
    """Search CVEs by keyword"""
    from modules.threat_intel.cve_lookup import CVELookup

    console.print(f"[bold green]🔍 Searching CVEs for: {keyword}...[/bold green]")

    lookup = CVELookup()
    cves = lookup.search_cves(keyword, max)


@threat.command("ioc")
@click.option("--indicator", required=True, help="IOC (IP, domain, hash, etc.)")
@click.option("--type", default="auto", help="IOC type")
def threat_ioc(indicator, type):
    """Analyze Indicator of Compromise"""
    from modules.threat_intel.ioc_analyzer import IOCAnalyzer

    console.print(f"[bold green]🔍 Analyzing IOC: {indicator}...[/bold green]")

    analyzer = IOCAnalyzer()
    result = analyzer.analyze_ioc(indicator, type)


# ==================== Natural Language Query ====================

@cli.command("ask")
@click.argument("question", nargs=-1, required=True)
def ask(question):
    """Ask a security question in natural language"""
    from core.llm_interface import get_llm

    question_str = " ".join(question)

    console.print(f"[bold green]💬 Question: {question_str}[/bold green]\n")

    llm = get_llm()

    # Build context-aware prompt
    prompt = f"""You are a cybersecurity expert assistant. Answer the following question:

Question: {question_str}

Provide a clear, actionable answer. If you need more context, ask for it.
If the question requires running tools, suggest which sec-llama commands to use."""

    try:
        response = llm.generate(prompt)
        console.print(f"[bold cyan]Answer:[/bold cyan]\n{response}\n")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ==================== Configuration Commands ====================

@cli.command("config")
@click.option("--show", is_flag=True, help="Show current configuration")
@click.option("--init", is_flag=True, help="Initialize configuration")
def config(show, init):
    """Manage configuration"""
    from core.config import get_config

    if init:
        console.print("[bold green]Initializing configuration...[/bold green]")
        # Copy example config
        import shutil
        import os

        src = "config/config.example.yaml"
        dst = "config/config.yaml"

        if os.path.exists(dst):
            console.print(f"[yellow]Config already exists: {dst}[/yellow]")
        else:
            shutil.copy(src, dst)
            console.print(f"[green]✓ Config created: {dst}[/green]")
            console.print("[cyan]Edit the file to customize your settings[/cyan]")

    if show:
        cfg = get_config()
        console.print("\n[bold]Current Configuration:[/bold]")
        console.print(f"  LLM Provider: {cfg.llm.provider}")
        console.print(f"  LLM Model: {cfg.llm.model}")
        console.print(f"  Base URL: {cfg.llm.base_url}")
        console.print(f"  Network Interface: {cfg.network.interface}")
        console.print(f"  Nmap Path: {cfg.scanning.nmap_path}")


# ==================== Utilities ====================

@cli.command("version")
def version():
    """Show version information"""
    console.print("[bold green]Sec-Llama Suite v1.0.0[/bold green]")
    console.print("Local LLM-Powered Cybersecurity Testing Suite")


@cli.command("doctor")
def doctor():
    """Check system dependencies"""
    console.print("[bold green]🏥 Checking dependencies...[/bold green]\n")

    checks = {
        "Ollama": "ollama",
        "Nmap": "nmap",
        "Tcpdump": "tcpdump",
        "Aircrack-ng": "aircrack-ng",
        "Bandit": "bandit",
        "Semgrep": "semgrep",
    }

    table = Table(title="Dependency Check")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")

    import shutil

    for name, cmd in checks.items():
        if shutil.which(cmd):
            table.add_row(name, "✓ Installed")
        else:
            table.add_row(name, "✗ Not found", style="red")

    console.print(table)


if __name__ == "__main__":
    cli()
