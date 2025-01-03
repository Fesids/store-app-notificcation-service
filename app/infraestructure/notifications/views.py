from decouple import config
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import status

from core.application.services import NotificationService
from infraestructure.adapters.aws_email_adapter import AwsEmailAdapter
from infraestructure.adapters.aws_sms_adapter import AwsSmsAdapter
from infraestructure.adapters.database_adapter import MongoDBNotificationRepository
from infraestructure.persistence.database_config import MongoDBConfig

email_sender = AwsEmailAdapter()
sms_sender = AwsSmsAdapter()

db_setup = {
    "uri": config("DATABASE_URL"),
    "database_name": config("DATABASE_NAME")
}

mongo_config = MongoDBConfig(db_setup.get("uri"), db_setup.get("database_name"))

repository = MongoDBNotificationRepository(mongo_config, "notifications")



class Teste(APIView):

    def get(self, request, format=None):

        return Response({'msg': 'ok ok'}, status=status.HTTP_200_OK)



notification_service = NotificationService(email_sender, sms_sender, repository)

class NotificationListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        notifications = notification_service.repository.get_notifications({"recipient": user_id})
        return Response(notifications, status=status.HTTP_200_OK)


class NotificationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, notification_id):
        notification = notification_service.repository.get_notifications({"_id": notification_id})
        if not notification:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(notification, status=status.HTTP_200_OK)

    def put(self, request, notification_id):

        updated = notification_service.repository.update_notification(
            notification_id, {"status": "read"}
        )
        if updated:
            return Response({"msg": "Notification marked as read"}, status=status.HTTP_200_OK)
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, notification_id):

        deleted = notification_service.repository.delete_notification(notification_id)
        if deleted:
            return Response({"msg": "Notification deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


class NotificationCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            notification_service.send_notification(data)
            return Response({"msg": "Notification sent"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_all_notifications_as_read(request):

    user_id = request.user.id
    updated = notification_service.repository.bulk_update_notifications(
        {"recipient": user_id}, {"status": "read"}
    )
    return Response({"msg": f"{updated} notifications marked as read"}, status=status.HTTP_200_OK)
