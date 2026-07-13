from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class DocumentContent:
    document_id: UUID
    raw_text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None