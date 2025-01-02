from dataclasses import dataclass
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "SMS"


@dataclass
class Notification:
    recipient: str
    content: str
    notification_type: NotificationType