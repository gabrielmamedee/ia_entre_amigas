from django.db import models

class Palavra(models.Model):
    key = models.CharField(max_length=255)
    frequencia = models.IntegerField()


class Drive_arquivo(models.Model):
    nome = models.CharField(max_length=255)
    link = models.URLField()
    link_download = models.URLField()