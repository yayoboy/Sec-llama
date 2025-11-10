"""
Defense Agent (Blue Team)
Specialized in defense, detection, and mitigation
"""

from typing import Dict, Any, List

from .base_agent import BaseAgent


class DefenseAgent(BaseAgent):
    """Agent specialized in defensive security"""

    def __init__(self, agent_id: str = "defense_agent"):
        super().__init__(agent_id)

    def get_capabilities(self) -> List[str]:
        """Agent capabilities"""
        return [
            "vulnerability_remediation",
            "security_hardening",
            "detection_rules",
            "incident_response",
            "threat_hunting",
        ]

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process defense task"""
        task_type = task.get("type")

        print(f"[{self.agent_id}] Processing task: {task_type}")

        if task_type == "recommend_fixes":
            return self._recommend_fixes(task)
        elif task_type == "create_detection_rules":
            return self._create_detection_rules(task)
        elif task_type == "assess_defenses":
            return self._assess_defenses(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    def _recommend_fixes(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend fixes for vulnerabilities"""
        vulnerabilities = task.get("vulnerabilities", [])

        print(f"[{self.agent_id}] Recommending fixes for {len(vulnerabilities)} vulnerabilities")

        recommendations = []

        for vuln in vulnerabilities:
            prompt = f"""As a defensive security expert, recommend fixes for:

Vulnerability: {vuln.get('title', 'Unknown')}
Service: {vuln.get('service', 'Unknown')} {vuln.get('version', '')}
Severity: {vuln.get('severity', 'Unknown')}

Provide:
1. **Immediate Actions**: Quick fixes to reduce risk
2. **Permanent Fix**: Long-term solution
3. **Configuration Changes**: Specific config changes
4. **Compensating Controls**: If patch not available
5. **Verification**: How to verify the fix worked

Be specific with commands and configurations."""

            try:
                fix_recommendation = self.llm.generate(prompt)

                recommendations.append({
                    "vulnerability": vuln,
                    "recommendations": fix_recommendation,
                })

                print(f"\n[{self.agent_id}] Fix for {vuln.get('title')}:")
                print(fix_recommendation[:200] + "...")

            except Exception as e:
                recommendations.append({
                    "vulnerability": vuln,
                    "error": str(e),
                })

        result = {
            "status": "success",
            "task": "recommend_fixes",
            "recommendations": recommendations,
        }

        self.record_task(task, result)
        return result

    def _create_detection_rules(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create detection rules for attacks"""
        attack_patterns = task.get("attack_patterns", [])

        print(f"[{self.agent_id}] Creating detection rules")

        rules = []

        for pattern in attack_patterns:
            prompt = f"""As a detection engineer, create detection rules for:

Attack Pattern: {pattern.get('description', 'Unknown attack')}
Indicators: {pattern.get('indicators', [])}

Create detection rules in these formats:
1. **Sigma Rule**: SIEM-agnostic detection rule
2. **Snort/Suricata**: Network IDS rule
3. **YARA**: File/memory scanning rule (if applicable)
4. **Splunk SPL**: Splunk search query
5. **KQL**: Azure Sentinel/Defender query

Provide specific, working rules."""

            try:
                detection_rules = self.llm.generate(prompt)

                rules.append({
                    "pattern": pattern,
                    "rules": detection_rules,
                })

            except Exception as e:
                rules.append({
                    "pattern": pattern,
                    "error": str(e),
                })

        result = {
            "status": "success",
            "task": "create_detection_rules",
            "rules": rules,
        }

        self.record_task(task, result)
        return result

    def _assess_defenses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current security posture"""
        target_info = task.get("target_info", {})
        findings = task.get("findings", [])

        print(f"[{self.agent_id}] Assessing defenses")

        findings_summary = "\n".join([
            f"- {f.get('title', 'Unknown')}: {f.get('severity', 'Unknown')}"
            for f in findings[:10]
        ])

        prompt = f"""As a defensive security expert, assess the security posture:

Target: {target_info.get('target', 'Unknown')}
OS: {target_info.get('os', 'Unknown')}

Findings:
{findings_summary}

Provide:
1. **Overall Security Posture**: Rating (1-10) and summary
2. **Critical Gaps**: Most critical security gaps
3. **Defense Strategy**: Recommended defense-in-depth strategy
4. **Quick Wins**: Easy improvements with high impact
5. **Long-term Roadmap**: Strategic security improvements
6. **Budget Priorities**: Where to invest security budget

Be strategic and actionable."""

        try:
            assessment = self.llm.generate(prompt)

            result = {
                "status": "success",
                "task": "assess_defenses",
                "assessment": assessment,
            }

            print("\n" + "=" * 80)
            print(f"[{self.agent_id}] DEFENSE ASSESSMENT:")
            print("=" * 80)
            print(assessment)
            print("=" * 80 + "\n")

            self.record_task(task, result)
            return result

        except Exception as e:
            return {
                "status": "error",
                "task": "assess_defenses",
                "error": str(e),
            }

    def suggest_hardening(self, system_info: Dict[str, Any]) -> List[str]:
        """
        Suggest hardening measures

        Args:
            system_info: Information about the system

        Returns:
            List of hardening recommendations
        """
        print(f"[{self.agent_id}] Suggesting hardening measures")

        os_type = system_info.get("os", "").lower()

        recommendations = []

        # OS-specific recommendations
        if "windows" in os_type:
            recommendations.extend([
                "Disable SMBv1",
                "Enable Windows Defender",
                "Configure Windows Firewall",
                "Disable unnecessary services",
                "Enable AppLocker",
            ])
        elif "linux" in os_type:
            recommendations.extend([
                "Update all packages",
                "Configure UFW/iptables",
                "Disable root SSH login",
                "Configure SELinux/AppArmor",
                "Remove unnecessary packages",
            ])

        # Service-specific
        services = system_info.get("services", [])
        for service in services:
            if service.get("service") == "ssh":
                recommendations.append("Configure SSH key-only authentication")
            elif service.get("service") == "http":
                recommendations.append("Enable HTTPS and disable HTTP")

        return recommendations
