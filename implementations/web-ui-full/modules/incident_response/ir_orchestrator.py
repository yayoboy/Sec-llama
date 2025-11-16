"""
Incident Response Orchestrator
Automated incident response using AI-powered playbooks
"""

from typing import Dict, Any, List
from datetime import datetime

from core.llm_interface import get_llm


class IncidentResponseOrchestrator:
    """Orchestrate incident response activities"""

    def __init__(self):
        self.llm = get_llm()
        self.incidents = []

    def create_incident(
        self,
        title: str,
        description: str,
        severity: str = "MEDIUM",
        indicators: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Create new incident

        Args:
            title: Incident title
            description: Incident description
            severity: Severity level
            indicators: IOCs

        Returns:
            Incident object
        """
        incident = {
            "id": f"INC-{len(self.incidents) + 1:04d}",
            "title": title,
            "description": description,
            "severity": severity,
            "indicators": indicators or [],
            "status": "NEW",
            "created_at": datetime.now(),
            "actions": [],
        }

        self.incidents.append(incident)

        print(f"[*] Created incident: {incident['id']} - {title}")
        print(f"[*] Severity: {severity}")

        # Generate IR playbook with AI
        self._generate_playbook(incident)

        return incident

    def _generate_playbook(self, incident: Dict[str, Any]):
        """Generate IR playbook with AI"""
        print(f"\n[*] Generating IR playbook for {incident['id']}...")

        prompt = f"""Generate an incident response playbook for:

Title: {incident['title']}
Description: {incident['description']}
Severity: {incident['severity']}
Indicators: {', '.join(incident['indicators'])}

Provide a step-by-step IR playbook following NIST framework:

1. **Preparation**: Pre-incident preparations
2. **Detection & Analysis**: How to investigate
3. **Containment**: Immediate containment actions
4. **Eradication**: Remove threat
5. **Recovery**: Restore operations
6. **Post-Incident**: Lessons learned

Include specific commands and tools."""

        try:
            playbook = self.llm.generate(prompt)

            incident["playbook"] = playbook

            print("\n" + "=" * 80)
            print(f"IR PLAYBOOK: {incident['id']}")
            print("=" * 80)
            print(playbook)
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"[!] Playbook generation failed: {e}")

    def execute_containment(self, incident_id: str) -> Dict[str, Any]:
        """Execute containment actions"""
        incident = self._get_incident(incident_id)

        if not incident:
            return {"status": "error", "message": "Incident not found"}

        print(f"[*] Executing containment for {incident_id}")

        prompt = f"""Provide immediate containment actions for:

Incident: {incident['title']}
Severity: {incident['severity']}

List specific commands to:
1. Isolate affected systems
2. Block malicious IPs/domains
3. Disable compromised accounts
4. Preserve evidence

Provide executable commands."""

        try:
            containment_plan = self.llm.generate(prompt)

            incident["status"] = "CONTAINED"
            incident["actions"].append({
                "type": "containment",
                "timestamp": datetime.now(),
                "plan": containment_plan,
            })

            print("\n" + "=" * 80)
            print("CONTAINMENT PLAN:")
            print("=" * 80)
            print(containment_plan)
            print("=" * 80 + "\n")

            return {"status": "success", "plan": containment_plan}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _get_incident(self, incident_id: str) -> Dict[str, Any]:
        """Get incident by ID"""
        for incident in self.incidents:
            if incident["id"] == incident_id:
                return incident
        return None

    def generate_report(self, incident_id: str) -> str:
        """Generate incident report"""
        incident = self._get_incident(incident_id)

        if not incident:
            return "Incident not found"

        report = f"""
INCIDENT RESPONSE REPORT
{'=' * 80}

Incident ID: {incident['id']}
Title: {incident['title']}
Severity: {incident['severity']}
Status: {incident['status']}
Created: {incident['created_at']}

Description:
{incident['description']}

Indicators of Compromise:
{chr(10).join(['- ' + ioc for ioc in incident['indicators']])}

Actions Taken:
{chr(10).join([f"- {a['type']} at {a['timestamp']}" for a in incident['actions']])}

Playbook:
{incident.get('playbook', 'Not generated')}

{'=' * 80}
"""

        print(report)
        return report
