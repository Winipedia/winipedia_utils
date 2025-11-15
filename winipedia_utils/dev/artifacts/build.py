"""Build artifacts for the project."""

from winipedia_utils.dev.artifacts.builder.base.base import Builder


def build() -> None:
    """Build all artifacts."""
    Builder.init_all_non_abstract_subclasses()
