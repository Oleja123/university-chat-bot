from dataclasses import dataclass
from datetime import datetime


@dataclass
class TeacherCourse:
    teacher_id: int
    course_id: int
    date_approved: datetime
    course_name: str

    def __init__():
        pass

    @staticmethod
    def from_dict(data):
        teacher_course = __class__()
        teacher_course.teacher_id = data['teacher_id']
        teacher_course.course_id = data['course_id']
        teacher_course.course_name = data['course_name']
        teacher_course.date_approved = datetime.strptime(data['time_sent'])
        return teacher_course
