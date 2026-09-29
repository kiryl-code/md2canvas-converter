from pydantic import BaseModel


class Criteria(BaseModel):
    id: int | None = None
    assignment_id: int
    criteria: str
    pass_text: str
    fail_text: str
