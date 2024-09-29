# setup.py

from setuptools import setup, find_packages

setup(
    name="distributed-testing-framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pytest-asyncio",
        "hypothesis",
        "pylint",
        "mypy",
        "click",
        "matplotlib",
        "networkx",
    ],
    entry_points={
        "console_scripts": [
            "dtf=cli.main:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive testing framework for distributed systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/distributed-testing-framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    options={
        'bdist_wheel': {
            'universal': True
        }
    },
)