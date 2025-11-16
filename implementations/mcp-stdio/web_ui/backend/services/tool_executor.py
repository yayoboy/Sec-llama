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
        Call MCP tool

        This would integrate with the actual MCP server.
        For now, simulates execution.
        """
        # TODO: Integrate with actual MCP server
        # For now, simulate with delay
        await asyncio.sleep(0.5)

        # Simulate result based on tool
        if tool_name == "network_discover":
            return {
                "summary": {
                    "total_hosts": 5,
                    "subnet": parameters.get("subnet", "unknown")
                },
                "hosts": [
                    {"ip": f"192.168.1.{i}", "mac": f"00:00:00:00:00:0{i}"}
                    for i in range(1, 6)
                ]
            }
        elif tool_name == "network_scan":
            return {
                "host": parameters.get("host", "unknown"),
                "open_ports": 3,
                "services": [
                    {"port": 22, "service": "ssh"},
                    {"port": 80, "service": "http"},
                    {"port": 443, "service": "https"}
                ]
            }
        else:
            return {"status": "completed", "message": f"Tool {tool_name} executed"}

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
