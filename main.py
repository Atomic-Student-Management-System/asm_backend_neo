from typing import Union

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, student

app = fastapi.FastAPI()
app.include_router(auth.router)
app.include_router(student.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
