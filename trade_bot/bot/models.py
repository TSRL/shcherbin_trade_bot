from django.db import models
from django.contrib.postgres.fields import ArrayField


# This model depends on postgress specific ArrayField for simplicity
class Chat(models.Model):
    chat_id = models.CharField(unique=True, primary_key=True)
    requests = ArrayField(models.TextField(), default=list)
    deals = ArrayField(models.JSONField(), default=list)
