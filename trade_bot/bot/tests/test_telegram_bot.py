from django.test import TestCase

from bot.trades import attempt_purchase, attempt_sell
from bot.models import Chat, Balance, TradeRequest
from bot.executors import DealExecutor, PriceFetcher
from bot.errors import InsufficientBalance


# Very basic unit tests for trade functions


class DealExecutorMock(DealExecutor):
    def execute_trade(self, sell, buy, amount_sell):
        return True


class PriceFetcherMock(PriceFetcher):
    def request_price(self, sell, buy, amount_sell=1):
        return 1


class TelegramBotTest(TestCase):

    def setUp(self):
        current_chat = Chat(chat_id='chat_id')
        eth_balance = Balance(coin="ETH", value=100, chat=current_chat)
        btc_balance = Balance(coin="BTC", value=10, chat=current_chat)
        usdt_balance = Balance(coin="USDT", value=1000000000, chat=current_chat)
        current_chat.save()
        eth_balance.save()
        btc_balance.save()
        usdt_balance.save()
        self.chat = current_chat

    def test_attempt_sell_insufficient(self):
        self.assertRaises(
            InsufficientBalance,
            attempt_sell,
            selling_token="BTC",
            buying_token="ETH",
            amount_sell=11,
            chat=self.chat,
            deal_executor=DealExecutorMock(),
            price_fetcher=PriceFetcherMock(),
        )

    def test_attempt_purchase_insufficient(self):
        self.assertRaises(
            InsufficientBalance,
            attempt_sell,
            selling_token="ETH",
            buying_token="BTC",
            amount_sell=101,
            chat=self.chat,
            deal_executor=DealExecutorMock(),
            price_fetcher=PriceFetcherMock(),
        )

    def test_attempt_sell_correct(self):
        before_eth_balance = Balance.objects.get(coin="ETH", chat=self.chat)
        before_btc_balance = Balance.objects.get(coin="BTC", chat=self.chat)
        response_message = attempt_sell(
            selling_token="BTC",
            buying_token="ETH",
            amount_sell=1,
            chat=self.chat,
            deal_executor=DealExecutorMock(),
            price_fetcher=PriceFetcherMock(),
        )
        self.assertIn("Your trade wass successfully executed", response_message)
        new_eth_balance = Balance.objects.get(coin="ETH", chat=self.chat)
        new_btc_balance = Balance.objects.get(coin="BTC", chat=self.chat)
        self.assertEqual(new_btc_balance.value + 1, before_btc_balance.value)
        self.assertEqual(new_eth_balance.value - 1, before_eth_balance.value)
        trades = TradeRequest.objects.count()
        self.assertEqual(trades, 1)

    def test_attempt_purchase_correct(self):
        before_eth_balance = Balance.objects.get(coin="ETH", chat=self.chat)
        before_btc_balance = Balance.objects.get(coin="BTC", chat=self.chat)
        response_message = attempt_purchase(
            selling_token="ETH",
            buying_token="BTC",
            amount_purchase=1,
            chat=self.chat,
            deal_executor=DealExecutorMock(),
            price_fetcher=PriceFetcherMock(),
        )
        self.assertIn("Your trade wass successfully executed", response_message)
        new_eth_balance = Balance.objects.get(coin="ETH", chat=self.chat)
        new_btc_balance = Balance.objects.get(coin="BTC", chat=self.chat)
        self.assertEqual(new_btc_balance.value - 1, before_btc_balance.value)
        self.assertEqual(new_eth_balance.value + 1, before_eth_balance.value)
        trades = TradeRequest.objects.count()
        self.assertEqual(trades, 1)