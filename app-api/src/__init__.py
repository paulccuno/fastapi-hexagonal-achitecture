from src.api.app import app, settings


def start_web_server():
    import uvicorn

    uvicorn.run(
        app,
        host=settings.FASTAPI_RUN_HOST,
        port=settings.FASTAPI_RUN_PORT,
        log_level="debug",
    )
