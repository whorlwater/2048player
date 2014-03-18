from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from random import choice
import argparse

class Session(object):
    def __init__(self):
        self.browser = webdriver.Firefox()

    def type_keys(self, xpath, keys):
        element = self.browser.find_element_by_xpath(xpath)
        ActionChains(self.browser).move_to_element(element).send_keys(keys).perform()

    def click_on_element(self, xpath):
        element = self.browser.find_element_by_xpath(xpath)
        element.click()

    def type_text(self, xpath, text):
        element = self.browser.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(text)

    def element_exists(self, xpath):
        elements = self.browser.find_elements_by_xpath(xpath)
        if len(elements) == 1:
            return True
        else:
            return False

    def an_element_exists(self, xpath):
        elements = self.browser.find_elements_by_xpath(xpath)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_details(self, xpath, element_type, parameter=None):
        if element_type == 'text':
            return self.browser.find_element_by_xpath(xpath).text
        elif element_type == 'attribute':
            return self.browser.find_element_by_xpath(xpath).get_attribute(parameter)
        else:
            print 'ERROR IN GET_ELEMENT: element_type can only be "text" or "attribute".'
            return None


def error(message):
    return 'ERROR: %s Retrying.' % (message)

def critical_error(message):
    return 'CRITICAL ERROR: %s Ending.' % (message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='Choose random or ordered method of play.', choices=['random','ordered'])
    args = parser.parse_args()
    args = vars(args)

    current_session = Session()
    current_session.browser.get('http://gabrielecirulli.github.io/2048/')
    play_2048(current_session, current_session.browser, args)

def play_2048(session, browser, args):
    xpath = {
    'gameboard' : '//div[@class="game-container"]',
    'gameover' : '//div[@class="game-message game-over"]',
    'retry' : '//a[@class="retry-button"]'
    }

    command_list = [Keys.ARROW_UP,Keys.ARROW_RIGHT,Keys.ARROW_DOWN,Keys.ARROW_LEFT]

    session.click_on_element(xpath['gameboard'])

    if args['method'] == 'random':
        while session.element_exists(xpath['gameboard']) is True:
            if session.element_exists(xpath['gameover']) is not True:
                command = choice(command_list)
                session.type_keys(xpath['gameboard'],command)
            else:
                session.click_on_element(xpath['retry'])

    elif args['method'] == 'ordered':
        while session.element_exists(xpath['gameboard']) is True:
            if session.element_exists(xpath['gameover']) is not True:
                for command in command_list:
                    session.type_keys(xpath['gameboard'],command)
            else:
                session.click_on_element(xpath['retry'])

    else:
        critical_error('Game method not available option. Check method argument choices against actual game methods.')


if __name__=="__main__":
    main()

