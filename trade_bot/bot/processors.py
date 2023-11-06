import logging

from telegram import Update
from telegram.ext import ContextTypes

from asgiref.sync import sync_to_async

from bot.models import Chat, Balance, ArbitraryRequest
from bot.trades import attempt_purchase, attempt_sell
from bot.errors import WrongCommand, InsufficientBalance, PriceFetchFail
from bot.report import generate_report
from bot.executors import DealExecutorImitator, PriceFetcherSwapZone

GREETINGS_MESSAGE = "Welcome to the trade bot!"

logger = logging.getLogger('django')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=GREETINGS_MESSAGE)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'message text being received: {update.message.text} for a chat: {update.effective_chat}')

    user_message = update.message.text.upper()
    elements = user_message.split(" ")
    first_message = elements[0]

    filter_query = await sync_to_async(Chat.objects.filter)(chat_id=update.effective_chat.id)
    exists = await sync_to_async(filter_query.exists)()

    if exists:
        logger.info(f'chat identified {update.effective_chat.id}')
        current_chat = await sync_to_async(Chat.objects.get)(chat_id=update.effective_chat.id)
    else:
        logger.info(f'creating a new chat {update.effective_chat.id}')
        current_chat = Chat(chat_id=update.effective_chat.id)
        eth_balance = Balance(coin="ETH", value=100, chat=current_chat)
        btc_balance = Balance(coin="BTC", value=10, chat=current_chat)
        usdt_balance = Balance(coin="USDT", value=1000000000, chat=current_chat)
        await sync_to_async(current_chat.save)()
        await sync_to_async(eth_balance.save)()
        await sync_to_async(btc_balance.save)()
        await sync_to_async(usdt_balance.save)()

    try:
        if first_message == "BUY":
            if len(elements) != 3:
                raise WrongCommand()
            token_elements = elements[2].split('/')
            if len(token_elements) != 2:
                raise WrongCommand()
            response_message = await sync_to_async(attempt_purchase)(
                selling_token=token_elements[1],
                buying_token=token_elements[0],
                amount_purchase=float(elements[1]),
                chat=current_chat,
                deal_executor=DealExecutorImitator(),
                price_fetcher=PriceFetcherSwapZone(),
            )
        elif first_message == "SELL":
            if len(elements) != 3:
                raise WrongCommand()
            token_elements = elements[2].split('/')
            if len(token_elements) != 2:
                raise WrongCommand()
            response_message = await sync_to_async(attempt_sell)(
                selling_token=token_elements[0],
                buying_token=token_elements[1],
                amount_sell=float(elements[1]),
                chat=current_chat,
                deal_executor=DealExecutorImitator(),
                price_fetcher=PriceFetcherSwapZone(),
            )
        elif first_message == "REPORT":
            response_message = await sync_to_async(generate_report)(
                chat=current_chat,
                price_fetcher=PriceFetcherSwapZone()
            )
        else:
            new_request = ArbitraryRequest(
                message=user_message,
                chat=current_chat,
            )
            await sync_to_async(new_request.save)()
            response_message = "Unfortunately I could not recognize your request but it was registered and we will come back to you!" # NOQA
    except WrongCommand:
        response_message = "Unfortunately I could not recognize your command, please try again"
    except InsufficientBalance:
        response_message = "Can not execute trade, not enough funds"
    except PriceFetchFail as e:
        response_message = f'Unexpected error when fetching a price: {str(e)}'

    await sync_to_async(current_chat.save)()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)
