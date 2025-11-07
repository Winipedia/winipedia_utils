"""module for the following module path (maybe truncated).

tests.base.scopes.session
"""

import re

from winipedia_utils.modules.module import to_path
from winipedia_utils.projects.poetry import dev_deps
from winipedia_utils.projects.poetry.config import PyprojectConfigFile
from winipedia_utils.projects.poetry.dev_deps import DEV_DEPENDENCIES
from winipedia_utils.testing.fixtures import autouse_session_fixture


@autouse_session_fixture
def assert_dev_dependencies_config_is_correct() -> None:
    """Verify that the dev dependencies in consts.py are correct.

    If not it dumps the correct config to consts.py.
    """
    expected_dev_deps = PyprojectConfigFile.get_dev_dependencies()
    actual_dev_deps = DEV_DEPENDENCIES

    if expected_dev_deps == actual_dev_deps:
        return

    path = to_path(module_name=dev_deps, is_package=False)
    content = path.read_text()
    # replace DEV_DEPENDENCIES = {.*} with the correct value with re
    new_content = re.sub(
        r"DEV_DEPENDENCIES: set\[str\] = \{.*\}",
        f"DEV_DEPENDENCIES: set[str] = {expected_dev_deps}",
        content,
        flags=re.DOTALL,
    )
    path.write_text(new_content)
