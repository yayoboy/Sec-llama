# 🎓 LLM Training & Fine-Tuning Guide

## Overview

Sec-Llama Suite includes comprehensive tools for **training and fine-tuning local LLMs** on security-specific datasets. This allows you to create specialized models with deep knowledge of cybersecurity.

---

## 🎯 Why Fine-Tune?

### **Benefits:**
- 🎯 **Specialized Knowledge**: Better understanding of security concepts
- 🚀 **Improved Accuracy**: More accurate vulnerability analysis
- 💡 **Domain Expertise**: Deep knowledge of CVEs, exploits, and tactics
- 🔒 **Privacy**: Train on your own proprietary security data
- ⚡ **Performance**: Faster, more relevant responses

---

## 📚 Dataset Collection

### **Collect CVE Dataset**

Automatically collect and format CVE data from NVD:

```bash
# Collect 10,000 CVEs
sec-llama train collect-dataset --type cve --max-items 10000

# Output: database/datasets/cve_dataset_20241110.json
```

**Dataset Format:**
```json
[
  {
    "instruction": "Analyze CVE-2021-44228 and provide security assessment",
    "input": "CVE ID: CVE-2021-44228\nDescription: Apache Log4j2 ...",
    "output": "This vulnerability has a CVSS score of 10.0 (CRITICAL). ..."
  }
]
```

### **Collect Exploit Dataset**

```bash
sec-llama train collect-dataset --type exploit
```

### **Security Q&A Dataset**

Pre-built Q&A pairs for security concepts:

```bash
sec-llama train collect-dataset --type qa
```

### **Collect All Datasets**

```bash
sec-llama train collect-dataset --type all --max-items 5000
```

---

## 🔧 Prepare Training Data

### **Merge Multiple Datasets**

```bash
# Prepare data in Alpaca format
sec-llama train prepare-data \
  --datasets "cve_dataset.json,exploit_dataset.json,security_qa.json" \
  --format alpaca

# Output: database/datasets/training_data_alpaca_20241110.json
```

### **Supported Formats:**

**Alpaca Format:**
```json
{
  "instruction": "Task description",
  "input": "Additional context",
  "output": "Expected response"
}
```

**ShareGPT Format:**
```json
{
  "conversations": [
    {"from": "human", "value": "Question"},
    {"from": "gpt", "value": "Answer"}
  ]
}
```

### **Validate Dataset**

```bash
sec-llama train validate --dataset training_data.json
```

---

## 🚀 Fine-Tuning Methods

### **Method 1: Ollama Modelfile (Recommended)**

**Easiest method** - Uses Ollama's Modelfile with enhanced system prompts:

```bash
sec-llama train fine-tune \
  --base-model llama3.1:8b \
  --dataset database/datasets/training_data.json \
  --name sec-llama-8b

# Use the fine-tuned model
ollama run sec-llama-8b

# Or update config
nano config/config.yaml
# Change: llm.model = "sec-llama-8b"
```

**How it works:**
1. Reads training examples
2. Creates enhanced system prompt with security knowledge
3. Creates new Ollama model with optimized parameters
4. Ready to use immediately!

### **Method 2: Unsloth (LoRA/QLoRA)**

**Most efficient** - Uses LoRA for parameter-efficient fine-tuning:

```bash
# Generate training script
sec-llama train fine-tune \
  --base-model meta-llama/Llama-2-7b-hf \
  --dataset training_data.json \
  --name sec-llama-7b \
  --method unsloth

# Install requirements
pip install unsloth trl datasets transformers

# Run generated script
python models/train_unsloth.py
```

**Advantages:**
- 💾 Memory efficient (trains on single GPU)
- ⚡ 2-5x faster than standard fine-tuning
- 🎯 Only trains ~1% of parameters
- 💰 Lower cost

**Training Configuration:**
```python
{
  "r": 16,                    # LoRA rank
  "lora_alpha": 16,           # LoRA alpha
  "lora_dropout": 0,          # Dropout
  "target_modules": [         # Modules to train
    "q_proj", "k_proj",
    "v_proj", "o_proj"
  ],
  "learning_rate": 2e-4,
  "max_steps": 100,
  "batch_size": 2,
}
```

### **Method 3: llama.cpp**

**Full fine-tuning** - Maximum customization:

```bash
# Requires llama.cpp compiled with CUDA
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make LLAMA_CUBLAS=1

# Fine-tune
./finetune \
  --model-base models/llama-2-7b.gguf \
  --train-data training_data.txt \
  --output models/sec-llama-7b.gguf \
  --epochs 3
```

