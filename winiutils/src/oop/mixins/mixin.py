"""Mixin utilities for class composition and behavior extension.

This module provides metaclasses and mixins that facilitate class composition
through the mixin pattern. It includes utilities for:
- Automatic method logging with performance tracking
- Abstract class implementation enforcement with type checking
- Combined metaclasses that merge multiple behaviors

These utilities help create robust class hierarchies with proper implementation
enforcement and built-in logging capabilities.
"""

import logging

from winiutils.src.oop.mixins.meta import ABCLoggingMeta

logger = logging.getLogger(__name__)


class ABCLoggingMixin(metaclass=ABCLoggingMeta):
    """Mixin class that provides automatic method logging with performance tracking.

    This mixin can be used as a base class for other mixins that need:
    - Automatic method logging (from LoggingMeta)

    """
