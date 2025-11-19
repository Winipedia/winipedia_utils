# winiutils

(This project uses [pyrig](https://github.com/Winipedia/pyrig))

## Overview

**winiutils** is a comprehensive Python utility library providing production-ready tools for data processing, concurrent execution, security, and object-oriented programming patterns. Built with strict type safety and code quality standards, it offers reusable components for common development tasks.

## Features

### DataFrame Cleaning Pipeline

The `CleaningDF` abstract base class provides a production-ready, extensible framework for cleaning and standardizing Polars DataFrames. It implements a comprehensive 8-step cleaning pipeline:

**Pipeline Stages:**
1. **Column Renaming** - Standardize column names from raw input
2. **Column Dropping** - Remove columns not in schema
3. **Null Filling** - Fill null values with configurable defaults
4. **Type Conversion** - Convert to correct data types with custom transformations
5. **Null Subset Dropping** - Remove rows where specified column groups are all null
6. **Duplicate Handling** - Aggregate duplicate rows and sum specified columns
7. **Sorting** - Multi-column sorting with per-column direction control
8. **Validation** - Enforce data quality (correct dtypes, no nulls in required columns, no NaN values)

**Key Features:**
- **Abstract Configuration**: 10 abstract methods for complete customization
  - `get_rename_map()` - Column name standardization
  - `get_col_dtype_map()` - Type schema definition
  - `get_fill_null_map()` - Null value defaults
  - `get_col_converter_map()` - Custom column transformations
  - `get_drop_null_subsets()` - Row deletion rules
  - `get_unique_subsets()` - Duplicate detection criteria
  - `get_add_on_duplicate_cols()` - Columns to aggregate on duplicates
  - `get_sort_cols()` - Sort order specification
  - `get_no_null_cols()` - Required non-null columns
  - `get_col_precision_map()` - Float rounding precision

- **Advanced Features**:
  - **Kahan Summation**: Compensated rounding for floats to prevent accumulation errors
  - **Automatic Logging**: Built-in method logging via `ABCLoggingMixin`
  - **Type Safety**: Full Polars type enforcement with validation
  - **NaN Handling**: Automatic NaN to null conversion
  - **Duplicate Aggregation**: Sum values when merging duplicate rows
  - **Standard Conversions**: Auto-strip strings, auto-round floats

**Usage Pattern:**
```python
class MyDataCleaner(CleaningDF):
    # Define column constants
    USER_ID = "user_id"
    EMAIL = "email"

    @classmethod
    def get_rename_map(cls) -> dict[str, str]:
        return {cls.USER_ID: "UserId", cls.EMAIL: "Email_Address"}

    @classmethod
    def get_col_dtype_map(cls) -> dict[str, type[pl.DataType]]:
        return {cls.USER_ID: pl.Int64, cls.EMAIL: pl.Utf8}

    # ... implement other abstract methods

# Use it
cleaned_data = MyDataCleaner(raw_dataframe)
result_df = cleaned_data.df
```

**Best For:**
- ETL pipelines requiring consistent data quality
- Data standardization before database loading
- Building composable data cleaning workflows
- Projects requiring audit trails (automatic logging)

### Concurrent Processing

A unified, intelligent framework for parallel execution supporting both multiprocessing (CPU-bound) and multithreading (I/O-bound) tasks with automatic resource optimization.

**Core Functions:**

**`multiprocess_loop()`** - CPU-bound parallel processing
- Uses `multiprocessing.Pool` with spawn context for true parallelism
- Bypasses Python's GIL for CPU-intensive tasks
- Automatic process pool sizing based on CPU count and active processes
- Deep-copy support for mutable static arguments

**`multithread_loop()`** - I/O-bound parallel processing
- Uses `ThreadPoolExecutor` for concurrent I/O operations
- Efficient for network requests, file I/O, database queries
- Automatic thread pool sizing (CPU count × 4)
- Safe for mutable objects (shared memory)

**`cancel_on_timeout()`** - Timeout enforcement
- Decorator/wrapper for functions that may hang
- Uses multiprocessing to forcefully terminate on timeout
- Proper cleanup with process termination and joining
- Works with pickle-able functions

**Key Features:**

- **Automatic Worker Optimization**: Calculates optimal pool size based on:
  - Available CPU cores
  - Currently active processes/threads
  - Number of tasks to process
  - Ensures at least 1 worker, prevents oversubscription

- **Progress Tracking**: Built-in tqdm integration
  - Real-time progress bars for all parallel operations
  - Descriptive labels showing function name and worker type
  - Accurate task counting

- **Order Preservation**: Results returned in original input order
  - Uses internal ordering system with `imap_unordered`
  - Efficient unordered processing with ordered output
  - No manual result sorting required

- **Flexible Argument Handling**:
  - `process_args`: Variable arguments per task (iterable of iterables)
  - `process_args_static`: Shared arguments across all tasks
  - `deepcopy_static_args`: Arguments deep-copied per process (for mutables)
  - `process_args_len`: Optional length hint for optimization

- **Smart Execution**: Single unified `concurrent_loop()` backend
  - Automatically selects map/imap_unordered based on task count
  - Handles both Pool and ThreadPoolExecutor transparently
  - Consistent API regardless of concurrency type

**Usage Examples:**

```python
from winiutils.src.iterating.concurrent.multiprocessing import multiprocess_loop
from winiutils.src.iterating.concurrent.multithreading import multithread_loop
from winiutils.src.iterating.concurrent.multiprocessing import cancel_on_timeout

# CPU-bound: Process large datasets in parallel
def process_data(data_chunk, config):
    # Heavy computation
    return analyzed_data

results = multiprocess_loop(
    process_function=process_data,
    process_args=[(chunk,) for chunk in data_chunks],
    process_args_static=(config,),
    process_args_len=len(data_chunks)
)

# I/O-bound: Fetch multiple URLs concurrently
def fetch_url(url, headers):
    return requests.get(url, headers=headers)

responses = multithread_loop(
    process_function=fetch_url,
    process_args=[(url,) for url in urls],
    process_args_static=(headers,),
    process_args_len=len(urls)
)

# Timeout enforcement for blocking operations
@cancel_on_timeout(seconds=5, message="User input timeout")
def get_user_input():
    return input("Enter value: ")

try:
    user_value = get_user_input()
except multiprocessing.TimeoutError:
    user_value = "default"
```

**Architecture Highlights:**

- **Spawn Context**: Uses `spawn` instead of `fork` for safer multiprocessing
- **Context Managers**: Proper resource cleanup with `with` statements
- **Type Safety**: Full type hints for all functions and parameters
- **Logging**: Integrated logging for pool size decisions and execution flow
- **Error Handling**: Graceful handling of timeouts and process failures

**Best For:**
- Parallel data processing pipelines
- Batch API requests or database queries
- CPU-intensive computations (image processing, ML inference)
- Operations requiring timeout enforcement
- Applications needing automatic resource management

### Object-Oriented Programming Utilities

Advanced metaclasses and mixins for automatic method instrumentation and class composition using the mixin pattern.

**Core Components:**

**`ABCLoggingMeta`** - Metaclass for automatic method logging
- Extends `ABCMeta` to combine abstract class enforcement with logging
- Automatically wraps all non-magic methods with logging decorators
- Supports `classmethod`, `staticmethod`, and instance methods
- Zero boilerplate - just use as metaclass

**`ABCLoggingMixin`** - Ready-to-use mixin class
- Pre-configured with `ABCLoggingMeta` metaclass
- Inherit to add automatic logging to any class
- Combines well with other mixins and base classes

**Logging Features:**

- **Automatic Instrumentation**: All methods automatically logged without decorators
- **Performance Tracking**: Measures and logs execution time for each method call
- **Argument Logging**: Captures and logs method arguments (truncated for readability)
- **Return Value Logging**: Logs method return values (truncated)
- **Rate Limiting**: Intelligent throttling to prevent log spam
  - Only logs if >1 second since last call to same method
  - Prevents flooding logs in tight loops
  - Per-method tracking (not global)
- **Truncation**: Arguments and returns truncated to 20 characters max
- **Magic Method Exclusion**: Skips `__init__`, `__str__`, etc. to avoid noise

**How It Works:**

The metaclass intercepts class creation and wraps methods at definition time:
1. Iterates through all class attributes during `__new__`
2. Identifies callable, non-magic methods
3. Wraps each with a logging decorator that:
   - Tracks call times per method
   - Logs method name, class name, arguments, kwargs
   - Executes the original method
   - Logs execution duration and return value
   - Updates last call time for rate limiting

**Usage Examples:**

```python
from winiutils.src.oop.mixins.mixin import ABCLoggingMixin
from abc import abstractmethod

# Option 1: Use the mixin
class MyService(ABCLoggingMixin):
    def process_data(self, data: list) -> dict:
        # Automatically logged with timing
        return {"processed": len(data)}

    @classmethod
    def validate(cls, value: str) -> bool:
        # Classmethods also logged
        return len(value) > 0

# Option 2: Use the metaclass directly
from winiutils.src.oop.mixins.meta import ABCLoggingMeta

class MyAbstractService(metaclass=ABCLoggingMeta):
    @abstractmethod
    def execute(self) -> None:
        pass

class ConcreteService(MyAbstractService):
    def execute(self) -> None:
        # Automatically logged
        print("Executing...")

# Usage - logging happens automatically
service = MyService()
result = service.process_data([1, 2, 3])
# Logs: "MyService - Calling process_data with ([1, 2, 3],) and {}"
# Logs: "MyService - process_data finished with 0.001 seconds -> returning {'processed': 3}"
```

**Log Output Example:**
```
INFO - MyService - Calling process_data with ([1, 2, 3],) and {}
INFO - MyService - process_data finished with 0.001234 seconds -> returning {'processed': 3}
INFO - MyService - Calling validate with ('test',) and {}
INFO - MyService - validate finished with 0.000123 seconds -> returning True
```

**Technical Details:**

- **Metaclass Inheritance**: Properly extends `ABCMeta` for abstract class support
- **Decorator Preservation**: Uses `@wraps` to maintain function metadata
- **Performance**: Minimal overhead - caches `time.time` function reference
- **Thread Safety**: Each method has independent call time tracking
- **Memory Efficient**: Call times stored in closure, not instance attributes

**Integration with Other Utilities:**

The `CleaningDF` class uses `ABCLoggingMixin` to automatically log all cleaning operations:
```python
class CleaningDF(ABCLoggingMixin):
    # All methods (rename_cols, fill_nulls, etc.) automatically logged
    # Provides audit trail of data cleaning pipeline
    pass
```

**Best For:**
- Debugging complex class hierarchies
- Performance profiling during development
- Audit trails for data processing pipelines
- Monitoring service method execution
- Classes with abstract methods requiring implementation tracking
- Reducing logging boilerplate in large codebases

### Security Utilities

Production-ready cryptography and secure credential storage utilities built on industry-standard libraries (`cryptography` and `keyring`).

**Cryptography Module** (`winiutils.src.security.cryptography`)

**AES-GCM Encryption/Decryption** - Authenticated encryption with proper IV handling

**`encrypt_with_aes_gcm(aes_gcm, data, aad=None)`**
- Encrypts data using AES-GCM (Galois/Counter Mode)
- Generates random 12-byte IV for each encryption
- Prepends IV to ciphertext for easy decryption
- Optional Additional Authenticated Data (AAD) support
- Returns: `IV + encrypted_data` as single bytes object

**`decrypt_with_aes_gcm(aes_gcm, data, aad=None)`**
- Decrypts AES-GCM encrypted data
- Automatically extracts IV from first 12 bytes
- Validates authentication tag (prevents tampering)
- Optional AAD support (must match encryption AAD)
- Returns: Original plaintext as bytes

**Key Features:**
- **Authenticated Encryption**: AES-GCM provides both confidentiality and integrity
- **Random IVs**: Each encryption uses a unique, cryptographically random IV
- **No IV Management**: IV automatically prepended/extracted - no separate storage needed
- **AAD Support**: Authenticate additional data without encrypting it
- **Standard Compliance**: Uses `cryptography` library's AEAD implementation

**Keyring Module** (`winiutils.src.security.keyring`)

**Secure Key Storage** - System keyring integration for credential management

**`get_or_create_fernet(service_name, username)`**
- Retrieves or generates Fernet symmetric encryption key
- Stores key securely in system keyring (OS-level security)
- Returns: `(Fernet instance, raw_key_bytes)` tuple
- Automatic base64 encoding for keyring storage

**`get_or_create_aes_gcm(service_name, username)`**
- Retrieves or generates 256-bit AES-GCM key
- Stores key securely in system keyring
- Returns: `(AESGCM instance, raw_key_bytes)` tuple
- Uses `AESGCM.generate_key(bit_length=256)`

**`get_or_create_key(service_name, username, key_class, generate_key_func)`**
- Generic key retrieval/creation function
- Supports any key type with custom generation function
- Service name automatically modified with key class name
- Base64 encoding for safe string storage
- Type-safe with generic type parameter

**Key Features:**
- **System Keyring**: Uses OS-native credential storage (Keychain on macOS, Credential Manager on Windows, Secret Service on Linux)
- **Automatic Generation**: Creates keys on first use if not found
- **Type Safety**: Generic type parameters for key class
- **Service Namespacing**: Prevents key collisions with class-based naming
- **Base64 Encoding**: Safe storage of binary keys as strings
- **Lazy Initialization**: Keys only generated when needed

**Usage Examples:**

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winiutils.src.security.keyring import get_or_create_aes_gcm
from winiutils.src.security.cryptography import encrypt_with_aes_gcm, decrypt_with_aes_gcm

# Get or create encryption key (stored in system keyring)
aes_gcm, raw_key = get_or_create_aes_gcm(
    service_name="my_app",
    username="user@example.com"
)

# Encrypt sensitive data
plaintext = b"Secret message"
aad = b"metadata"  # Optional authenticated data
encrypted = encrypt_with_aes_gcm(aes_gcm, plaintext, aad)

# Decrypt data
decrypted = decrypt_with_aes_gcm(aes_gcm, encrypted, aad)
assert decrypted == plaintext

# Using Fernet (simpler, includes timestamp)
from cryptography.fernet import Fernet
from winiutils.src.security.keyring import get_or_create_fernet

fernet, key = get_or_create_fernet("my_app", "user@example.com")
token = fernet.encrypt(b"Secret data")
original = fernet.decrypt(token)

# Custom key type
from winiutils.src.security.keyring import get_or_create_key

custom_cipher, key = get_or_create_key(
    service_name="my_app",
    username="admin",
    key_class=AESGCM,
    generate_key_func=lambda: AESGCM.generate_key(bit_length=128)
)
```

**Security Best Practices:**

- **Key Storage**: Never hardcode keys - always use keyring
- **IV Uniqueness**: Never reuse IVs with the same key (handled automatically)
- **AAD Usage**: Use AAD for context binding (e.g., user ID, timestamp)
- **Key Rotation**: Periodically regenerate keys and re-encrypt data
- **Access Control**: Limit keyring access to authorized users only

**Architecture Highlights:**

- **Service Name Modification**: Appends key class name to prevent collisions
  - `"my_app"` + `Fernet` → `"my_app_Fernet"`
  - `"my_app"` + `AESGCM` → `"my_app_AESGCM"`
- **Idempotent**: Multiple calls return same key (no regeneration)
- **Cross-Platform**: Works on Windows, macOS, Linux via `keyring` library
- **No Database**: Keys stored in OS credential manager, not files
- **Separation of Concerns**: Cryptography operations separate from key management

**Best For:**
- Encrypting sensitive application data (passwords, tokens, PII)
- Secure configuration file encryption
- Database credential protection
- API key storage and retrieval
- Multi-user applications requiring per-user encryption
- Applications requiring OS-level security integration
- Compliance with data protection regulations (GDPR, HIPAA)