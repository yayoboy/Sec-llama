"""
Threat Intelligence Tools for MCP Server

Exposes CVE lookup, IOC analysis, and threat intelligence tools
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.types as types

from modules.threat_intel.cve_lookup import CVELookup
from modules.threat_intel.ioc_analyzer import IOCAnalyzer


def register(server: Server):
    """Register threat intelligence tools"""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available threat intelligence tools"""
        return [
            Tool(
                name="threat_cve_lookup",
                description="Look up detailed information about a CVE (Common Vulnerabilities and Exposures). Returns CVSS score, severity, affected versions, exploit availability, and AI-generated remediation advice from NIST NVD database.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cve_id": {
                            "type": "string",
                            "description": "CVE identifier (e.g., 'CVE-2021-41773')",
                            "pattern": "^CVE-\\d{4}-\\d{4,}$"
                        },
                        "include_exploits": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include information about available exploits"
                        },
                        "include_ai_analysis": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include AI-powered threat analysis and mitigation strategies"
                        }
                    },
                    "required": ["cve_id"]
                }
            ),
            Tool(
                name="threat_ioc_analyze",
                description="Analyze Indicators of Compromise (IOC) to identify threats. Auto-detects IOC type (IP, domain, URL, file hash, email) and provides threat classification, reputation, malware family association, and recommended actions.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ioc": {
                            "type": "string",
                            "description": "Indicator of Compromise (IP, domain, URL, hash, email, etc.)"
                        },
                        "ioc_type": {
                            "type": "string",
                            "enum": ["auto", "ip", "domain", "url", "hash", "email"],
                            "default": "auto",
                            "description": "Type of IOC (auto-detect if not specified)"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context (e.g., log entry, alert description)"
                        }
                    },
                    "required": ["ioc"]
                }
            ),
            Tool(
                name="threat_osint",
                description="Perform Open Source Intelligence (OSINT) gathering on a target. Collects publicly available information including domains, subdomains, IP addresses, email addresses, social media profiles, and technology stack. Useful for reconnaissance and attack surface mapping.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "Target domain, IP, or organization name"
                        },
                        "osint_type": {
                            "type": "string",
                            "enum": ["domain", "ip", "email", "organization", "all"],
                            "default": "all",
                            "description": "Type of OSINT to gather"
                        },
                        "depth": {
                            "type": "string",
                            "enum": ["basic", "standard", "deep"],
                            "default": "standard",
                            "description": "OSINT gathering depth"
                        }
                    },
                    "required": ["target"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool execution"""

        if name == "threat_cve_lookup":
            return await _threat_cve_lookup(arguments)
        elif name == "threat_ioc_analyze":
            return await _threat_ioc_analyze(arguments)
        elif name == "threat_osint":
            return await _threat_osint(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")


async def _threat_cve_lookup(args: dict) -> list[TextContent]:
    """Look up CVE information"""
    try:
        cve_id = args["cve_id"]
        include_exploits = args.get("include_exploits", True)
        ai_analysis = args.get("include_ai_analysis", True)

        cve_lookup = CVELookup()
        cve_data = cve_lookup.lookup(cve_id, ai_analysis=ai_analysis)

        if not cve_data:
            return [TextContent(
                type="text",
                text=f"❌ CVE {cve_id} not found in database."
            )]

        # Format output
        output = f"# {cve_id}\n\n"

        # Severity badge
        severity = cve_data.get('severity', 'UNKNOWN')
        severity_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢',
            'UNKNOWN': '⚪'
        }
        output += f"{severity_emoji.get(severity, '⚪')} **Severity:** {severity}\n"
        output += f"**CVSS Score:** {cve_data.get('cvss_score', 'N/A')}\n\n"

        # Description
        if 'description' in cve_data:
            output += f"## Description\n\n{cve_data['description']}\n\n"

        # Affected Products
        if 'affected_products' in cve_data and cve_data['affected_products']:
            output += f"## Affected Products\n\n"
            for product in cve_data['affected_products'][:5]:
                output += f"- {product}\n"
            output += "\n"

        # CVSS Metrics
        if 'cvss_metrics' in cve_data:
            metrics = cve_data['cvss_metrics']
            output += f"## CVSS v3.1 Metrics\n\n"
            output += f"- **Attack Vector:** {metrics.get('attack_vector', 'N/A')}\n"
            output += f"- **Attack Complexity:** {metrics.get('attack_complexity', 'N/A')}\n"
            output += f"- **Privileges Required:** {metrics.get('privileges_required', 'N/A')}\n"
            output += f"- **User Interaction:** {metrics.get('user_interaction', 'N/A')}\n"
            output += f"- **Confidentiality Impact:** {metrics.get('confidentiality_impact', 'N/A')}\n"
            output += f"- **Integrity Impact:** {metrics.get('integrity_impact', 'N/A')}\n"
            output += f"- **Availability Impact:** {metrics.get('availability_impact', 'N/A')}\n\n"

        # Exploits
        if include_exploits and 'exploits' in cve_data:
            exploits = cve_data['exploits']
            if exploits:
                output += f"## 🎯 Known Exploits\n\n"
                for exploit in exploits[:3]:
                    output += f"- **{exploit.get('name', 'Unknown')}**\n"
                    output += f"  - Source: {exploit.get('source', 'N/A')}\n"
                    output += f"  - Type: {exploit.get('type', 'N/A')}\n"
                output += "\n"
            else:
                output += f"## Exploits\n\nNo public exploits found.\n\n"

        # AI Analysis
        if ai_analysis and 'ai_analysis' in cve_data:
            output += f"## AI Security Analysis\n\n{cve_data['ai_analysis']}\n\n"

        # Remediation
        if 'remediation' in cve_data:
            output += f"## Remediation\n\n{cve_data['remediation']}\n\n"

        # References
        if 'references' in cve_data and cve_data['references']:
            output += f"## References\n\n"
            for ref in cve_data['references'][:5]:
                output += f"- {ref}\n"
            output += "\n"

        # JSON export
        output += f"\n```json\n{json.dumps(cve_data, indent=2)}\n```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"CVE lookup failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]


async def _threat_ioc_analyze(args: dict) -> list[TextContent]:
    """Analyze IOC"""
    try:
        ioc = args["ioc"]
        ioc_type = args.get("ioc_type", "auto")
        context = args.get("context", "")

        analyzer = IOCAnalyzer()
        analysis = analyzer.analyze(ioc, ioc_type=ioc_type, context=context)

        # Format output
        output = f"# IOC Analysis: `{ioc}`\n\n"

        # Detected type
        detected_type = analysis.get('type', 'unknown')
        output += f"**Type:** {detected_type.upper()}\n"

        # Classification
        classification = analysis.get('classification', 'unknown')
        classification_emoji = {
            'malicious': '🔴',
            'suspicious': '🟠',
            'benign': '🟢',
            'unknown': '⚪'
        }
        output += f"**Classification:** {classification_emoji.get(classification, '⚪')} {classification.upper()}\n\n"

        # Threat Level
        if 'threat_level' in analysis:
            output += f"**Threat Level:** {analysis['threat_level']}/10\n\n"

        # Details
        if 'details' in analysis:
            details = analysis['details']
            output += f"## Details\n\n"

            if detected_type == 'ip':
                output += f"- **Geolocation:** {details.get('country', 'Unknown')}\n"
                output += f"- **ASN:** {details.get('asn', 'Unknown')}\n"
                output += f"- **ISP:** {details.get('isp', 'Unknown')}\n"

            elif detected_type == 'domain':
                output += f"- **Registrar:** {details.get('registrar', 'Unknown')}\n"
                output += f"- **Created:** {details.get('created_date', 'Unknown')}\n"
                output += f"- **Expires:** {details.get('expiry_date', 'Unknown')}\n"

            elif detected_type == 'hash':
                output += f"- **Algorithm:** {details.get('algorithm', 'Unknown')}\n"
                output += f"- **File Name:** {details.get('file_name', 'Unknown')}\n"
                output += f"- **Malware Family:** {details.get('malware_family', 'Unknown')}\n"

            output += "\n"

        # Associated Threats
        if 'associated_threats' in analysis and analysis['associated_threats']:
            output += f"## Associated Threats\n\n"
            for threat in analysis['associated_threats']:
                output += f"- {threat}\n"
            output += "\n"

        # AI Analysis
        if 'ai_analysis' in analysis:
            output += f"## AI Threat Analysis\n\n{analysis['ai_analysis']}\n\n"

        # Recommended Actions
        if 'recommended_actions' in analysis:
            output += f"## Recommended Actions\n\n"
            for action in analysis['recommended_actions']:
                output += f"- {action}\n"
            output += "\n"

        # Context analysis
        if context:
            output += f"## Context\n\n```\n{context}\n```\n\n"

        # JSON export
        output += f"\n```json\n{json.dumps(analysis, indent=2)}\n```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"IOC analysis failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]


async def _threat_osint(args: dict) -> list[TextContent]:
    """Perform OSINT gathering"""
    try:
        target = args["target"]
        osint_type = args.get("osint_type", "all")
        depth = args.get("depth", "standard")

        output = f"# OSINT Report: {target}\n\n"
        output += f"**Type:** {osint_type}\n"
        output += f"**Depth:** {depth}\n\n"

        # This is a placeholder - actual implementation would use:
        # - theHarvester
        # - Shodan API
        # - DNS enumeration
        # - Whois lookup
        # - Social media APIs

        output += "⚠️ **OSINT feature coming soon!**\n\n"
        output += "This will gather:\n"
        output += "- Subdomains via DNS enumeration\n"
        output += "- IP addresses and geolocation\n"
        output += "- Email addresses\n"
        output += "- Social media profiles\n"
        output += "- Technology stack\n"
        output += "- SSL/TLS certificates\n"
        output += "- Historical DNS records\n\n"

        output += "For now, use external tools:\n"
        output += "```bash\n"
        output += f"# Subdomain enumeration\nsublist3r -d {target}\n\n"
        output += f"# WHOIS lookup\nwhois {target}\n\n"
        output += f"# DNS enumeration\ndig {target} ANY\n"
        output += "```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"OSINT gathering failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]
