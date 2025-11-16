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

    @staticmethod
    def get_code_vulnerability_prompt(code: str, language: str = "python", context: str = "") -> str:
        """
        Generate prompt for code vulnerability analysis

        Used by: modules/code_review/git_reviewer.py
        """
        prompt = f"""You are a senior security engineer conducting a vulnerability assessment of {language} code.

{f'Context: {context}' if context else ''}

Code to analyze:
```{language}
{code}
```

Perform a deep security analysis and identify ALL vulnerabilities:

**1. CRITICAL VULNERABILITIES** (Immediate Action Required):
   - Remote Code Execution (RCE)
   - SQL Injection (SQLi)
   - Authentication bypass
   - Hardcoded credentials/secrets
   - Deserialization vulnerabilities

**2. HIGH SEVERITY VULNERABILITIES**:
   - Cross-Site Scripting (XSS)
   - Command Injection
   - Path Traversal
   - XML External Entity (XXE)
   - Server-Side Request Forgery (SSRF)
   - Insecure Direct Object References (IDOR)

**3. MEDIUM SEVERITY ISSUES**:
   - Weak cryptography
   - Missing input validation
   - Information disclosure
   - Insecure session management
   - Missing security headers

**4. LOW SEVERITY & CODE QUALITY**:
   - Error handling issues
   - Logging sensitive data
   - Resource leaks
   - Race conditions

For EACH vulnerability found, provide:
- **Line Number**: Exact location in code
- **Severity**: Critical/High/Medium/Low
- **CWE ID**: Common Weakness Enumeration identifier
- **Vulnerability Type**: Specific category
- **Explanation**: Why this is vulnerable
- **Exploit Scenario**: How an attacker could exploit this
- **Remediation**: Secure code example to fix the issue
- **References**: OWASP or security guidelines

Be extremely thorough - this code may go into production."""

        return prompt

    @staticmethod
    def get_exploit_suggestion_prompt(vulnerability_info: Dict[str, Any], target_info: Dict[str, Any]) -> str:
        """
        Generate prompt for exploit suggestions

        Used by: modules/pentest_assistant/attack_planner.py

        **IMPORTANT**: For authorized penetration testing only!
        """
        prompt = f"""You are a penetration testing expert suggesting exploitation techniques.

**AUTHORIZATION NOTICE**: This analysis is for AUTHORIZED penetration testing only.

Vulnerability Information:
{vulnerability_info}

Target Information:
{target_info}

Provide exploitation guidance for authorized security testing:

**1. EXPLOITATION STRATEGY**:
   - Pre-conditions needed
   - Attack prerequisites
   - Required tools and resources
   - Estimated difficulty level

**2. EXPLOITATION STEPS**:
   - Step-by-step methodology
   - Commands/scripts to use
   - Expected responses
   - Alternative approaches

**3. PROOF OF CONCEPT**:
   - Safe PoC that demonstrates the vulnerability
   - Non-destructive testing approach
   - Evidence collection methods

**4. POST-EXPLOITATION**:
   - What access/data can be obtained
   - Privilege escalation opportunities
   - Lateral movement possibilities
   - Persistence mechanisms

**5. DETECTION & BLUE TEAM PERSPECTIVE**:
   - How this attack can be detected
   - Logs/alerts that would trigger
   - IOCs (Indicators of Compromise)
   - Defense recommendations

**6. REMEDIATION PRIORITY**:
   - Business impact assessment
   - Fix complexity
   - Recommended timeline
   - Compensating controls

**IMPORTANT REMINDERS**:
- Only exploit in authorized scope
- Document all actions
- Maintain professional ethics
- Report findings responsibly

Provide practical, ethical exploitation guidance for professional pentesters."""

        return prompt

    @staticmethod
    def get_executive_summary_prompt(scan_results: Dict[str, Any], findings: List[Dict[str, Any]]) -> str:
        """
        Generate prompt for executive summary report

        Used by: modules/reporting/report_generator.py

        Creates a high-level summary suitable for C-level executives and management.
        """
        total_findings = len(findings)
        critical = sum(1 for f in findings if f.get('severity', '').lower() == 'critical')
        high = sum(1 for f in findings if f.get('severity', '').lower() == 'high')
        medium = sum(1 for f in findings if f.get('severity', '').lower() == 'medium')
        low = sum(1 for f in findings if f.get('severity', '').lower() == 'low')

        prompt = f"""You are a Chief Information Security Officer (CISO) writing an executive summary for the board of directors.

**Assessment Overview**:
- Total Findings: {total_findings}
- Critical: {critical}
- High: {high}
- Medium: {medium}
- Low: {low}

**Scan Results**:
{scan_results}

**Key Findings**:
{findings}

Write a professional executive summary that includes:

**1. EXECUTIVE OVERVIEW** (2-3 paragraphs):
   - Overall security posture assessment
   - Business risk summary
   - Key takeaways for executives

**2. RISK ASSESSMENT**:
   - **Critical Risks**: Immediate threats to business operations
   - **High Priority Issues**: Significant vulnerabilities requiring attention
   - **Business Impact**: Potential financial, reputational, and operational impact
   - **Compliance Implications**: Regulatory or compliance concerns

**3. KEY METRICS**:
   - Security score/rating
   - Comparison to industry benchmarks
   - Trend analysis (if available)
   - Risk exposure quantification

**4. STRATEGIC RECOMMENDATIONS**:
   - Top 3-5 priority actions
   - Resource requirements (budget, personnel)
   - Estimated timeline for remediation
   - Quick wins vs. long-term initiatives

**5. BUSINESS CONTEXT**:
   - How vulnerabilities affect business objectives
   - Customer/stakeholder impact
   - Competitive risk considerations
   - Market/industry implications

**TONE & STYLE**:
- Write for non-technical executives
- Use business language, not technical jargon
- Focus on risk, impact, and ROI
- Be concise and action-oriented
- Use metrics and quantifiable data
- Highlight both problems AND solutions

**LENGTH**: 1-2 pages maximum. Executives are busy - be succinct but comprehensive."""

        return prompt

    @staticmethod
    def get_technical_report_prompt(scan_results: Dict[str, Any], findings: List[Dict[str, Any]], detailed_data: Dict[str, Any]) -> str:
        """
        Generate prompt for technical security report

        Used by: modules/reporting/report_generator.py

        Creates a detailed technical report for security teams and engineers.
        """
        prompt = f"""You are a senior security analyst writing a comprehensive technical security report.

**Scan Results Summary**:
{scan_results}

**Findings** ({len(findings)} total):
{findings}

**Detailed Technical Data**:
{detailed_data}

Create a detailed technical report with the following sections:

**1. EXECUTIVE SUMMARY** (Brief - 1 paragraph):
   - High-level technical overview
   - Critical findings count
   - Overall risk assessment

**2. METHODOLOGY**:
   - Assessment scope
   - Tools and techniques used
   - Testing timeline
   - Limitations and constraints

**3. TECHNICAL FINDINGS** (Detailed):
   For EACH finding, include:
   - **Finding ID**: Unique identifier
   - **Title**: Clear, descriptive title
   - **Severity**: Critical/High/Medium/Low with justification
   - **CVSS Score**: If applicable
   - **CWE/CVE**: Classification
   - **Affected Systems/Components**: What is vulnerable
   - **Technical Description**:
     * How the vulnerability works
     * Attack vector and complexity
     * Required privileges
     * User interaction needed
   - **Proof of Concept**:
     * Commands/requests used
     * Screenshots or output
     * Step-by-step reproduction
   - **Impact Analysis**:
     * Confidentiality impact
     * Integrity impact
     * Availability impact
     * Scope of compromise
   - **Remediation**:
     * Specific fix recommendations
     * Code examples or configurations
     * Patch information
     * Workarounds if no patch available
   - **Verification**:
     * How to verify the fix
     * Regression testing steps
   - **References**:
     * OWASP guidelines
     * Vendor advisories
     * Security best practices

**4. NETWORK TOPOLOGY & ATTACK SURFACE**:
   - Network diagram (description)
   - Open ports and services
   - Trust boundaries
   - Attack paths identified

**5. COMPLIANCE MAPPING**:
   - Map findings to compliance frameworks:
     * OWASP Top 10
     * CIS Controls
     * NIST CSF
     * PCI-DSS (if applicable)
     * ISO 27001 (if applicable)

**6. RISK ANALYSIS**:
   - Risk matrix (likelihood × impact)
   - Exploitability assessment
   - Business context for each risk

**7. REMEDIATION ROADMAP**:
   - **Phase 1 (Immediate - 0-30 days)**: Critical fixes
   - **Phase 2 (Short-term - 30-90 days)**: High priority
   - **Phase 3 (Medium-term - 90-180 days)**: Medium priority
   - **Phase 4 (Long-term - 180+ days)**: Low priority & improvements

**8. APPENDICES**:
   - A: Vulnerability details (raw data)
   - B: Tool output (scan logs)
   - C: Affected systems inventory
   - D: Glossary of terms
   - E: References and resources

**TECHNICAL DEPTH**:
- Include commands, code snippets, and technical details
- Provide sufficient detail for engineers to reproduce and fix
- Use industry-standard terminology
- Include packet captures, logs, or screenshots where relevant
- Reference CVEs, CWEs, and security standards

**FORMAT**:
- Use clear headings and subheadings
- Include tables for structured data
- Use code blocks for technical content
- Add severity indicators (color coding suggestions)
- Include timestamps and metadata

This report will be used by security engineers, developers, and system administrators for remediation."""

        return prompt
