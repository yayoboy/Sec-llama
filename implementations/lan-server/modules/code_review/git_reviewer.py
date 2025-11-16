"""
Git Code Reviewer - AI-powered security code review
"""

import subprocess
from typing import Dict, Any, List

from core.llm_interface import get_llm
from core.prompt_templates import PromptTemplates


class GitCodeReviewer:
    """AI-powered code reviewer with Git integration"""

    def __init__(self):
        self.llm = get_llm()

    def review_commit(self, commit_hash: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Review a specific commit

        Args:
            commit_hash: Git commit hash
            repo_path: Path to git repository

        Returns:
            Review results
        """
        print(f"[*] Reviewing commit: {commit_hash}")

        try:
            # Get commit diff
            cmd = ["git", "-C", repo_path, "show", commit_hash]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                return {"status": "error", "message": "Failed to get commit"}

            diff = result.stdout

            # AI review
            review = self._review_diff_with_ai(diff, commit_hash)

            return {
                "status": "success",
                "commit": commit_hash,
                "review": review,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _review_diff_with_ai(self, diff: str, commit_hash: str) -> str:
        """Review diff with AI"""
        print(f"\n[*] AI reviewing commit {commit_hash}...")

        # Truncate diff if too long
        if len(diff) > 3000:
            diff = diff[:3000] + "\n... (truncated)"

        prompt = PromptTemplates.get_code_review_prompt(diff, "auto")

        try:
            review = self.llm.generate(prompt)

            print("\n" + "=" * 80)
            print(f"CODE REVIEW: {commit_hash}")
            print("=" * 80)
            print(review)
            print("=" * 80 + "\n")

            return review

        except Exception as e:
            return f"Review failed: {e}"

    def review_pr(self, pr_number: int, repo: str) -> Dict[str, Any]:
        """
        Review GitHub Pull Request

        Args:
            pr_number: PR number
            repo: Repository (owner/repo)

        Returns:
            Review results
        """
        print(f"[*] Reviewing PR #{pr_number} in {repo}")

        try:
            # Get PR diff using gh CLI
            cmd = ["gh", "pr", "diff", str(pr_number), "-R", repo]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                return {"status": "error", "message": "Failed to get PR diff"}

            diff = result.stdout

            # AI review
            review = self._review_diff_with_ai(diff, f"PR-{pr_number}")

            return {
                "status": "success",
                "pr": pr_number,
                "review": review,
            }

        except FileNotFoundError:
            return {"status": "error", "message": "gh CLI not found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def review_file(self, file_path: str, language: str = "auto") -> Dict[str, Any]:
        """Review a single file"""
        print(f"[*] Reviewing file: {file_path}")

        try:
            with open(file_path, 'r') as f:
                code = f.read()

            prompt = PromptTemplates.get_code_vulnerability_prompt(code, language)

            review = self.llm.generate(prompt)

            print("\n" + "=" * 80)
            print(f"FILE REVIEW: {file_path}")
            print("=" * 80)
            print(review)
            print("=" * 80 + "\n")

            return {
                "status": "success",
                "file": file_path,
                "review": review,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}
