"""
Reconnaissance Agent
Specialized in information gathering and network reconnaissance
"""

from typing import Dict, Any, List

from .base_agent import BaseAgent
from modules.network.discovery.host_discovery import HostDiscovery
from modules.network.scanning.port_scanner import PortScanner


class ReconAgent(BaseAgent):
    """Agent specialized in reconnaissance"""

    def __init__(self, agent_id: str = "recon_agent"):
        super().__init__(agent_id)
        self.host_discovery = HostDiscovery()
        self.port_scanner = PortScanner()

    def get_capabilities(self) -> List[str]:
        """Agent capabilities"""
        return [
            "network_discovery",
            "port_scanning",
            "service_detection",
            "os_fingerprinting",
            "information_gathering",
        ]

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process reconnaissance task

        Args:
            task: Task with type and parameters

        Returns:
            Reconnaissance results
        """
        task_type = task.get("type")

        print(f"[{self.agent_id}] Processing task: {task_type}")

        if task_type == "network_discovery":
            return self._discover_network(task)
        elif task_type == "port_scan":
            return self._scan_ports(task)
        elif task_type == "full_recon":
            return self._full_reconnaissance(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    def _discover_network(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Discover hosts in network"""
        network = task.get("network")
        method = task.get("method", "arp")

        print(f"[{self.agent_id}] Discovering network: {network}")

        try:
            hosts = self.host_discovery.discover_network(network, method)

            # Store in knowledge base
            self.update_knowledge(f"network_{network}_hosts", [h.ip for h in hosts])

            result = {
                "status": "success",
                "task": "network_discovery",
                "hosts_found": len(hosts),
                "hosts": [h.to_dict() for h in hosts],
            }

            self.record_task(task, result)
            return result

        except Exception as e:
            return {
                "status": "error",
                "task": "network_discovery",
                "error": str(e),
            }

    def _scan_ports(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan ports on target"""
        target = task.get("target")
        ports = task.get("ports")

        print(f"[{self.agent_id}] Scanning ports on: {target}")

        try:
            result = self.port_scanner.scan(target, ports=ports, ai_suggest=False)

            # Store findings
            self.update_knowledge(f"host_{target}_services", [s.to_dict() for s in result.services])

            scan_result = {
                "status": "success",
                "task": "port_scan",
                "target": target,
                "services_found": len(result.services),
                "services": [s.to_dict() for s in result.services],
            }

            self.record_task(task, scan_result)
            return scan_result

        except Exception as e:
            return {
                "status": "error",
                "task": "port_scan",
                "error": str(e),
            }

    def _full_reconnaissance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform full reconnaissance on target"""
        target = task.get("target")

        print(f"[{self.agent_id}] Full reconnaissance on: {target}")

        results = {
            "status": "success",
            "task": "full_recon",
            "target": target,
            "phases": {},
        }

        # Phase 1: Network discovery if CIDR
        if "/" in target:
            discovery_result = self._discover_network({"network": target, "method": "arp"})
            results["phases"]["discovery"] = discovery_result

            # Get first host for deeper scan
            if discovery_result.get("hosts"):
                target = discovery_result["hosts"][0]["ip"]

        # Phase 2: Port scan
        scan_result = self._scan_ports({"target": target, "ports": "1-10000"})
        results["phases"]["port_scan"] = scan_result

        # Phase 3: AI analysis
        prompt = f"""As a reconnaissance agent, analyze the following findings:

Target: {target}

Services found:
{scan_result.get('services', [])}

Provide:
1. **Attack Surface**: What attack vectors are available?
2. **Vulnerability Assessment**: Likely vulnerabilities based on services
3. **Prioritization**: Which services to investigate first
4. **Next Steps**: Recommended actions for exploitation team

Be specific and actionable."""

        try:
            analysis = self.llm.generate(prompt)
            results["phases"]["analysis"] = analysis

            print("\n" + "=" * 80)
            print(f"[{self.agent_id}] RECONNAISSANCE ANALYSIS:")
            print("=" * 80)
            print(analysis)
            print("=" * 80 + "\n")

        except Exception as e:
            results["phases"]["analysis"] = f"Analysis failed: {e}"

        self.record_task(task, results)
        return results

    def suggest_next_targets(self) -> List[str]:
        """Suggest next targets based on knowledge"""
        # Analyze knowledge base to suggest interesting targets
        targets = []

        for key, value in self.knowledge_base.items():
            if "services" in key and isinstance(value, list):
                # Look for interesting services
                for service in value:
                    if service.get("port") in [21, 22, 23, 445, 3389]:  # Interesting ports
                        targets.append(service.get("file", "").split("_")[1])

        return list(set(targets))  # Unique targets
