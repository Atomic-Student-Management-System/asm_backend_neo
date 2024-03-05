from typing import Literal

import pydantic


class Student(pydantic.BaseModel):
    name: str


class StudentIntegralUpdate(pydantic.BaseModel):
    name: str
    type: Literal['add', 'remove']
    score: float
    time: float
    reason: str
