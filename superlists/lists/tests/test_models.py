from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ListAndItemModelsTest(TestCase):

    def test_items(self):
        test_list = List()
        test_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = test_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = test_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, test_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, test_list)

        second_saved_item = saved_items[1]
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, test_list)

    def test_cannot_save_empty(self):
        my_list = List.objects.create()
        item = Item(text='', list=my_list)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()