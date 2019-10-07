from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty(self):
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        error_text = 'Empty list item not allowed'
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            error_text
        ))

        item_text_A = 'Make tea'
        self.browser.find_element_by_id('id_new_item').send_keys(item_text_A)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.check_row(1, item_text_A)

        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            error_text
        ))

        item_text_B = 'Drink tea'
        self.browser.find_element_by_id('id_new_item').send_keys(item_text_B)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.check_row(1, item_text_A)
        self.check_row(2, item_text_B)
