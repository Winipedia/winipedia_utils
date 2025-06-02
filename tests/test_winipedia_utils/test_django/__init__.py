"""__init__ module."""

from winipedia_utils import django
from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)

logger.info(
    "Imported django: %s to setup django in tests for winipedia_utils.django",
    django,
)
