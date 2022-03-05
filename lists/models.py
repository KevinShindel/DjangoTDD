from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.CharField(max_length=100)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
