from django.conf import settings
from django.db import models
from django.urls import reverse


class List(models.Model):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @classmethod
    def create_new(cls, first_item_text, owner=None):
        list_ = cls.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.item_set.first().text


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
