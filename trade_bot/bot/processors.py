import json
import logging

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from asgiref.sync import sync_to_async

from bot.models import Chat

GREETINGS_MESSAGE = "Welcome to the trade bot!"

logger = logging.getLogger('django')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=GREETINGS_MESSAGE)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'message text being received: {update.message.text} for a chat: {update.effective_chat}')

    user_message = update.message.text
    elements = user_message.split(" ")
    first_message = elements[0].upper()

    filter_query = await sync_to_async(Chat.objects.filter)(chat_id=update.effective_chat.id)
    exists = await sync_to_async(filter_query.exists)()

    if exists:
        logger.info(f'chat identified {update.effective_chat.id}')
        current_chat = await sync_to_async(Chat.objects.get)(chat_id=update.effective_chat.id)
    else:
        logger.info(f'creating a new chat {update.effective_chat.id}')
        current_chat = Chat(chat_id=update.effective_chat.id)

    if first_message == "BUY":
        logger.info("attempting purchase operation")
        # TODO make buy request
        deal = {
            "pair": "USD/BTC",
            "value": 300,
            "price": 20000,
            "buying": True,
        }
        if current_chat.deals is None:
            current_chat.deals = [deal]
        else:
            current_chat.deals.append(deal)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You successfully purchased something!"
        )
    elif first_message == "SELL":
        logger.info("attempting selling operation")
        # TODO make sell request
        deal = {
            "pair": "USD/BTC",
            "value": 300,
            "price": 20000,
            "buying": False,
        }
        if current_chat.deals is None:
            current_chat.deals = [deal]
        else:
            current_chat.deals.append(deal)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You successfully purchased something!"
        )
    elif first_message == "REPORT":
        # TODO generate a report
        logger.info("generating and returning PNL report")
        report = {
            "your PNL": 1,
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=json.dumps(report)
        )
    else:
        logger.info("registering a new request")
        # TODO save a new request
        request = update.message.text
        if current_chat.requests is None:
            current_chat.requests = [request]
        else:
            current_chat.requests.append(request)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your request has been registered!"
        )
    await sync_to_async(current_chat.save)()