---

## 📊 Model Evaluation

### **Benchmark on Security Tasks**

```bash
sec-llama train evaluate --model sec-llama-8b
```

**Output:**
```
EVALUATION SUMMARY
=================================================================
Model: sec-llama-8b
Total Questions: 8
Correct Answers: 7
Accuracy: 87.50%
Avg Response Time: 1.23s
=================================================================
```

### **Compare Models**

```bash
sec-llama train compare --models "llama3.1:8b,sec-llama-8b,codellama:7b"
```

**Output:**
```
MODEL COMPARISON
=================================================================
Model                          Accuracy       Avg Time
-----------------------------------------------------------------
llama3.1:8b                    75.00%        1.45s
sec-llama-8b                   87.50%        1.23s
codellama:7b                   62.50%        1.67s
=================================================================
```

### **Test Specific Capabilities**

```python
from modules.training.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator()

# Test vulnerability analysis
results = evaluator.test_specific_capabilities(
    model_name="sec-llama-8b",
    capability="vuln_analysis"
)

# Test exploit development
results = evaluator.test_specific_capabilities(
    model_name="sec-llama-8b",
    capability="exploit_dev"
)
```

---

## 🎨 Custom Datasets

### **Create Custom Dataset**

```python
from modules.training.dataset_manager import DatasetManager

manager = DatasetManager()

examples = [
    {
        "instruction": "Analyze this code for vulnerabilities",
        "input": "def login(username, password):\n    query = f\"SELECT * FROM users WHERE user='{username}' AND pass='{password}'\"",
        "output": "This code is vulnerable to SQL injection. The f-string directly interpolates user input into the SQL query. Fix: Use parameterized queries."
    },
    {
        "instruction": "Explain this CVE",
        "input": "CVE-2021-44228 (Log4Shell)",
        "output": "Critical RCE vulnerability in Apache Log4j 2. Allows unauthenticated remote code execution via JNDI lookup. CVSS 10.0. Patch immediately to 2.17.1+."
    }
]

dataset_file = manager.create_custom_dataset(examples, name="my_security_data")
```

### **Add Proprietary Data**

```python
# Your internal vulnerability data
internal_vulns = [
    {
        "instruction": "Analyze internal vulnerability #1234",
        "input": "SQL injection in payment module",
        "output": "Critical vulnerability allowing unauthorized access to payment data. Fix: Implement parameterized queries in payment_process.py line 156."
    }
]

manager.create_custom_dataset(internal_vulns, name="internal_vulns")
```

---

## 📈 Training Best Practices

### **1. Dataset Quality**

✅ **DO:**
- Use diverse examples (CVEs, exploits, code analysis, Q&A)
- Include both vulnerable and secure code examples
- Balance severity levels (CRITICAL, HIGH, MEDIUM, LOW)
- Provide detailed, accurate outputs

❌ **DON'T:**
- Use duplicate examples
- Include outdated information
- Mix multiple topics in one example
- Use vague or generic responses

### **2. Dataset Size**

| Model Size | Recommended Examples | Training Time |
|------------|---------------------|---------------|
| 7B         | 1,000 - 5,000       | 1-3 hours     |
| 13B        | 3,000 - 10,000      | 3-8 hours     |
| 70B        | 10,000 - 50,000     | 12-48 hours   |

### **3. Iteration**

```bash
# Version 1: Basic dataset
sec-llama train fine-tune --base-model llama3.1:8b \
  --dataset basic_dataset.json --name sec-llama-v1

# Evaluate
sec-llama train evaluate --model sec-llama-v1

# Version 2: Enhanced dataset
sec-llama train fine-tune --base-model llama3.1:8b \
  --dataset enhanced_dataset.json --name sec-llama-v2

# Compare
sec-llama train compare --models "sec-llama-v1,sec-llama-v2"
```

### **4. Specialization**

Create domain-specific models:

```bash
# Web security specialist
sec-llama train fine-tune --dataset web_security.json --name sec-llama-web

# Network security specialist
sec-llama train fine-tune --dataset network_security.json --name sec-llama-network

# Malware analysis specialist
sec-llama train fine-tune --dataset malware_analysis.json --name sec-llama-malware
```

---

## 🔬 Advanced Techniques

### **Progressive Training**

```bash
# Stage 1: General security knowledge
sec-llama train fine-tune --base-model llama3.1:8b \
  --dataset general_security.json --name sec-llama-stage1

# Stage 2: Specialized knowledge
sec-llama train fine-tune --base-model sec-llama-stage1 \
  --dataset specialized_vulns.json --name sec-llama-stage2
```

