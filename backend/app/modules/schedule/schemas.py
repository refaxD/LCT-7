import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class StageCreate(BaseModel):
    code: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=255)
    planned_start: date | None = None
    planned_end: date | None = None
    checkable_by_equipment: bool = True


class ScheduleImport(BaseModel):
    stages: list[StageCreate]


class StageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    planned_start: date | None
    planned_end: date | None
    checkable_by_equipment: bool
