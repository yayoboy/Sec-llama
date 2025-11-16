"""
Tool Execution Service

Handles execution of MCP tools and tracking of execution history
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.tool import (
    ToolStatus, ToolExecutionResponse, ToolInfo, ToolExecutionHistory
)

# Import security modules
from modules.network.discovery.host_discovery import HostDiscovery
from modules.network.scanning.port_scanner import PortScanner
from modules.vuln_scanner.code_scanner import CodeScanner
from modules.threat_intel.cve_lookup import CVELookup
from modules.network.wireless.wifi_audit import WifiAuditor
from modules.network.traffic.packet_analyzer import PacketAnalyzer
from modules.container_security.docker_scanner import DockerScanner
from modules.api_security.api_fuzzer import APIFuzzer
from modules.log_analyzer.log_parser import LogParser
from modules.threat_intel.ioc_analyzer import IOCAnalyzer
from modules.code_review.git_reviewer import GitReviewer
from modules.pentest_assistant.attack_planner import AttackPlanner


class ToolExecutor:
    """Service for executing MCP tools"""

    def __init__(self):
        self.executions: Dict[str, ToolExecutionResponse] = {}
        self.history: List[ToolExecutionHistory] = []
        self._start_time = datetime.utcnow()

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> ToolExecutionResponse:
        """
        Execute a tool asynchronously

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters

        Returns:
            ToolExecutionResponse with execution details
        """
        execution_id = str(uuid.uuid4())
        started_at = datetime.utcnow()

        # Create execution record
        execution = ToolExecutionResponse(
            execution_id=execution_id,
            tool_name=tool_name,
            status=ToolStatus.RUNNING,
            started_at=started_at
        )

        self.executions[execution_id] = execution

        try:
            # Execute tool via MCP server
            result = await self._call_mcp_tool(tool_name, parameters)

            # Update execution
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()

            execution.status = ToolStatus.COMPLETED
            execution.completed_at = completed_at
            execution.duration = duration
            execution.result = result

            # Add to history
            self._add_to_history(execution, parameters, success=True)

        except Exception as e:
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()

            execution.status = ToolStatus.FAILED
            execution.completed_at = completed_at
            execution.duration = duration
            execution.error = str(e)

            # Add to history
            self._add_to_history(execution, parameters, success=False)

        return execution

    async def _call_mcp_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call MCP tool - Execute real security modules

        Integrates with actual security scanning modules
        """
        try:
            if tool_name == "network_discover":
                # Real network discovery
                subnet = parameters.get("subnet", "192.168.1.0/24")
                method = parameters.get("method", "arp")

                discovery = HostDiscovery()
                hosts = await asyncio.to_thread(
                    discovery.discover_network, subnet, method
                )

                return {
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
                            "is_alive": h.is_alive,
                            "open_ports": h.open_ports
                        }
                        for h in hosts
                    ]
                }

            elif tool_name == "network_scan":
                # Real port scanning
                host = parameters.get("host")
                ports = parameters.get("ports")
                profile = parameters.get("profile", "standard")

                if not host:
                    raise ValueError("Host parameter is required")

                scanner = PortScanner()
                result = await asyncio.to_thread(
                    scanner.scan, host, ports, profile
                )

                return {
                    "host": result.host,
                    "hostname": result.hostname,
                    "state": result.state,
                    "os_guess": result.os_guess,
                    "open_ports": len(result.services),
                    "services": [
                        {
                            "port": s.port,
                            "protocol": s.protocol,
                            "service": s.service,
                            "version": s.version,
                            "product": s.product
                        }
                        for s in result.services
                    ]
                }

            elif tool_name == "code_scan":
                # Real code scanning
                path = parameters.get("path")
                language = parameters.get("language", "auto")

                if not path:
                    raise ValueError("Path parameter is required")

                scanner = CodeScanner()
                vulns = await asyncio.to_thread(
                    scanner.scan_directory, path, language
                )

                return {
                    "path": path,
                    "language": language,
                    "total_vulnerabilities": len(vulns),
                    "by_severity": {
                        "CRITICAL": len([v for v in vulns if v.severity == "CRITICAL"]),
                        "HIGH": len([v for v in vulns if v.severity == "HIGH"]),
                        "MEDIUM": len([v for v in vulns if v.severity == "MEDIUM"]),
                        "LOW": len([v for v in vulns if v.severity == "LOW"])
                    },
                    "vulnerabilities": [
                        {
                            "file": v.file,
                            "line": v.line,
                            "severity": v.severity,
                            "title": v.title,
                            "description": v.description,
                            "cwe": v.cwe
                        }
                        for v in vulns[:20]  # Limit to 20 most critical
                    ]
                }

            elif tool_name == "threat_cve_lookup":
                # Real CVE lookup
                cve_id = parameters.get("cve_id")

                if not cve_id:
                    raise ValueError("CVE ID parameter is required")

                lookup = CVELookup()
                cve_info = await asyncio.to_thread(lookup.lookup_cve, cve_id)

                if not cve_info:
                    return {
                        "error": f"CVE {cve_id} not found",
                        "status": "not_found"
                    }

                return {
                    "id": cve_info.get("id"),
                    "description": cve_info.get("description"),
                    "published": cve_info.get("published"),
                    "modified": cve_info.get("modified"),
                    "cvss_score": cve_info.get("cvss_score"),
                    "references": cve_info.get("references", []),
                    "affected_products": cve_info.get("cpes", [])
                }

            else:
                return {
                    "error": f"Unknown tool: {tool_name}",
                    "status": "not_implemented"
                }

        except Exception as e:
            # Return error details
            return {
                "error": str(e),
                "status": "execution_failed",
                "tool": tool_name
            }

    def _add_to_history(
        self,
        execution: ToolExecutionResponse,
        parameters: Dict[str, Any],
        success: bool
    ):
        """Add execution to history"""
        history_entry = ToolExecutionHistory(
            execution_id=execution.execution_id,
            tool_name=execution.tool_name,
            status=execution.status,
            parameters=parameters,
            started_at=execution.started_at,
            completed_at=execution.completed_at,
            duration=execution.duration,
            success=success
        )
        self.history.append(history_entry)

        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def get_execution(self, execution_id: str) -> Optional[ToolExecutionResponse]:
        """Get execution by ID"""
        return self.executions.get(execution_id)

    def get_recent_executions(self, limit: int = 10) -> List[ToolExecutionHistory]:
        """Get recent executions"""
        return sorted(
            self.history,
            key=lambda x: x.started_at,
            reverse=True
        )[:limit]

    def get_available_tools(self) -> List[ToolInfo]:
        """Get list of available tools"""
        # TODO: Get from MCP server
        # For now, return hardcoded list
        return [
            ToolInfo(
                name="network_discover",
                description="Discover hosts in a network subnet",
                category="network",
                input_schema={
                    "type": "object",
                    "properties": {
                        "subnet": {"type": "string"},
                        "method": {"type": "string", "enum": ["arp", "icmp", "tcp"]}
                    },
                    "required": ["subnet"]
                },
                examples=[{"subnet": "192.168.1.0/24", "method": "arp"}]
            ),
            ToolInfo(
                name="network_scan",
                description="Port scanning with AI analysis",
                category="network",
                input_schema={
                    "type": "object",
                    "properties": {
                        "host": {"type": "string"},
                        "ports": {"type": "string"},
                        "profile": {"type": "string", "enum": ["quick", "standard", "thorough"]}
                    },
                    "required": ["host"]
                },
                examples=[{"host": "192.168.1.1", "profile": "standard"}]
            ),
            ToolInfo(
                name="code_scan",
                description="SAST code analysis",
                category="code",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["path"]
                },
                examples=[{"path": "/path/to/code", "language": "python"}]
            ),
            ToolInfo(
                name="threat_cve_lookup",
                description="CVE database lookup",
                category="threat",
                input_schema={
                    "type": "object",
                    "properties": {
                        "cve_id": {"type": "string"}
                    },
                    "required": ["cve_id"]
                },
                examples=[{"cve_id": "CVE-2021-41773"}]
            )
        ]


# Global instance
_executor = None


def get_executor() -> ToolExecutor:
    """Get global tool executor instance"""
    global _executor
    if _executor is None:
        _executor = ToolExecutor()
    return _executor
