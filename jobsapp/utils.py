from typing import Any, Dict

from django.core.mail import send_mail

from jobs.settings import EMAIL_HOST


def contact_us_email(data: Dict[str, Any]) -> None:
    message = f"""{data.get("name").title()} sent the follow mensage:
    {data.get("message")}
    """
    print(message)
    send_mail(
        data.get("subject"),
        message,
        data.get("email"),
        recipient_list=[
            EMAIL_HOST,
        ],
    )
