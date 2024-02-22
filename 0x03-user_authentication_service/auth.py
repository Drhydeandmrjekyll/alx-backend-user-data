#!/usr/bin/env python3
"""
Module to hash_password and interact with auth_DB
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
        Hashes a password using bcrypt
        password: Raw bunhashed password
        return: Hashed password as bytes.
    """
    encoded_pwd = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)

    return hashed_pwd


if __name__ == '__main__':
    print(_hash_password("password"))
