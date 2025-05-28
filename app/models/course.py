from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Course:
    id: int
    name: str
    course_type_id: int
    is_included: bool

    def __init__(self):
        pass

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        course = __class__()
        course.id = data['id']
        course.name = data['name']
        course.course_type_id = data['course_type_id']
        course.is_included =  data['is_included']
        return course

    def __repr__(self):
        return f"Название курса:\n{self.name}\n"
