from datetime import datetime

from pydantic import BaseModel, Field


class History(BaseModel):
    user: int
    subject: int
    message: dict
    created: datetime = Field(default_factory=datetime.now)
