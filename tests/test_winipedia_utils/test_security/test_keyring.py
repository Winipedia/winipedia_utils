"""Tests for winipedia_utils.security.keyring module."""

from base64 import b64encode

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pytest_mock import MockerFixture

from winipedia_utils.security.keyring import (
    get_key_as_str,
    get_or_create_aes_gcm,
    get_or_create_fernet,
    get_or_create_key,
    make_service_name,
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

    fernet_instance, binary_key = get_or_create_fernet(service_name, username)

    # Verify keyring.get_password was called with correct service name
    expected_service_name = f"{service_name}_Fernet"
    mock_get_password.assert_called_once_with(expected_service_name, username)

    # Verify keyring.set_password was called to store the new key
    assert_with_msg(
        mock_set_password.called,
        "Expected keyring.set_password to be called when creating new key",
    )

    # Verify that binary_key is returned
    assert_with_msg(
        isinstance(binary_key, bytes),
        "Expected binary_key to be bytes",
    )

    # Test that the returned Fernet can encrypt/decrypt (basic functionality test)
    test_data = b"test_encryption_data"
    encrypted = fernet_instance.encrypt(test_data)
    decrypted = fernet_instance.decrypt(encrypted)
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

    fernet_instance2, binary_key2 = get_or_create_fernet(service_name, username)

    # Verify keyring.set_password was NOT called (key already exists)
    assert_with_msg(
        not mock_set_password.called,
        "Expected keyring.set_password NOT to be called when key exists",
    )

    # Verify that binary_key is returned
    assert_with_msg(
        isinstance(binary_key2, bytes),
        "Expected binary_key to be bytes",
    )

    # Test that the returned Fernet can encrypt/decrypt (basic functionality test)
    encrypted2 = fernet_instance2.encrypt(test_data)
    decrypted2 = fernet_instance2.decrypt(encrypted2)
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

    aesgcm_instance, binary_key = get_or_create_aes_gcm(service_name, username)

    # Verify keyring.get_password was called with correct service name
    expected_service_name = f"{service_name}_AESGCM"
    mock_get_password.assert_called_once_with(expected_service_name, username)

    # Verify keyring.set_password was called to store the new key
    assert_with_msg(
        mock_set_password.called,
        "Expected keyring.set_password to be called when creating new key",
    )

    # Verify that binary_key is returned
    assert_with_msg(
        isinstance(binary_key, bytes),
        "Expected binary_key to be bytes",
    )

    # Test that the returned AESGCM can encrypt/decrypt (basic functionality test)
    test_data = b"test_encryption_data"
    test_nonce = b"test_nonce12"  # 12 bytes for AESGCM
    encrypted = aesgcm_instance.encrypt(test_nonce, test_data, None)
    decrypted = aesgcm_instance.decrypt(test_nonce, encrypted, None)
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

    aesgcm_instance2, binary_key2 = get_or_create_aes_gcm(service_name, username)

    # Verify keyring.set_password was NOT called (key already exists)
    assert_with_msg(
        not mock_set_password.called,
        "Expected keyring.set_password NOT to be called when key exists",
    )

    # Verify that binary_key is returned
    assert_with_msg(
        isinstance(binary_key2, bytes),
        "Expected binary_key to be bytes",
    )

    # Test that the returned AESGCM can encrypt/decrypt (basic functionality test)
    encrypted2 = aesgcm_instance2.encrypt(test_nonce, test_data, None)
    decrypted2 = aesgcm_instance2.decrypt(test_nonce, encrypted2, None)
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

    key_instance, binary_key_result = get_or_create_key(
        service_name, username, mock_key_class, mock_generate_key_func
    )

    # Verify it returns the mock key instance and binary key
    assert_with_msg(
        key_instance is mock_key_instance,
        f"Expected mock key instance, got {key_instance}",
    )
    assert_with_msg(
        binary_key_result == test_binary_key,
        f"Expected {test_binary_key!r}, got {binary_key_result!r}",
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

    key_instance2, binary_key_result2 = get_or_create_key(
        service_name, username, mock_key_class, mock_generate_key_func
    )

    # Verify it returns the mock key instance and binary key
    assert_with_msg(
        key_instance2 is mock_key_instance,
        f"Expected mock key instance, got {key_instance2}",
    )
    assert_with_msg(
        binary_key_result2 == test_binary_key,
        f"Expected {test_binary_key!r}, got {binary_key_result2!r}",
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


def test_get_key_as_str(mocker: MockerFixture) -> None:
    """Test func for get_key_as_str."""
    # Mock keyring functions
    mock_get_password = mocker.patch(
        "winipedia_utils.security.keyring.keyring.get_password"
    )
    service_name = "test_service"
    username = "test_user"
    mock_key_class = mocker.MagicMock()
    mock_key_class.__name__ = "TestKeyClass"
    expected_service_name = f"{service_name}_{mock_key_class.__name__}"
    mock_get_password.return_value = "test_key"
    result = get_key_as_str(service_name, username, mock_key_class)
    mock_get_password.assert_called_once_with(expected_service_name, username)
    assert_with_msg(result == "test_key", f"Expected 'test_key', got {result}")
    mock_get_password.return_value = None
    result = get_key_as_str(service_name, username, mock_key_class)
    assert_with_msg(result is None, f"Expected None, got {result}")
    mock_get_password.assert_called_with(expected_service_name, username)


def test_make_service_name(mocker: MockerFixture) -> None:
    """Test func for make_service_name."""
    service_name = "test_service"
    mock_key_class = mocker.MagicMock()
    mock_key_class.__name__ = "TestKeyClass"
    result = make_service_name(service_name, mock_key_class)
    expected = f"{service_name}_{mock_key_class.__name__}"
    assert_with_msg(result == expected, f"Expected '{expected}', got '{result}'")
