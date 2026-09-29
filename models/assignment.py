from pydantic import BaseModel


class Assignment(BaseModel):
    id: int | None = None
    course_id: int
    name: str
    introduction_template: str
