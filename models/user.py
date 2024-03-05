import pydantic


class User(pydantic.BaseModel):
    """用户"""
    time: int
    sec: str
    url: str
