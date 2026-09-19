"""sites, stages, stage_statuses

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

STATUS_VALUES = "'ahead', 'on_track', 'behind', 'not_started', 'not_observed', 'not_checkable'"
CONFIDENCE_VALUES = "'low', 'medium', 'high'"


def upgrade() -> None:
    op.create_table(
        "sites",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sites_code"), "sites", ["code"], unique=True)

    op.create_table(
        "stages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("site_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("planned_start", sa.Date(), nullable=True),
        sa.Column("planned_end", sa.Date(), nullable=True),
        sa.Column(
            "checkable_by_equipment",
            sa.Boolean(),
            server_default="true",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("site_id", "code", name="uq_stages_site_code"),
    )
    op.create_index(op.f("ix_stages_site_id"), "stages", ["site_id"])

    op.create_table(
        "stage_statuses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("stage_id", sa.Uuid(), nullable=False),
        sa.Column("as_of", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("delay_days", sa.Integer(), nullable=True),
        sa.Column("basis", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=8), nullable=True),
        sa.Column("evidence_dates", sa.JSON(), nullable=False),
        sa.CheckConstraint(f"status IN ({STATUS_VALUES})", name="ck_stage_statuses_status"),
        sa.CheckConstraint(
            f"confidence IS NULL OR confidence IN ({CONFIDENCE_VALUES})",
            name="ck_stage_statuses_confidence",
        ),
        sa.ForeignKeyConstraint(["stage_id"], ["stages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stage_id", "as_of", name="uq_stage_statuses_stage_as_of"),
    )
    op.create_index(op.f("ix_stage_statuses_stage_id"), "stage_statuses", ["stage_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_stage_statuses_stage_id"), table_name="stage_statuses")
    op.drop_table("stage_statuses")
    op.drop_index(op.f("ix_stages_site_id"), table_name="stages")
    op.drop_table("stages")
    op.drop_index(op.f("ix_sites_code"), table_name="sites")
    op.drop_table("sites")
