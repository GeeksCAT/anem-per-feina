from typing import Any, Dict

from django.core.mail import send_mail


def contact_us_email(data: Dict[str, Any]) -> None:
    send_mail(
        data.get("name"),
        data.get("email"),
        data.get("subject"),
        data.get("message"),
    )
