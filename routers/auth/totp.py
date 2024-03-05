import datetime
import io
import random
import tempfile
from typing import Literal

import fastapi
import pydantic
import pyotp
import qrcode
from fastapi import HTTPException, Response
from fastapi.responses import FileResponse
from PIL import Image
from qrcode.main import QRCode

import config
from utils import db, otp_verify

router = fastapi.APIRouter(prefix='/totp')


@router.get('/bind', response_class=FileResponse, name='绑定 TOTP 密钥', tags=['验证', 'TOTP'])
async def handle_totp_bind(admin_password: str):
    if admin_password != config.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=403,
            detail='管理员密码错误'
        )

    sec = pyotp.random_base32()
    otp = pyotp.TOTP(
        sec, name=f'atomic_student_manager_{random.randint(0, 1e4)}')
    qr = QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_H
    )

    qr.add_data(otp.provisioning_uri(otp.name))
    qr.make()
    qr_img = qr.make_image()
    qr_img_bytes = io.BytesIO()
    qr_img.save(qr_img_bytes, 'PNG')
    qr_img_bytes.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        qr_img.save(temp_file, "PNG")
        temp_file_path = temp_file.name

    await db['totp_secs'].insert_one({
        'time': datetime.datetime.now().timestamp(),
        'sec': sec,
        'url': otp.provisioning_uri(otp.name)
    })

    # return Response(content=qr_img_bytes.getvalue(), media_type='image/png')
    return temp_file_path


class HandleVerifyResponse(pydantic.BaseModel):
    code: Literal[200, -2]
    data: dict
    message: Literal['验证成功', '验证失败']


@router.get('/verify', response_model=HandleVerifyResponse, name='验证 TOTP 数字', tags=['验证', 'TOTP'])
async def handle_verify(otp: str):
    if await otp_verify(otp):
        return {
            'code': 200,
            'message': '验证成功',
            'data': {}
        }
    else:
        return {
            'code': -2,
            'message': '验证失败',
            'data': {}
        }
