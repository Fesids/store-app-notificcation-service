from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class NotificationStatus(Enum):
    UNREAD = "unread"
    READ = "read"

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"


@dataclass
class Notification:
    recipient: str
    content: str
    notification_type: NotificationType
    status: NotificationStatus.UNREAD
    metaData: {}
    timestamp: datetime = datetime.now().timestamp()