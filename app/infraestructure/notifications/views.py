from botocore.exceptions import ValidationError
from bson import ObjectId
from decouple import config
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission,  AllowAny
from rest_framework import status

from core.application.services import NotificationService
from core.domain.entities import Notification, NotificationType
from framework.django.authentication import JWTAuthentication
from framework.django.permissions import IsAuthenticated
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print(request.user)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)



notification_service = NotificationService(email_sender, sms_sender, repository)

class NotificationListView(APIView):

    #permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = "5511932744814" #request.user.id
        notifications = notification_service.repository.get_notifications({"recipient": user_id})
        return Response(notifications, status=status.HTTP_200_OK)


class NotificationDetailView(APIView):

    #permission_classes = [IsAuthenticated]

    def get(self, request, notification_id):
        notification_convert_id = ObjectId(notification_id)
        notification = notification_service.repository.get_notifications({"_id": notification_convert_id})

        if not notification:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(notification, status=status.HTTP_200_OK)

    def put(self, request, notification_id):
        notification_convert_id = ObjectId(notification_id)
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
    #permission_classes = [AllowAny]

    def get(self, request):
        return Response({"Ok": "get"})

    def post(self, request):
        data = request.data
        channels = data.get("channels", ["email"])


        if "notification_type" not in data:
            raise ValidationError({"error": "Field 'notification_type' is required."})

        try:
            notification = Notification(
                recipient=data["recipient"],
                content=data["content"],
                notification_type=NotificationType[data["notification_type"]],
                metaData=data.get("metaData", {}),
                status=data.get("status", "unread"),
            )
            notification_service.send_notification(notification, channels)
            return Response({"msg": "Notification sent"}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {"error": f"Missing required field: {e.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
@permission_classes([AllowAny])
def mark_all_notifications_as_read(request):

    user_id = "5511932744814" #request.user.id
    updated = notification_service.repository.bulk_update_notifications(
        {"recipient": user_id}, {"status": "read"}
    )
    return Response({"msg": f"{updated} notifications marked as read"}, status=status.HTTP_200_OK)
