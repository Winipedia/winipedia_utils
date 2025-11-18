"""Tests for winipedia_utils.security.cryptography module."""

import pytest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pyrig.src.testing.assertions import assert_with_msg

from winipedia_utils.src.security.cryptography import (
    IV_LEN,
    decrypt_with_aes_gcm,
    encrypt_with_aes_gcm,
)


def test_encrypt_with_aes_gcm() -> None:
    """Test func for encrypt_with_aes_gcm."""
    # Create an AESGCM instance for testing
    key = AESGCM.generate_key(bit_length=256)
    aes_gcm = AESGCM(key)

    # Test data
    test_data = b"Hello, World! This is test data for encryption."

    # Test encryption without AAD
    encrypted_result = encrypt_with_aes_gcm(aes_gcm, test_data)

    # Verify the result is bytes
    assert_with_msg(
        isinstance(encrypted_result, bytes),
        f"Expected bytes result, got {type(encrypted_result)}",
    )

    # Verify the result is longer than original data (includes IV + encrypted data)
    assert_with_msg(
        len(encrypted_result) > len(test_data),
        f"Expected encrypted result to be longer than original data, "
        f"got {len(encrypted_result)} vs {len(test_data)}",
    )

    # Verify the result starts with IV (first IV_LEN bytes)
    assert_with_msg(
        len(encrypted_result) >= IV_LEN,
        f"Expected encrypted result to be at least {IV_LEN} bytes long, "
        f"got {len(encrypted_result)}",
    )

    # Test encryption with AAD
    test_aad = b"additional_authenticated_data"
    encrypted_with_aad = encrypt_with_aes_gcm(aes_gcm, test_data, test_aad)

    # Verify AAD encryption also works
    assert_with_msg(
        isinstance(encrypted_with_aad, bytes),
        f"Expected bytes result with AAD, got {type(encrypted_with_aad)}",
    )

    assert_with_msg(
        len(encrypted_with_aad) > len(test_data),
        f"Expected encrypted result with AAD to be longer than original data, "
        f"got {len(encrypted_with_aad)} vs {len(test_data)}",
    )

    # Verify that encryption with different AAD produces different results
    different_aad = b"different_aad"
    encrypted_different_aad = encrypt_with_aes_gcm(aes_gcm, test_data, different_aad)

    assert_with_msg(
        encrypted_with_aad != encrypted_different_aad,
        "Expected different AAD to produce different encrypted results",
    )

    # Test that multiple encryptions of same data produce different results
    # (due to random IV)
    encrypted_again = encrypt_with_aes_gcm(aes_gcm, test_data)
    assert_with_msg(
        encrypted_result != encrypted_again,
        "Expected multiple encryptions to produce different results due to random IV",
    )


def test_decrypt_with_aes_gcm() -> None:
    """Test func for decrypt_with_aes_gcm."""
    # Create an AESGCM instance for testing
    key = AESGCM.generate_key(bit_length=256)
    aes_gcm = AESGCM(key)

    # Test data
    test_data = b"Hello, World! This is test data for decryption."

    # Test encryption and decryption without AAD
    encrypted_data = encrypt_with_aes_gcm(aes_gcm, test_data)
    decrypted_data = decrypt_with_aes_gcm(aes_gcm, encrypted_data)

    # Verify decryption returns original data
    assert_with_msg(
        decrypted_data == test_data,
        f"Expected decrypted data to match original, "
        f"got {decrypted_data!r} vs {test_data!r}",
    )

    # Test encryption and decryption with AAD
    test_aad = b"additional_authenticated_data"
    encrypted_with_aad = encrypt_with_aes_gcm(aes_gcm, test_data, test_aad)
    decrypted_with_aad = decrypt_with_aes_gcm(aes_gcm, encrypted_with_aad, test_aad)

    # Verify decryption with AAD returns original data
    assert_with_msg(
        decrypted_with_aad == test_data,
        f"Expected decrypted data with AAD to match original, "
        f"got {decrypted_with_aad!r} vs {test_data!r}",
    )

    # Test that decryption with wrong AAD fails
    wrong_aad = b"wrong_aad"
    with pytest.raises(InvalidTag):  # InvalidTag from cryptography library
        decrypt_with_aes_gcm(aes_gcm, encrypted_with_aad, wrong_aad)

    # Test that decryption without AAD when AAD was used fails
    with pytest.raises(InvalidTag):  # InvalidTag from cryptography library
        decrypt_with_aes_gcm(aes_gcm, encrypted_with_aad, None)

    # Test round-trip with empty data
    empty_data = b""
    encrypted_empty = encrypt_with_aes_gcm(aes_gcm, empty_data)
    decrypted_empty = decrypt_with_aes_gcm(aes_gcm, encrypted_empty)

    assert_with_msg(
        decrypted_empty == empty_data,
        f"Expected decrypted empty data to match original, "
        f"got {decrypted_empty!r} vs {empty_data!r}",
    )

    # Test round-trip with large data
    large_data = b"x" * 10000  # 10KB of data
    encrypted_large = encrypt_with_aes_gcm(aes_gcm, large_data)
    decrypted_large = decrypt_with_aes_gcm(aes_gcm, encrypted_large)

    assert_with_msg(
        decrypted_large == large_data,
        f"Expected decrypted large data to match original, "
        f"got length {len(decrypted_large)} vs {len(large_data)}",
    )
