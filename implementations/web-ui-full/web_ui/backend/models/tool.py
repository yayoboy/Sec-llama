"""
Pydantic models for MCP Tools
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ToolStatus(str, Enum):
    """Tool execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ToolExecutionRequest(BaseModel):
    """Request to execute a tool"""
    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")

    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "network_discover",
                "parameters": {
                    "subnet": "192.168.1.0/24",
                    "method": "arp"
                }
            }
        }


class ToolExecutionResponse(BaseModel):
    """Response from tool execution"""
    execution_id: str
    tool_name: str
    status: ToolStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ToolInfo(BaseModel):
    """Information about an available tool"""
    name: str
    description: str
    category: str
    input_schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = Field(default_factory=list)


class ToolExecutionHistory(BaseModel):
    """Historical tool execution record"""
    execution_id: str
    tool_name: str
    status: ToolStatus
    parameters: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime]
    duration: Optional[float]
    success: bool
    user: str = "web-ui"
