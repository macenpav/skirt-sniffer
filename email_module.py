import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from os import path

DIR_PATH = path.dirname(path.realpath(__file__))
CONFIG_FILENAME = path.join(DIR_PATH, r"config.ini")
CONFIG_ADMIN_R = 'Admin_Recipients'
CONFIG_PRINT_R = 'Print_Recipients'
CONFIG_REGULAR_R = 'Recipients'


class Email:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILENAME)
        self.subject = r"No subject"
        self.content = r""

    def set_subject(self, subject):
        self.subject = subject

    def set_content(self, content):
        self.content = content

    def send(self, recipient_class):
        msg = MIMEMultipart('alternative')

        msg['Subject'] = self.subject
        msg['From'] = formataddr((str(Header('Sukničkář Pavel', 'utf-8')), self.config.get('General', 'Sender')))
        msg['To'] = self.config.get('General', recipient_class)

        server = smtplib.SMTP_SSL(self.config.get('SMTP', 'Address'), self.config.get('SMTP', 'Port'))
        server.ehlo()
        server.login(self.config.get('General', 'Sender'), self.config.get('General', 'Password'))
        msg.attach(MIMEText(self.content, 'html'))
        server.send_message(msg)
        server.quit()

