from typing import Optional

import pydantic


class TotpSec(pydantic.BaseModel):
    """Totp密钥"""
    time: int
    sec: str
    url: str


class RSAKey(pydantic.BaseModel):
    """RSA密钥"""
    time: Optional[int] = None
    pubkey: str
    pubkey_sha1: str
