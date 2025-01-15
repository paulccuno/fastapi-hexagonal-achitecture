from src.domain.base_entity import BaseEntity


class DemoEntity(BaseEntity):
    def __init__(self, id, value):
        self.id = id
        self.value = value
