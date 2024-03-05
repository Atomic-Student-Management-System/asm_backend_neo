import fastapi

from routers import auth

app = fastapi.FastAPI()
app.include_router(auth.router)
