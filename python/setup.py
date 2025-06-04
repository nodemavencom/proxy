#!/usr/bin/env python3
"""
Setup script for NodeMaven Python SDK
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "NodeMaven Python SDK for residential and mobile proxies"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="nodemaven",
    version="1.0.0",
    author="NodeMaven Team",
    author_email="support@nodemaven.com",
    description="Professional Proxy API - Residential & Mobile Proxies",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nodemavencom/proxy",
    project_urls={
        "Bug Tracker": "https://github.com/nodemavencom/proxy/issues",
        "Documentation": "https://dashboard.nodemaven.com/documentation",
        "Dashboard": "https://dashboard.nodemaven.com",
        "Support": "https://t.me/node_maven",
    },
    packages=find_packages(),
    py_modules=["quick_test"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "nodemaven-test=quick_test:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="proxy, residential, mobile, api, web-scraping, geo-targeting",
) 