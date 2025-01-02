from app.core.application.ports import EmailSender, SmsSender
from app.core.domain.entities import Notification
from app.infraestructure.adapters.database_adapter import MongoDBNotificationRepository


class NotificationService:
    def __init__(self, email_sender: EmailSender, sms_sender: SmsSender, repository: MongoDBNotificationRepository):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.repository = repository

    def send_notification(self, notification: Notification):
        if notification.notification_type == Notification.EMAIL:
            self.email_sender.send_email(notification.recipient, notification.content)

        elif notification.notification_type == Notification.SMS:
            self.sms_sender.send_sms(notification.recipient, notification.content)

        self.repository.save_notification(notification)