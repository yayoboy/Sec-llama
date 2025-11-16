# Sec-Llama - Code Style & Conventions

## Python Code Style

### General Guidelines
Based on observed code in the repository:

1. **Type Hints**: Use type hints for function parameters and return values
   ```python
   def lookup_cve(self, cve_id: str) -> Dict[str, Any]:
   ```

2. **Docstrings**: Use Google-style docstrings for classes and functions
   ```python
   """
   Lookup CVE information

   Args:
       cve_id: CVE ID (e.g., CVE-2024-1234)

   Returns:
       CVE information dictionary
   """
   ```

3. **Import Organization**: Organize imports in this order:
   - Standard library imports
   - Third-party imports
   - Local/project imports
   ```python
   import requests
   import json
   from typing import Dict, Any, Optional
   from datetime import datetime

   from core.config import get_config
   from core.llm_interface import get_llm
   ```

4. **Class-based Modules**: Security modules use class-based design
   ```python
   class CVELookup:
       """CVE database lookup and analysis"""
       
       def __init__(self):
           self.config = get_config()
           self.llm = get_llm()
   ```

5. **Private Methods**: Use single underscore prefix for internal methods
   ```python
   def _extract_cvss(self, cve_item: Dict) -> Dict[str, Any]:
       """Extract CVSS score"""
   ```

### User Feedback Convention
Use consistent prefixes for print statements:
- `[*]` - Info/progress messages: `print(f"[*] Looking up {cve_id}...")`
- `[+]` - Success messages: `print(f"[+] Found {len(cves)} CVEs")`
- `[!]` - Error/warning messages: `print(f"[!] API request failed: {e}")`

### Exception Handling
- Use specific exception types
- Provide clear error messages
- Handle both specific and general exceptions
```python
try:
    # operation
except requests.RequestException as e:
    print(f"[!] API request failed: {e}")
    return {}
except Exception as e:
    print(f"[!] CVE lookup failed: {e}")
    return {}
```

### Configuration
- Configuration stored in YAML files (`config/config.example.yaml`)
- Settings organized by category (llm, network, scanning, etc.)
- Use sensible defaults

## File Naming
- Python modules: lowercase with underscores (`cve_lookup.py`, `port_scanner.py`)
- Classes: PascalCase (`CVELookup`, `PortScanner`)
- Functions/methods: snake_case (`lookup_cve`, `scan_ports`)

## Directory Structure
- `modules/` - Security functionality organized by domain
- `__init__.py` - Present in all package directories
- Module-specific subdirectories (e.g., `network/scanning/`, `network/discovery/`)

## Linting & Formatting
**Note**: No formal linting/formatting configuration found yet in the repository.

Recommended tools (listed in requirements.txt but not configured):
- **pylint** (>=3.0.0) - Available but no .pylintrc
- **bandit** (>=1.7.5) - Security linting
- **semgrep** (>=1.45.0) - Static analysis

**TODO**: Consider adding:
- `.pylintrc` or `pyproject.toml` for pylint configuration
- `.flake8` for flake8 configuration
- `black` for code formatting
- `isort` for import sorting
- Pre-commit hooks

## Shell Scripts
- Use `#!/bin/bash` shebang
- Set strict mode: `set -e` (exit on error)
- Use colors for output (GREEN, BLUE, YELLOW, NC)
- Portable path handling:
  ```bash
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "$SCRIPT_DIR"
  ```

## Documentation
- Each implementation has its own README.md
- Main README.md provides overview and navigation
- Docs in `docs/` for specific topics
- Use markdown for all documentation
- Include code examples in documentation

## Security Best Practices
Based on config file (`config.example.yaml`):
- Require confirmation for dangerous operations: `require_confirmation: true`
- Log all operations: `log_all_operations: true`
- Define authorized networks
- Never commit API keys or secrets (use `.env` files)
- Include `.dockerignore` for container builds