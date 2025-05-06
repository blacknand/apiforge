from setuptools import setup, find_packages

setup(
    name="apiforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pytest>=7.0.0",
        "pyyaml>=6.0",
        "pytest-html>=3.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated API Testing Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/APIForge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)