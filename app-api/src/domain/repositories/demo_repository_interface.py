from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.demo_entity import DemoEntity


class DemoRepositoryInterface(ABC):

    @abstractmethod
    async def list_demo(self) -> List[object]:
        raise NotImplemented

    @abstractmethod
    def get_demo(self, params: DemoEntity) -> DemoEntity:
        raise NotImplemented

    @abstractmethod
    def create_demo(self, params: DemoEntity) -> DemoEntity:
        raise NotImplemented

    @abstractmethod
    def update_demo(self, params: DemoEntity) -> DemoEntity:
        raise NotImplemented

    @abstractmethod
    def delete_demo(self, params: DemoEntity) -> DemoEntity:
        raise NotImplemented

    @abstractmethod
    def validate_exist_demo(self, params: DemoEntity) -> DemoEntity:
        raise NotImplemented
