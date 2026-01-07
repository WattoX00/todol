from setuptools import setup, find_packages

setup(
    name='todol',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'prompt_toolkit>=3.0.52'
    ],
    entry_points={
        "console_scripts": [
            "todol = todol.main:main"
        ]
    }
)