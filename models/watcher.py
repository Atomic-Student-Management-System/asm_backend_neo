import datetime

import pydantic


class WatchLog(pydantic.BaseModel):
    computer: str
    time: datetime.datetime
    operation: str
    data: dict
    describe: str
