from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

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

    def test_post(self):
        item_text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['id_new_item'] = item_text
        response = home_page(request)

        self.assertIn(item_text, response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': item_text}
        )
        self.assertIn(item_text, response.content.decode())