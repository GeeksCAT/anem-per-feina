import twitter

from .base import ProviderBase


class Twitter(ProviderBase):
    """
    Twitter Provider that interacts with Twitter API
    """

    code = "twitter"

    def _publish(self, tpl: str):
        """
        Publish notifications creating a new Post via TW API
        """
        assert self.settings.get("keys"), "Telegram keys should be defined for telegram settings"
        assert self.settings.get("keys").get(
            "consumer_key"
        ), "Telegram API key env (`TWITTER_API_KEY`) is not defined"
        assert self.settings.get("keys").get(
            "consumer_secret"
        ), "Telegram API secret env (`TWITTER_API_SECRET`) is not defined"
        assert self.settings.get("keys").get(
            "access_token_key"
        ), "Telegram access token env (`TWITTER_ACCESS_TOKEN`) is not defined"
        assert self.settings.get("keys").get(
            "access_token_secret"
        ), "Telegram access token secret env (`TWITTER_ACCESS_TOKEN_SECRET`) is not defined"

        api = twitter.Api(
            **self.settings.get("keys"),
        )
        api.PostUpdate(tpl)
