from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.domain.services.auth_service import AuthService
from src.api.container import ApiContainer


router = APIRouter(prefix="", tags=["auth"])


@router.get("/test")
@inject
async def test(
    auth_service: AuthService = Depends(Provide[ApiContainer.auth_service])
):
    response = await auth_service.test()
    return response
