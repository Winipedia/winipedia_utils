# winipedia-utils

A comprehensive Python development framework that streamlines project setup, testing, CLI generation, and build automation. Built with Poetry and designed for Python 3.12+.

## Table of Contents
- [Quick Start](#quick-start)
- [Project Setup](#project-setup)
- [Core Features](#core-features)
  - [ConfigFile System](#configfile-system)
  - [Builder System](#builder-system)
  - [CLI System](#cli-system)
  - [Testing Utilities](#testing-utilities)
- [Utils Package](#utils-package)
- [CLI Commands](#cli-commands)
- [Advanced Usage](#advanced-usage)
- [Requirements](#requirements)

## Quick Start

```bash
# Create a new project
poetry new my-project # or poetry init
cd my-project

# Add winipedia-utils
poetry add winipedia-utils

# Set up the project structure
poetry run winipedia-utils setup
```

That's it! Your project is now set up with a complete development environment.

## Project Setup

When you start a new project, you can use winipedia-utils to set up the project structure automatically.

### Prerequisites
- Python 3.12 or higher
- Poetry for dependency management
- Git for version control
- Project root folder name matches repository name (e.g., `my-project`)

### Setup Process

Let's say your project is called `my-project`. Here's what you do:

```bash
# Initialize a new Poetry project
poetry init  # or poetry new my-project

# Add winipedia-utils as a dependency
poetry add winipedia-utils

# Run the setup command
poetry run winipedia-utils setup
```

### Generated Project Structure

This will create the following structure (with `__init__.py` files):

```bash
my-project/
├── my_project/                    # Source package (underscores)
│   ├── dev/                       # Development utilities
│   │   ├── artifacts/
│   │   │   └── builder/
│   │   │       └── builder.py     # Build scripts
│   │   ├── cli/
│   │   │   └── subcommands.py     # CLI commands
│   │   └── configs/
│   │       └── configs.py         # Config file definitions
│   └── ...                        # Your application code
├── tests/                         # Test package
│   ├── base/
│   │   ├── fixtures/
│   │   │   ├── scopes/            # Fixtures organized by scope
│   │   │   │   ├── session.py     # Session-scoped fixtures
│   │   │   │   ├── package.py     # Package-scoped fixtures
│   │   │   │   ├── module.py      # Module-scoped fixtures
│   │   │   │   ├── class_.py      # Class-scoped fixtures
│   │   │   │   └── function.py    # Function-scoped fixtures
│   │   │   └── fixture.py         # Regular fixtures
│   │   └── utils/
│   │       └── utils.py           # Test utilities
│   ├── test_my_project/           # Test mirror of source
│   │   └── test_dev/
│   │       ├── test_artifacts/
│   │       │   └── test_builder/
│   │       │       └── test_builder.py
│   │       ├── test_cli/
│   │       │   └── test_subcommands.py
│   │       └── test_configs/
│   │           └── test_configs.py
│   ├── conftest.py                # Auto-generated pytest config
│   └── test_zero.py               # Placeholder test
├── .env                           # Environment variables
├── .gitignore                     # Git ignore patterns
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .python-version                # Python version specification
├── experiment.py                  # Experimentation file (gitignored)
├── LICENSE                        # EmptyLicense
├── poetry.lock                    # Locked dependencies
├── pyproject.toml                 # Project configuration
└── README.md                      # Project documentation
```

## Core Features

### ConfigFile System

The ConfigFile system provides a powerful way to manage configuration files in your project. All configuration files are automatically generated and validated.

#### How It Works

1. **Define a ConfigFile subclass** in `my_project/dev/configs/configs.py`
2. **Implement required methods** (get_configs, get_parent_path, etc.)
3. **Run setup or tests** - files are automatically created and validated

#### Example: Creating a Custom Config File

```python
from pathlib import Path
from winipedia_utils.dev.configs.base.base import YamlConfigFile

class MyCustomConfigFile(YamlConfigFile):
    """Config file for my custom settings."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Where to create the config file."""
        return Path()  # Root directory

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
        """Define the expected config structure."""
        return {
            "app_name": "my-project",
            "version": "1.0.0",
            "settings": {
                "debug": False,
                "port": 8000
            }
        }
```

#### Available ConfigFile Types

- **`YamlConfigFile`** - For YAML configuration files
- **`TomlConfigFile`** - For TOML files (like pyproject.toml)
- **`PythonConfigFile`** - For Python configuration files
- **`TextConfigFile`** - For plain text files

#### Built-in ConfigFiles

- **`PyprojectConfigFile`** - Manages pyproject.toml
- **`PreCommitConfigFile`** - Manages .pre-commit-config.yaml
- **`GitIgnoreConfigFile`** - Manages .gitignore
- **`ReadmeConfigFile`** - Manages README.md
- **`DotEnvConfigFile`** - Manages .env files

#### Key Features

- **Auto-initialization**: All ConfigFile subclasses are discovered and initialized automatically
- **Smart merging**: Missing configs are added without overwriting existing values
- **Validation**: Configs are validated on every test run


### Builder System

Create build artifacts with ease using the Builder system. Perfect for creating executables, packages, or any build artifacts.

#### How to Use

1. **Define a Builder subclass** in `my_project/dev/artifacts/builder/builder.py`
2. **Implement `create_artifacts()`** method
3. **Run** `poetry run winipedia-utils build`

#### Example: Simple Builder

```python
from pathlib import Path
from winipedia_utils.dev.artifacts.builder.base.base import Builder

class MyProjectBuilder(Builder):
    """Build script for my-project."""

    @classmethod
    def create_artifacts(cls) -> None:
        """Create build artifacts."""
        # Create a simple text artifact
        artifact_path = cls.ARTIFACTS_PATH / "version.txt"
        artifact_path.write_text("1.0.0")

        # Artifacts are automatically renamed with platform suffix
        # e.g., version-Linux.txt, version-Darwin.txt, version-Windows.txt
```

#### Example: PyInstaller Builder

```python
from pathlib import Path
from winipedia_utils.dev.artifacts.builder.base.base import PyInstallerBuilder

class MyAppBuilder(PyInstallerBuilder):
    """Build executable with PyInstaller."""

    @classmethod
    def get_add_datas(cls) -> list[tuple[Path, Path]]:
        """Specify data files to include."""
        return [
            (Path("config.yaml"), Path(".")),
            (Path("assets"), Path("assets")),
        ]
```

#### Features

- **Auto-discovery**: All Builder subclasses are automatically found and executed
- **Platform tagging**: Artifacts are automatically tagged with the platform name
- **PyInstaller support**: Built-in support for creating executables
- **Validation**: Ensures artifacts are created in the correct location

### CLI System

Automatically generate CLI commands from Python functions. No boilerplate required!

#### How It Works

1. **Define functions** in `my_project/dev/cli/subcommands.py`
2. **Functions automatically become CLI commands**
3. **Run** `poetry run my-project --help` to see available commands

#### Example: CLI Commands

```python
# my_project/dev/cli/subcommands.py

def hello(name: str = "World") -> None:
    """Say hello to someone.

    Args:
        name: The name to greet
    """
    print(f"Hello, {name}!")

def deploy(environment: str, dry_run: bool = False) -> None:
    """Deploy the application.

    Args:
        environment: Target environment (dev, staging, prod)
        dry_run: Run without making changes
    """
    if dry_run:
        print(f"Would deploy to {environment}")
    else:
        print(f"Deploying to {environment}...")
```

#### Usage

```bash
# See all commands
poetry run my-project --help

# Run commands
poetry run my-project hello
poetry run my-project hello --name Alice
poetry run my-project deploy staging --dry-run
```

#### Features

- **Auto-discovery**: All functions in subcommands.py become CLI commands
- **Type hints**: Automatically parsed for argument types
- **Docstrings**: Used for help text
- **Powered by Typer**: Full Typer functionality available

**Note**: You must define at least one function in subcommands.py for the CLI to work.

### Testing Utilities

Comprehensive testing utilities with automatic test generation and organized fixture management.

#### Auto-Generated Tests

winipedia-utils automatically creates test skeletons for all your functions and classes:

```bash
# Generate tests for all code
poetry run winipedia-utils create-tests

# Or just run pytest (tests are auto-generated if missing)
pytest
```

#### Fixture Organization by Scope

Organize your fixtures by scope in `tests/base/fixtures/scopes/`:

```python
# tests/base/fixtures/scopes/session.py
from winipedia_utils.utils.testing.fixtures import autouse_session_fixture

@autouse_session_fixture
def setup_database() -> None:
    """Set up database once per test session."""
    # This runs once before all tests
    initialize_test_database()
```

```python
# tests/base/fixtures/scopes/function.py
from winipedia_utils.utils.testing.fixtures import autouse_function_fixture

@autouse_function_fixture
def clean_temp_files() -> None:
    """Clean temp files before each test."""
    # This runs before each test function
    clear_temp_directory()
```

#### Available Fixture Decorators

```python
from winipedia_utils.utils.testing.fixtures import (
    # Regular fixtures
    function_fixture,
    class_fixture,
    module_fixture,
    package_fixture,
    session_fixture,

    # Autouse fixtures
    autouse_function_fixture,
    autouse_class_fixture,
    autouse_module_fixture,
    autouse_package_fixture,
    autouse_session_fixture,
)
```

#### Regular Fixtures

Define non-autouse fixtures in `tests/base/fixtures/fixture.py`:

```python
# tests/base/fixtures/fixture.py
from winipedia_utils.utils.testing.fixtures import function_fixture

@function_fixture
def sample_data() -> dict:
    """Provide sample data for tests."""
    return {"key": "value", "count": 42}
```

#### Testing Assertions

Enhanced assertion utilities:

```python
from winipedia_utils.utils.testing.assertions import (
    assert_with_msg,
    assert_with_info,
    assert_isabstrct_method,
)

def test_example():
    result = calculate_something()

    # Simple assertion with custom message
    assert_with_msg(result > 0, "Result should be positive")

    # Assertion with expected vs actual
    expected = 42
    assert_with_info(result == expected, expected, result, "Calculation failed")
```

#### Important Files

- **`conftest.py`**: Auto-generated, **do not modify**. Imports all fixtures and plugs in standard tests.
- **`test_zero.py`**: Auto-generated, **do not modify**. Placeholder test for initial setup.

## Utils Package

The `winipedia_utils.utils` package provides a comprehensive collection of utility functions organized by domain.

### Data Utilities

#### String Manipulation (`utils.data.structures.text.string`)

```python
from winipedia_utils.utils.data.structures.text.string import (
    split_on_uppercase,
    make_name_from_obj,
    get_reusable_hash,
    value_to_truncated_string,
    ask_for_input_with_timeout,
)

# Split on uppercase letters
split_on_uppercase("MyClassName")  # ["My", "Class", "Name"]

# Create name from object
make_name_from_obj(MyClass)  # "my_class"

# Generate consistent hash
get_reusable_hash("some value")  # SHA-256 hash

# Truncate long strings
value_to_truncated_string(long_dict, max_length=100)

# Get input with timeout
user_input = ask_for_input_with_timeout("Enter value: ", timeout=30)
```

#### Dictionary Utilities (`utils.data.structures.dicts`)

```python
from winipedia_utils.utils.data.structures.dicts import reverse_dict

# Reverse a dictionary
original = {"a": 1, "b": 2}
reversed_dict = reverse_dict(original)  # {1: "a", 2: "b"}
```

### Git Utilities

#### GitHub Integration (`utils.git.github`)

```python
from winipedia_utils.utils.git.github.github import (
    get_github_repo_token,
    running_in_github_actions,
)

# Get GitHub token from env or .env
token = get_github_repo_token()

# Check if running in GitHub Actions
if running_in_github_actions():
    print("Running in CI")
```

#### GitIgnore Support (`utils.git.gitignore`)

```python
from winipedia_utils.utils.git.gitignore.gitignore import (
    walk_os_skipping_gitignore_patterns,
)

# Walk directory respecting .gitignore
for path in walk_os_skipping_gitignore_patterns(Path(".")):
    print(path)
```

### Module Utilities

#### Module Inspection (`utils.modules.module`)

```python
from winipedia_utils.utils.modules.module import (
    import_module_from_path,
    import_module_with_default,
    to_path,
    create_module,
    get_module_content_as_str,
)

# Import module from file path
module = import_module_from_path(Path("my_module.py"))

# Import with fallback
module = import_module_with_default("optional.module")  # Returns None if not found

# Convert module to path
path = to_path("my_package.my_module", is_package=False)

# Create a new module
create_module("my_package.new_module", is_package=True)
```

#### Class Utilities (`utils.modules.class_`)

```python
from winipedia_utils.utils.modules.class_ import (
    get_all_nonabstract_subclasses,
    get_all_cls_from_module,
    get_all_methods_from_cls,
)

# Get all non-abstract subclasses
subclasses = get_all_nonabstract_subclasses(BaseClass)

# Get all classes from a module
classes = get_all_cls_from_module(my_module)

# Get all methods from a class
methods = get_all_methods_from_cls(MyClass)
```

#### Function Utilities (`utils.modules.function`)

```python
from winipedia_utils.utils.modules.function import (
    get_all_functions_from_module,
    is_abstractmethod,
)

# Get all functions from a module
functions = get_all_functions_from_module(my_module)

# Check if method is abstract
if is_abstractmethod(some_method):
    print("This is an abstract method")
```

### Logging Utilities

```python
from winipedia_utils.utils.logging.logger import get_logger

# Get a configured logger
logger = get_logger(__name__)

logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### OS Utilities

```python
from winipedia_utils.utils.os.os import (
    which_with_raise,
    run_subprocess,
)

# Find command path
python_path = which_with_raise("python3")

# Run subprocess with enhanced error handling
result = run_subprocess(
    ["git", "status"],
    capture_output=True,
    check=True,
    cwd=Path.cwd()
)
```

### Security Utilities

```python
from winipedia_utils.utils.security.keyring import (
    get_or_create_key,
    get_or_create_fernet,
    get_or_create_aes_gcm,
)

# Get or create encryption key (stored in system keyring)
key = get_or_create_key("my-app", "encryption-key")

# Get Fernet cipher
fernet = get_or_create_fernet("my-app", "fernet-key")
encrypted = fernet.encrypt(b"secret data")

# Get AES-GCM cipher
aes_gcm = get_or_create_aes_gcm("my-app", "aes-key")
```

### OOP Utilities

#### Metaclasses and Mixins

```python
from winipedia_utils.utils.oop.mixins.meta import (
    ABCLoggingMeta,
    StrictABCMeta,
    StrictABCLoggingMeta,
)

# Automatic logging for all methods
class MyClass(metaclass=ABCLoggingMeta):
    def my_method(self):
        # Automatically logged with timing and arguments
        pass

# Strict ABC enforcement with type checking
class StrictBase(metaclass=StrictABCMeta):
    @abstractmethod
    def required_method(self) -> int:
        pass
```



## CLI Commands

winipedia-utils provides several built-in CLI commands:

### `setup`

Complete project initialization. Runs all setup steps in sequence.

```bash
poetry run winipedia-utils setup
```

**What it does:**
1. Initializes all ConfigFile subclasses
2. Creates project root structure
3. Updates dependencies in pyproject.toml
4. Runs pre-commit hooks
5. Creates and runs tests

**When to use:** First time setting up a new project, or after major structural changes.

### `create-root`

Creates the root project structure without running tests or hooks.

```bash
poetry run winipedia-utils create-root
```

**What it does:**
1. Initializes all ConfigFile subclasses
2. Creates `__init__.py` files for source and test packages
3. Creates missing directories

**When to use:** When you need to regenerate project structure without running full setup.

### `create-tests`

Generates test skeletons for all functions and classes.

```bash
poetry run winipedia-utils create-tests
```

**What it does:**
1. Scans all source code
2. Creates test files mirroring source structure
3. Generates test function stubs with `NotImplementedError`
4. Never overwrites existing tests

**When to use:** After adding new functions/classes, or to ensure test coverage.

### `build`

Builds all artifacts defined in Builder subclasses.

```bash
poetry run winipedia-utils build
```

**What it does:**
1. Discovers all Builder subclasses
2. Executes `create_artifacts()` for each
3. Renames artifacts with platform suffix
4. Validates artifact locations

**When to use:** When you need to create distribution artifacts, executables, or packages.

## Advanced Usage

### Custom Project Scripts

You can define your own CLI commands in `my_project/dev/cli/subcommands.py`:

```python
from winipedia_utils.utils.logging.logger import get_logger
from winipedia_utils.utils.os.os import run_subprocess

logger = get_logger(__name__)

def deploy(environment: str = "staging", skip_tests: bool = False) -> None:
    """Deploy the application to specified environment.

    Args:
        environment: Target environment (dev, staging, prod)
        skip_tests: Skip running tests before deployment
    """
    if not skip_tests:
        logger.info("Running tests...")
        run_subprocess(["pytest"])

    logger.info(f"Deploying to {environment}...")
    # Your deployment logic here
```

Then run:
```bash
poetry run my-project deploy --environment prod
```

### Custom ConfigFiles

Create custom configuration files for your project:

```python
from pathlib import Path
from typing import Any
from winipedia_utils.dev.configs.base.base import YamlConfigFile

class DatabaseConfigFile(YamlConfigFile):
    """Database configuration file."""

    @classmethod
    def get_parent_path(cls) -> Path:
        return Path("config")

    @classmethod
    def get_filename(cls) -> str:
        return "database"

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "pool_size": 10,
        }
```

This will automatically create `config/database.yaml` with the specified structure.

### Extending Builders

Create sophisticated build pipelines:

```python
from pathlib import Path
from winipedia_utils.dev.artifacts.builder.base.base import Builder
from winipedia_utils.utils.os.os import run_subprocess

class DockerBuilder(Builder):
    """Build Docker images."""

    @classmethod
    def create_artifacts(cls) -> None:
        """Build Docker image and save as tar."""
        # Build Docker image
        run_subprocess(["docker", "build", "-t", "myapp:latest", "."])

        # Save image as tar
        artifact_path = cls.ARTIFACTS_PATH / "myapp.tar"
        run_subprocess([
            "docker", "save", "-o", str(artifact_path), "myapp:latest"
        ])

        # Will be renamed to myapp-Linux.tar, myapp-Darwin.tar, etc.
```

### Integration with Pre-commit

The generated `.pre-commit-config.yaml` includes:
- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanning

Customize hooks in your project's `my_project/dev/configs/pre_commit.py`.

### Environment Variables

Use the `.env` file for environment-specific configuration:

```bash
# .env
REPO_TOKEN=ghp_your_github_token
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your_api_key
```

Access in code:

```python
import os
from winipedia_utils.dev.configs.dot_env import DotEnvConfigFile

# Load .env file
dotenv = DotEnvConfigFile.load()
api_key = dotenv.get("API_KEY")

# Or use os.getenv
api_key = os.getenv("API_KEY")
```

### Experiment File

The `experiment.py` file is automatically gitignored and perfect for:
- Quick prototyping
- Testing code snippets
- Debugging
- Temporary experiments

```python
# experiment.py
from my_project.my_module import my_function

# Test your code here
result = my_function()
print(result)
```

## Requirements

### Python Version
- **Python 3.12 or higher** (required)

### Dependencies

#### Core Dependencies
- **poetry**: Package and dependency management
- **typer**: CLI framework
- **pytest**: Testing framework
- **pyyaml**: YAML parsing
- **tomlkit**: TOML parsing
- **networkx**: Graph algorithms (for dependency analysis)
- **polars**: Fast DataFrame library
- **cryptography**: Encryption utilities
- **keyring**: Secure credential storage
- **pygithub**: GitHub API integration
- **pathspec**: Gitignore pattern matching
- **defusedxml**: Secure XML parsing
- **tqdm**: Progress bars

#### Development Dependencies
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **bandit**: Security linter
- **pre-commit**: Git hook framework
- **pytest-mock**: Mocking for pytest
- **pyinstaller**: Executable builder (Python <3.15)

### System Requirements
- **Git**: Version control
- **Poetry**: Installed and available in PATH

### Installation

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new my-project
cd my-project

# Add winipedia-utils
poetry add winipedia-utils

# Set up project
poetry run winipedia-utils setup
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

This is a personal utility package by Winipedia. Feel free to fork and adapt for your own use.

## Version

Current version: **0.7.19**

---

**Happy coding! 🚀**


