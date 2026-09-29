from pydantic import BaseModel


class Feedback(BaseModel):
    id: int | None = None
    assignment_id: int
    student_id: str
    student_name: str
    grade: str
    criteria: dict[int, bool]
    extra_comment: str
    feedback: str