### **Multi-Task Training**

```python
# Combine multiple security tasks
datasets = [
    "cve_analysis.json",
    "exploit_development.json",
    "code_review.json",
    "incident_response.json",
    "threat_intel.json",
]

manager.prepare_training_data(datasets, format="alpaca")
```

### **Continuous Learning**

```bash
# Week 1: Initial training
sec-llama train fine-tune --dataset week1_data.json --name sec-llama-w1

# Week 2: Add new data
sec-llama train fine-tune --base-model sec-llama-w1 \
  --dataset week2_data.json --name sec-llama-w2

# Keep improving...
```

---

## 🎯 Example Workflows

### **Workflow 1: CVE Expert Model**

```bash
# 1. Collect CVE data
sec-llama train collect-dataset --type cve --max-items 50000

# 2. Prepare for training
sec-llama train prepare-data \
  --datasets "cve_dataset.json" \
  --format alpaca

# 3. Fine-tune
sec-llama train fine-tune \
  --base-model llama3.1:70b \
  --dataset training_data_alpaca.json \
  --name cve-expert-70b

# 4. Evaluate
sec-llama train evaluate --model cve-expert-70b

# 5. Use for CVE analysis
sec-llama threat cve --id CVE-2024-1234
```

### **Workflow 2: Code Security Model**

```bash
# 1. Create code examples dataset
python create_code_dataset.py

# 2. Validate dataset
sec-llama train validate --dataset code_security.json

# 3. Fine-tune
sec-llama train fine-tune \
  --base-model codellama:13b \
  --dataset code_security.json \
  --name sec-codellama-13b

# 4. Use for code review
sec-llama review file --path app.py
```

---

## 💾 Model Management

### **List Models**

```bash
ollama list
```

### **Delete Model**

```bash
ollama rm sec-llama-old
```

### **Export Model**

```bash
# Export for sharing (GGUF format)
# See model_trainer.py export_to_gguf()
```

### **Switch Models**

Update `config/config.yaml`:
```yaml
llm:
  model: "sec-llama-8b"  # Your fine-tuned model
```

---

## 📊 Performance Tips

### **GPU Memory**

| Model Size | Min VRAM | Recommended | Quantization |
|------------|----------|-------------|--------------|
| 7B         | 6GB      | 8GB         | Q4_0         |
| 13B        | 10GB     | 16GB        | Q4_0         |
| 70B        | 40GB     | 80GB        | Q4_K_M       |

### **Speed Optimization**

```yaml
# config/config.yaml
llm:
  model: "sec-llama-8b"
  temperature: 0.5        # Lower = faster
  max_tokens: 2048        # Limit response length
```

### **Batch Processing**

```python
# Process multiple samples efficiently
from core.llm_interface import get_llm

llm = get_llm()

samples = [...]  # Your data
for sample in samples:
    result = llm.generate(sample)
```

---

## 🔍 Troubleshooting

### **Out of Memory**

```bash
# Use smaller model or quantization
ollama pull llama3.1:8b-q4_0  # 4-bit quantized

# Or reduce batch size
```

### **Poor Performance**

```bash
# More training data
sec-llama train collect-dataset --max-items 100000

# Better base model
sec-llama train fine-tune --base-model llama3.1:70b

# Evaluate and iterate
sec-llama train evaluate --model my-model
```

### **Ollama Issues**

```bash
# Check Ollama is running
ollama list

# Restart Ollama
systemctl restart ollama

# Check logs
journalctl -u ollama -f
```

---

## 📚 Resources

### **Dataset Sources**
- [NVD - National Vulnerability Database](https://nvd.nist.gov/)
- [Exploit-DB](https://www.exploit-db.com/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

### **Training Frameworks**
- [Ollama](https://ollama.com/)
- [Unsloth](https://github.com/unslothai/unsloth)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)

### **Pre-trained Security Models**
- [SecBERT](https://huggingface.co/jackaduma/SecBERT)
- [CyberBERT](https://huggingface.co/jackaduma/CyberBERT)

---

## 🎉 Next Steps

1. ✅ Collect your first dataset
2. ✅ Fine-tune a small model (7B-8B)
3. ✅ Evaluate performance
4. ✅ Iterate and improve
5. ✅ Create specialized models
6. ✅ Share your results!

---

**Happy Training! 🚀**

Create the best security-focused LLM for your needs!
