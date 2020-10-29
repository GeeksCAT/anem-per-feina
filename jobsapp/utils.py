from typing import Any, Dict

from jobs.settings import EMAIL_HOST
from jobsapp.tasks import _send_email


def contact_us_email(data: Dict[str, Any]) -> None:
    """Send email on background using celery."""
    # TODO: Improve message template. Maybe add html template.
    message = f"""
    Hi, {data.get("name").title()} sent the follow mensage:

    {data.get("message")}
    """

    _send_email.apply_async(
        args=(
            data.get("subject"),
            message,
            data.get("email"),
            [
                EMAIL_HOST,
            ],
        )
    )
