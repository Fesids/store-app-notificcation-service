from rest_framework import serializers

from app.core.domain.entities import NotificationType


class NotificationSerializer(serializers):
    recipient = serializers.CharField(max_length=255)
    content = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=[e.value for e in NotificationType])