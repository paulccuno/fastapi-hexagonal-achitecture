from typing import List, Optional
from pydantic import BaseModel


class S3PresignedRequest(BaseModel):

    bucket: str
    key: List[str]
    duration: Optional[int]
