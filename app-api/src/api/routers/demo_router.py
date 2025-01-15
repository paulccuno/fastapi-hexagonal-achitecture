from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.domain.services.demo_service import DemoService
from src.api.container import ApiContainer


router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/repo_list")
@inject
async def list_demo(
    demo_service: DemoService = Depends(Provide[ApiContainer.demo_service])
):
    response = await demo_service.list_demo()
    return response
