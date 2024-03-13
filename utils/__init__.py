import base64
import datetime
import json
from typing import Literal, Union

import motor.motor_asyncio
import pyotp
import rsa
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

import config
from models.user import RSAKey, TotpSec

db = motor.motor_asyncio.AsyncIOMotorClient(
    config.MONGODB_URI)[config.DATABASE_NAME]

apikey_schema = APIKeyHeader(name='api-key')


async def otp_verify(otp: str) -> Union[None, TotpSec]:
    for totp_document in await db['totp_secs'].find().to_list(None):
        sec = totp_document['sec']
        totp = pyotp.TOTP(sec)
        if totp.verify(otp):
            return TotpSec(totp_document)
    raise HTTPException(status_code=401, detail='身份验证失败')


async def rsa_verify(apikey: str) -> RSAKey:
    apikey: list = apikey.split('.')
    header = json.loads(apikey[0])
    payload: str = apikey[1]
    sign: str = apikey[2]

    rsa_document = await db['rsa'].find_one({'pubkey_sha1': header['pubkey_hash']})
    if rsa_document is None:
        raise HTTPException(status_code=401, detail='身份验证失败，找不到公钥')

    rsakey = RSAKey(**rsa_document)

    if rsakey.pubkey_sha1 == header['pubkey_hash']:
        pubkey = rsa.PublicKey.load_pkcs1(rsakey.pubkey.encode('utf-8'))
        try:
            rsa.verify(payload.encode('utf-8'),
                       base64.b64decode(sign), pubkey)

            # 检查有效期
            payload_dict = json.loads(payload)
            if datetime.datetime.now() - datetime.datetime.fromtimestamp(payload_dict['generate']) > config.APIKEY_EXPIRY:
                raise HTTPException(status_code=401, detail='身份验证失败，APIKEY已过期')

            return rsakey
        except rsa.VerificationError:
            raise HTTPException(status_code=401, detail='身份验证失败')


async def verify(key=Depends(apikey_schema)) -> TotpSec:
    try:
        key = int(key)
        result = otp_verify(key)
    except ValueError:
        result = rsa_verify(key)

    return result
