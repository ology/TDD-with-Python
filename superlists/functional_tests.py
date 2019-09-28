from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_page(self):
        # Visit the URL
        self.browser.get('http://localhost:8000')

        # Check title
        self.assertIn('To-Do', self.browser.title)

        # Check H1 text
        h1_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', h1_text)

        # Check user is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User enters a first to-do item
        item_text = 'Buy peacock feathers'
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        # Page updates and lists the first entered to-do item
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_text, [row.text for row in rows])

        # User enters a second to-do item
        item_text = 'Use peacock feathers'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        # Page updates and lists the second entered to-do item
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_text, [row.text for row in rows])

        # User visits a different page
        # User returns to the site
        # Two to-do items are listed


if __name__ == '__main__':
    unittest.main()