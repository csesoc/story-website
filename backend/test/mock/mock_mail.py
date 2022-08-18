import email
import flask_mail

class MockMail:
    def __init__(self):
        self.ascii_attachments = False
        self.messages = []

    def init_app(self, app):
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mail'] = self

    def send(self, message: flask_mail.Message):
        self.messages.append(message.as_bytes())

    def get_message(self, n):
        return email.message_from_bytes(self.messages[n])

mailbox = MockMail()
