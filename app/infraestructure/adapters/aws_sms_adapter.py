
import boto3
from decouple import config
from app.core.application.ports import SmsSender


class AwsSmsAdapter(SmsSender):
    def __init__(self):
        self.client = boto3.client(
            'sns',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY'),
            region_name=config('AWS_REGION')
        )

    def send_sms(self, recipient: str, content: str):
        self.client.publish(PhoneNumber=recipient, Message=content)
