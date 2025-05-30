#!/usr/bin/env python3
"""
Setup script for NodeMaven API client.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "NodeMaven API Client - Professional Residential & Mobile Proxy API Client"

# Read requirements
def read_requirements():
    here = os.path.abspath(os.path.dirname(__file__))
    requirements_path = os.path.join(here, 'requirements.txt')
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="nodemaven-api-client",
    version="1.0.0",
    author="NodeMaven Team",
    author_email="support@nodemaven.com",
    description="Professional Residential & Mobile Proxy API Client",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nodemaven-api-client",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/nodemaven-api-client/issues",
        "Documentation": "https://dashboard.nodemaven.com/documentation/v2/swagger/",
        "Homepage": "https://nodemaven.com",
        "Source Code": "https://github.com/yourusername/nodemaven-api-client",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "async": [
            "aiohttp>=3.8.0",
            "httpx>=0.24.0",
        ],
        "socks": [
            "PySocks>=1.7.1",
        ],
    },
    keywords=[
        "proxy", "residential-proxy", "mobile-proxy", "socks5", "http-proxy",
        "web-scraping", "api-client", "nodemaven", "ip-rotation", "geo-targeting"
    ],
    entry_points={
        "console_scripts": [
            "nodemaven-test=examples.basic_usage:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nodemaven": ["py.typed"],
    },
    zip_safe=False,
) 