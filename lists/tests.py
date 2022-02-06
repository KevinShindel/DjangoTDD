from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_post_request(self):
        response: HttpResponse = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response: HttpResponse = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_save_items_when_necessary(self):
        ''' тест: сохраянет элементы только когда нужно '''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        ''' отображаются все элементы списка '''
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn('item 1', content)
        self.assertIn('item 2', content)

    def test_root_url_resolves_to_home_page_view(self):
        ''' тест домашней страницы '''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        html = response.content.decode(encoding='utf-8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.endswith('</html>'))


class ItemModelTest(TestCase):
    ''' тест модели элемента списка '''

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items.first()
        second_saved_item = saved_items.last()

        self.assertEqual(first_item, first_saved_item)
        self.assertEqual(second_item, second_saved_item)
