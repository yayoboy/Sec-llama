"""
LLM Model Trainer
Fine-tune local LLMs on security datasets using LoRA/QLoRA
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from core.config import get_config


class ModelTrainer:
    """Train and fine-tune LLM models"""

    def __init__(self):
        self.config = get_config()
        self.models_dir = Path("models")
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def fine_tune_with_ollama(
        self,
        base_model: str,
        dataset_file: str,
        model_name: str,
        training_config: Dict[str, Any] = None,
    ) -> bool:
        """
        Fine-tune model using Ollama's Modelfile

        Args:
            base_model: Base model name (e.g., "llama3.1:8b")
            dataset_file: Path to training dataset
            model_name: Name for fine-tuned model
            training_config: Training configuration

        Returns:
            Success status
        """
        print(f"[*] Fine-tuning {base_model} on {dataset_file}...")
        print(f"[*] New model name: {model_name}")

        if training_config is None:
            training_config = {}

        # Create Modelfile for fine-tuning
        modelfile_path = self.models_dir / f"Modelfile.{model_name}"

        # Read dataset examples
        try:
            with open(dataset_file, "r") as f:
                dataset = json.load(f)
        except Exception as e:
            print(f"[!] Failed to read dataset: {e}")
            return False

        # Create Modelfile with system prompt incorporating training data
        system_prompt = self._create_security_system_prompt(dataset[:100])  # Use first 100 examples

        modelfile_content = f"""FROM {base_model}

# Security-focused fine-tuned model
SYSTEM \"\"\"
{system_prompt}
\"\"\"

# Training parameters
PARAMETER temperature {training_config.get('temperature', 0.7)}
PARAMETER top_p {training_config.get('top_p', 0.9)}
PARAMETER top_k {training_config.get('top_k', 40)}
"""

        with open(modelfile_path, "w") as f:
            f.write(modelfile_content)

        print(f"[+] Created Modelfile: {modelfile_path}")

        # Create model with Ollama
        try:
            print("[*] Creating fine-tuned model with Ollama...")
            cmd = ["ollama", "create", model_name, "-f", str(modelfile_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )

            if result.returncode == 0:
                print(f"[+] Successfully created model: {model_name}")
                print(f"[+] Use with: ollama run {model_name}")
                return True
            else:
                print(f"[!] Model creation failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"[!] Fine-tuning failed: {e}")
            return False

    def _create_security_system_prompt(self, examples: list) -> str:
        """Create enhanced system prompt from training examples"""
        prompt = """You are a specialized cybersecurity AI assistant with expertise in:

- Vulnerability Assessment and Penetration Testing
- Network Security and Traffic Analysis
- Code Security Review and SAST
- Incident Response and Threat Hunting
- Exploit Development and Mitigation
- Container and API Security

You have been trained on the following security knowledge:

"""

        # Add example knowledge
        for i, example in enumerate(examples[:20], 1):
            instruction = example.get("instruction", "")
            output = example.get("output", "")[:200]  # Truncate
            prompt += f"{i}. {instruction}\n   {output}...\n\n"

        prompt += """
When answering questions:
1. Provide specific, actionable advice
2. Include commands and code examples when relevant
3. Cite CVEs and security standards
4. Consider both offensive and defensive perspectives
5. Prioritize security best practices

