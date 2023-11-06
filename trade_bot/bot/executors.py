import os
import time
import requests

from abc import abstractmethod

from bot.errors import PriceFetchFail


SWAP_ZONE_ENDPOINT = 'api.swapzone.io/v1/exchange/get-rate'
SWAP_ZONE_KEY = os.environ['SWAP_ZONE_KEY']


class DealExecutor:

    @abstractmethod
    def execute_trade(self, sell, buy, amount_sell):
        return True


class DealExecutorImitator(DealExecutor):

    def execute_trade(self, sell, buy, amount_sell):
        time.sleep(2)
        return True


class PriceFetcher:

    @abstractmethod
    def request_price(self, sell, buy, amount_sell=1):
        return 1


class PriceFetcherSwapZone(PriceFetcher):

    def request_price(self, sell, buy, amount_sell=1):
        try:
            url = f'https://{SWAP_ZONE_ENDPOINT}/'
            response = requests.get(
                url=url,
                params={
                    'from': sell.lower(),
                    'to': buy.lower(),
                    'amount': amount_sell,
                    'chooseRate': 'best',
                    'rateType': 'all',
                },
                headers={
                    'x-api-key': SWAP_ZONE_KEY
                },
            )
        except Exception as e:
            raise PriceFetchFail(e)
        if response.status_code != 200:
            raise PriceFetchFail(response.json())
        if response.json().get("error"):
            raise PriceFetchFail()
        return response.json()['amountTo']
