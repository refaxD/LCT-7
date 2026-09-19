import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Stage(Base):
    __tablename__ = "stages"
    __table_args__ = (UniqueConstraint("site_id", "code", name="uq_stages_site_code"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    code: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(255))
    # UC-1: дат в файле может не быть, инженер проставляет их потом руками
    planned_start: Mapped[date | None] = mapped_column(Date, default=None)
    planned_end: Mapped[date | None] = mapped_column(Date, default=None)
    checkable_by_equipment: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
