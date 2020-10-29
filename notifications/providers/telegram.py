import telegram

from .base import ProviderBase


class Telegram(ProviderBase):
    code = "telegram"

    def _publish(self, tpl: str):
        """
        Publish notifications to Telegram using a BOT
        """
        assert self.settings.get("token"), "Telegram token env (`TELEGRAM_TOKEN`) is not defined"
        assert self.settings.get(
            "chat_ids"
        ), "Telegram chat IDs env (`TELEGRAM_CHAT_IDS`) is not defined"

        bot = telegram.Bot(token=self.settings.get("token"))
        for chat_id in self.settings.get("chat_ids"):
            bot.send_message(
                chat_id=f"{chat_id}",
                text=tpl,
                parse_mode=telegram.ParseMode.HTML,
            )
