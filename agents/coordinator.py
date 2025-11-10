"""
Agent Coordinator
Orchestrates multiple agents for collaborative security testing
"""

from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base_agent import BaseAgent, AgentMessage
from .recon_agent import ReconAgent
from .exploit_agent import ExploitAgent
from .defense_agent import DefenseAgent


class AgentCoordinator:
    """Coordinates multiple agents for collaborative security testing"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_bus: List[AgentMessage] = []

        # Initialize agents
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all agents"""
        print("[*] Initializing multi-agent system...")

        self.agents["recon"] = ReconAgent()
        self.agents["exploit"] = ExploitAgent()
        self.agents["defense"] = DefenseAgent()

        print(f"[+] Initialized {len(self.agents)} agents")

    def run_collaborative_assessment(
        self,
        target: str,
        objective: str = "full_security_assessment",
    ) -> Dict[str, Any]:
        """
        Run collaborative security assessment with all agents

        Args:
            target: Target to assess
            objective: Assessment objective

        Returns:
            Complete assessment results
        """
        print("\n" + "=" * 80)
        print(f"COLLABORATIVE SECURITY ASSESSMENT: {target}")
        print(f"Objective: {objective}")
        print("=" * 80 + "\n")

        results = {
            "target": target,
            "objective": objective,
            "phases": {},
        }

        # Phase 1: Reconnaissance
        print("\n--- PHASE 1: RECONNAISSANCE ---")
        recon_task = {
            "type": "full_recon",
            "target": target,
        }
        recon_results = self.agents["recon"].process_task(recon_task)
        results["phases"]["reconnaissance"] = recon_results

        # Phase 2: Exploitation Analysis
        print("\n--- PHASE 2: EXPLOITATION ANALYSIS ---")

        services = []
        if "port_scan" in recon_results.get("phases", {}):
            services = recon_results["phases"]["port_scan"].get("services", [])

        exploit_task = {
            "type": "find_exploits",
            "services": services,
        }
        exploit_results = self.agents["exploit"].process_task(exploit_task)
        results["phases"]["exploitation"] = exploit_results

        # Phase 3: Defense Recommendations
        print("\n--- PHASE 3: DEFENSE RECOMMENDATIONS ---")

        vulnerabilities = []
        for exploit in exploit_results.get("exploits", []):
            vulnerabilities.append({
                "title": f"Vulnerable {exploit['service']}",
                "service": exploit["service"],
                "version": exploit["version"],
                "severity": "HIGH",
            })

        defense_task = {
            "type": "recommend_fixes",
            "vulnerabilities": vulnerabilities,
        }
        defense_results = self.agents["defense"].process_task(defense_task)
        results["phases"]["defense"] = defense_results

        # Phase 4: Final Summary
        print("\n--- PHASE 4: FINAL ANALYSIS ---")
        final_summary = self._generate_final_summary(results)
        results["summary"] = final_summary

        print("\n" + "=" * 80)
        print("ASSESSMENT COMPLETE")
        print("=" * 80)

        return results

    def _generate_final_summary(self, results: Dict[str, Any]) -> str:
        """Generate final summary using AI"""
        from core.llm_interface import get_llm

        llm = get_llm()

        # Compile key findings
        recon = results["phases"].get("reconnaissance", {})
        exploit = results["phases"].get("exploitation", {})
        defense = results["phases"].get("defense", {})

        summary_data = f"""Target: {results['target']}

Reconnaissance Results:
- Services found: {len(recon.get('phases', {}).get('port_scan', {}).get('services', []))}

Exploitation Analysis:
- Potential exploits: {len(exploit.get('exploits', []))}

Defense Recommendations:
- Fixes recommended: {len(defense.get('recommendations', []))}
"""

        prompt = f"""As a security assessment lead, provide an executive summary of this collaborative security assessment:

{summary_data}

Provide:
1. **Executive Summary**: High-level overview (2-3 sentences)
2. **Critical Findings**: Top 3-5 most critical issues
3. **Risk Assessment**: Overall risk level and justification
4. **Priority Actions**: Top 3 actions to take immediately
5. **Strategic Recommendations**: Long-term security improvements

Make it suitable for both technical and executive audiences."""

        try:
            summary = llm.generate(prompt)

            print("\n" + "=" * 80)
            print("EXECUTIVE SUMMARY:")
            print("=" * 80)
            print(summary)
            print("=" * 80 + "\n")

            return summary

        except Exception as e:
            return f"Summary generation failed: {e}"

    def run_parallel_tasks(
        self,
        tasks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple tasks in parallel across agents

        Args:
            tasks: List of tasks with agent_id and task details

        Returns:
            List of results
        """
        print(f"[*] Running {len(tasks)} tasks in parallel")

        results = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}

            for task in tasks:
                agent_id = task.get("agent_id")
                if agent_id in self.agents:
                    future = executor.submit(
                        self.agents[agent_id].process_task,
                        task,
                    )
                    futures[future] = agent_id

            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    result = future.result()
                    results.append({
                        "agent_id": agent_id,
                        "result": result,
                    })
                except Exception as e:
                    results.append({
                        "agent_id": agent_id,
                        "error": str(e),
                    })

        return results

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}

        for agent_id, agent in self.agents.items():
            status[agent_id] = agent.get_status()

        return status

    def query_agents(self, question: str) -> Dict[str, str]:
        """
        Ask a question to all agents

        Args:
            question: Question to ask

        Returns:
            Responses from all agents
        """
        print(f"[*] Querying all agents: {question}")

        responses = {}

        for agent_id, agent in self.agents.items():
            message = AgentMessage(
                sender="coordinator",
                recipient=agent_id,
                message_type="query",
                content={"question": question},
            )

            response = agent.receive_message(message)
            responses[agent_id] = response.get("answer", "No response")

        return responses
