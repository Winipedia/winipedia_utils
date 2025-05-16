"""Pytest configuration for winipedia_utils tests.

This module configures pytest plugins for the test suite, setting up the necessary
fixtures and hooks for different test scopes (function, class, module, package, session).
It imports plugins from both the package's testing module and the tests directory,
ensuring that all custom fixtures and test utilities are available to the test suite.
"""

from winipedia_utils.consts import PACKAGE_NAME

tests_to_scopes_route = "tests.base.scopes"
tests_to_func_scope_route = f"{tests_to_scopes_route}.function"
tests_to_class_scope_route = f"{tests_to_scopes_route}.class_"
tests_to_module_scope_route = f"{tests_to_scopes_route}.module"
tests_to_package_scope_route = f"{tests_to_scopes_route}.package"
tests_to_session_scope_route = f"{tests_to_scopes_route}.session"

package_to_tests_route = f"{PACKAGE_NAME}.testing"

custom_plugins = [
    tests_to_func_scope_route,
    tests_to_class_scope_route,
    tests_to_module_scope_route,
    tests_to_package_scope_route,
    tests_to_session_scope_route,
]
package_plugins = [f"{package_to_tests_route}.{p}" for p in custom_plugins]


pytest_plugins = package_plugins + custom_plugins
