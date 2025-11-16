"""
Prompt Templates for Security Analysis
Optimized prompts for various security testing scenarios
"""

from typing import Dict, Any


class PromptTemplates:
    """Security-focused prompt templates"""

    # ==================== Vulnerability Analysis ====================

    @staticmethod
    def get_code_vulnerability_prompt(code: str, language: str) -> str:
        """Prompt for code vulnerability analysis"""
        return f"""You are a security expert analyzing {language} code for vulnerabilities.

Analyze the following code and identify any security vulnerabilities:

```{language}
{code}
```

Provide a detailed analysis covering:
1. **Security Vulnerabilities**: List all vulnerabilities (SQL injection, XSS, CSRF, etc.)
2. **Severity**: Rate each vulnerability (CRITICAL, HIGH, MEDIUM, LOW)
3. **Exploitation**: How could each vulnerability be exploited?
4. **Remediation**: Specific code fixes for each vulnerability
5. **Best Practices**: Additional security recommendations

Format your response as a structured analysis."""

    @staticmethod
    def get_security_analysis_prompt(analysis_type: str) -> str:
        """Generic security analysis prompt"""
        prompts = {
            "vulnerability": """You are a vulnerability assessment expert. Analyze the following data for security vulnerabilities:

{data}

Identify:
1. Vulnerabilities found
2. Severity levels
3. Potential impact
4. Remediation steps""",

            "threat": """You are a threat intelligence analyst. Analyze the following threat data:

{data}

Provide:
1. Threat classification
2. IOCs (Indicators of Compromise)
3. Attack vectors
4. Mitigation strategies""",

            "log": """You are a security log analyst. Analyze the following logs for suspicious activity:

{data}

Identify:
1. Suspicious patterns
2. Potential security incidents
3. Attack indicators
4. Recommended actions""",

            "network": """You are a network security expert. Analyze the following network data:

{data}

Assess:
1. Security posture
2. Exposed services
3. Potential attack vectors
4. Hardening recommendations""",
        }

        return prompts.get(analysis_type, prompts["vulnerability"])

    # ==================== Exploit Suggestions ====================

    @staticmethod
    def get_exploit_suggestion_prompt(service: str, version: str, context: str) -> str:
        """Prompt for exploit suggestions"""
        return f"""You are a penetration testing expert. Analyze the following service for potential exploits:

**Service**: {service}
**Version**: {version}
**Context**: {context}

Provide:
1. **Known CVEs**: List CVEs affecting this version
2. **Exploit Availability**: Public exploits (Metasploit, ExploitDB, etc.)
3. **Attack Vectors**: How to exploit each vulnerability
4. **Payload Examples**: Example payloads or commands
5. **Mitigation**: How to patch/mitigate these vulnerabilities

Format as a structured report with clear sections."""

    # ==================== Attack Planning ====================

    @staticmethod
    def get_attack_planning_prompt(target_info: Dict[str, Any], objective: str) -> str:
        """Prompt for attack chain planning"""
        target_str = "\n".join([f"- {k}: {v}" for k, v in target_info.items()])

        return f"""You are a red team operator planning an attack. Given the following target information:

{target_str}

**Objective**: {objective}

Create a detailed attack plan:

1. **Reconnaissance**: What additional information is needed?
2. **Initial Access**: How to gain initial foothold?
3. **Privilege Escalation**: Steps to elevate privileges
4. **Lateral Movement**: How to move through the network
5. **Objective Achievement**: Steps to achieve the stated objective
6. **Persistence**: How to maintain access (if applicable)
7. **Evasion**: Techniques to avoid detection

Provide a step-by-step plan with specific commands and techniques."""

    # ==================== Network Security ====================

    @staticmethod
    def get_network_analysis_prompt(scan_results: str) -> str:
        """Prompt for network scan analysis"""
        return f"""You are a network security analyst. Analyze the following network scan results:

{scan_results}

Provide a comprehensive analysis:

1. **Critical Findings**: Most severe security issues
2. **Exposed Services**: Services accessible from the network
3. **Vulnerable Services**: Services with known vulnerabilities
4. **Configuration Issues**: Misconfigurations found
5. **Attack Surface**: Overall attack surface assessment
6. **Risk Rating**: Overall risk level (CRITICAL, HIGH, MEDIUM, LOW)
7. **Recommendations**: Prioritized remediation steps

Be specific and actionable."""

    @staticmethod
    def get_port_scan_strategy_prompt(target_info: Dict[str, Any]) -> str:
        """Prompt for intelligent port scanning strategy"""
        return f"""You are a network reconnaissance expert. Based on the following information:

{target_info}

Suggest an optimal port scanning strategy:

1. **Ports to Scan**: Which specific ports to prioritize?
2. **Scan Techniques**: Which nmap techniques to use?
3. **Timing**: Recommended timing template
4. **Evasion**: Any evasion techniques needed?
5. **Service Detection**: Specific service detection flags

Provide specific nmap commands."""

    # ==================== Wireless Security ====================

    @staticmethod
    def get_wireless_analysis_prompt(wireless_data: str) -> str:
        """Prompt for wireless security analysis"""
        return f"""You are a wireless security expert. Analyze the following wireless network data:

{wireless_data}

Assess:

1. **Encryption**: Encryption protocols in use
2. **Vulnerabilities**: Known wireless vulnerabilities
3. **Attack Vectors**: Possible attack methods
4. **Client Security**: Client device security issues
5. **Recommendations**: Security improvements

Provide specific recommendations."""

    # ==================== Traffic Analysis ====================

    @staticmethod
    def get_traffic_analysis_prompt(pcap_summary: str) -> str:
        """Prompt for network traffic analysis"""
        return f"""You are a network traffic analyst. Analyze the following packet capture summary:

{pcap_summary}

Identify:

1. **Suspicious Patterns**: Unusual traffic patterns
2. **Protocol Anomalies**: Protocol-level issues
3. **Credential Leakage**: Potential credential exposure
4. **Data Exfiltration**: Signs of data exfiltration
5. **C2 Communication**: Possible C2 traffic
6. **Malicious Activity**: Other malicious indicators

Be thorough and specific."""

    # ==================== Threat Intelligence ====================

    @staticmethod
    def get_ioc_analysis_prompt(ioc: str, ioc_type: str) -> str:
        """Prompt for IOC analysis"""
        return f"""You are a threat intelligence analyst. Analyze the following Indicator of Compromise (IOC):

**IOC**: {ioc}
**Type**: {ioc_type}

Provide:

1. **Classification**: What type of threat is this associated with?
2. **Known Campaigns**: Any known campaigns using this IOC?
3. **Threat Actor**: Possible threat actor attribution
4. **Risk Level**: Risk assessment
5. **Recommended Actions**: What should be done if this IOC is found?

Be specific and cite sources when possible."""

    @staticmethod
    def get_cve_analysis_prompt(cve_id: str, cve_data: Dict[str, Any]) -> str:
        """Prompt for CVE analysis"""
        return f"""You are a vulnerability researcher. Analyze the following CVE:

**CVE ID**: {cve_id}
**Data**: {cve_data}

Provide:

1. **Vulnerability Summary**: Clear explanation of the vulnerability
2. **Technical Details**: How the vulnerability works
3. **Affected Systems**: Which systems/versions are affected
4. **CVSS Score**: Risk rating
5. **Exploitation**: Is it being actively exploited?
6. **Proof of Concept**: Are there public PoCs available?
7. **Mitigation**: How to fix/mitigate
8. **Detection**: How to detect if you're vulnerable

Be thorough and actionable."""

    # ==================== Incident Response ====================

    @staticmethod
    def get_incident_analysis_prompt(incident_data: str) -> str:
        """Prompt for incident analysis"""
        return f"""You are an incident responder. Analyze the following security incident:

{incident_data}

Provide:

1. **Incident Summary**: What happened?
2. **Attack Vector**: How did the attacker gain access?
3. **Scope**: What systems/data were affected?
4. **IOCs**: Indicators of Compromise to search for
5. **Containment**: Immediate containment steps
6. **Eradication**: How to remove the threat
7. **Recovery**: Steps to recover systems
8. **Lessons Learned**: Recommendations to prevent recurrence

Follow NIST incident response framework."""

    # ==================== Report Generation ====================

    @staticmethod
    def get_executive_summary_prompt(findings: str) -> str:
        """Prompt for executive summary generation"""
        return f"""You are a security consultant writing an executive summary. Based on the following technical findings:

{findings}

Write a concise executive summary for non-technical leadership:

1. **Overview**: High-level summary (2-3 sentences)
2. **Key Risks**: Top 3-5 critical risks in business terms
3. **Business Impact**: Potential impact to the organization
4. **Recommendations**: Priority actions (high-level)
5. **Timeline**: Suggested remediation timeline

Use clear, non-technical language suitable for executives."""

    @staticmethod
    def get_technical_report_prompt(findings: str) -> str:
        """Prompt for technical report generation"""
        return f"""You are a security analyst writing a technical report. Based on the following findings:

{findings}

Write a detailed technical report:

1. **Executive Summary**: Brief overview
2. **Methodology**: Testing methodology used
3. **Findings**: Detailed findings with:
   - Vulnerability name
   - Severity
   - Description
   - Evidence
   - Impact
   - Remediation
4. **Risk Matrix**: Risk assessment
5. **Recommendations**: Detailed remediation steps
6. **Conclusion**: Overall assessment

Use professional security reporting standards."""

    # ==================== Natural Language Query ====================

    @staticmethod
    def get_nl_query_prompt(query: str, context: Dict[str, Any]) -> str:
        """Prompt for natural language queries"""
        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])

        return f"""You are a security assistant. Answer the following security question based on the available data:

**Question**: {query}

**Available Data**:
{context_str}

Provide a clear, actionable answer. If you don't have enough information, say so and suggest what additional data is needed."""

    # ==================== Code Review ====================

    @staticmethod
    def get_code_review_prompt(code_diff: str, language: str) -> str:
        """Prompt for security-focused code review"""
        return f"""You are a senior security engineer reviewing code changes. Review the following {language} code diff:

```diff
{code_diff}
```

Provide a security-focused code review:

1. **Security Issues**: Any security vulnerabilities introduced?
2. **Best Practices**: Deviations from security best practices?
3. **Input Validation**: Proper input validation?
4. **Authentication/Authorization**: Auth issues?
5. **Data Protection**: Sensitive data handling?
6. **Injection Risks**: SQL, command, XSS, etc.?
7. **Recommendations**: Specific improvements

Format as code review comments with line references."""

    # ==================== Helper Methods ====================

    @staticmethod
    def format_json_prompt(data: Dict[str, Any], task: str) -> str:
        """Format JSON data for LLM prompt"""
        import json
        json_str = json.dumps(data, indent=2)
        return f"""Task: {task}

Data:
```json
{json_str}
```

Analyze the above data and complete the task."""
