# XXX $ rm db.sqlite3
# XXX $ python3 manage.py migrate --noinput

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def input_keys(self, inputbox, item_text):
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def check_row(self, item_num, item_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(str(item_num) + ': ' + item_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_page(self):
        # Visit the URL
        self.browser.get(self.live_server_url)

        # Check title
        self.assertIn('To-Do', self.browser.title)

        # Check H1 text
        h1_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', h1_text)

        # Declare the new item input
        inputbox = self.browser.find_element_by_id('id_new_item')

        # Check user is invited to enter a to-do item
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User enters a to-do item and updates form
        item_text = 'Buy peacock feathers'
        self.input_keys(inputbox, item_text)

        # The to-do item is shown
        self.check_row(1, item_text)

        # Re-declare the new item input
        inputbox = self.browser.find_element_by_id('id_new_item')

        # User enters a to-do item and updates form
        item_text = 'Use peacock feathers'
        self.input_keys(inputbox, item_text)

        # The to-do item is shown
        self.check_row(2, item_text)
