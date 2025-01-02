from abc import ABC, abstractmethod

class EmailSender(ABC):

    @abstractmethod
    def send_email(self, recipient: str, content: str):
        pass

class SmsSender(ABC):

    @abstractmethod
    def send_sms(self, recipient: str, content: str):
        pass