from app.core.domain.entities import Notification
from app.infraestructure.persistence.database_config import MongoDBConfig
from datetime import datetime

class MongoDBNotificationRepository:
    def __init__(self, db_config: MongoDBConfig, collection_name: str):
        self.collection = db_config.get_collection(collection_name)

    def save_notification(self, notification: Notification):
        notification_data = {
            "recipient": notification.recipient,
            "content": notification.content,
            "notification_type": notification.notification_type.value,
            "timestamp": datetime.now().timestamp()
        }
        self.collection.insert_one(notification_data)

    def get_notifications(self, filters: dict = None):
        filters = filters or {}
        return list(self.collection.find(filters))
















