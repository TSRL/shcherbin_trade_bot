import os

from django.core.management.base import BaseCommand

import logging
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler

from bot.processors import start, message

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('django')


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info('Connecting to the telegram bot')
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        start_handler = CommandHandler('start', start)
        message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)
        application.add_handler(start_handler)
        application.add_handler(message_handler)

        application.run_polling()
