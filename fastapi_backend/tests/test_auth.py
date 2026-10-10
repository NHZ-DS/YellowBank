"""Tests unitaires pour la sécurité et le hachage des mots de passe."""

import pytest
from utils import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hashing():
    pwd = "Secr3tPassword!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation_and_decoding():
    data = {"sub": "42", "username": "testuser"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "42"
    assert decoded["username"] == "testuser"
