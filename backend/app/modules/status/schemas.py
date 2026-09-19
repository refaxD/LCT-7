from datetime import date

from pydantic import BaseModel, Field

from app.modules.status.enums import Confidence, StageStatusValue


class PlannedWindow(BaseModel):
    start: date | None
    end: date | None


class StageStatusUpsert(BaseModel):
    stage_code: str
    status: StageStatusValue
    delay_days: int | None = None
    basis: str = ""
    confidence: Confidence | None = None
    evidence_dates: list[date] = Field(default_factory=list)


class SiteStatusUpsert(BaseModel):
    as_of: date
    stages: list[StageStatusUpsert]


class StageStatusRead(BaseModel):
    stage_code: str
    stage_name: str
    planned: PlannedWindow
    status: StageStatusValue
    delay_days: int | None
    evidence_dates: list[date]
    basis: str
    confidence: Confidence | None


class SiteStatusRead(BaseModel):
    site_id: str
    as_of: date
    stages: list[StageStatusRead]
