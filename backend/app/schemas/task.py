from pydantic import BaseModel
from typing import Optional


class TaskWithScoreResponse(BaseModel):
    id: str
    name: str
    status: Optional[str]
    score: Optional[int]
    assignee_id: Optional[str]
    assignee_name: str

    class Config:
        orm_mode = True
