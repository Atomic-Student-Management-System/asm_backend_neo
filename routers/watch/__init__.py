import datetime
from typing import List, Optional

import fastapi
from fastapi import APIRouter, Query

from models.watcher import WatchLog
from utils import db

router = APIRouter(prefix='/watch')


@router.get('/logs/', response_model=list[WatchLog], name='查询监控记录', tags=['监控'])
async def handle_get_watch_logs(
    start_time: Optional[datetime.datetime] = datetime.datetime.fromtimestamp(
        0),
    end_time: Optional[datetime.datetime] = datetime.datetime.fromtimestamp(
        3376656000),
    computer: Optional[str] = None
):
    q = {'time': {'$gte': start_time, '$lte': end_time}}

    if computer is not None:
        q['computer'] = computer

    records = await db['watch_logs'].find(q).sort('time', direction=-1).to_list(None)
    return records


@router.post('/logs', response_model=WatchLog, name='添加监控记录', tags=['监控'])
async def handle_add_watch_log(record: WatchLog):
    inserted = await db['watch_logs'].insert_one(record.model_dump())
    result = await db['watch_logs'].find_one({'_id': inserted.inserted_id})

    return result
