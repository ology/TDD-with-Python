from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root(self):
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_save(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 0)

    def test_post(self):
        item_text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

        self.assertIn(item_text, response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': item_text}
        )
        self.assertIn(item_text, response.content.decode())

class ItemModelTest(TestCase):

    def test_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')

        second_saved_item = saved_items[1]
        self.assertEqual(second_saved_item.text, 'Item the second')
