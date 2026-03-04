from setuptools import setup, find_packages

setup(
    name="antigravity-core",
    version="1.0.0",
    description="Proaktif AI tabanlı Yazılım Geliştirme Asistanı ve Mimari Denetleme Motoru",
    author="Antigravity Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "watchdog>=2.3.0",
        "pyyaml>=6.0",
        "requests>=2.31.0"
    ],
    entry_points={
        "console_scripts": [
            "antigravity=antigravity_agent.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
