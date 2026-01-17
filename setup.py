"""Setup configuration for Timbuktoo"""

from setuptools import setup, find_packages

setup(
    name="timbuktoo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    python_requires=">=3.9",
    author="Timbuktoo Team",
    description="Multi-agent AI travel concierge system",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
)
