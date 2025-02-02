import boto3
from decouple import config
from core.application.ports import EmailSender


class AwsEmailAdapter(EmailSender):
    def __init__(self):
        print(config('AWS_ACCESS_KEY'))
        self.client = boto3.client(
            'ses',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY'),
            region_name=config('AWS_REGION')
        )

    def send_email(self, recipient: str, content: str):
        self.client.send_email(
            Source=config('EMAIl_USER'),
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': "Notification"},
                'Body': {'Text': {'Data': content}}
            }
        )