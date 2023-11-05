import time
import random

from abc import abstractmethod


class DealExecutor:

    @abstractmethod
    def execute_trade(self, sell, buy, amount_sell):
        return True


class DealExecutorImitator(DealExecutor):

    def execute_trade(self, sell, buy, amount_sell):
        time.sleep(5)
        return bool(random.getrandbits(1))


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
        # TODO implement
        return 1
