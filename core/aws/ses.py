import boto3
import email.utils

from email.mime.multipart import MIMEMultipart

from core import configuration, errors

import logging
logger = logging.getLogger(__name__)

SES_CLIENT = boto3.client('ses')


def send_email(recipients, subject, text_body, html_body='', attachment_name=None, attachment_contents=None):
    logger.info('Sending email to ', extra={'to_addresses': recipients})
    sender = configuration.get_setting('NOTIFICATION_SENDER')
    try:
        if attachment_name is None:
            send_email_without_attachment(sender,
                                          recipients,
                                          subject,
                                          text_body,
                                          html_body)
        else:
            send_email_with_attachment(sender,
                                       recipients,
                                       subject,
                                       text_body,
                                       attachment_name,
                                       attachment_contents)
    except Exception as e:
        logger.exception("Error sending email through SES")
        raise errors.SESError()


def send_email_without_attachment(source_email, recipients, subject, text_body, html_body):
    SES_CLIENT.send_email(
        Source=source_email,
        Destination={
            'BccAddresses': recipients
        },
        Message={
            'Body': {
                # 'Html': {
                #     'Charset': 'UTF-8',
                #     'Data': html_body,
                # },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': text_body,
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject
            }
        }
    )


def send_email_with_attachment(source_email, recipients, subject, body, attachment_name, attachment_contents):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = source_email

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
    part = MIMEText(attachment_contents)
    part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
    message.attach(part)

    # Send the message
    SES_CLIENT.send_raw_email(
        Source=source_email,
        Destinations=recipients,
        RawMessage={'Data': message.as_string()}
    )
