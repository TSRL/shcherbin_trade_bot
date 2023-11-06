import json

from bot.models import Balance, TradeRequest
from bot.executors import PriceFetcher

from bot.errors import PriceFetchFail


def generate_report(chat, price_fetcher: PriceFetcher):
    relevant_trades = TradeRequest.objects.filter(chat=chat, finished=True, successful=True)
    if not relevant_trades.exists():
        return json.dumps({})

    result = {
        "total_pnl": 0
    }
    for elem in relevant_trades:
        try:
            curr_price = price_fetcher.request_price(sell=elem.coin_sold, buy=elem.coin_purchased)
        except PriceFetchFail:
            # TODO due to swapzone returning error every time the price is too small for one unit - just skipping it for simplicity # NOQA
            continue
        if elem.amount_sell != 0:
            delta = elem.price - curr_price
            result["total_pnl"] += delta * elem.amount_sell
        else:
            delta = curr_price - elem.price
            result["total_pnl"] += delta * elem.amount_purchase

    balances = Balance.objects.filter(chat=chat)
    if not balances.exists():
        return json.dumps({})

    for balance in balances:
        result[balance.coin] = balance.value
    return json.dumps(result)
