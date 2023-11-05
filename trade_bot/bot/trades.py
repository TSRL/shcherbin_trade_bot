from django.core.exceptions import ObjectDoesNotExist

from bot.models import TradeRequest, Balance
from bot.errors import InsufficientBalance
from bot.executors import DealExecutor, PriceFetcher


BUY_OPERATION = "BUY"
SELL_OPERATION = "SELL"
REPORT_OPERATION = "REPORT"
UNKNOWN_OPERATION = "UNKNOWN"


def attempt_purchase(
        selling_token,
        buying_token,
        amount_purchase,
        chat,
        price_fetcher: PriceFetcher,
        deal_executor: DealExecutor,
):
    request = TradeRequest(
        coin_sold=selling_token,
        coin_purchased=buying_token,
        amount_purchase=amount_purchase,
        finished=False,
        successful=False,
        chat=chat,
    )
    request.save()

    try:
        selling_balance = Balance.objects.get(chat=chat.chat_id, coin=selling_token)
    except ObjectDoesNotExist:
        raise InsufficientBalance

    price = price_fetcher.request_price(selling_token, buying_token)
    if selling_balance.value * price < amount_purchase:
        raise InsufficientBalance

    result = deal_executor.execute_trade(selling_token, buying_token, price * amount_purchase)
    request.successful = result
    request.finished = True
    request.price = price
    request.amount_sell = price * amount_purchase
    request.save()

    if result:
        selling_balance.value -= amount_purchase / price
        try:
            buying_balance = Balance.objects.get(chat=chat.chat_id, coin=buying_token)
        except ObjectDoesNotExist:
            buying_balance = Balance.objects.get(chat=chat.chat_id, coin=buying_token, value=0)
        buying_balance.value += amount_purchase
        selling_balance.save()
        buying_balance.save()
        response_message = f'Your trade wass successfully executed, your new balances: {selling_token}:{selling_balance.value}, {buying_token}:{buying_balance.value}' # NOQA
    else:
        response_message = 'Unfortunately we failed to execute your trade'

    return response_message


def attempt_sell(
        selling_token,
        buying_token,
        amount_sell,
        chat,
        price_fetcher: PriceFetcher,
        deal_executor: DealExecutor,
):
    request = TradeRequest(
        coin_sold=selling_token,
        coin_purchased=buying_token,
        amount_sell=amount_sell,
        finished=False,
        successful=False,
        chat=chat
    )
    request.save()

    try:
        selling_balance = Balance.objects.get(chat=chat.chat_id, coin=selling_token)
    except ObjectDoesNotExist:
        raise InsufficientBalance

    if selling_balance.value < amount_sell:
        raise InsufficientBalance

    price = price_fetcher.request_price(selling_token, buying_token)
    result = deal_executor.execute_trade(selling_token, buying_token, amount_sell)
    request.successful = result
    request.finished = True
    request.price = price
    request.amount_purchase = price * amount_sell
    request.save()

    if result:
        selling_balance.value -= amount_sell
        try:
            buying_balance = Balance.objects.get(chat=chat.chat_id, coin=buying_token)
        except ObjectDoesNotExist:
            buying_balance = Balance(chat=chat, coin=buying_token, value=0)
        buying_balance.value += amount_sell * price
        selling_balance.save()
        buying_balance.save()
        response_message = f'Your trade wass successfully executed, your new balances: {selling_token}:{selling_balance.value}, {buying_token}:{buying_balance.value}' # NOQA
    else:
        response_message = 'Unfortunately we failed to execute your trade'

    return response_message
