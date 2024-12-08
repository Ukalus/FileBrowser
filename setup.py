from setuptools import setup, find_packages

setup(
    name="ukalusEditor",
    version="0.1",
    packages=find_packages(),  # Automatically finds and includes all Python modules
    py_modules=["main"],  # Specify standalone modules explicitly
    entry_points={
        "console_scripts": [
            "ukalusEditor=main:main",  # Maps CLI command to main.py's main() function
        ],
    },
)