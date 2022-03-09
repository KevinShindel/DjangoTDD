from django.db import models
from django.urls import reverse


class List(models.Model):
    pass

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):

    class Meta:
        ordering = ('id', )
        constraints = [
            models.UniqueConstraint(fields=('text', 'list'), name='uniq list with text'),
        ]
    text = models.CharField(max_length=100)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text
