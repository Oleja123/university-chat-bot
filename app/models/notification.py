from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Notifification:
    id: int
    message: str
    has_read: bool
    time_sent: datetime
    self_url: Optional[str]

    def __init__(self):
        pass

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        notification = __class__()
        notification.id = data['id']
        notification.message = data['message']
        notification.has_read = data['has_read']
        notification.time_sent = datetime.fromisoformat(data['time_sent'])
        notification.self_url = data['_links']['self']
        return notification

    def __repr__(self):
        return f"Текст сообщения:\n{self.message}\n" +\
            f"Сообщение прочитано: {'✅' if self.has_read else '❌'}\n" +\
            f"Время отправки: {self.time_sent}\n"
