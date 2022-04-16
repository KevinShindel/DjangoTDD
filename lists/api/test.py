import json

from django.test import TestCase

from lists.models import List, Item


class ListAPITest(TestCase):
    base_url = '/api/lists/{}'

    def test_get_returns_json_200(self):
        ''' тест возвращает json и код состояния 200'''
        list_ = List.objects.create()
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_for_correct_list(self):
        ''' тест получает отклик с элементами списка '''
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='item 1')
        our_list = List.objects.create()
        item1 = Item.objects.create(list=our_list, text='item 1')
        item2 = Item.objects.create(list=our_list, text='item 2')
        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            [
                {'id': item1.id, 'text': item1.text},
                {'id': item2.id, 'text': item2.text}
            ]
        )

    def test_POSTing_a_new_item(self):
        list_ = List.objects.create()
        response = self.client.post(self.base_url.format(list_.id), data={'text': 'new_item'})
        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.get()
        self.assertEqual(new_item.text, 'new_item')

