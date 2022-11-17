from urllib.parse import urljoin

from celery import shared_task
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string

from mail_system.settings import READ_MAIL_LINK, UNSUB_LINK


def render_template(mail_info: dict, subject, body):
    messages_list = []

    for mail, full_name in mail_info.items():
        unsub_link = urljoin(UNSUB_LINK, mail)
        track_link = urljoin(READ_MAIL_LINK, str(full_name['mailing_user_id']))

        temp = render_to_string('event.html',
                                context={'full_name': full_name['full_name'], 'body': body,
                                         'unsub_link': unsub_link, 'track_link': track_link})
        messages_list.append((subject, temp, None, [mail]))
    return tuple(messages_list)


def send_custom_mass_mail(datatuple, fail_silently=False, auth_user=None,
                          auth_password=None, connection=None):
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    EmailMessage.content_subtype = 'html'
    messages = [
        EmailMessage(subject, message, sender, recipient, connection=connection)
        for subject, message, sender, recipient in datatuple
    ]
    return connection.send_messages(messages)


@shared_task
def send_mails(mail_info: dict, subject, body):
    messages = render_template(mail_info, subject, body)
    send_custom_mass_mail(messages)
    return True
