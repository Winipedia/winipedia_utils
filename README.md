# Winipedia Utils

A comprehensive Python utility package that enforces best practices, automates project setup, and provides a complete testing framework for modern Python projects.

> **Note:** Code examples in this README are provided for reference. Please check the source code and docstrings for complete and accurate implementations.

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Setup Process](#setup-process)
- [Utilities](#utilities)
- [Configuration Files](#configuration-files)
- [Important Notes](#important-notes)
- [Requirements](#requirements)

## Overview

**Winipedia Utils** is a utility library that serves two primary purposes:

1. **Utility Package** - Provides reusable functions across several domains (concurrency, data handling, security, testing, etc.)
2. **Project Framework** - Automates project setup, testing infrastructure, code quality checks, and best practices enforcement

## Key Features

- **Automatic Test Generation** - Creates mirror test structure matching your source code
- **Security First** - Built-in encryption, keyring integration, and security scanning
- **Concurrent Processing** - Unified interface for multiprocessing and multithreading
- **Data Handling** - Polars-based dataframe utilities with cleaning pipelines
- **Strict Type Checking** - mypy in strict mode with full type annotations
- **Code Quality** - Automated linting, formatting, and security checks
- **Comprehensive Logging** - Automatic method instrumentation and performance tracking

## Quick Start

### How to setup a new project

```bash
# 1: Create a new repository on GitHub
# The default branch must be called main
# add a PAT or Fine-Grained Access Token to your repo secrets called REPO_TOKEN that has write access to the repository (Adminstration and Contents)(needed for branch protection in health_check.yaml - see winipedia_utils.git.github.repo.protect and for commiting as an action in release.yaml)

# 2: Clone the repository
git clone https://github.com/owner/repo.git

# 3: Create a new poetry project
poetry init # or poetry new
# 4: Poetry will ask you some stuff when you run poetry init.
# First author name must be equal to the GitHub repository owner (username).
# The repository name must be equal to the package/project name.

# 5: Add winipedia-utils to your project
poetry add winipedia-utils

# 6: Run the automated setup
poetry run python -m winipedia_utils.setup
```

The setup script will automatically configure your project with all necessary files and standards.

## Setup Process

The `winipedia_utils.setup` command automates the entire project initialization in three main steps:

1. **Initialize Configuration Files** - Creates all necessary config files with standard configurations
2. **Create Project Root** - Sets up the project root directory with __init__.py files
3. **Run Pre-commit Hooks** - Executes all pre-commit hooks to validate the setup

### Generated Configuration Files

The setup creates the following configuration files:
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `.gitignore` - Git ignore rules (assumes you added one on GitHub before.)
- `pyproject.toml` - Project configuration with Poetry settings
- `.github/workflows/health_check.yaml` - Health check workflow (Runs on every push and pull request)
- `.github/workflows/release.yaml` - Release workflow (Creates a release on GitHub when the same actions as in health check pass and commits are pushed to main)
- `.github/workflows/publish.yaml` - Publishing workflow (Publishes to PyPI when a release is created by the release workflow, if you use this workflow, you need to add a PYPI_TOKEN (named PYPI_TOKEN) to your GitHub secrets that has write access to the package on PyPI.)
- `py.typed` - PEP 561 marker for type hints
- `experiment.py` - For experimentation (ignored by git)
- `test0.py` - Test file with one empyt test (so that initial tests pass)
- `conftest.py` - Pytest configuration file

### Pre-commit Hook Workflow

When you commit code using `git commit`, the following checks run automatically:

Info: If git commit fails bc of ModuleNotFoundError or smth similar, you need to run `poetry run git commit` instead.
winipedia_utils hook is a python script that depends on winipedia_utils being installed. Poetry is needed to install winipedia_utils.
Usually VSCode or other IDEs activates the venv automatically when opening the terminal but if not you need to activate it manually or run `poetry run git commit` instead.

1. Patch version (poetry version patch)
2. Add version patch to git (git add pyproject.toml)
3. Update package manager (poetry self update)
4. Install packages (poetry install --with dev)
5. Update packages (poetry update --with dev (winipedia_utils forces all dependencies with * to be updated to latest compatible version))
6. Lock dependencies (poetry lock)
7. Check package manager configs (poetry check --strict)
8. Create tests (python -m winipedia_utils.testing.create_tests)
9. Lint code (ruff check --fix)
10. Format code (ruff format)
11. Check static types (mypy)
12. Check security (bandit -c pyproject.toml -r .)
13. Run tests (pytest (uses pyproject.toml as config))

### Auto-generated Test Structure

The test generation creates a **mirror structure** of your source code:

```
my_project/
├── my_project/
│   ├── module_a.py
│   └── package_b/
│       └── module_c.py
└── tests/
    ├── test_module_a.py
    └── test_package_b/
        └── test_module_c.py
```

For each function, class, and method, skeleton tests are created with `NotImplementedError` placeholders for you to implement.

## Configuration Files

Configuration files are managed automatically by the setup system:

- **Deleted files** - If you delete a config file, it will be recreated with standard configurations
- **Empty files** - If you want to disable a config file, make it empty. This signals that the file is unwanted and won't be modified
- **Custom additions** - You can add custom configurations as long as the standard configurations remain intact
- **Modified standards** - If you modify the standard configurations, they will be restored on the next setup run

## Utilities

Winipedia Utils provides comprehensive utility modules for common development tasks:

### Concurrent Processing

Unified interface for multiprocessing and multithreading:

```python
from winipedia_utils.concurrent.multiprocessing import multiprocess_loop
from winipedia_utils.concurrent.multithreading import multithread_loop
```

### Data Cleaning & Handling

Build data cleaning pipelines using Polars:

```python
from winipedia_utils.data.dataframe.cleaning import CleaningDF
import polars as pl
```

### Logging Utilities

Simple, standardized logging setup with automatic method instrumentation:

```python
from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

**Features:**
- Pre-configured logging levels
- ANSI color support for terminal output
- Automatic method logging via metaclasses

### Object-Oriented Programming Utilities

Advanced metaclasses and mixins for class composition and behavior extension:

```python
from winipedia_utils.oop.mixins.mixin import ABCLoggingMixin, StrictABCLoggingMixin
```

### Security Utilities

Encryption and secure credential storage using keyring:

```python
from winipedia_utils.security.keyring import (
    get_or_create_fernet,
    get_or_create_aes_gcm
)
```

### Testing Utilities

Comprehensive testing framework with automatic test generation:

```python
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.convention import (
    make_test_obj_name,
    get_test_obj_from_obj,
    make_test_obj_importpath_from_obj
)

# Custom assertions
assert_with_msg(result == expected, "Result does not match expected value")

# Test naming conventions
test_name = make_test_obj_name(my_function)  # "test_my_function"

# Get corresponding test object
test_obj = get_test_obj_from_obj(my_function)

# Get test import path
test_path = make_test_obj_importpath_from_obj(my_function)
```

**Features:**
- Automatic test file generation
- Mirror test structure matching source code
- Test naming conventions
- Fixture management with scopes (function, class, module, package, session)

### Module Introspection Utilities

Tools for working with Python modules, packages, classes, and functions:

```python
from winipedia_utils.modules.package import find_packages, walk_package
from winipedia_utils.modules.module import create_module, import_obj_from_importpath
from winipedia_utils.modules.class_ import get_all_cls_from_module, get_all_methods_from_cls
from winipedia_utils.modules.function import get_all_functions_from_module
```

### Text and String Utilities

String manipulation and configuration file handling:

```python
from winipedia_utils.text.string import value_to_truncated_string
```

### OS and System Utilities

Operating system and subprocess utilities:

```python
from winipedia_utils.os.os import run_subprocess
```

### Iteration Utilities

Utilities for working with iterables and nested structures:

```python
from winipedia_utils.iterating.iterate import get_len_with_default, nested_structure_is_subset
```

### Philosophy

The core philosophy of Winipedia Utils is to:

> **Enforce good habits, ensure clean code, and save time when starting new projects**

By automating setup, testing, linting, formatting, and type checking, you can focus on writing business logic instead of configuring tools.

## Requirements

- **Python:** 3.12 or higher
- **Poetry:** For dependency management
- **Git:** For version control and pre-commit hooks

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please ensure all code follows the project's quality standards.

