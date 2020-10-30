from smtplib import SMTPException
from typing import List, Union

from django.conf import settings
from django.core.mail import send_mail

from jobs.celery import app as celery_app

ASYNC_QUEUE_NAME = getattr(settings, "NOTIFICATIONS_ASYNC_QUEUE_NAME", "default")


@celery_app.task(
    name="jobsapp.tasks._send_email",
    queue=ASYNC_QUEUE_NAME,
    autoretry=[SMTPException],
    max_retries=3,
)  # type: ignore
def _send_email(*, subject: str, message: str, from_email: str, recipient_list: List[str]) -> None:
    """Email us users contact form message using django send_mail."""
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
    )
