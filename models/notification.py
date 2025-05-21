from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notifification:
    id: int
    message: str
    has_read: bool
    time_sent: datetime

    def __init__():
        pass

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        notification = __class__()
        notification.id = data['id']
        notification.message = data['message']
        notification.has_read = True if str(
            data['has_read']) == 'true' else False
        notification.time_sent = datetime.strptime(data['time_sent'])
        return notification
