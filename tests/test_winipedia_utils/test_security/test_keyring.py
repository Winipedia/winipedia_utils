"""Tests for winipedia_utils.security.keyring module."""

from base64 import b64encode

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pytest_mock import MockerFixture

from winipedia_utils.security.keyring import (
    get_or_create_aes_gcm,
    get_or_create_fernet,
    get_or_create_key,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_or_create_fernet(mocker: MockerFixture) -> None:
    """Test func for get_or_create_fernet."""
    # Mock keyring functions
    mock_get_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.get_password"
    )
    mock_set_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.set_password"
    )

    service_name = "test_service"
    username = "test_user"

    # Test case 1: Key doesn't exist, should create new one
    mock_get_password.return_value = None

    result = get_or_create_fernet(service_name, username)

    # Verify keyring.get_password was called with correct service name
    expected_service_name = f"{service_name}_Fernet"
    mock_get_password.assert_called_once_with(expected_service_name, username)

    # Verify keyring.set_password was called to store the new key
    assert_with_msg(
        mock_set_password.called,
        "Expected keyring.set_password to be called when creating new key",
    )

    # Test that the returned Fernet can encrypt/decrypt (basic functionality test)
    test_data = b"test_encryption_data"
    encrypted = result.encrypt(test_data)
    decrypted = result.decrypt(encrypted)
    assert_with_msg(
        decrypted == test_data,
        "Expected decrypted data to match original",
    )

    # Test case 2: Key exists, should retrieve existing one
    mock_get_password.reset_mock()
    mock_set_password.reset_mock()

    # Create a test key and encode it
    test_key = Fernet.generate_key()
    encoded_key = b64encode(test_key).decode("ascii")
    mock_get_password.return_value = encoded_key

    result2 = get_or_create_fernet(service_name, username)

    # Verify keyring.set_password was NOT called (key already exists)
    assert_with_msg(
        not mock_set_password.called,
        "Expected keyring.set_password NOT to be called when key exists",
    )

    # Test that the returned Fernet can encrypt/decrypt (basic functionality test)
    encrypted2 = result2.encrypt(test_data)
    decrypted2 = result2.decrypt(encrypted2)
    assert_with_msg(
        decrypted2 == test_data,
        "Expected decrypted data to match original",
    )


def test_get_or_create_aes_gcm(mocker: MockerFixture) -> None:
    """Test func for get_or_create_aes_gcm."""
    # Mock keyring functions
    mock_get_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.get_password"
    )
    mock_set_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.set_password"
    )

    service_name = "test_service"
    username = "test_user"

    # Test case 1: Key doesn't exist, should create new one
    mock_get_password.return_value = None

    result = get_or_create_aes_gcm(service_name, username)

    # Verify keyring.get_password was called with correct service name
    expected_service_name = f"{service_name}_AESGCM"
    mock_get_password.assert_called_once_with(expected_service_name, username)

    # Verify keyring.set_password was called to store the new key
    assert_with_msg(
        mock_set_password.called,
        "Expected keyring.set_password to be called when creating new key",
    )

    # Test that the returned AESGCM can encrypt/decrypt (basic functionality test)
    test_data = b"test_encryption_data"
    test_nonce = b"test_nonce12"  # 12 bytes for AESGCM
    encrypted = result.encrypt(test_nonce, test_data, None)
    decrypted = result.decrypt(test_nonce, encrypted, None)
    assert_with_msg(
        decrypted == test_data,
        "Expected decrypted data to match original",
    )

    # Test case 2: Key exists, should retrieve existing one
    mock_get_password.reset_mock()
    mock_set_password.reset_mock()

    # Create a test key and encode it
    test_key = AESGCM.generate_key(bit_length=256)
    encoded_key = b64encode(test_key).decode("ascii")
    mock_get_password.return_value = encoded_key

    result2 = get_or_create_aes_gcm(service_name, username)

    # Verify keyring.set_password was NOT called (key already exists)
    assert_with_msg(
        not mock_set_password.called,
        "Expected keyring.set_password NOT to be called when key exists",
    )

    # Test that the returned AESGCM can encrypt/decrypt (basic functionality test)
    encrypted2 = result2.encrypt(test_nonce, test_data, None)
    decrypted2 = result2.decrypt(test_nonce, encrypted2, None)
    assert_with_msg(
        decrypted2 == test_data,
        "Expected decrypted data to match original",
    )


def test_get_or_create_key(mocker: MockerFixture) -> None:
    """Test func for get_or_create_key."""
    # Mock keyring functions
    mock_get_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.get_password"
    )
    mock_set_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.set_password"
    )

    service_name = "test_service"
    username = "test_user"

    # Create a mock key class and generate function
    mock_key_class = mocker.MagicMock()
    mock_key_instance = mocker.MagicMock()
    mock_key_class.return_value = mock_key_instance
    mock_key_class.__name__ = "TestKeyClass"

    test_binary_key = b"test_binary_key_data"
    mock_generate_key_func = mocker.MagicMock(return_value=test_binary_key)

    # Test case 1: Key doesn't exist, should create new one
    mock_get_password.return_value = None

    result = get_or_create_key(
        service_name, username, mock_key_class, mock_generate_key_func
    )

    # Verify it returns the mock key instance
    assert_with_msg(
        result is mock_key_instance,
        f"Expected mock key instance, got {result}",
    )

    # Verify keyring.get_password was called with correct service name
    expected_service_name = f"{service_name}_TestKeyClass"
    mock_get_password.assert_called_once_with(expected_service_name, username)

    # Verify generate_key_func was called
    mock_generate_key_func.assert_called_once()

    # Verify keyring.set_password was called with encoded key
    expected_encoded_key = b64encode(test_binary_key).decode("ascii")
    mock_set_password.assert_called_once_with(
        expected_service_name, username, expected_encoded_key
    )

    # Verify key_class was called with the binary key
    mock_key_class.assert_called_once_with(test_binary_key)

    # Test case 2: Key exists, should retrieve existing one
    mock_get_password.reset_mock()
    mock_set_password.reset_mock()
    mock_generate_key_func.reset_mock()
    mock_key_class.reset_mock()
    mock_key_class.return_value = mock_key_instance

    existing_encoded_key = b64encode(test_binary_key).decode("ascii")
    mock_get_password.return_value = existing_encoded_key

    result2 = get_or_create_key(
        service_name, username, mock_key_class, mock_generate_key_func
    )

    # Verify it returns the mock key instance
    assert_with_msg(
        result2 is mock_key_instance,
        f"Expected mock key instance, got {result2}",
    )

    # Verify generate_key_func was NOT called (key already exists)
    assert_with_msg(
        not mock_generate_key_func.called,
        "Expected generate_key_func NOT to be called when key exists",
    )

    # Verify keyring.set_password was NOT called (key already exists)
    assert_with_msg(
        not mock_set_password.called,
        "Expected keyring.set_password NOT to be called when key exists",
    )

    # Verify key_class was called with the decoded binary key
    mock_key_class.assert_called_once_with(test_binary_key)
