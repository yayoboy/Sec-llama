"""
WebSocket Routes

Provides WebSocket endpoints for real-time updates.
"""

from typing import Dict, Set
import sys
from pathlib import Path
import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

router = APIRouter()

# Active WebSocket connections
active_connections: Set[WebSocket] = set()

# Connection metadata
connection_metadata: Dict[WebSocket, dict] = {}


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.connection_metadata: Dict[WebSocket, dict] = {}

    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)

        self.connection_metadata[websocket] = {
            "client_id": client_id,
            "connected_at": datetime.utcnow(),
            "subscriptions": set()
        }

        # Send welcome message
        await self.send_personal_message({
            "type": "connection",
            "status": "connected",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)

    def disconnect(self, websocket: WebSocket):
        """Unregister a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific connection"""
        if websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_json(message)
            except Exception:
                pass

    async def broadcast(self, message: dict, event_type: str = None):
        """
        Broadcast a message to all connected clients

        Args:
            message: Message to broadcast
            event_type: Optional event type for subscription filtering
        """
        disconnected = set()

        for connection in self.active_connections:
            # Check subscription filter
            if event_type:
                metadata = self.connection_metadata.get(connection, {})
                subscriptions = metadata.get("subscriptions", set())

                if subscriptions and event_type not in subscriptions:
                    continue  # Skip if not subscribed to this event type

            # Send message
            if connection.client_state == WebSocketState.CONNECTED:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def send_tool_execution_update(
        self,
        execution_id: str,
        tool_name: str,
        status: str,
        result: dict = None,
        error: str = None
    ):
        """Send tool execution update to all connected clients"""
        message = {
            "type": "tool_execution",
            "execution_id": execution_id,
            "tool_name": tool_name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result,
            "error": error
        }

        await self.broadcast(message, event_type="tool_execution")

    async def send_system_status_update(self, status: dict):
        """Send system status update to all connected clients"""
        message = {
            "type": "system_status",
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.broadcast(message, event_type="system_status")

    async def send_audit_log_update(self, log_entry: dict):
        """Send new audit log entry to all connected clients"""
        message = {
            "type": "audit_log",
            "log_entry": log_entry,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.broadcast(message, event_type="audit_log")

    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

    def get_connection_info(self) -> list:
        """Get information about all connections"""
        info = []
        for conn, metadata in self.connection_metadata.items():
            info.append({
                "client_id": metadata.get("client_id"),
                "connected_at": metadata.get("connected_at").isoformat(),
                "subscriptions": list(metadata.get("subscriptions", set()))
            })
        return info


# Global connection manager
manager = ConnectionManager()


@router.websocket("/events")
async def websocket_events(websocket: WebSocket, client_id: str = None):
    """
    WebSocket endpoint for real-time events

    Args:
        websocket: WebSocket connection
        client_id: Optional client identifier

    Events:
        - tool_execution: Tool execution updates
        - system_status: System status updates
        - audit_log: New audit log entries
    """
    await manager.connect(websocket, client_id)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "subscribe":
                # Subscribe to event types
                event_types = data.get("events", [])
                metadata = manager.connection_metadata.get(websocket, {})
                subscriptions = metadata.get("subscriptions", set())

                for event_type in event_types:
                    subscriptions.add(event_type)

                metadata["subscriptions"] = subscriptions

                await manager.send_personal_message({
                    "type": "subscription",
                    "status": "subscribed",
                    "events": list(subscriptions),
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)

            elif message_type == "unsubscribe":
                # Unsubscribe from event types
                event_types = data.get("events", [])
                metadata = manager.connection_metadata.get(websocket, {})
                subscriptions = metadata.get("subscriptions", set())

                for event_type in event_types:
                    subscriptions.discard(event_type)

                metadata["subscriptions"] = subscriptions

                await manager.send_personal_message({
                    "type": "subscription",
                    "status": "unsubscribed",
                    "events": list(subscriptions),
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)

            elif message_type == "ping":
                # Respond to ping
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)

            elif message_type == "get_info":
                # Send connection info
                metadata = manager.connection_metadata.get(websocket, {})
                await manager.send_personal_message({
                    "type": "connection_info",
                    "client_id": metadata.get("client_id"),
                    "connected_at": metadata.get("connected_at").isoformat(),
                    "subscriptions": list(metadata.get("subscriptions", set())),
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)


@router.websocket("/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    """
    WebSocket endpoint for dashboard real-time updates

    Automatically subscribes to all relevant events for the dashboard.
    """
    await manager.connect(websocket, client_id="dashboard")

    # Auto-subscribe to dashboard events
    metadata = manager.connection_metadata.get(websocket, {})
    metadata["subscriptions"] = {"tool_execution", "system_status", "audit_log"}

    try:
        # Send periodic updates
        while True:
            # Wait for messages or send periodic updates
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=5.0)

                # Handle client messages
                if data.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }, websocket)

            except asyncio.TimeoutError:
                # Send periodic system status update
                from web_ui.backend.services.tool_executor import get_executor

                executor = get_executor()
                start_time = getattr(executor, '_start_time', datetime.utcnow())

                status = {
                    "active_executions": len([
                        e for e in executor.executions.values()
                        if e.status.value == "running"
                    ]),
                    "total_tools": len(executor.get_available_tools()),
                    "uptime": (datetime.utcnow() - start_time).total_seconds(),
                    "connections": manager.get_connection_count()
                }

                await manager.send_personal_message({
                    "type": "system_status",
                    "status": status,
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


@router.get("/connections")
async def get_active_connections():
    """
    Get information about active WebSocket connections

    Returns:
        Connection count and details
    """
    return {
        "count": manager.get_connection_count(),
        "connections": manager.get_connection_info()
    }


# Export manager for use in other modules
def get_websocket_manager() -> ConnectionManager:
    """Get the global WebSocket connection manager"""
    return manager
