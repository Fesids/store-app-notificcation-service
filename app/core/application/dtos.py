from dataclasses import dataclass

from app.core.domain.entities import NotificationType


@dataclass
class NotificationDTO:
    recipient: str
    content: str
    metaData: {}
    notification_type: NotificationType