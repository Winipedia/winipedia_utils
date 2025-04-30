"""This module contains string manipulation utilities for the winipedia_utils package."""

import hashlib
import textwrap
from io import StringIO
from typing import Any
from urllib.parse import urlparse, urlunparse
from xml.etree import ElementTree as ET

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.logging.logger import get_logger
from utils.multiprocessing import cancel_on_timeout_with_multiprocessing

logger = get_logger(__name__)


def find_best_fit_for_text(given_text: str, text_list: list[str]) -> tuple[str, float]:
    # Combine the given text with the text list for vectorization
    texts = [given_text, *text_list]

    # Vectorize the texts using TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(texts)

    # Compute the cosine similarity matrix
    cosine_sim: np.ndarray[Any, Any] = cosine_similarity(
        vectorizer[0:1],
        vectorizer[1:],
    )

    # Find the index of the best fit text
    best_fit_index = np.argmax(cosine_sim)

    # Get the best fit text and its similarity score
    best_fit_text = text_list[best_fit_index]
    best_fit_score = cosine_sim[0, best_fit_index]
    best_fit_score = round(best_fit_score, 2)

    return best_fit_text, best_fit_score


def remove_query_params_from_url(url: str) -> str:
    """A function that removes query parameters from a URL.

    :param url: The input URL.
    :return: The URL without query parameters.
    """
    # Parse the URL into components
    parsed_url = urlparse(url)

    # Reconstruct the URL without query parameters
    stripped_url = urlunparse(parsed_url._replace(query=""))

    return str(stripped_url)


def ask_for_input_with_timeout(prompt: str, timeout: int) -> str:
    """A function that asks for user input with a timeout.

    :param prompt: The input prompt.
    :param timeout: The timeout in seconds.
    :return: The user input or an empty string if the timeout is reached.
    """

    @cancel_on_timeout_with_multiprocessing(timeout, "Input not given within the timeout")
    def give_input() -> str:
        return input(prompt)

    user_input: str = give_input()

    return user_input


def get_new_unique_character_for_str(str_: str) -> str:
    """Find a character that is not present in the given string.

    Args:
        str_: The input string to check against

    Returns:
        A character that is not present in the input string

    Raises:
        ValueError: If no unique character can be found

    """
    # Use string.punctuation for a more comprehensive set of special characters
    from string import punctuation

    # Convert input string to set for O(1) lookups
    existing_chars = set(str_)

    # Check each punctuation character
    for char in punctuation:
        if char not in existing_chars:
            logger.info(f"Found unique character: {char} for given string")
            return char

    # If no punctuation character works, try whitespace characters
    whitespace_chars = {"\t", "\n", "\r", " "}
    for char in whitespace_chars:
        if char not in existing_chars:
            logger.info(f"Found unique character: {char} for given string")
            return char

    msg = "No unique character found in standard character sets"
    raise ValueError(msg)


def to_stripped_str(value: Any) -> str:
    return str(value).strip()


def to_lower_stripped_str(value: Any) -> str:
    return to_stripped_str(value).lower()


def find_xml_namespaces(xml_io_str: Any) -> dict[str, str]:
    xml_io_str = to_str_io(xml_io_str)
    # Extract the namespaces from the root tag
    namespaces_: dict[str, str] = {}
    for _, elem in ET.iterparse(xml_io_str, events=["start-ns"]):
        prefix, uri = elem
        namespaces_[prefix] = uri

    _ = namespaces_.pop("", None)

    return namespaces_


def to_str_io(string: Any) -> StringIO:
    if isinstance(string, str):
        return StringIO(string)
    if isinstance(string, StringIO):
        return string
    msg = "Input must be a string or StringIO object"
    raise ValueError(msg)


def get_variable_name(var: str):
    """Expects an f-string literal like: f'{variable_name=}' which allows name extraction.
    A normal string like 'variable_name' will return 'variable_name', like normal.
    """
    var = var.split("=")[0]
    # sometimes we give smth like self.variable_name, so we need to remove the self.
    return var.split(".")[-1]


def value_to_truncated_string(value: Any, max_length: int) -> str:
    string = str(value)
    return textwrap.shorten(string, width=max_length, placeholder="...")


def get_reusable_hash(value: Any) -> str:
    """Get a hash that is reusable across different python instances, or any values like strings also across sessions."""
    value_str = str(value)
    return hashlib.sha256(value_str.encode("utf-8")).hexdigest()
