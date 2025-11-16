"""
Audit Logs API Routes

Provides endpoints for querying audit logs.
"""

from datetime import datetime, timedelta
from typing import List, Optional
import sys
from pathlib import Path
import json

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

router = APIRouter()

# Audit log file path
AUDIT_LOG_PATH = Path("/home/user/Sec-llama/logs/mcp_audit.log")
AUDIT_DB_PATH = Path("/home/user/Sec-llama/database/audit_logs.json")


class AuditLogEntry(BaseModel):
    """Audit log entry model"""
    timestamp: datetime
    api_key_id: Optional[str] = None
    tool_name: str
    status: str
    duration: Optional[float] = None
    ip_address: Optional[str] = None
    parameters: Optional[dict] = None
    error: Optional[str] = None


class AuditLogStats(BaseModel):
    """Audit log statistics"""
    total_entries: int
    successful_executions: int
    failed_executions: int
    unique_tools: int
    unique_api_keys: int
    average_duration: float


def load_audit_logs(limit: int = 100) -> List[AuditLogEntry]:
    """Load audit logs from database"""
    if not AUDIT_DB_PATH.exists():
        return []

    try:
        with open(AUDIT_DB_PATH, 'r') as f:
            data = json.load(f)
            logs = data.get("logs", [])

            # Convert to AuditLogEntry objects
            entries = []
            for log in logs[-limit:]:  # Get last 'limit' entries
                entries.append(AuditLogEntry(
                    timestamp=datetime.fromisoformat(log["timestamp"]),
                    api_key_id=log.get("api_key_id"),
                    tool_name=log["tool_name"],
                    status=log["status"],
                    duration=log.get("duration"),
                    ip_address=log.get("ip_address"),
                    parameters=log.get("parameters"),
                    error=log.get("error")
                ))

            return entries

    except Exception as e:
        # If JSON fails, try to parse text log file
        return parse_text_audit_log(limit)


def parse_text_audit_log(limit: int = 100) -> List[AuditLogEntry]:
    """Parse audit log from text file (fallback)"""
    if not AUDIT_LOG_PATH.exists():
        return []

    entries = []

    try:
        with open(AUDIT_LOG_PATH, 'r') as f:
            lines = f.readlines()

            for line in lines[-limit:]:
                # Parse format: timestamp - api_key - tool - status - duration
                parts = [p.strip() for p in line.split('-')]

                if len(parts) >= 4:
                    try:
                        timestamp = datetime.fromisoformat(parts[0].strip())
                        api_key_id = parts[1].strip() if len(parts) > 1 else None
                        tool_name = parts[2].strip() if len(parts) > 2 else "unknown"
                        status = parts[3].strip() if len(parts) > 3 else "unknown"
                        duration = float(parts[4].strip().rstrip('s')) if len(parts) > 4 else None

                        entries.append(AuditLogEntry(
                            timestamp=timestamp,
                            api_key_id=api_key_id,
                            tool_name=tool_name,
                            status=status,
                            duration=duration
                        ))
                    except (ValueError, IndexError):
                        continue

    except Exception:
        pass

    return entries


def save_audit_log(entry: AuditLogEntry) -> None:
    """Save audit log entry to database"""
    AUDIT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load existing logs
    if AUDIT_DB_PATH.exists():
        with open(AUDIT_DB_PATH, 'r') as f:
            data = json.load(f)
    else:
        data = {"logs": []}

    # Add new entry
    data["logs"].append({
        "timestamp": entry.timestamp.isoformat(),
        "api_key_id": entry.api_key_id,
        "tool_name": entry.tool_name,
        "status": entry.status,
        "duration": entry.duration,
        "ip_address": entry.ip_address,
        "parameters": entry.parameters,
        "error": entry.error
    })

    # Keep only last 10000 entries
    if len(data["logs"]) > 10000:
        data["logs"] = data["logs"][-10000:]

    # Save
    with open(AUDIT_DB_PATH, 'w') as f:
        json.dump(data, f, indent=2, default=str)


