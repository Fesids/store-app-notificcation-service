from dataclasses import dataclass

from app.core.domain.entities import NotificationType


@dataclass
class NotificationDTO:
    recipient: str
    content: str
    notification_type: NotificationType