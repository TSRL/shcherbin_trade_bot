import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Chat(models.Model):
    chat_id = models.CharField(unique=True, primary_key=True)


class TradeRequest(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    coin_sold = models.CharField(null=False)
    coin_purchased = models.CharField(null=False)
    amount_sell = models.FloatField(null=True)
    amount_purchase = models.FloatField(null=True)
    price = models.FloatField(null=True)
    finished = models.BooleanField(null=False)
    finished_timestamp = models.DateTimeField(null=True)
    successful = models.BooleanField(null=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)


class Balance(models.Model):
    coin = models.CharField(primary_key=True)
    value = models.FloatField(default=0)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)


class ArbitraryRequest(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.TextField(null=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)

