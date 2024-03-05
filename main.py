from typing import Union

import fastapi

from routers import auth, student

app = fastapi.FastAPI()
app.include_router(auth.router)
app.include_router(student.router)
