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

    def get_details(self, xpath, element_type, how_many, parameter=None):
        if element_type == 'text':
            if how_many == 'first':
                return self.browser.find_element_by_xpath(xpath).text
            elif how_many == 'all':
                list_of_details = self.browser.find_elements_by_xpath(xpath)
                list_of_details_text = [detail.text for detail in list_of_details]
                return list_of_details_text
            else:
                critical_error('The total of get_details() can only be "first" or "all".')
        elif element_type == 'attribute':
            if how_many == 'first':
                return self.browser.find_element_by_xpath(xpath).get_attribute(parameter)
            elif how_many == 'all':
                list_of_details = self.browser.find_elements_by_xpath(xpath)
                list_of_details_attributes = [detail.get_attribute(parameter) for detail in list_of_details]
                return list_of_details_attributes
            else:
                critical_error('The total of get_details() can only be "first" or "all".')
        else:
            critical_error('The element_type of get_details() can only be "text" or "attribute".')
            return None


def error(message):
    return 'ERROR: %s Retrying.' % (message)

def critical_error(message):
    return 'CRITICAL ERROR: %s Ending.' % (message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='Choose random, ordered, or preferred method of play.', choices=['random','ordered','preferred'])
    args = parser.parse_args()
    args = vars(args)

    current_session = Session()
    current_session.browser.get('http://gabrielecirulli.github.io/2048/')
    play_2048(current_session, current_session.browser, args)


def play_2048(session, browser, args):
    xpath = {
    'gameboard'     : '//div[@class="game-container"]',
    'gameover'      : '//div[@class="game-message game-over"]',
    'retry'         : '//a[@class="retry-button"]',
    'cell_contents' : '//div[@class="tile-inner"]',
    'new_tiles'     : '//div[contains(@class, "tile-new")]',
    'merged_tiles'  : '//div[contains(@class, "tile-merged")]'
    }

    command_list = [Keys.ARROW_UP,Keys.ARROW_RIGHT,Keys.ARROW_DOWN,Keys.ARROW_LEFT]

    up    = command_list[0]
    right = command_list[1]
    down  = command_list[2]
    left  = command_list[3]

    session.click_on_element(xpath['gameboard'])

    def retry():
        session.click_on_element(xpath['retry'])

    def gameboard_exists():
        return session.element_exists(xpath['gameboard'])

    def game_is_over():
        return session.element_exists(xpath['gameover'])

    def move(command):
        session.type_keys(xpath['gameboard'],command)

    def new_tiles():
        return session.get_details(xpath['new_tiles'], 'attribute', 'all', 'class')

    def merged_tiles():
        return session.get_details(xpath['merged_tiles'], 'attribute', 'all', 'class')

    if args['method'] == 'random':
        while gameboard_exists() is True:
            if game_is_over() is not True:
                command = choice(command_list)
                move(command)
            else:
                retry()

    elif args['method'] == 'ordered':
        while gameboard_exists() is True:
            if game_is_over() is not True:
                for command in command_list:
                    move(command)
            else:
                retry()

    elif args['method'] == 'preferred':
        while gameboard_exists() is True:
            if game_is_over() is not True:
                initial_new_tiles = new_tiles()
                initial_merged_tiles = merged_tiles()
                move(down)
                if new_tiles() == initial_new_tiles and merged_tiles() == initial_merged_tiles:
                    move(left)
                    if new_tiles() == initial_new_tiles and merged_tiles() == initial_merged_tiles:
                        move(right)
                        if new_tiles() == initial_new_tiles and merged_tiles() == initial_merged_tiles:
                            move(up)
            else:
                retry()

    else:
        critical_error('Game method not available option. Check method argument choices against actual game methods.')


if __name__=="__main__":
    main()

