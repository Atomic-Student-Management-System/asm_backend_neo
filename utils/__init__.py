from typing import Literal, Union

import motor.motor_asyncio
import pyotp
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

import config
from models.user import User

db = motor.motor_asyncio.AsyncIOMotorClient(
    config.MONGODB_URI)[config.DATABASE_NAME]

apikey_schema = APIKeyHeader(name='api-key')


async def otp_verify(otp: str) -> Union[None, User]:
    for totp_document in await db['totp_secs'].find().to_list(None):
        sec = totp_document['sec']
        totp = pyotp.TOTP(sec)
        if totp.verify(otp):
            return User(totp_document)
    return None


async def verify(key=Depends(apikey_schema)) -> User:
    result = otp_verify(key)

    if result is None:
        raise HTTPException(status_code=401, detail='身份验证失败')
    else:
        return result
