from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

from lists.views import home_page, view_list

class HomePageTest(TestCase):

    def post_text(self, item_text):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_text
        response = home_page(request)
        return response

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

    def test_post(self):
        item_text = 'A new list item'
        response = self.post_text(item_text)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect(self):
        response = self.post_text('A new list item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/foo/')

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

class ListViewTest(TestCase):

    def test_list_template(self):
        response = self.client.get('/lists/foo/')
        self.assertTemplateUsed(response, 'list.html')

    def test_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/foo/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
