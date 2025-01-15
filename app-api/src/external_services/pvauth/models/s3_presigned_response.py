from typing import List
from pydantic import BaseModel


class S3PresignedValueResponse(BaseModel):
    key: str
    presigned: str


class S3PresignedResponse(BaseModel):
    Status: bool
    State: int
    Message: str
    Value: List[S3PresignedValueResponse]
