from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

from lists.views import home_page, view_list

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

    def test_no_post(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 0)

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

class ListViewTest(TestCase):

    def test_list_template(self):
        response = self.client.get('/lists/foo/')
        self.assertTemplateUsed(response, 'list.html')

    def test_all_items(self):
        test_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=test_list)
        Item.objects.create(text='itemey 2', list=test_list)

        response = self.client.get('/lists/foo/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

    def test_post(self):
        item_text = 'A new list item'
        self.client.post('/lists/new', data={ 'item_text': item_text })

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect(self):
        item_text = 'A new list item'
        response = self.client.post('/lists/new', data={ 'item_text': item_text })
        self.assertRedirects(response, '/lists/foo/')
