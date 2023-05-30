from django.db import models

class Palavra(models.Model):
    key = models.CharField(max_length=255)
    frequencia = models.IntegerField()
