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

    def check_update(self, inputbox, item_text):
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_text, [row.text for row in rows])

    def test_page(self):
        # Visit the URL
        self.browser.get('http://localhost:8000')

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

        # User enters a to-do item
        # Page updates and lists the to-do item
        self.check_update(inputbox, 'Buy peacock feathers')

        # Re-declare the new item input
        inputbox = self.browser.find_element_by_id('id_new_item')

        # User enters a to-do item
        # Page updates and lists the to-do item
        self.check_update(inputbox, 'Use peacock feathers')

        # User visits a different page
        # User returns to the site
        # Two to-do items are listed


if __name__ == '__main__':
    unittest.main()