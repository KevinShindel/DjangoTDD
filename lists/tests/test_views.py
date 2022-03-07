from html import escape
from unittest import skip

from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    @skip
    def test_home_page_uses_item_form(self):
        pass


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response: HttpResponse = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response=response, expected_url=f'/lists/{new_list.id}/')

    def test_root_url_resolves_to_home_page_view(self):
        ''' тест домашней страницы '''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        html = response.content.decode(encoding='utf-8')
        self.assertTrue(html.__contains__('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_validation_errors_are_sent_back_to_template(self):
        ''' тест: ошибки валидации отсылаются назад в шаблон домашней страницы '''
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        ''' тест: сохраняются недопустимые элементы списка '''
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    ''' тест представления списка '''

    def test_passes_correct_list_to_template(self):
        _ = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response: HttpResponse = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response=response, template_name='lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Another element 1', list=other_list)
        Item.objects.create(text='Another element 2', list=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

        self.assertNotContains(response, 'Another element 1')
        self.assertNotContains(response, 'Another element 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """ тест: можно сохранить пост-запрос в существующий список """
        _ = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(path=f'/lists/{correct_list.id}/',
                         data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """ тест: переадресуется в представление списка """
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(path=f'/lists/{correct_list.id}/',
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        ''' тест: ошибки валидации оканчиваютяс на странице списков '''
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)