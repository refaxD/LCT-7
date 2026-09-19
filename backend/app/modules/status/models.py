import uuid
from datetime import date
from enum import StrEnum

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.schedule.models import Stage
from app.modules.status.enums import Confidence, StageStatusValue


def _in_clause(column: str, values: type[StrEnum]) -> str:
    return f"{column} IN ({', '.join(repr(str(value)) for value in values)})"


class StageStatus(Base):
    __tablename__ = "stage_statuses"
    __table_args__ = (
        UniqueConstraint("stage_id", "as_of", name="uq_stage_statuses_stage_as_of"),
        CheckConstraint(_in_clause("status", StageStatusValue), name="ck_stage_statuses_status"),
        CheckConstraint(
            f"confidence IS NULL OR {_in_clause('confidence', Confidence)}",
            name="ck_stage_statuses_confidence",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    stage_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stages.id", ondelete="CASCADE"), index=True
    )
    as_of: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(16))
    delay_days: Mapped[int | None] = mapped_column(Integer, default=None)
    basis: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[str | None] = mapped_column(String(8), default=None)
    evidence_dates: Mapped[list[str]] = mapped_column(JSON, default=list)

    # lazy="selectin": роутер собирает ответ из этапа, а тянуть его лениво в async нельзя
    stage: Mapped[Stage] = relationship(lazy="selectin")
