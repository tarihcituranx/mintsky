from setuptools import setup, find_packages

setup(
    name="mintsky",
    version="7.1.7",
    description="Linux Mint Desktop & Taskbar Weather App",
    author="Turan Kaya (tarihcituranx)",
    url="https://github.com/tarihcituranx",
    packages=find_packages(),
    install_requires=[
        "requests>=2.34.2",
        "PyGObject>=3.56.3",
        "groq>=1.4.0",
        "edge-tts>=7.0.0"
    ],
    entry_points={
        "console_scripts": [
            "mintsky=mintsky.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)
