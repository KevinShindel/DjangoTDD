from selenium.webdriver.common.by import By


class MyListsPage:

    def __init__(self, test):
        self.test = test

    def got_to_my_lists_page(self):
        ''' перейти на мою страницу списков '''
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        self.test.wait_for(
            lambda: self.test.assertEqual(
                self.test.browser.find_element(by=By.TAG_NAME, value='h1').text, 'My Lists'
            )
        )
        return self
