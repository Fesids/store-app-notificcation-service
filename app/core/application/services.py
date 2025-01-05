from datetime import datetime

from core.application.ports import EmailSender, SmsSender
from core.domain.entities import Notification
from infraestructure.adapters.database_adapter import MongoDBNotificationRepository
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

    def send_notification(self, notification: Notification, channels):

        if "email" in channels and self.email_sender:
            try:
                print(channels)
                self.email_sender.send_email(notification.recipient, notification.content)
                self.repository.save_notification(notification)
            except Exception as e:
                self.logger.error(f"Failed to send email notification: {e}")

        if "sms" in channels and self.sms_sender:
            try:
                print(channels)
                self.sms_sender.send_sms(notification.recipient, notification.content)
                self.repository.save_notification(notification)
            except Exception as e:
                self.logger.error(f"Failed to send SMS notification: {e}")


        self.logger.info(f"Notification sent: {notification}")
        '''try:
            print(channels)
            self.repository.save_notification(notification)

            self.email_sender.send_email(notification.recipient, notification.content)
        except Exception as e:
            print(e)'''

















