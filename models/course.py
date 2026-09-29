from pydantic import BaseModel, Field
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Course(BaseModel):
    id: int | None = None
    course_code: str
    name: str
    directory: str
    is_archived: bool = False
