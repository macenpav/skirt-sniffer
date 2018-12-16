import smtplib
from email.message import EmailMessage

# TODO: grab smtp addr and port from a config file
google_smtp_addr = r"smtp.gmail.com"
google_smtp_port = 465


class Email:
    def __init__(self):
        self.recipients = []
        self.sender = r"****@****.**" # TODO: grab sender from a config file
        self.password = r"***"  # TODO: grab password from a config file
        self.subject = r"No subject"

    # TODO: deprecate this method and also grab this from a config file
    def add_recipient(self, email):
        self.recipients.append(email)

    def set_subject(self, subject):
        self.subject = subject

    def send(self):
        msg = EmailMessage()

        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = r", ".join(self.recipients)

        try:
            server = smtplib.SMTP_SSL(google_smtp_addr, google_smtp_port)
            server.ehlo()
            server.login(self.sender, self.password)  # login is the same as sender
            server.send_message(msg)
            server.quit()

        except:
            pass  # TODO: log something
