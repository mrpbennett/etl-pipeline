"""
This module provides a function for salting Personally Identifiable Information (PII) and hashing it.

The `hash_pii` function takes a string of sensitive information (PII) as input and returns the hashed PII information ready for storage. The function uses salting to enhance the security of the hashed PII.

Salting involves appending a random string of characters to the original PII before hashing it. This random string is generated using the `random.choices` function from the `random` module and consists of 30 characters from the ASCII letters.

The function uses the SHA-512 hashing algorithm from the `hashlib` module to compute the hash of the salted PII. The resulting hash is then converted to a number using the `struct.unpack` function from the `struct` module.

If the input PII is not a valid string or is empty, a `ValueError` is raised.

Example usage:
    hashed_pii = hash_pii("John Doe")
    print(hashed_pii)  # Output: '1234567890'
"""
import hashlib
import random
import string
import struct


def hash_pii(pii: str) -> str:
    """
    Function for Salting PII information

    Hashes PII with salting

    Args:
        pii: string of sensitive information to be hashed

    Returns:
        Hashed PII information ready for storage

    Raises:
        ValueError: If the input is not a valid string or is empty.
    """
    if not isinstance(pii, str) or not pii:
        raise ValueError("Invalid input: PII must be a non-empty string.")

    hash_object = hashlib.sha512(
        (pii + "".join(random.choices(string.ascii_letters, k=30))).encode("ascii")
    ).digest()
    number = struct.unpack(">Q", b"\x00" + hash_object[:7])[0]
    return str(number)
