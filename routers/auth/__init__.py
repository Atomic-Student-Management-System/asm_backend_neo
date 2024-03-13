import fastapi

from routers.auth import rsa_auth, totp

router = fastapi.APIRouter(prefix='/auth')
router.include_router(totp.router)
router.include_router(rsa_auth.router)
