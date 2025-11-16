"""
Dashboard API Routes

Provides endpoints for dashboard statistics and system health monitoring.
"""

from datetime import datetime, timedelta
from typing import List
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.dashboard import (
    DashboardData, SystemStats, RecentExecution, ToolUsageStats
)
from web_ui.backend.services.tool_executor import get_executor

router = APIRouter()


@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """
    Get current system statistics

    Returns:
        SystemStats with current metrics
    """
    try:
        executor = get_executor()
        start_time = getattr(executor, '_start_time', datetime.utcnow())

        # Calculate stats
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_executions = [
            h for h in executor.history
            if h.started_at >= today_start
        ]

        active_executions = len([
            e for e in executor.executions.values()
            if e.status.value == "running"
        ])

        # Check Ollama status
        try:
            import httpx
            ollama_host = "http://localhost:11434"
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ollama_host}/api/tags", timeout=2.0)
                ollama_status = "running" if response.status_code == 200 else "error"
        except Exception:
            ollama_status = "offline"

        stats = SystemStats(
            total_executions_today=len(today_executions),
            active_executions=active_executions,
            available_tools=len(executor.get_available_tools()),
            uptime_seconds=(datetime.utcnow() - start_time).total_seconds(),
            ollama_status=ollama_status
        )

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


@router.get("/recent-executions", response_model=List[RecentExecution])
async def get_recent_executions(limit: int = 10):
    """
    Get recent tool executions

    Args:
        limit: Maximum number of executions to return (default: 10)

    Returns:
        List of recent executions
    """
    try:
        executor = get_executor()
        history = executor.get_recent_executions(limit=limit)

        recent = [
            RecentExecution(
                execution_id=h.execution_id,
                tool_name=h.tool_name,
                status=h.status,
                started_at=h.started_at,
                duration=h.duration
            )
            for h in history
        ]

        return recent

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching executions: {str(e)}")


@router.get("/tool-usage", response_model=List[ToolUsageStats])
async def get_tool_usage_stats(days: int = 7):
    """
    Get tool usage statistics

    Args:
        days: Number of days to analyze (default: 7)

    Returns:
        List of tool usage statistics
    """
    try:
        executor = get_executor()
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Filter executions within date range
        recent_history = [
            h for h in executor.history
            if h.started_at >= cutoff_date
        ]

        # Count executions per tool
        tool_counts: dict = {}
        tool_success: dict = {}

        for h in recent_history:
            tool_name = h.tool_name

            if tool_name not in tool_counts:
                tool_counts[tool_name] = 0
                tool_success[tool_name] = 0

            tool_counts[tool_name] += 1
            if h.success:
                tool_success[tool_name] += 1

        # Create stats
        stats = [
            ToolUsageStats(
                tool_name=tool_name,
                execution_count=count,
                success_rate=tool_success[tool_name] / count if count > 0 else 0.0,
                avg_duration=sum(
                    h.duration for h in recent_history
                    if h.tool_name == tool_name and h.duration is not None
                ) / count if count > 0 else 0.0
            )
            for tool_name, count in tool_counts.items()
        ]

        # Sort by execution count
        stats.sort(key=lambda x: x.execution_count, reverse=True)

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating usage: {str(e)}")


@router.get("/executions-by-hour")
async def get_executions_by_hour(hours: int = 24):
    """
    Get execution counts grouped by hour

    Args:
        hours: Number of hours to analyze (default: 24)

    Returns:
        Dictionary mapping hour to execution count
    """
    try:
        executor = get_executor()
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        # Filter and group by hour
        executions_by_hour = {}

        for h in executor.history:
            if h.started_at >= cutoff:
                hour_key = h.started_at.strftime("%Y-%m-%d %H:00")
                executions_by_hour[hour_key] = executions_by_hour.get(hour_key, 0) + 1

        return executions_by_hour

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating hourly stats: {str(e)}")


@router.get("", response_model=DashboardData)
async def get_dashboard_data(
    recent_limit: int = 10,
    usage_days: int = 7
):
    """
    Get complete dashboard data

    Args:
        recent_limit: Limit for recent executions
        usage_days: Days for usage statistics

    Returns:
        Complete dashboard data
    """
    try:
        # Fetch all data
        stats = await get_system_stats()
        recent_executions = await get_recent_executions(limit=recent_limit)
        top_tools = await get_tool_usage_stats(days=usage_days)
        executions_by_hour = await get_executions_by_hour(hours=24)

        dashboard_data = DashboardData(
            stats=stats,
            recent_executions=recent_executions,
            top_tools=top_tools[:5],  # Top 5 tools
            executions_by_hour=executions_by_hour
        )

        return dashboard_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard: {str(e)}")
