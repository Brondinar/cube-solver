from django.db import models

class OnlineGameData(models.Model):
    secret_number = models.CharField(max_length=10)
    move = models.IntegerField(default=0)
    cows = models.IntegerField(default=0)
    bulls = models.IntegerField(default=0)