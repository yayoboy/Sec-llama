"""
Code Security Tools for MCP Server

Exposes SAST, dependency checking, and code review tools
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.types as types

from modules.vuln_scanner.code_scanner import CodeScanner


def register(server: Server):
    """Register code security tools"""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available code security tools"""
        return [
            Tool(
                name="code_scan",
                description="Perform static application security testing (SAST) on code. Analyzes source code for security vulnerabilities including SQL injection, XSS, hardcoded secrets, insecure configurations, and OWASP Top 10 issues. Supports Python, JavaScript, Java, Go, and PHP.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to code file or directory to scan"
                        },
                        "language": {
                            "type": "string",
                            "enum": ["python", "javascript", "java", "go", "php", "auto"],
                            "default": "auto",
                            "description": "Programming language (auto-detect if not specified)"
                        },
                        "severity_filter": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
                            },
                            "default": ["MEDIUM", "HIGH", "CRITICAL"],
                            "description": "Filter results by severity levels"
                        },
                        "include_ai_analysis": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include AI-powered vulnerability analysis and remediation suggestions"
                        }
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="code_dependency_check",
                description="Check project dependencies for known vulnerabilities (CVEs). Scans package.json, requirements.txt, pom.xml, go.mod, and other dependency files to identify vulnerable libraries and suggests updates.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Path to project root directory"
                        },
                        "ecosystem": {
                            "type": "string",
                            "enum": ["npm", "pip", "maven", "go", "auto"],
                            "default": "auto",
                            "description": "Package ecosystem (auto-detect if not specified)"
                        }
                    },
                    "required": ["project_path"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool execution"""

        if name == "code_scan":
            return await _code_scan(arguments)
        elif name == "code_dependency_check":
            return await _code_dependency_check(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")


async def _code_scan(args: dict) -> list[TextContent]:
    """Execute code security scan"""
    try:
        path = args["path"]
        language = args.get("language", "auto")
        severity_filter = args.get("severity_filter", ["MEDIUM", "HIGH", "CRITICAL"])
        ai_analysis = args.get("include_ai_analysis", True)

        scanner = CodeScanner()
        results = scanner.scan(
            path=path,
            language=language,
            ai_analysis=ai_analysis
        )

        # Filter by severity
        filtered_issues = [
            issue for issue in results.issues
            if issue.severity in severity_filter
        ]

        # Format output
        output = f"# Code Security Scan Results\n\n"
        output += f"**Path:** {path}\n"
        output += f"**Language:** {language}\n"
        output += f"**Total Issues:** {len(filtered_issues)}\n\n"

        # Group by severity
        by_severity = {}
        for issue in filtered_issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)

        # Display by severity (CRITICAL first)
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity in by_severity:
                issues = by_severity[severity]
                output += f"## {severity} Severity ({len(issues)} issues)\n\n"

                for i, issue in enumerate(issues[:10], 1):  # Show first 10 per severity
                    output += f"### {i}. {issue.title}\n\n"
                    output += f"- **File:** {issue.file_path}:{issue.line_number}\n"
                    output += f"- **Type:** {issue.vulnerability_type}\n"
                    output += f"- **CWE:** {issue.cwe_id}\n\n"

                    if issue.description:
                        output += f"**Description:**\n{issue.description}\n\n"

                    if issue.code_snippet:
                        output += f"**Code:**\n```{language}\n{issue.code_snippet}\n```\n\n"

                    if issue.remediation and ai_analysis:
                        output += f"**Remediation:**\n{issue.remediation}\n\n"

                if len(issues) > 10:
                    output += f"*...and {len(issues) - 10} more {severity} issues*\n\n"

        # AI Summary
        if ai_analysis and hasattr(results, 'ai_summary'):
            output += f"## AI Security Analysis\n\n{results.ai_summary}\n\n"

        # Summary statistics
        output += "## Summary\n\n"
        for severity, issues in by_severity.items():
            output += f"- **{severity}:** {len(issues)}\n"

        # JSON export
        result_dict = {
            "path": path,
            "language": language,
            "total_issues": len(filtered_issues),
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "issues": [
                {
                    "severity": i.severity,
                    "title": i.title,
                    "file": i.file_path,
                    "line": i.line_number,
                    "type": i.vulnerability_type,
                    "cwe": i.cwe_id
                }
                for i in filtered_issues[:20]  # First 20 for JSON
            ]
        }

        output += f"\n```json\n{json.dumps(result_dict, indent=2)}\n```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"Code scan failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]


async def _code_dependency_check(args: dict) -> list[TextContent]:
    """Execute dependency vulnerability check"""
    try:
        project_path = args["project_path"]
        ecosystem = args.get("ecosystem", "auto")

        # Note: This would integrate with safety, npm audit, etc.
        # For now, return a structured response

        output = f"# Dependency Vulnerability Check\n\n"
        output += f"**Project:** {project_path}\n"
        output += f"**Ecosystem:** {ecosystem}\n\n"

        output += "## Scanning for vulnerable dependencies...\n\n"

        # This is a placeholder - actual implementation would use:
        # - safety check (Python)
        # - npm audit (JavaScript)
        # - OWASP Dependency Check (Java)
        # - go list (Go)

        output += "⚠️ **Feature coming soon!**\n\n"
        output += "This will check:\n"
        output += "- Python: requirements.txt, Pipfile\n"
        output += "- Node.js: package.json, package-lock.json\n"
        output += "- Java: pom.xml, build.gradle\n"
        output += "- Go: go.mod\n\n"

        output += "For now, use:\n"
        output += "```bash\n"
        if ecosystem == "pip" or ecosystem == "auto":
            output += "# Python\nsafety check\n\n"
        if ecosystem == "npm" or ecosystem == "auto":
            output += "# Node.js\nnpm audit\n\n"
        output += "```\n"

        return [TextContent(type="text", text=output)]

    except Exception as e:
        error_msg = f"Dependency check failed: {str(e)}"
        return [TextContent(type="text", text=f"❌ **Error:** {error_msg}")]
