from dataclasses import dataclass

from datetime import datetime

from app.core.domain.entities import NotificationType


@dataclass
class NotificationSentEvent:
    recipient: str
    content: str
    notification_type: NotificationType
    timestamp: datetime = datetime.now().timestamp()