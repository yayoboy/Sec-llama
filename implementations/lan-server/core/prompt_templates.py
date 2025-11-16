"""
Prompt Templates for Security Analysis
Contains templates for various security analysis tasks
"""

from typing import Dict, Any, List


class PromptTemplates:
    """Collection of prompt templates for security analysis"""

    @staticmethod
    def get_cve_analysis_prompt(cve_id: str, cve_info: Dict[str, Any]) -> str:
        """Generate prompt for CVE analysis"""
        prompt = f"""You are a cybersecurity expert analyzing a CVE vulnerability.

CVE ID: {cve_id}
Description: {cve_info.get('description', 'N/A')}
CVSS Score: {cve_info.get('cvss_score', {}).get('score', 'N/A')} ({cve_info.get('cvss_score', {}).get('severity', 'N/A')})
Published: {cve_info.get('published', 'N/A')}

Provide a comprehensive security analysis including:
1. **Vulnerability Summary**: Explain the vulnerability in simple terms
2. **Attack Vector**: How can this be exploited?
3. **Impact**: What damage can an attacker cause?
4. **Affected Systems**: What systems/software are vulnerable?
5. **Mitigation**: How to fix or mitigate this vulnerability?
6. **Detection**: How to detect if systems are vulnerable or exploited?
7. **Severity Assessment**: Is this critical? Should it be prioritized?

Keep the analysis practical and actionable for security teams."""

        return prompt

    @staticmethod
    def get_network_analysis_prompt(network_data: Dict[str, Any]) -> str:
        """Generate prompt for network analysis"""
        prompt = f"""You are a network security expert analyzing network scan results.

Scan Results:
{network_data}

Provide a security analysis including:
1. **Network Overview**: Summary of discovered hosts and services
2. **Security Risks**: Identify potential vulnerabilities and misconfigurations
3. **Open Ports Analysis**: Analysis of exposed services
4. **Recommendations**: Security hardening suggestions
5. **Priority Actions**: What should be addressed immediately?

Focus on practical security recommendations."""

        return prompt

    @staticmethod
    def get_code_review_prompt(code: str, language: str = "python") -> str:
        """Generate prompt for code security review"""
        prompt = f"""You are a security-focused code reviewer analyzing {language} code.

Code to review:
```{language}
{code}
```

Perform a security-focused code review and identify:
1. **Security Vulnerabilities**: SQL injection, XSS, command injection, etc.
2. **Authentication/Authorization Issues**: Access control problems
3. **Data Exposure**: Sensitive data handling issues
4. **Cryptography Issues**: Weak encryption, hardcoded secrets
5. **Input Validation**: Missing or weak input validation
6. **Best Practices**: Code quality and security best practices

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Location in code
- Explanation of the vulnerability
- Remediation suggestion with code example

Be thorough but practical."""

        return prompt

    @staticmethod
    def get_attack_planning_prompt(target_info: Dict[str, Any]) -> str:
        """Generate prompt for attack planning (authorized pentesting)"""
        prompt = f"""You are a penetration testing expert planning an authorized security assessment.

Target Information:
{target_info}

**IMPORTANT**: This is for authorized penetration testing only.

Develop a penetration testing strategy including:
1. **Reconnaissance Phase**: Information gathering approach
2. **Vulnerability Assessment**: Expected vulnerabilities based on target info
3. **Exploitation Strategy**: Potential attack vectors to test
4. **Privilege Escalation**: Post-exploitation techniques
5. **Persistence & Lateral Movement**: Advanced techniques to test
6. **Detection Evasion**: Stealthy testing approaches
7. **Testing Timeline**: Suggested phases and timeline

Provide a professional, methodical approach suitable for authorized security testing."""

        return prompt

    @staticmethod
    def get_log_analysis_prompt(logs: str, log_type: str = "system") -> str:
        """Generate prompt for log analysis"""
        prompt = f"""You are a security analyst analyzing {log_type} logs for security incidents.

Logs to analyze:
{logs}

Analyze these logs for:
1. **Security Events**: Failed logins, privilege escalations, suspicious commands
2. **Attack Patterns**: Brute force, scanning, exploitation attempts
3. **Anomalies**: Unusual behavior, unexpected access patterns
4. **IOCs (Indicators of Compromise)**: Malicious IPs, file hashes, domains
5. **Timeline**: Chronological sequence of events
6. **Recommendations**: Investigation steps and mitigation actions

Provide actionable intelligence for incident response."""

        return prompt

    @staticmethod
    def get_ioc_analysis_prompt(ioc: str, ioc_type: str) -> str:
        """Generate prompt for IOC analysis"""
        prompt = f"""You are a threat intelligence analyst analyzing an Indicator of Compromise.

IOC Type: {ioc_type}
IOC Value: {ioc}

Analyze this IOC and provide:
1. **Threat Assessment**: Is this IOC malicious? Confidence level?
2. **Associated Threats**: Known malware, APT groups, campaigns
3. **Behavior**: What does this IOC typically do?
4. **Context**: When/where is this IOC seen?
5. **Blocking Recommendations**: How to block/mitigate this threat?
6. **Related IOCs**: Other indicators to watch for
7. **Investigation Steps**: How to investigate if found in your environment?

Be specific and actionable."""

        return prompt

    @staticmethod
    def get_incident_response_prompt(incident_data: Dict[str, Any]) -> str:
        """Generate prompt for incident response planning"""
        prompt = f"""You are an incident response expert handling a security incident.

Incident Information:
{incident_data}

Provide an incident response plan following NIST guidelines:
1. **Preparation**: Initial response steps
2. **Detection & Analysis**: What to investigate first
3. **Containment**: Immediate containment actions
   - Short-term containment
   - Long-term containment
4. **Eradication**: Remove threat from environment
5. **Recovery**: Restore systems safely
6. **Post-Incident**: Lessons learned and improvements

For each phase, provide specific, actionable steps."""

        return prompt

    @staticmethod
    def get_threat_hunting_prompt(environment_info: Dict[str, Any]) -> str:
        """Generate prompt for proactive threat hunting"""
        prompt = f"""You are a threat hunter conducting proactive security analysis.

Environment Information:
{environment_info}

Design a threat hunting campaign:
1. **Hypothesis**: What threats might be present and why?
2. **Hunt Tactics**: What to look for (MITRE ATT&CK techniques)
3. **Data Sources**: Where to look (logs, endpoints, network)
4. **Hunt Queries**: Specific queries/searches to run
5. **Indicators to Find**: What would confirm the hypothesis?
6. **Response Plan**: What to do if threats are found

Use MITRE ATT&CK framework for structured hunting."""

        return prompt

    @staticmethod
    def get_vulnerability_assessment_prompt(scan_results: Dict[str, Any]) -> str:
        """Generate prompt for vulnerability assessment analysis"""
        prompt = f"""You are a vulnerability assessment expert analyzing scan results.

Scan Results:
{scan_results}

Provide a comprehensive vulnerability assessment:
1. **Executive Summary**: High-level overview for management
2. **Critical Findings**: Most severe vulnerabilities
3. **Risk Analysis**: Business impact and likelihood
4. **Vulnerability Details**: Technical details of each finding
5. **Remediation Roadmap**: Prioritized fix recommendations
6. **Compensating Controls**: Temporary mitigations
7. **Validation Steps**: How to verify fixes

Organize by severity and provide clear, actionable guidance."""

        return prompt

    @staticmethod
    def get_traffic_analysis_prompt(traffic_data: str) -> str:
        """Generate prompt for network traffic analysis"""
        prompt = f"""You are a network security analyst analyzing network traffic.

Traffic Data:
{traffic_data}

Analyze this traffic for:
1. **Normal vs. Suspicious**: Baseline vs. anomalies
2. **Protocols**: Protocol usage and abnormalities
3. **Data Exfiltration**: Large data transfers, unusual destinations
4. **Command & Control**: C2 communication patterns
5. **Lateral Movement**: East-west traffic analysis
6. **Encrypted Traffic**: TLS/SSL analysis
7. **Recommendations**: Network security improvements

Focus on detecting malicious activity and insider threats."""

        return prompt

    @staticmethod
    def get_api_security_prompt(api_spec: Dict[str, Any]) -> str:
        """Generate prompt for API security analysis"""
        prompt = f"""You are an API security expert analyzing an API specification.

API Specification:
{api_spec}

Analyze this API for security issues:
1. **Authentication**: Auth mechanisms and weaknesses
2. **Authorization**: Access control issues
3. **Input Validation**: Injection vulnerabilities
4. **Rate Limiting**: DDoS protection
5. **Data Exposure**: Sensitive data leakage
6. **OWASP API Top 10**: Coverage of common API vulnerabilities
7. **Security Headers**: Missing security headers
8. **Testing Strategy**: How to test this API for vulnerabilities

Provide specific recommendations for each endpoint."""

        return prompt

    @staticmethod
    def get_general_security_prompt(context: str, question: str) -> str:
        """Generate a general security analysis prompt"""
        prompt = f"""You are a cybersecurity expert providing security guidance.

Context:
{context}

Question:
{question}

Provide a comprehensive, professional response that:
1. Addresses the security concern directly
2. Explains technical concepts clearly
3. Provides actionable recommendations
4. Considers business impact
5. Follows industry best practices

Be practical and specific in your recommendations."""

        return prompt
