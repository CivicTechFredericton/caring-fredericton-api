import base64
import boto3
import email.utils

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from core import errors
from core import configuration

import logging
logger = logging.getLogger(__name__)


class SES:
    def __init__(self):
        # TODO: Remove region restriction when Cognito supported in Canadian region
        self.client = boto3.client('ses', region_name='us-east-1')
        hosted_zone_name = configuration.get_setting('hosted_zone_name')
        if hosted_zone_name[-1] == '.':
            hosted_zone_name = hosted_zone_name[:-1]
        # self.source_email = 'no-reply@%s' % hosted_zone_name
        self.source_email = 'howard.powell@bluespurs.com'

    def send_email(self, recipients, subject, body, attachment_name=None, encoded_contents=None):
        logger.info('Sending email', extra={'to addresses': recipients})
        try:
            if attachment_name is None:
                self.send_email_without_attachment(recipients, subject, body)
            else:
                self.send_email_with_attachment(recipients, subject, body, attachment_name, encoded_contents)
        except Exception:
            logger.exception("Error sending email through SES")
            raise errors.SESError()

    def send_email_without_attachment(self, recipients, subject, body):
        self.client.send_email(
            Source=self.source_email,
            Destination={
                'ToAddresses': recipients
            },
            Message={
                'Body': {
                    'Text': {
                        'Data': body
                    }
                },
                'Subject': {
                    'Data': subject
                }
            }
        )

    def send_email_with_attachment(self, recipients, subject, body, attachment_name, encoded_contents):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.source_email

        if isinstance(recipients, (list, tuple)):
            message['To'] = email.utils.COMMASPACE.join(recipients)
        else:
            message['To'] = recipients

        # What a recipient sees if they don't use an email reader
        message.preamble = 'Multipart message with attachment.\n'

        # Set the message body
        from email.mime.text import MIMEText
        message.attach(MIMEText(body, 'plain'))

        # Attach the file
        part = MIMEApplication(base64.b64decode(encoded_contents))
        part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        message.attach(part)

        # Send the message
        self.client.send_raw_email(
            Source=self.source_email,
            Destinations=recipients,
            RawMessage={'Data': message.as_string()}
        )