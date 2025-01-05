from django.urls import path, include

from infraestructure.notifications.views import Teste, NotificationListView, NotificationDetailView, \
    NotificationCreateView, mark_all_notifications_as_read

urlpatterns = [
    path('teste', Teste.as_view(), name="teste"),
    path("", NotificationListView.as_view(), name="notification-list"),
    path("detail/<str:notification_id>", NotificationDetailView.as_view(), name="notification-detail"),
    path("create/", NotificationCreateView.as_view(), name="notification-create"),
    path("mark-all-read", mark_all_notifications_as_read, name="mark-all-notifications-read"),

]