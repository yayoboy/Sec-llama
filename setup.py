#!/usr/bin/env python3
"""
Sec-Llama Suite - Local LLM-Powered Cybersecurity Testing Suite
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="sec-llama-suite",
    version="1.0.0",
    author="Sec-Llama Team",
    author_email="security@sec-llama.local",
    description="Local LLM-Powered Cybersecurity Testing Suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Sec-llama",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "sec-llama=cli.main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
