"""
Pydantic models for Dashboard
"""

from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class SystemStats(BaseModel):
    """System statistics for dashboard"""
    total_executions_today: int = 0
    total_executions_total: int = 0
    active_executions: int = 0
    available_tools: int = 0
    uptime_seconds: float = 0
    ollama_status: str = "unknown"  # online, offline, error
    ollama_model: str = "unknown"


class ToolUsageStats(BaseModel):
    """Tool usage statistics"""
    tool_name: str
    execution_count: int
    success_count: int
    failure_count: int
    avg_duration: float


class RecentExecution(BaseModel):
    """Recent tool execution summary"""
    execution_id: str
    tool_name: str
    status: str
    started_at: datetime
    duration: float
    success: bool


class DashboardData(BaseModel):
    """Complete dashboard data"""
    stats: SystemStats
    recent_executions: List[RecentExecution] = Field(default_factory=list)
    top_tools: List[ToolUsageStats] = Field(default_factory=list)
    executions_by_hour: Dict[str, int] = Field(default_factory=dict)
