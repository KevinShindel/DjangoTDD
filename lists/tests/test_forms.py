from unittest import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        ''' тест: форма отображает текстовое поле ввода '''
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        ''' тест: валидации формы для пустых элементов '''
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        ''' тест: метод сохранения формы '''
        form = ItemForm(data={'text': 'do me'})
        list_ = List.objects.create()
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)
