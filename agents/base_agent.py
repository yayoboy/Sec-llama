"""
Base Agent Class
Foundation for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from core.config import get_config
from core.llm_interface import get_llm


@dataclass
class AgentMessage:
    """Message between agents"""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(self, agent_id: str, model: str = None):
        """
        Initialize agent

        Args:
            agent_id: Unique agent identifier
            model: LLM model to use (overrides config)
        """
        self.agent_id = agent_id
        self.config = get_config()
        self.llm = get_llm()
        self.model = model or self.config.llm.model

        self.knowledge_base: Dict[str, Any] = {}
        self.message_queue: List[AgentMessage] = []
        self.task_history: List[Dict[str, Any]] = []

        print(f"[*] {self.__class__.__name__} initialized: {agent_id}")

    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task assigned to this agent

        Args:
            task: Task description and parameters

        Returns:
            Task result
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get agent capabilities

        Returns:
            List of capabilities this agent provides
        """
        pass

    def send_message(self, recipient: str, message_type: str, content: Dict[str, Any]):
        """Send message to another agent"""
        message = AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content,
        )
        self.message_queue.append(message)
        return message

    def receive_message(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Receive and process message from another agent

        Args:
            message: Message from another agent

        Returns:
            Response
        """
        print(f"[{self.agent_id}] Received message from {message.sender}: {message.message_type}")

        # Process based on message type
        if message.message_type == "task_request":
            return self.process_task(message.content)
        elif message.message_type == "query":
            return self.answer_query(message.content)
        elif message.message_type == "collaboration":
            return self.collaborate(message.content)

        return {"status": "unknown_message_type"}

    def answer_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Answer a query from another agent"""
        question = query.get("question", "")

        prompt = f"""You are {self.agent_id}, a specialized security agent.
Another agent asks: {question}

Context from your knowledge base:
{self.get_relevant_knowledge(question)}

Provide a helpful, specific answer based on your specialization."""

        try:
            response = self.llm.generate(prompt)
            return {
                "status": "success",
                "answer": response,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
            }

    def collaborate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with another agent"""
        return {"status": "collaboration_received"}

    def update_knowledge(self, key: str, value: Any):
        """Update agent's knowledge base"""
        self.knowledge_base[key] = value

    def get_relevant_knowledge(self, query: str) -> str:
        """Get relevant knowledge for a query"""
        # Simple keyword matching (could be improved with embeddings)
        relevant = []
        for key, value in self.knowledge_base.items():
            if any(word in key.lower() for word in query.lower().split()):
                relevant.append(f"{key}: {value}")

        return "\n".join(relevant) if relevant else "No relevant knowledge"

    def record_task(self, task: Dict[str, Any], result: Dict[str, Any]):
        """Record completed task"""
        self.task_history.append({
            "timestamp": datetime.now(),
            "task": task,
            "result": result,
        })

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "type": self.__class__.__name__,
            "capabilities": self.get_capabilities(),
            "tasks_completed": len(self.task_history),
            "knowledge_items": len(self.knowledge_base),
        }
