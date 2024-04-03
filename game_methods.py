from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, NoAlertPresentException

# URL for the scaling simulation
URL = "http://sdetchallenge.fetch.com/"

# bowls strings
LEFT_BOWL = "left"
RIGHT_BOWL = "right"

# allert message strings
ALLERT_MESSAGE_RIGHT = "Yay! You find it!"
ALLERT_MESSAGE_WRONG = "Oops! Try Again!"


def open_game_page():
    """ Opens google chrome to the specified webpage and maxamizes the window """

    try:
        chrome_driver = webdriver.Chrome()
        chrome_driver.get(URL)
        chrome_driver.maximize_window()  # if not maximized the number may not be visible

        return chrome_driver
    except WebDriverException as e:
        print(f"An error occurred while opening the page: {e}")


def click_weigh_button(driver):
    """ 
    Clicks the 'Weigh' button on the web page and waits until the weighing results are updated.

    Parameters:
        driver : WebDriver
            The Selenium WebDriver instance used to interact with the web page.
    """
    try:
        driver.find_element(By.ID, "weigh").click()
        WebDriverWait(driver, 10).until(
            lambda wait: get_compare_results(driver) != "?")

    except NoSuchElementException as e:
        print(f"An error occurred while clicking the weigh button: {e}")
    except TimeoutException as e:
        print(
            f"An error occurred while waiting for the weighing results to update: {e}")


def click_reset_button(driver):
    """
    Clicks the reset button to clear the bowls

    Parameters:
        driver : WebDriver
            The Selenium WebDriver instance used to interact with the web page.
    """
    try:
        reset_buttons = driver.find_elements(By.ID, "reset")
        reset_buttons[1].click()
    except NoSuchElementException as e:
        print(f"An error occurred while clicking the reset button: {e}")


def get_compare_results(driver):
    """ 
    Gets the compare results which is displayed between the bowls.

    Parameters:
        driver : WebDriver
            The Selenium WebDriver instance used to interact with the web page. 

    Return:
        The compare results as a string.
    """
    try:
        compare_results = driver.find_element(
            By.CLASS_NAME, "result").find_element(By.ID, "reset")
        return compare_results.text
    except NoSuchElementException as e:
        print(f"An error occurred while getting the compare results: {e}")


def fill_one_cell(driver, bowl, cell_number, bar_number):
    """ 
        Enters the value of 'bar_number' into one specific cell at left bowl or right bowl

        Parameters:
            driver : webdriver
               The Selenium WebDriver instance used to interact with the web page. 

            bowl : str 
                which bowl the bar number should be put in 'left' or 'right'

            cell_number : int
                cell number indicating which cell the bar number should be put in, 0-8

            bar_number : int
                the number that will be typed into the field 
    """
    try:
        cell = driver.find_element(By.ID, f"{bowl}_{cell_number}")
        cell.send_keys(bar_number)

        WebDriverWait(driver, 10).until(
            lambda driver: cell.get_attribute("value") == str(bar_number),
            f"Failed to fill cell {cell_number} in {bowl} with {bar_number}"
        )
    except NoSuchElementException as e:
        print(
            f"An error occurred while finding the cell to fill bar number: {e}")
    except TimeoutException as e:
        print(f"An error occurred while waiting for the cell to fill: {e}")


def fill_bowl(driver, bowl, list_of_settings):
    """ 
        Fills the indicated bowl using the values and box numbers in the list

        Parameters:
            driver : webdriver
                The Selenium WebDriver instance used to interact with the web page. 

            bowl : str
                which bowl the bar number should be put in 'left' or 'right'

            list_of_settings : list
                list of tuples containting the cell number and a bar number should be placed in that cell 
                Format[(cell_number, bar_number)....]
    """
    for cell_number, bar_number in list_of_settings:
        fill_one_cell(driver, bowl, cell_number, bar_number)


def get_weighings(driver):
    """ 
    Gets the list of weighings

    Parameters:
        driver : webdriver
            The Selenium WebDriver instance used to interact with the web page.

    Return:
        The list of weighings as a string.
    """
    try:
        weighings_info = driver.find_element(By.CLASS_NAME, "game-info")
        weighings_list = weighings_info.find_element(By.TAG_NAME, "ol")
        weighings = weighings_list.get_property("innerText")

        return weighings
    except NoSuchElementException as e:
        print(f"An error occurred while getting the weighings: {e}")


def click_bottom_gold_bar(driver, bar_number):
    """ 
    Clicks the gold bar number at the bottom of the website, and checks for the alert message. 

    Parameters:
        driver : webdriver
           The Selenium WebDriver instance used to interact with the web page.
        bar_number : int
            the number of the gold bar that should be clicked
    Return:
        The alert message as a string. 
    """
    try:
        bar = driver.find_element(By.ID, f"coin_{bar_number}")
        bar.click()

        # Wait for the alert to be present and switch to it
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        message = alert.text
        alert.accept()

        return message
    except NoSuchElementException as e:
        print(f"An error occurred while clicking the gold bar: {e}")
    except NoAlertPresentException as e:
        print(f"An error occurred while waiting for the alert: {e}")


def verify_alert_message(actual_alert):
    """ 
        Verifies that the allert text is the expected text 
            Parameters:
                driver : webdriver

                acutal_alert : str
                    the actual allert message text
            Return: 
                The return value. True for allert is as expected, False otherwise.

    """
    if ALLERT_MESSAGE_RIGHT in actual_alert:
        return True
    else:
        return False