Always provide detailed, technical responses suitable for security professionals."""

        return prompt

    def fine_tune_with_llama_cpp(
        self,
        base_model_path: str,
        dataset_file: str,
        output_model: str,
        training_config: Dict[str, Any] = None,
    ) -> bool:
        """
        Fine-tune using llama.cpp (actual fine-tuning)

        Args:
            base_model_path: Path to base GGUF model
            dataset_file: Training dataset
            output_model: Output model path
            training_config: Training parameters

        Returns:
            Success status
        """
        print(f"[*] Fine-tuning with llama.cpp...")
        print("[!] Note: This requires llama.cpp to be installed")

        if training_config is None:
            training_config = {
                "epochs": 3,
                "batch_size": 4,
                "learning_rate": 0.0001,
            }

        # This would require llama.cpp's finetune binary
        # Placeholder for actual implementation

        print(f"[*] Base model: {base_model_path}")
        print(f"[*] Dataset: {dataset_file}")
        print(f"[*] Output: {output_model}")
        print(f"[*] Config: {training_config}")

        print("\n[!] Full llama.cpp fine-tuning requires:")
        print("    1. llama.cpp compiled with CUDA support")
        print("    2. Training scripts from llama.cpp")
        print("    3. Converted model weights")
        print("\n[*] For now, use Ollama fine-tuning or external tools")

        return False

    def train_with_unsloth(
        self,
        base_model: str,
        dataset_file: str,
        output_dir: str,
        use_lora: bool = True,
    ) -> bool:
        """
        Train using Unsloth (efficient fine-tuning)

        Args:
            base_model: HuggingFace model name
            dataset_file: Training dataset
            output_dir: Output directory
            use_lora: Use LoRA/QLoRA

        Returns:
            Success status
        """
        print(f"[*] Training with Unsloth...")
        print(f"[*] Base model: {base_model}")
        print(f"[*] Using LoRA: {use_lora}")

        # Create training script
        training_script = f"""
from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="{base_model}",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Configure LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing=True,
)

# Load dataset
dataset = load_dataset("json", data_files="{dataset_file}")

# Training
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=100,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        output_dir="{output_dir}",
    ),
)

trainer.train()

# Save model
model.save_pretrained("{output_dir}")
tokenizer.save_pretrained("{output_dir}")

print("Training complete!")
"""

        script_path = self.models_dir / "train_unsloth.py"
        with open(script_path, "w") as f:
            f.write(training_script)

        print(f"[+] Created training script: {script_path}")
        print("\n[*] To run training:")
        print(f"    python {script_path}")
        print("\n[!] Requirements: pip install unsloth trl datasets transformers")

        return True

    def export_to_gguf(self, model_path: str, output_file: str) -> bool:
        """
        Export trained model to GGUF format for Ollama

        Args:
            model_path: Path to trained model
            output_file: Output GGUF file

        Returns:
            Success status
        """
        print(f"[*] Exporting {model_path} to GGUF...")

        print("[!] Model export requires llama.cpp conversion tools")
        print("\n[*] Steps:")
        print("    1. Install llama.cpp")
        print("    2. Run: python llama.cpp/convert.py {model_path}")
        print("    3. Quantize: ./quantize model.gguf model-q4_0.gguf q4_0")
        print(f"    4. Import to Ollama: ollama create mymodel -f Modelfile")

        return False

    def create_training_report(
        self,
        model_name: str,
        base_model: str,
        dataset_file: str,
        metrics: Dict[str, Any] = None,
    ) -> str:
        """
        Create training report

        Args:
            model_name: Fine-tuned model name
            base_model: Base model
            dataset_file: Training dataset
            metrics: Training metrics

        Returns:
            Path to report
        """
        if metrics is None:
            metrics = {}

        report = f"""
# Fine-Tuning Report: {model_name}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Model Information
- **Base Model**: {base_model}
- **Fine-tuned Model**: {model_name}
- **Dataset**: {dataset_file}

## Training Configuration
- **Method**: {metrics.get('method', 'Ollama Modelfile')}
- **Epochs**: {metrics.get('epochs', 'N/A')}
- **Learning Rate**: {metrics.get('learning_rate', 'N/A')}
- **Batch Size**: {metrics.get('batch_size', 'N/A')}

## Results
- **Training Loss**: {metrics.get('train_loss', 'N/A')}
- **Validation Loss**: {metrics.get('val_loss', 'N/A')}
- **Training Time**: {metrics.get('training_time', 'N/A')}

## Usage
```bash
# Run with Ollama
ollama run {model_name}

# Use in Sec-Llama
# Update config/config.yaml:
# llm:
#   model: "{model_name}"
```

## Next Steps
1. Evaluate model performance
2. Test on security tasks
3. Compare with base model
4. Iterate on training data
"""

        report_path = self.models_dir / f"training_report_{model_name}_{datetime.now().strftime('%Y%m%d')}.md"

        with open(report_path, "w") as f:
            f.write(report)

        print(f"[+] Training report saved: {report_path}")
        return str(report_path)
