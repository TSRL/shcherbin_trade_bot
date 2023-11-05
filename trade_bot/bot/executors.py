import time
import random
import requests

from abc import abstractmethod

from bot.errors import PriceFetchFail


SWAP_ZONE_ENDPOINT = 'api.swapzone.io/v1/exchange/get-rate'
SWAP_ZONE_KEY = 'L49bXKWN4'


class DealExecutor:

    @abstractmethod
    def execute_trade(self, sell, buy, amount_sell):
        return True


class DealExecutorImitator(DealExecutor):

    def execute_trade(self, sell, buy, amount_sell):
        time.sleep(2)
        return True


class DealExecutorSuccessful(DealExecutor):

    def execute_trade(self, sell, buy, amount_sell):
        return True


class PriceFetcher:

    @abstractmethod
    def request_price(self, sell, buy):
        return 1


class PriceFetcherMock(PriceFetcher):

    def request_price(self, sell, buy):
        return 1


class PriceFetcherSwapZone(PriceFetcher):

    def request_price(self, sell, buy):
        try:
            url = f'https://{SWAP_ZONE_ENDPOINT}/'
            print(f'making request from {sell.lower()} to {buy.lower()}')
            response = requests.get(
                url=url,
                params={
                    'from': sell.lower(),
                    'to': buy.lower(),
                    'amount': 1,
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
        print(f'price response: {response.json()}')
        return response.json()['amountTo']
