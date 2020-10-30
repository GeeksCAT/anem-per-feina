import logging

from django.conf import settings
from django.template.loader import render_to_string

from ..settings import PROVIDERS_SETTINGS

logger = logging.getLogger(__name__)


class ProviderBase:
    """
    Base object for providers.
    """

    code: str = None

    @property
    def settings(self):
        """
        Get provider settings
        """
        return PROVIDERS_SETTINGS.get(self.code, {})

    def _publish(self, tpl: str):
        """
        Method must be override for each provider.
        """
        raise NotImplemented

    def publish(self, event_name: str, instance: any) -> bool:
        """
        This method render the provider template and call _publish method.
        It return a success bool.
        """

        logger.info(f"Publishing to {self.code}, event {event_name}, instance {instance.pk}")
        context = {
            "object": instance,
            "base_url": settings.BASE_URL,
        }
        tpl = render_to_string(f"notifications/{self.code}_{event_name}.html", context)
        try:
            self._publish(tpl)
        except Exception as e:
            logger.error(
                f"Publishing error to {self.code}, event {event_name}, instance {instance.pk}",
                e,
            )
            return False
        return True
