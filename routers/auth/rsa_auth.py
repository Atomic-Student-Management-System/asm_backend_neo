import json
import time
from hashlib import sha1

import fastapi
import pydantic
import rsa
from fastapi import HTTPException

from models.user import RSAKey
from utils import db, rsa_verify

router = fastapi.APIRouter(prefix='/rsa')


@router.post('/submit_pubkey', tags=['验证', 'RSA'], response_model=RSAKey, name='新增RSA公钥', description='传入的 time 参数无效')
async def handle_submit_pubkey(pubkey: RSAKey):
    rsakey = RSAKey(time=int(time.time()), pubkey=pubkey.pubkey,
                    pubkey_sha1=pubkey.pubkey_sha1)

    insert_result = await db['rsa'].insert_one(rsakey.model_dump())
    data = await db['rsa'].find_one({'_id': insert_result.inserted_id})

    return data


@router.get('/verify_apikey', tags=['验证', 'RSA'], response_model=RSAKey, name='验证RSA签名的Apikey')
async def handle_verify_apikey(apikey: str):
    return await rsa_verify(apikey)
