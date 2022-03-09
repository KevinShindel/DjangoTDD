from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import TestCase

from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    ''' тест представления списка '''



    def test_item_is_related_to_list(self):
        ''' тест элемент связан со списком '''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_duplicate_items_are_invalid(self):
        ''' тест повторы элементов не допустимы '''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        ''' test может сохранить один и тот же елемент в разные списки'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

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

    def test_cannot_save_empty_list_items(self):
        ''' тест: нельзя добавлять пустые елементы списка '''
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()



    def test_list_ordering(self):
        ''' тест упорядочения списка '''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='item 1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='item 3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        ''' тест строкового представления '''
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ItemModelTest(TestCase):

    def test_default_text(self):
        ''' тест заданного по-умолчанию теста '''
        item = Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        ''' тест: получен асболютный url '''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
