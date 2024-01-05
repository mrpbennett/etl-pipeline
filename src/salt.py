""" Salting of PII information

This function accepts a string to be passed so it can be hashed ready for storage
in database tables

Typical usage example:

   hash_pii('some_sensitive_string')
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
