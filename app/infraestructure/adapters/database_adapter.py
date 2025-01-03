from app.core.domain.entities import Notification
from app.infraestructure.persistence.database_config import MongoDBConfig
from datetime import datetime
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Dict, Optional
from core.domain.entities import Notification

class MongoDBNotificationRepository:
    def __init__(self, db_config: MongoDBConfig, collection_name: str):
        self.collection = db_config.get_collection(collection_name)

    def save_notification(self, notification: Notification) -> str:

        try:
            notification_data = {
                "recipient": notification.recipient,
                "content": notification.content,
                "notification_type": notification.notification_type.value,
                "metaData": notification.metaData,
                "status": notification.status,
                "timestamp": datetime.now().isoformat(),  # Use ISO format for readability
            }
            result = self.collection.insert_one(notification_data)
            return str(result.inserted_id)
        except Exception as e:
            raise RuntimeError(f"Failed to save notification: {e}")

    def get_notifications(self, filters: Optional[Dict] = None) -> List[Dict]:

        try:
            filters = filters or {}
            notifications = self.collection.find(filters).sort("timestamp", -1)
            return [{**doc, "_id": str(doc["_id"])} for doc in notifications]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve notifications: {e}")

    def update_notification(self, notification_id: str, updates: Dict) -> bool:

        try:
            result = self.collection.update_one(
                {"_id": ObjectId(notification_id)}, {"$set": updates}
            )
            return result.matched_count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to update notification: {e}")

    def delete_notification(self, notification_id: str) -> bool:

        try:
            result = self.collection.delete_one({"_id": ObjectId(notification_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to delete notification: {e}")

    def bulk_update_notifications(self, filters: Dict, updates: Dict) -> int:

        try:
            result = self.collection.update_many(filters, {"$set": updates})
            return result.modified_count
        except Exception as e:
            raise RuntimeError(f"Failed to bulk update notifications: {e}")




