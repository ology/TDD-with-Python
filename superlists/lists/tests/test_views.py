from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
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

        self.assertTrue(response.content.startswith(b'<!doctype html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        #self.assertTrue(response.content.endswith(b'</html>'))

    def test_no_post(self):
        request = HttpRequest()
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def test_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(f'/lists/{my_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_all_items(self):
        test_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=test_list)
        Item.objects.create(text='itemey 2', list=test_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{test_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_post_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        item_text = 'A new item for an existing list'

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': item_text}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        item_text = 'A new item for an existing list'

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': item_text}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_on_lists_page(self):
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape('Empty list item not allowed')
        self.assertContains(response, expected_error)

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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape('Empty list item not allowed')
        self.assertContains(response, expected_error)

    def test_invalid_items_not_saved(self):
        self.client.post('/lists/new', data={ 'item_text': '' })
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
