from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware

from src.infraestructure.container import AppContainer
from src.external_services.container import ExternalServicesContainer
from src.api.container import ApiContainer, directory_router


def register_events(app: FastAPI):
    app.on_event("startup")  # (""" Some function event """)
    app.on_event("shutdown")  # (""" Some function event """)


app_container = AppContainer()
app = app_container.app()
settings = app_container.settings()
logger = app_container.logger()

external_services_container = ExternalServicesContainer(
    app_container=app_container
)
api_container = ApiContainer(
    app_container=app_container,
    external_services_container=external_services_container
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FASTAPI_CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)
app.add_middleware(app_container.error_handler_middleware)
app.add_middleware(api_container.header_handler_middleware)

register_events(app)
directory_router.include_routers(app)
