from typing import List

import fastapi
import pydantic
from fastapi import Depends, HTTPException, Response

from models.student import Student, StudentIntegralUpdate
from models.user import User
from utils import db, verify

router = fastapi.APIRouter(prefix='/student')


@router.get('/', response_model=List[Student], name='获取所有学生', tags=['学生'])
async def handle_get_students():
    students = db['students'].find()
    return await students.to_list(None)


@router.get('/{name}', response_model=float, name='获取操行分', tags=['学生'])
async def handle_get_student_integral(name: str):
    student = await db['students'].find_one({'name': name})
    if student is None:
        raise HTTPException(status_code=404, detail='学生不存在')

    integral_update_records = db['integral'].find({'name': student['name']})

    integral = 0
    for record in await integral_update_records.to_list(None):
        if record['type'] == 'add':
            integral += record['score']
        elif record['type'] == 'remove':
            integral -= record['score']

    return integral


@router.post('/', response_model=Student, name='创建学生', tags=['学生'])
async def handle_create_student(student: Student, user: User = Depends(verify)):
    inserted_id = (await db['students'].insert_one(student.model_dump())).inserted_id
    inserted_doc = await db['students'].find_one({'_id': inserted_id})

    return inserted_doc


@router.get('/integral_update_records', response_model=List[StudentIntegralUpdate], name='获取积分更新记录', tags=['学生'])
async def handle_get_integral_update_records():
    records = db['integral'].find()
    return await records.to_list(None)


@router.post('/integral_update_records', response_model=StudentIntegralUpdate, name='创建积分更新记录', tags=['学生'])
async def handle_create_integral_update_record(record: StudentIntegralUpdate, user: User = Depends(verify)):
    if (await db['students'].find_one({'name': record.name})) is None:
        raise HTTPException(status_code=404, detail='学生不存在')

    inserted_id = (await db['integral'].insert_one(record.model_dump())).inserted_id
    inserted_doc = await db['integral'].find_one({'_id': inserted_id})

    return inserted_doc
