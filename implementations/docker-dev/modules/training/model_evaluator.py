"""
Model Evaluator
Evaluate and benchmark fine-tuned security models
"""

import time
from typing import Dict, Any, List
from core.llm_interface import get_llm


class ModelEvaluator:
    """Evaluate model performance"""

    def __init__(self):
        self.llm = get_llm()

    def evaluate_on_benchmark(
        self,
        model_name: str,
        benchmark_file: str = None,
    ) -> Dict[str, Any]:
        """
        Evaluate model on security benchmark

        Args:
            model_name: Model to evaluate
            benchmark_file: Path to benchmark questions

        Returns:
            Evaluation results
        """
        print(f"[*] Evaluating model: {model_name}")

        # Security benchmark questions
        benchmark = self._get_security_benchmark()

        results = {
            "model": model_name,
            "total_questions": len(benchmark),
            "correct": 0,
            "avg_response_time": 0,
            "answers": [],
        }

        total_time = 0

        for i, question in enumerate(benchmark, 1):
            print(f"\n[*] Question {i}/{len(benchmark)}")
            print(f"    {question['question'][:60]}...")

            # Generate answer
            start_time = time.time()
            try:
                answer = self.llm.generate(question["question"])
                response_time = time.time() - start_time

                # Simple correctness check (contains expected keywords)
                is_correct = any(
                    keyword.lower() in answer.lower()
                    for keyword in question.get("expected_keywords", [])
                )

                if is_correct:
                    results["correct"] += 1

                results["answers"].append({
                    "question": question["question"],
                    "answer": answer[:200],  # Truncate
                    "correct": is_correct,
                    "response_time": response_time,
                })

                total_time += response_time

            except Exception as e:
                print(f"[!] Error: {e}")
                results["answers"].append({
                    "question": question["question"],
                    "error": str(e),
                })

        # Calculate metrics
        results["accuracy"] = results["correct"] / results["total_questions"]
        results["avg_response_time"] = total_time / results["total_questions"]

        # Print summary
        self._print_evaluation_summary(results)

        return results

    def _get_security_benchmark(self) -> List[Dict[str, Any]]:
        """Get security benchmark questions"""
        return [
            {
                "question": "What is SQL injection and how to prevent it?",
                "expected_keywords": ["sql", "injection", "parameterized", "prepared statements"],
            },
            {
                "question": "Explain Cross-Site Scripting (XSS) vulnerability",
                "expected_keywords": ["xss", "script", "injection", "sanitize", "encode"],
            },
            {
                "question": "What tools are used for network reconnaissance?",
                "expected_keywords": ["nmap", "scan", "reconnaissance"],
            },
            {
                "question": "How to escalate privileges on Linux?",
                "expected_keywords": ["privilege", "escalation", "sudo", "suid"],
            },
            {
                "question": "What is a CSRF attack?",
                "expected_keywords": ["csrf", "cross-site", "token", "forgery"],
            },
            {
                "question": "Explain the OWASP Top 10",
                "expected_keywords": ["owasp", "injection", "broken", "authentication"],
            },
            {
                "question": "How to detect SQL injection in code?",
                "expected_keywords": ["sql", "injection", "input", "validation", "parameterized"],
            },
            {
                "question": "What is a buffer overflow?",
                "expected_keywords": ["buffer", "overflow", "memory", "stack"],
            },
        ]

    def _print_evaluation_summary(self, results: Dict[str, Any]):
        """Print evaluation summary"""
        print("\n" + "=" * 80)
        print("EVALUATION SUMMARY")
        print("=" * 80)

        print(f"\nModel: {results['model']}")
        print(f"Total Questions: {results['total_questions']}")
        print(f"Correct Answers: {results['correct']}")
        print(f"Accuracy: {results['accuracy']:.2%}")
        print(f"Avg Response Time: {results['avg_response_time']:.2f}s")

        print("\n" + "=" * 80 + "\n")

    def compare_models(
        self,
        model_names: List[str],
        benchmark_file: str = None,
    ) -> Dict[str, Any]:
        """
        Compare multiple models

        Args:
            model_names: List of models to compare
            benchmark_file: Benchmark questions

        Returns:
            Comparison results
        """
        print(f"[*] Comparing {len(model_names)} models...")

        results = {}

        for model in model_names:
            print(f"\n{'=' * 80}")
            print(f"Evaluating: {model}")
            print('=' * 80)

            # Would need to switch models - simplified for now
            result = self.evaluate_on_benchmark(model, benchmark_file)
            results[model] = result

        # Print comparison
        self._print_comparison(results)

        return results

    def _print_comparison(self, results: Dict[str, Dict]):
        """Print model comparison"""
        print("\n" + "=" * 80)
        print("MODEL COMPARISON")
        print("=" * 80)

        print(f"\n{'Model':<30} {'Accuracy':<15} {'Avg Time':<15}")
        print("-" * 60)

        for model, result in results.items():
            accuracy = result.get('accuracy', 0)
            avg_time = result.get('avg_response_time', 0)
            print(f"{model:<30} {accuracy:.2%:<15} {avg_time:.2f}s")

        print("=" * 80 + "\n")

    def test_specific_capabilities(
        self,
        model_name: str,
        capability: str,
    ) -> Dict[str, Any]:
        """
        Test specific security capabilities

        Args:
            model_name: Model to test
            capability: Capability to test (vuln_analysis, exploit_dev, etc.)

        Returns:
            Test results
        """
        print(f"[*] Testing {capability} capability...")

        test_cases = {
            "vuln_analysis": [
                "Analyze this code for SQL injection: cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
                "Find vulnerabilities in: eval(request.GET['code'])",
            ],
            "exploit_dev": [
                "Suggest exploits for Apache 2.4.49",
                "How to exploit a buffer overflow in strcpy()?",
            ],
            "incident_response": [
                "Create an incident response plan for ransomware",
                "What are the first steps when detecting a breach?",
            ],
        }

        cases = test_cases.get(capability, [])
        results = []

        for case in cases:
            answer = self.llm.generate(case)
            results.append({
                "question": case,
                "answer": answer,
            })

        return {
            "capability": capability,
            "tests": results,
        }
