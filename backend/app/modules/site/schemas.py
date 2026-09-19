import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)


class SiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    created_at: datetime
