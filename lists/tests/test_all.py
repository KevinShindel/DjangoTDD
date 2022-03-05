from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.views import home_page


class NewListTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
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


class ItemModelTest(TestCase):
    ''' тест модели элемента списка '''

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items.first()
        second_saved_item = saved_items.last()

        self.assertEqual(first_item, first_saved_item)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_item, second_saved_item)
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    ''' тест представления списка '''

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
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


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """ тест: можно сохранить пост-запрос в существующий список """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(path=f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """ тест: переадресуется в представление списка """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(path=f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
