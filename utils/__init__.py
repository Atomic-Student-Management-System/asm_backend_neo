from typing import Literal

import motor.motor_asyncio
import pyotp

import config

db = motor.motor_asyncio.AsyncIOMotorClient(
    config.MONGODB_URI)[config.DATABASE_NAME]


async def otp_verify(otp: str) -> bool:
    result = False
    for totp_document in await db['totp_secs'].find().to_list(None):
        sec = totp_document['sec']
        totp = pyotp.TOTP(sec)
        if totp.verify(otp):
            result = True
    return result


async def verify(type: Literal['TOTP'] = 'TOTP', otp=None):
    if type == 'TOTP':
        return otp_verify(otp)
