from html import escape
import unittest
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm, NewListForm
from lists.models import Item, List
from lists.views import home_page, new_list_isolated

User = get_user_model()


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        ''' тест: домашняя страница использует форму для элемента '''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListViewIntegratedTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_validation_errors_are_shown_on_home_page(self):
        ''' ошибки валидации выводятся на домашнюю страницу '''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        ''' тест владелец сохраняется если пользователь аутинтифицирован '''
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class ListViewTest(TestCase):
    ''' тест представления списка '''

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

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
                         data={'text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """ тест: переадресуется в представление списка """
        _ = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(path=f'/lists/{correct_list.id}/',
                                    data={'text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def POST_invalid_input(self):
        ''' отправляет не допустимый ввод '''
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        ''' тест на недопустимый ввод: ничего не сохраняется в бд '''
        self.POST_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        ''' тест на недопустимый ввод: отображается шаблон списка '''
        response = self.POST_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        ''' тест на недопустимый ввод: форма передается в шаблон '''
        response = self.POST_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        ''' тест на недопустимый ввод на странице отображается ошибка '''
        response = self.POST_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        ''' тест ошибки валидации повторяющегося элемента '''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(f'/lists/{list1.id}/', data={'text': 'textey'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class MyListTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get('/lists/users/a@b.com')
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner_to_template(self):
        ''' тест передается правильный владелец в шаблон '''
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com')
        self.assertEqual(response.context['owner'], correct_user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    ''' модульный тест нового представления списка '''

    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = unittest.mock.Mock()

    @patch('lists.views.redirect')
    def test_saves_form_with_owner_if_form_valid(
            self, mock_redirect, mockNewListForm
                                                 ):
        ''' тест '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list_isolated(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    def test_saves_form_with_owner_if_form_invalid(
            self, mockNewListForm
    ):
        ''' тест сохраняет форму с владельцем если форма допустима '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list_isolated(self.request)
        self.assertFalse(mock_form.save.called)

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        ''' тест передаются POST данные в новую форму списка '''
        mock_from = mockNewListForm.return_value
        list_ = mock_from.save.return_value
        list_.get_absolute_url.return_value = 'fakeurl'
        new_list_isolated(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mockNewListForm
    ):
        ''' тест отображает домашний шаблон с формой если форма не достустима '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list_isolated(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            request=self.request, template_name='lists/home.html', context={'form': mock_form}
        )
