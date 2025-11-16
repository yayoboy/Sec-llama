# AI & Machine Learning

AI, LLM integration, and model training for Sec-Llama.

## 📁 Structure

```
ai/
├── llm/              # LLM interface and configuration
├── prompts/          # Prompt templates for security analysis
└── training/         # Model training and fine-tuning
```

## 🤖 LLM Integration (`llm/`)

Local and remote LLM integration.

**Files:**
- `llm_interface.py` - LLM abstraction layer
- `config.py` - LLM configuration
- `__init__.py` - Module initialization

**Supported Backends:**
- **Ollama** (local LLM)
- OpenAI API
- Anthropic Claude
- Cohere
- Custom endpoints

**Usage:**
```python
from ai.llm import LLMInterface

llm = LLMInterface()
response = await llm.analyze(
    "Analyze this vulnerability scan result...",
    context={"scan_data": results}
)
```

## 📝 Prompt Templates (`prompts/`)

Security-specific prompt templates.

**Templates:**
- Network analysis prompts
- Code review prompts
- Vulnerability assessment prompts
- Threat intelligence prompts
- Incident response prompts

**Usage:**
```python
from ai.prompts import PromptTemplates

templates = PromptTemplates()
prompt = templates.code_review(
    code=source_code,
    language="python",
    focus="security"
)
```

## 🎓 Training (`training/`)

Model fine-tuning for security-specific tasks.

**Features:**
- **Dataset Management**: CVE, exploit, and security report datasets
- **Fine-tuning**: LoRA/QLoRA support
- **Model Optimization**: Quantization and optimization
- **Evaluation**: Security-specific benchmarks

**Components:**
- `dataset_manager.py` - Dataset collection and preparation
- `model_trainer.py` - Model training workflows
- `evaluator.py` - Model evaluation

**Datasets:**
- CVE descriptions (NVD API)
- Security advisories
- Exploit databases
- MITRE ATT&CK data
- Custom security Q&A

### Training Workflow

1. **Collect Data**:
```bash
python -m ai.training.dataset_manager --source nvd --limit 10000
```

2. **Prepare Dataset**:
```bash
python -m ai.training.dataset_manager --prepare --format alpaca
```

3. **Train Model**:
```bash
python -m ai.training.model_trainer \
  --base-model llama3.1:8b \
  --dataset datasets/security_qa.json \
  --method lora
```

4. **Evaluate**:
```bash
python -m ai.training.evaluator --model fine-tuned-model
```

## 🔧 Configuration

### Configure Ollama (Local)

**Via Web UI**: http://localhost:8080/ai-config
- Set host: `http://localhost:11434`
- Test connection
- Pull models
- Configure defaults

**Via Config File**:
```yaml
# config/mcp_server_config.yaml
ollama:
  host: "http://localhost:11434"
  model: "llama3.1:8b"
  timeout: 120
  temperature: 0.7
  max_tokens: 2048
```

### Configure Remote Ollama

Point to Ollama on another machine:

**Web UI**: http://localhost:8080/ai-config
- Set host: `http://192.168.1.100:11434`
- Test connection
- Save

**On Remote Server**:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Configure for remote access
export OLLAMA_HOST=0.0.0.0:11434

# Start Ollama
ollama serve
```

### Configure External Providers

```yaml
ai_providers:
  - provider_type: openai
    api_key: "sk-..."
    model: "gpt-4"
    enabled: false

  - provider_type: anthropic
    api_key: "sk-ant-..."
    model: "claude-3-opus"
    enabled: false

ai_fallback_enabled: true
```

## 🎯 Use Cases

### Security Code Review
```python
from ai.llm import LLMInterface
from ai.prompts import PromptTemplates

llm = LLMInterface()
templates = PromptTemplates()

prompt = templates.code_review(code=source, language="python")
analysis = await llm.analyze(prompt)
```

### Vulnerability Analysis
```python
vuln_prompt = templates.vulnerability_analysis(
    scan_results=results,
    severity_threshold="high"
)
assessment = await llm.analyze(vuln_prompt)
```

### Threat Intelligence
```python
threat_prompt = templates.threat_analysis(
    indicators=iocs,
    context="APT28 activity"
)
intel = await llm.analyze(threat_prompt)
```

## 📊 Model Management

### Available Models

**Recommended for Security:**
- `llama3.1:8b` - General purpose, good balance
- `codellama:13b` - Code analysis
- `mixtral:8x7b` - Advanced reasoning
- `phi-3:mini` - Fast, lightweight

**Via Web UI**: http://localhost:8080/ai-config
- View installed models
- Pull new models
- Delete unused models
- Test generation

**Via CLI**:
```bash
# List models
curl http://localhost:11434/api/tags

# Pull model
curl http://localhost:11434/api/pull -d '{"name":"llama3.1:8b"}'

# Delete model
curl -X DELETE http://localhost:11434/api/delete -d '{"name":"model:tag"}'
```

## 📚 Documentation

- [LLM Integration Guide](../docs/LLM_INTEGRATION.md)
- [Training Guide](../docs/TRAINING.md)
- [Prompt Engineering](../docs/PROMPT_ENGINEERING.md)

---

**Quick Start:**
```python
from ai.llm import LLMInterface

llm = LLMInterface()
result = await llm.analyze("Analyze this security issue...")
```
