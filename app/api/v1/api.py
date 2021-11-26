from fastapi import APIRouter

from .endpoints import prizebonds
router = APIRouter()


router.include_router(prizebonds.router, prefix="/prizebonds", tags=["Prize bonds"])

