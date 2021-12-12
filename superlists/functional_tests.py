from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from os.path import dirname, join

from main.settings import GECKO_DRIVER


def main():
    service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
    options = Options()
    browser = webdriver.Firefox(service=service, options=options)
    browser.get('http://localhost:8000')
    assert 'The install worked successfully! Congratulations!' == browser.title
    browser.close()
    browser.quit()


if __name__ == '__main__':
    main()