@router.get("", response_model=List[AuditLogEntry])
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    tool_name: Optional[str] = None,
    status: Optional[str] = None,
    api_key_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get audit logs with optional filtering

    Args:
        limit: Maximum number of entries to return
        tool_name: Filter by tool name
        status: Filter by status (success, failed)
        api_key_id: Filter by API key ID
        start_date: Filter by start date
        end_date: Filter by end date

    Returns:
        List of audit log entries
    """
    try:
        entries = load_audit_logs(limit=limit * 2)  # Load more for filtering

        # Apply filters
        if tool_name:
            entries = [e for e in entries if e.tool_name == tool_name]

        if status:
            entries = [e for e in entries if e.status == status]

        if api_key_id:
            entries = [e for e in entries if e.api_key_id == api_key_id]

        if start_date:
            entries = [e for e in entries if e.timestamp >= start_date]

        if end_date:
            entries = [e for e in entries if e.timestamp <= end_date]

        # Sort by timestamp (newest first) and limit
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        entries = entries[:limit]

        return entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching audit logs: {str(e)}")


@router.get("/stats", response_model=AuditLogStats)
async def get_audit_log_stats(days: int = Query(7, ge=1, le=365)):
    """
    Get audit log statistics

    Args:
        days: Number of days to analyze

    Returns:
        Audit log statistics
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        entries = load_audit_logs(limit=10000)

        # Filter by date
        entries = [e for e in entries if e.timestamp >= cutoff_date]

        # Calculate stats
        successful = len([e for e in entries if e.status in ["success", "completed"]])
        failed = len([e for e in entries if e.status in ["failed", "error"]])
        unique_tools = len(set(e.tool_name for e in entries))
        unique_keys = len(set(e.api_key_id for e in entries if e.api_key_id))

        # Calculate average duration
        durations = [e.duration for e in entries if e.duration is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0.0

        return AuditLogStats(
            total_entries=len(entries),
            successful_executions=successful,
            failed_executions=failed,
            unique_tools=unique_tools,
            unique_api_keys=unique_keys,
            average_duration=avg_duration
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")


@router.get("/export")
async def export_audit_logs(
    format: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, ge=1, le=365)
):
    """
    Export audit logs in specified format

    Args:
        format: Export format (json or csv)
        days: Number of days to export

    Returns:
        Exported audit logs
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        entries = load_audit_logs(limit=10000)

        # Filter by date
        entries = [e for e in entries if e.timestamp >= cutoff_date]

        if format == "json":
            return {
                "exported_at": datetime.utcnow().isoformat(),
                "entries": [e.dict() for e in entries]
            }

        elif format == "csv":
            import io
            import csv

            output = io.StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=["timestamp", "api_key_id", "tool_name", "status", "duration", "ip_address"]
            )

            writer.writeheader()
            for entry in entries:
                writer.writerow({
                    "timestamp": entry.timestamp.isoformat(),
                    "api_key_id": entry.api_key_id or "",
                    "tool_name": entry.tool_name,
                    "status": entry.status,
                    "duration": entry.duration or "",
                    "ip_address": entry.ip_address or ""
                })

            return {
                "format": "csv",
                "data": output.getvalue()
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting logs: {str(e)}")


@router.delete("")
async def clear_audit_logs(days: Optional[int] = None):
    """
    Clear audit logs

    Args:
        days: If specified, only clear logs older than this many days.
              If not specified, clear all logs.

    Returns:
        Success message with count of cleared entries
    """
    try:
        if days is not None:
            # Clear only old logs
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            entries = load_audit_logs(limit=10000)

            # Keep recent entries
            kept_entries = [e for e in entries if e.timestamp >= cutoff_date]
            cleared_count = len(entries) - len(kept_entries)

            # Save remaining entries
            AUDIT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(AUDIT_DB_PATH, 'w') as f:
                json.dump({
                    "logs": [
                        {
                            "timestamp": e.timestamp.isoformat(),
                            "api_key_id": e.api_key_id,
                            "tool_name": e.tool_name,
                            "status": e.status,
                            "duration": e.duration,
                            "ip_address": e.ip_address,
                            "parameters": e.parameters,
                            "error": e.error
                        }
                        for e in kept_entries
                    ]
                }, f, indent=2, default=str)

            return {
                "message": f"Cleared {cleared_count} audit log entries older than {days} days",
                "cleared_count": cleared_count,
                "remaining_count": len(kept_entries)
            }

        else:
            # Clear all logs
            entries = load_audit_logs(limit=10000)
            cleared_count = len(entries)

            # Reset audit log
            AUDIT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(AUDIT_DB_PATH, 'w') as f:
                json.dump({"logs": []}, f, indent=2)

            return {
                "message": "All audit logs cleared",
                "cleared_count": cleared_count
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing logs: {str(e)}")
