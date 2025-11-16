"""
Tools Execution API Routes

Provides endpoints for listing and executing MCP tools.
"""

from typing import List, Optional
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from web_ui.backend.models.tool import (
    ToolInfo,
    ToolExecutionRequest,
    ToolExecutionResponse,
    ToolExecutionHistory,
    ToolStatus
)
from web_ui.backend.services.tool_executor import get_executor

router = APIRouter()


@router.get("", response_model=List[ToolInfo])
async def list_tools():
    """
    List all available MCP tools

    Returns:
        List of available tools with their metadata
    """
    try:
        executor = get_executor()
        tools = executor.get_available_tools()
        return tools

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")


@router.get("/{tool_name}", response_model=ToolInfo)
async def get_tool_info(tool_name: str):
    """
    Get information about a specific tool

    Args:
        tool_name: Name of the tool

    Returns:
        Tool information
    """
    try:
        executor = get_executor()
        tools = executor.get_available_tools()

        tool = next((t for t in tools if t.name == tool_name), None)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        return tool

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tool info: {str(e)}")


@router.post("/{tool_name}/execute", response_model=ToolExecutionResponse)
async def execute_tool(
    tool_name: str,
    request: ToolExecutionRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute a tool asynchronously

    Args:
        tool_name: Name of the tool to execute
        request: Execution request with parameters
        background_tasks: FastAPI background tasks

    Returns:
        Execution response with status and execution ID
    """
    try:
        executor = get_executor()

        # Verify tool exists
        tools = executor.get_available_tools()
        tool = next((t for t in tools if t.name == tool_name), None)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        # Validate tool_name matches request
        if request.tool_name != tool_name:
            raise HTTPException(
                status_code=400,
                detail=f"URL tool_name '{tool_name}' doesn't match request tool_name '{request.tool_name}'"
            )

        # Execute tool
        execution = await executor.execute_tool(tool_name, request.parameters)

        return execution

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")


@router.get("/executions/{execution_id}", response_model=ToolExecutionResponse)
async def get_execution_status(execution_id: str):
    """
    Get status of a tool execution

    Args:
        execution_id: Execution ID

    Returns:
        Execution response with current status
    """
    try:
        executor = get_executor()
        execution = executor.get_execution(execution_id)

        if not execution:
            raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found")

        return execution

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching execution: {str(e)}")


@router.delete("/executions/{execution_id}")
async def cancel_execution(execution_id: str):
    """
    Cancel a running tool execution

    Args:
        execution_id: Execution ID

    Returns:
        Success message
    """
    try:
        executor = get_executor()
        execution = executor.get_execution(execution_id)

        if not execution:
            raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found")

        if execution.status == ToolStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Execution already completed")

        if execution.status == ToolStatus.FAILED:
            raise HTTPException(status_code=400, detail="Execution already failed")

        # TODO: Implement actual cancellation logic
        execution.status = ToolStatus.CANCELLED

        return {
            "message": f"Execution {execution_id} cancelled",
            "execution_id": execution_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling execution: {str(e)}")


@router.get("/history", response_model=List[ToolExecutionHistory])
async def get_execution_history(
    limit: int = 50,
    tool_name: Optional[str] = None,
    status: Optional[ToolStatus] = None
):
    """
    Get execution history with optional filtering

    Args:
        limit: Maximum number of executions to return
        tool_name: Filter by tool name (optional)
        status: Filter by status (optional)

    Returns:
        List of execution history entries
    """
    try:
        executor = get_executor()
        history = executor.get_recent_executions(limit=limit)

        # Apply filters
        if tool_name:
            history = [h for h in history if h.tool_name == tool_name]

        if status:
            history = [h for h in history if h.status == status]

        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.get("/categories")
async def get_tool_categories():
    """
    Get tool categories with counts

    Returns:
        Dictionary of categories with tool counts
    """
    try:
        executor = get_executor()
        tools = executor.get_available_tools()

        categories = {}
        for tool in tools:
            category = tool.category
            if category not in categories:
                categories[category] = {
                    "name": category,
                    "count": 0,
                    "tools": []
                }
            categories[category]["count"] += 1
            categories[category]["tools"].append(tool.name)

        return list(categories.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")
