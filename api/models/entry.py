from datetime import UTC, datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

AnalysisText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)
    entry_id: str = Field(description="ID of the analyzed entry")
    sentiment: Literal["positive", "negative", "neutral"]
    summary: AnalysisText
    topics: list[AnalysisText] = Field(min_length=2, max_length=4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


EntryText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]


class EntryCreate(BaseModel):
    """Text fields required to create a journal entry."""

    work: EntryText
    struggle: EntryText
    intention: EntryText

    @field_validator("work", "struggle", "intention", mode="before")
    @classmethod
    def reject_bytes(cls, value: Any) -> Any:
        if isinstance(value, bytes):
            raise ValueError("String required")
        return value


def _drop_default(schema: dict[str, Any]) -> None:
    schema.pop("default", None)


class EntryUpdate(BaseModel):
    work: EntryText = Field(default=None, json_schema_extra=_drop_default)  # pyright: ignore[reportAssignmentType]
    struggle: EntryText = Field(default=None, json_schema_extra=_drop_default)  # pyright: ignore[reportAssignmentType]
    intention: EntryText = Field(default=None, json_schema_extra=_drop_default)  # pyright: ignore[reportAssignmentType]

    @field_validator("work", "struggle", "intention", mode="before")
    @classmethod
    def reject_null_and_bytes(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("Supplied fields must contain text, not null")
        if isinstance(value, bytes):
            raise ValueError("String required")
        return value


class Entry(BaseModel):
    id: str
    work: str
    struggle: str
    intention: str
    created_at: datetime
    updated_at: datetime


class EntryCreatedResponse(BaseModel):
    detail: str
    entry: Entry


class EntryListResponse(BaseModel):
    entries: list[Entry]
    count: int


class DetailResponse(BaseModel):
    detail: str
