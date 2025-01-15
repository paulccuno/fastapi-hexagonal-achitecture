import importlib
import os
from dependency_injector import containers
from typing import List

from fastapi import FastAPI


class DirectoryRouter():

    base_path: str
    api_prefix: str
    packages: List[str]
    routers: List[str]

    def __init__(self, base_path: str, api_prefix: str) -> None:
        self.base_path = base_path
        self.api_prefix = api_prefix
        self.packages = []
        self.routers = []

    def include_packages(self) -> List[str]:
        for root, dirs, files in os.walk(self.base_path):
            if not '__pycache__' in root:
                wiring_package = root.replace('\\', '.').replace('/', '.')

                if not wiring_package in self.packages:
                    self.packages.append(wiring_package)

        return self.packages

    def include_routers(self, app: FastAPI):
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    router_prefix = root.split(
                        self.base_path, 1)[-1].replace('\\', '/')
                    module_path = os.path.relpath(os.path.join(root, file), self.base_path).replace(
                        os.sep, ".").replace(".py", "")

                    # Importar el archivo como un módulo
                    module = importlib.import_module(
                        f"{self.api_prefix}.{module_path}")

                    # Verificar si el módulo tiene un router
                    if hasattr(module, "router"):
                        router = getattr(module, "router")
                        self.routers.append(router)
                        app.include_router(
                            router, prefix=router_prefix)
