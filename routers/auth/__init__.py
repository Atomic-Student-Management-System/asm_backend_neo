import fastapi

from routers.auth import totp

router = fastapi.APIRouter(prefix='/auth')
router.include_router(totp.router)
