from app.core.application.ports import EmailSender, SmsSender
from app.core.domain.entities import Notification
from app.infraestructure.adapters.database_adapter import MongoDBNotificationRepository
import logging

class NotificationService:
    def __init__(self, email_sender: EmailSender, sms_sender: SmsSender, repository: MongoDBNotificationRepository):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.repository = repository
        self.logger = logging.getLogger(__name__)

    '''def send_notification(self, notification: Notification):
        if notification.notification_type == Notification.EMAIL:
            self.email_sender.send_email(notification.recipient, notification.content)

        elif notification.notification_type == Notification.SMS:
            self.sms_sender.send_sms(notification.recipient, notification.content)

        self.repository.save_notification(notification)'''

    def send_notification(self, data: dict):

        recipient = data.get("recipient")
        content = data.get("content")
        metadata = data.get("metadata", {})
        channels = data.get("channels", ["system"])  # Default to "system"


        notification_id = self.repository.save_notification({
            "recipient": recipient,
            "content": content,
            "metadata": metadata,
            "status": "unread",
        })


        if "email" in channels and self.email_sender:
            try:
                self.email_sender.send_email(recipient, content)
            except Exception as e:
                self.logger.error(f"Failed to send email notification: {e}")

        if "sms" in channels and self.sms_sender:
            try:
                self.sms_sender.send_sms(recipient, content)
            except Exception as e:
                self.logger.error(f"Failed to send SMS notification: {e}")


        self.logger.info(f"Notification sent: {notification_id}")

















