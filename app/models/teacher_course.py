from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TeacherCourse:
    teacher_id: int
    course_id: int
    date_approved: datetime
    course_name: str
    self_url: Optional[str]

    def __init__():
        pass

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        teacher_course = __class__()
        teacher_course.teacher_id = data['teacher_id']
        teacher_course.course_id = data['course_id']
        teacher_course.course_name = data['course_name']
        teacher_course.date_approved = datetime.strptime(data['time_sent'])
        teacher_course.self_url = data['_links']['self']
        return teacher_course
