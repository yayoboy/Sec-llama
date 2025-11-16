# Sec-Llama - Task Completion Checklist

## When a Development Task is Completed

### 1. Code Quality Checks
Since no formal linting configuration exists yet, run these manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Security scanning (REQUIRED for security project)
bandit -r modules/ cli/ web_ui/ 2>&1 | grep -E "(Issue|CRITICAL|HIGH)"

# Dependency vulnerability check
safety check

# Basic syntax check
python -m py_compile path/to/your/file.py
```

### 2. Testing
**Note**: No tests currently exist in the repository.

When tests are added:
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=modules --cov=cli --cov=web_ui

# Ensure coverage is adequate (aim for >70%)
pytest --cov=modules --cov-report=term-missing
```

**TODO for the project**: 
- Create test files in `tests/` directory
- Add unit tests for modules
- Add integration tests for CLI/Web UI
- Configure pytest.ini or pyproject.toml

### 3. Documentation
Ensure documentation is updated:

- [ ] Update relevant README.md if adding new features
- [ ] Update docstrings for new/modified functions
- [ ] Update `docs/` if adding major features
- [ ] Update configuration examples if adding new config options
- [ ] Add usage examples for new CLI commands

### 4. Configuration Files
If adding new features that require configuration:

- [ ] Update `config/config.example.yaml` with new settings
- [ ] Update `.env.example` if adding environment variables
- [ ] Document new configuration in README.md

### 5. Dependencies
If adding new dependencies:

```bash
# Update requirements file
pip freeze > requirements.txt

# or manually add to requirements.txt with version
echo "new-package>=1.0.0" >> requirements.txt

# Update requirements-full.txt if it's a Web UI dependency
```

- [ ] Add dependency with version constraint
- [ ] Update Docker requirements if applicable
- [ ] Document why the dependency is needed

### 6. Security Considerations
For a security tool, extra care is needed:

- [ ] Review code for security vulnerabilities
- [ ] Ensure no hardcoded credentials or API keys
- [ ] Check that sensitive data isn't logged
- [ ] Verify proper input validation
- [ ] Ensure error messages don't leak sensitive info
- [ ] Review for command injection vulnerabilities
- [ ] Check file path handling for path traversal issues

### 7. Git Commit
```bash
# Check status
git status

# Review changes
git diff

# Stage changes
git add path/to/files

# Commit with descriptive message
git commit -m "feat: Add CVE lookup functionality

- Implement CVE database lookup via NVD API
- Add AI-powered CVE analysis
- Include CVSS score extraction
- Add tests for CVE lookup

Fixes #123"

# Push changes
git push origin branch-name
```

**Commit Message Convention** (inferred, not formally defined):
- Use descriptive messages
- Include what was changed and why
- Reference issue numbers if applicable

### 8. Docker (if applicable)
If changes affect Docker deployments:

```bash
# Test Docker build
docker build -t sec-llama-test .

# Test Docker Compose
docker-compose up -d
docker-compose logs -f

# Verify services are running
curl http://localhost:8080/health  # Web UI
curl http://localhost:8765/health  # MCP HTTP

# Clean up test
docker-compose down
```

### 9. Manual Testing
Before considering task complete:

- [ ] Test the feature manually
- [ ] Test in CLI mode (if applicable)
- [ ] Test in Web UI mode (if applicable)
- [ ] Test with Docker deployment (if applicable)
- [ ] Verify Ollama integration works
- [ ] Check logs for errors
- [ ] Test error handling (invalid inputs, network failures, etc.)

### 10. Performance Check
For security tools, performance matters:

- [ ] Check if operations complete in reasonable time
- [ ] Verify memory usage is acceptable
- [ ] Ensure no resource leaks (connections, files, etc.)
- [ ] Check for unnecessary API calls
- [ ] Verify proper use of async/await if applicable

## Implementation-Specific Checks

### For Standalone Implementation
- [ ] Test `./sec-llama.sh` CLI commands
- [ ] Test `./start.sh` menu options
- [ ] Verify both CLI and Web UI modes work

### For MCP Implementations
- [ ] Test MCP server starts correctly
- [ ] Verify tools are exposed properly
- [ ] Test authentication (for MCP HTTP)
- [ ] Check client integration (Claude Desktop for stdio)

### For Web UI Implementations
- [ ] Test frontend build: `cd web_ui/frontend && npm run build`
- [ ] Verify API endpoints work
- [ ] Check WebSocket connections (if used)
- [ ] Test authentication/API keys
- [ ] Verify database migrations (if applicable)

### For Docker Production
- [ ] Test stack deployment
- [ ] Verify health checks work
- [ ] Test auto-scaling (if configured)
- [ ] Check secrets management
- [ ] Verify backup scripts work

## Known Issues / TODOs
Based on codebase analysis:

1. **Missing `core` module**: Code imports `core.config`, `core.llm_interface`, `core.prompt_templates` but this module doesn't exist yet
2. **No tests**: pytest is listed in requirements but no test files exist
3. **No linting config**: No .pylintrc, .flake8, or black configuration
4. **No pre-commit hooks**: Consider adding for automatic checks
5. **No CI/CD**: Consider adding GitHub Actions or similar

## Final Checklist
Before marking a task as complete:

- [ ] Code quality checks passed
- [ ] Tests written and passing (when test framework is set up)
- [ ] Documentation updated
- [ ] Security reviewed
- [ ] Manual testing completed
- [ ] Git commit with good message
- [ ] Changes pushed to repository
- [ ] No errors in logs
- [ ] Ready for review (if working in a team)