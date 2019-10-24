import unittest
import time

from configs.page_configs import PageConfig
from page.page import Page
from step.step import Step


class TestOtherPages(unittest.TestCase):
    def test_saucedemo_page(self):
        cf = PageConfig('https://www.saucedemo.com/inventory.html')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        bp.collect_elements([
            ("xpath", "(//button[@class='btn_primary btn_inventory'])[1]", "inv_btn1"),
            ("xpath", "(//button[@class='btn_primary btn_inventory'])[2]", "inv_btn2"),
            ("xpath", "(//button[@class='btn_primary btn_inventory'])[3]", "inv_btn3"),
            ("class", "shopping_cart_badge", "Cart Badge"),
            ("class", "shopping_cart_link", "Cart Link"),
            ("class", "cart_button", "Cart Button"),
            ("class", "checkout_button", "Checkout Button"),
            ("id", "first-name", "First Name"),
            ("id", "last-name", "Last Name"),
            ("id", "postal-code", "Zip"),
            ("class", "complete-header", "Completion Header")
        ])

        steps = [
            Step("click", bp.element("inv_btn1")),
            Step("click", bp.element("inv_btn2")),
            Step("click", bp.element("inv_btn3"))
        ]
        bp.do(steps)
        items_in_cart = bp.element("Cart Badge").get("innerHTML")
        self.assertEqual(items_in_cart, "3")

        bp.element("Cart Link").click()
        bp.element("Cart Button").click()
        items_in_cart = bp.element("Cart Badge").get("innerHTML")
        self.assertEqual(items_in_cart, "2")

        bp.element("Checkout Button").click()

        steps = [
            Step("type", bp.element("First Name"), "Jane"),
            Step("type", bp.element("Last Name"), "Doe"),
            Step("type", bp.element("Zip"), "12345"),
            Step("click", bp.element("Cart Button"))
        ]
        bp.do(steps)

        bp.element("Cart Button").click()
        checkout_complete_page = bp.element("Completion Header").get("innerHTML")
        self.assertEqual(checkout_complete_page, "THANK YOU FOR YOUR ORDER")

        bp.close()

    def test_saucedemo_refresh_page(self):
        cf = PageConfig('https://www.saucedemo.com/inventory.html')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        bp.collect_elements([
            ("xpath", "(//button[@class='btn_primary btn_inventory'])[1]", "button 1"),
            ("xpath", "(//div[@class='inventory_item_name'])[1]", "inventory item"),
            ("class", "shopping_cart_badge", "shopping cart badge"),
            ("class", "inventory_item_name", "item name")
        ])

        bp.element("button 1").click()
        item_name = bp.element("inventory item").get("innerHTML")
        items_in_cart = bp.element("shopping cart badge").get("innerHTML")

        self.assertEqual(items_in_cart, "1")
        bp.go()

        items_in_cart = bp.element("shopping cart badge").get("innerHTML")
        self.assertEqual(items_in_cart, "1")

        bp.navigate_to('https://www.saucedemo.com/cart.html')

        inventory_item_name = bp.element("item name").get("innerHTML")
        self.assertEqual(item_name, inventory_item_name)

        bp.close()

    def test_javascript_alert(self):
        cf = PageConfig('https://the-internet.herokuapp.com/javascript_alerts')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        bp.grab("xpath", "(//button)[1]").click()
        alert = bp.get_alert()

        self.assertEqual(alert.text, "I am a JS Alert")
        
        alert.accept()
        bp.close()

    def test_javascript_confirm(self):
        cf = PageConfig('https://the-internet.herokuapp.com/javascript_alerts')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        bp.grab("xpath", "(//button)[2]").click()
        alert = bp.get_alert()

        self.assertEqual(alert.text, "I am a JS Confirm")
        
        alert.dismiss()
        bp.close()

    def test_javascript_prompt(self):
        cf = PageConfig('https://the-internet.herokuapp.com/javascript_alerts')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        bp.grab("xpath", "(//button)[3]").click()
        alert = bp.get_alert()

        self.assertEqual(alert.text, "I am a JS prompt")

        alert.input_text("This is a test")
        alert.accept()

        result = bp.grab("id", "result").get("innerHTML")
        self.assertEqual(result, "You entered: This is a test")

        bp.close()

    def test_floating_menu(self):
        """
        Checks if a menu floats when scrolling the page

        Considerations taken to asserts it floats:
            1) The element moves when scrolling
            2) At least half of the element is visible after scrolling
               a distance greater than its height + initial top offset
        """
        cf = PageConfig('https://the-internet.herokuapp.com/floating_menu')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()

        menu = bp.grab("id", "menu")
        height = int(menu.get('offsetHeight'))
        initial_top_offset = menu.element.rect.get('y')

        scroll_distance = 300
        bp.page.execute_script('window.scrollTo(0, {});'.format(scroll_distance))
        time.sleep(1)

        final_top_offset = menu.element.rect.get('y')

        self.assertGreater(final_top_offset, initial_top_offset)
        self.assertGreater(scroll_distance, height + initial_top_offset)
        self.assertGreater(final_top_offset + height/2, scroll_distance)

        bp.close()

    def test_autocompletion(self):
        def get_number_suggestions():
            suggestions = bp.grab('id', 'ui-id-1')
            suggestions.activate_element()
            suggestions_list = suggestions.element.find_elements_by_tag_name('li')        
            return len(suggestions_list)
             
        cf = PageConfig('https://demoqa.com/autocomplete/')
        cf.options_list.append("headless")
        bp = Page(cf)
        bp.go()
 
        sug_number = []
        textbox = bp.grab('id', 'tags')
        textbox.input_text('a')
        sug_number.append(get_number_suggestions())
        textbox.input_text('s')  # needs time to repopulate list
        time.sleep(0.5)
        sug_number.append(get_number_suggestions())
 
        self.assertEqual(sug_number, [10, 4])
         
        bp.close()
