from enum import StrEnum


class StageStatusValue(StrEnum):
    """CONTRACTS §3. not_started — утверждение о стройке, not_observed — о наших данных."""

    AHEAD = "ahead"
    ON_TRACK = "on_track"
    BEHIND = "behind"
    NOT_STARTED = "not_started"
    NOT_OBSERVED = "not_observed"
    NOT_CHECKABLE = "not_checkable"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
