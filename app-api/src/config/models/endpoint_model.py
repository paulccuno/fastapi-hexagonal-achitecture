from pydantic import BaseModel


class EndpointModel(BaseModel):

    path: str
    method: str
