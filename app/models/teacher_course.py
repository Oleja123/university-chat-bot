from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TeacherCourse:
    teacher_id: int
    course_id: int
    date_completion: datetime
    course_name: str
    confirming_document: str
    sertificate_loaded: bool
    self_url: Optional[str]

    def __init__(self):
        pass

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        teacher_course = __class__()
        teacher_course.teacher_id = data['teacher_id']
        teacher_course.course_id = data['course_id']
        teacher_course.course_name = data['course_name']
        teacher_course.date_completion = (datetime.fromisoformat(
            data['date_completion']).date() if data['date_completion'] else None)
        teacher_course.confirming_document = data['confirming_document']
        teacher_course.sertificate_loaded = data['sertificate_loaded']
        teacher_course.self_url = data['_links']['self']
        return teacher_course

    def __repr__(self):
        return f"Название курса:\n{self.course_name}\n" +\
            f"Сертификат загружен: {'✅' if self.sertificate_loaded else '❌'}\n" +\
            (f"Дата прохождения: {self.date_completion.isoformat()}\n" if self.date_completion else 'Курс пока не пройден\n') +\
            f"№ Подтверждающего документа: " + (f"{self.confirming_document}" if self.confirming_document else 'Не проставлен')
