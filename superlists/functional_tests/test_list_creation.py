from .base import FunctionalTest
from selenium import webdriver

class NewVisitorTest(FunctionalTest):

    def test_list_for_one_user(self):
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

    def test_list_for_multiple_users(self):
        # Visit the URL
        self.browser.get(self.live_server_url)

        # Declare the new item input
        inputbox = self.browser.find_element_by_id('id_new_item')

        # User enters a to-do item and updates form
        item_text_A = 'Buy peacock feathers'
        self.input_keys(inputbox, item_text_A)

        # The to-do item is shown
        self.check_row(1, item_text_A)

        # Check that URL is unique
        list_url_A = self.browser.current_url
        self.assertRegex(list_url_A, '/lists/.+')

        # Create a new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Visit the URL
        self.browser.get(self.live_server_url)

        # Check page text
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(item_text_A, page_text)
        
        # Declare the new item input
        inputbox = self.browser.find_element_by_id('id_new_item')

        # User enters a to-do item and updates form
        item_text_B = 'Buy milk'
        self.input_keys(inputbox, item_text_B)

        # The to-do item is shown
        self.check_row(1, item_text_B)

        # Check that URL is unique
        list_url_B = self.browser.current_url
        self.assertRegex(list_url_B, '/lists/.+')
        self.assertNotEqual(list_url_B, list_url_A)

        # Check page text
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(item_text_A, page_text)
        self.assertIn(item_text_B, page_text)
