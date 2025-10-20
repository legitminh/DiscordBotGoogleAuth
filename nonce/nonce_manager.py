"""
Create and validate one-time nonces for secure operations.
"""

import secrets
import time
from typing import Dict
import os
import jsonDatabase
import pathlib
# import nonce_to_userId

# In-memory store for nonces (token: expiration)
NONCE_EXPIRY_SECONDS = 300  # 5 minutes
dbFile = os.path.join(pathlib.Path(__file__).parent,"link_token_to_userId.json")
database = jsonDatabase.createDatabase(dbFile) 

def generate_nonce() -> str:
    """Generate a secure random token and store it with an expiry."""
    nonce = secrets.token_urlsafe(32)
    return nonce

def generate_nonce_linked(linkedId, createdTime = -1):
    nonce = generate_nonce()
    database(jsonDatabase.set, nonce, {"id": linkedId, "createdTime":createdTime})
    return nonce

# def generate_user_auth(userId):
#     nonce_to_userId.set(generate_nonce(), {userId})