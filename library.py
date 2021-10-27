import datetime
import time
import dataclasses
import enum
import csv
import json
import typing
from collections.abc import Sequence, Mapping, Container
from functools import partial

from pynput import keyboard
from pynput.keyboard import Key

import selenium
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.support.select import Select

from PARAM import *


def today_date(option="world") -> str:
    "Returns today's date for form."
    now = datetime.datetime.now()
    if option == 'world':
        str1 = now.strftime('%d/%m/%Y')
    elif option == "usa":
        str1 = now.strftime('%m/%d/%Y')
    else:
        str1 = now.strftime('%m/%d/%Y')
    return str1

def best_of_dict(dict1:dict, key:typing.Any):
    """Returns the best value of dict1 given key."""
    # Check dict1 for key directly
    try:
        dict1[key]
        # dict1.get(key)
    except KeyError:
    # Match key as best as possible
        # return 'key' if it is in values
        if key in dict1.values(): return key
        # text match
        keys = list(dict1.keys())
        if isinstance(key, str):
            # Case insensitive key match
            best_key = [k for k in keys if key.lower() == k.lower()]
            if best_key: return best_key[0]
            # Levenshtein Distance
            # TO BE DONE



#Configure
observer_name : str = "Darnell Baird"
date : str = today_date()
tsv_load_file = 'file.tsv'
tsv_save_file = "completed.tsv"
website_url = "https://forms.office.com/pages/responsepage.aspx?id=KupABOviREat2LyPNxBbYeaRdFMG3AdBl5FpMuhBKwdUOTlWWUlCVUxHUFU3TENVUUVaMDlMUkw3USQlQCN0PWcu"

class Config():
    data = dict()

    def __init__(self):
        """Load config file and assign variables"""
        # Load config file
        self.load_config()
        # Assign variables
        self.assign_configs()

    def load_config(self, filename=CONFIG_FILE):
        """Load data with json file info."""
        with open(filename, mode="r") as file:
            self.data = json.load(file)

    def assign_configs(self):
        """Assign config values to classes/variables."""
        classes = [Inputs, ]
        for clas in classes:
            # Get class dict
            if clas in self.data:
                clas_nm = clas.__name__
                # Pop/remove dict from config 
                dict1 = self.data.pop(clas_nm)
                # Assign variables of dict to class
                for k,v in dict1.items():
                    setattr(clas, k, v)
        # Assign other variables globally
        for k,v in self.data.items():
            globals()[k] = v


class KeyboardManager():

    class Intermission():
        pass

    end = False
    pause = False

    def __init__(self):
        self.main_listener = keyboard.Listener(on_release=self._main_on_release_callback)

    @classmethod
    def _main_on_release_callback(cls, key:Key):
        try:
            if key.char == 'q':
                cls.end = True
                print("Quit it.")
            if key.char == 'p':
                # print("I am printing.")
                cls.pause = True
                print("Paused it.")
        except AttributeError:
            pass


class Action:
    str : str = ""
    actions = list()

    def __init__(self, str1:str=""):
        """Create an action object by parsing str1"""
        self.get_driver()
        self.factory_parse_string(str1)

    def factory_parse_string(self, str1:str):
        """Parse str1 to define object"""
        self.str = str1
        if str1.lower().startswith("odor"):
            # Deal with mold odor
            # Get partitions
            try:
                _odor, intensity, message = str1.split(' ', 2)
            except ValueError:
                _odor, intensity = str1.split(' ', 1)
                message = ""
            intensity_option = best_of_dict(MOLD_ODOR, intensity)
            # Add actions to object
            self.actions = [
                # Open 'Mold Odor' dropdown
                partial(self.click_by, By.ID, "SelectId_4_placeholder", ),
                # Select intensity
                partial(self.click_by, By.CSS_SELECTOR, '[aria-label="{}"]'.format(intensity_option), ),
                # Input text: Describing Source of Mold Odor
                partial(self.send_keys_to_x(By.CSS_SELECTOR, "textarea", message, silent=True))
            ]
        elif str1.lower().startwith(""):
            pass
        elif str1.lower().startwith(""):
            pass

    def get_driver(self) -> selenium.webdriver:
        """Get driver from Selenium"""
        self.driver = Selenium.driver
        return self.driver

    def click_by_x(self, method:By, key, silent=False) -> selenium.webdriver.remote.webelement.WebElement:
        """Use driver to click on an element by method."""
        print("This is 'By' method:", method)
        try:
            element = self.driver.find_element(method, key)
            element.click()
        except selenium.common.exceptions.NoSuchElementException as err:
            if silent:
                pass
            else:
                raise err from None
        return element

    def send_keys_to_x(self, method:By, key, message, silent=False) -> selenium.webdriver.remote.webelement.WebElement:
        """ Send text/'send_keys to html element, text input.
        Search for element by method and with key.
        """
        try:
            element = self.driver.find_element(method, key)
            element.send_keys(message)
        except selenium.common.exceptions.NoSuchElementException as err:
            if silent:
                pass
            else:
                # https://stackoverflow.com/a/18188660/6556801
                raise err from None
        return element

    def run(self):
        """Carry-out the functions in action."""
        for func in self.actions:
            func()


#Inputs
@dataclasses.dataclass
class Inputs:
    room_name : str = ""
    floor_id : int = None
    room_type_id : int = None
    building_id : int = None
    date : int = today_date()

    other_arguments = list()
    other_actions = list()

    @classmethod
    def user_input_prompt(cls):
        """Prompt user for input data."""
        # observer_name = input(OBSERVER_NAME_PROMPT)
        cls.room_name = input(ROOM_NAME_PROMPT)
        cls.floor_id = int(input(FLOOR_PROMPT))
        cls.room_type_id = int(input(ROOM_TYPE_PROMPT))
        cls.building_id = int(input(BUILDING_PROMPT))
        date_response = input(BUILDING_PROMPT)
        cls.date = int(date_response) if date_response else today_date()

    @classmethod
    def row_update(cls, row):
        """Assign tsv file row to class variables."""
        cls.room_name, cls.floor_id, cls.room_type_id, cls.building_id = row

    @classmethod
    def save_tsv(cls, container:'list|tuple', filename=tsv_save_file, add_header=False):
        """Save container to tsv file."""
        with open(filename, mode="w") as fd:
            rd = csv.writer(fd, delimiter='\t')
            if add_header:
                # Adds header to top of document
                rd.writerow(TSV_HEADER)
            # Each element of container on a new line
            for ele in container:
                rd.writerow(ele)

    @classmethod
    def load_tsv(cls, filename=tsv_load_file, ignore_header=True) -> list:
        """Load tsv file"""
        ans_list = list()
        with open(filename) as fd:
            rd = csv.reader(fd, delimiter="\t")
            for i, row in enumerate(rd):
                if ignore_header and i==0 and row[0].startswith("Room "): continue
                ans_list.append(row)
        return ans_list

    @classmethod
    def get_user_inputs(cls) -> 'list[tuple[4]]':
        """Use tsv file to load in user inputs."""
        ans_list = list()
        for row in cls.load_tsv():
            row_with_type = [int(str1) if str1.isdigit() else str1 for str1 in row ]
            ans_list.append(row_with_type)
        return ans_list

    @classmethod
    def set_user_input(cls, row:list):
        """Assign arguments to/in Inputs"""
        # Assign variables
        cls.room_name, cls.floor_id, cls.room_type_id, cls.building_id, *cls.other_arguments = row
        # Create object parsers of other_arguments
        cls.parse_other_arguments()

    @classmethod
    def parse_other_arguments(cls):
        """Use factory to parse arguments."""
        cls.other_actions = list()
        for arg_str in cls.other_arguments:
            action = Action(arg_str)
            cls.other_actions.append(action)


class Xpath:
    @classmethod
    def xpath_index(cls, xpath:str, index:int) -> str:
        """Returns an xpath of index of nodes"""
        str1 = "({})[]".format(xpath, index)
        return str1

    @classmethod
    def ancestor(cls, self_xpath:str, ancestor_xpath:str) -> str:
        """Formulate and return xpath of self node and ancestor xpath"""
        str1 = "{}//ancestor::{}".format(self_xpath, ancestor_xpath)
        return str1

    @classmethod
    def descendant(cls, xpath_current:str, xpath_descending_to:str) -> str:
        """Formulate and return xpath of self node and descendant xpath"""
        str1 = "{}//descendant::{}".format(xpath_current, xpath_descending_to)
        return str1


@dataclasses.dataclass
class Question:
    label : str
    page : int
    element_type : ELEMENT_TYPE
    
    # Do not put in question_no unless you will be using it
    question_no : int = None

    def __post_init__(self):
        self.get_driver()

    def get_driver(self) -> selenium.webdriver:
        """Get driver from Selenium"""
        self.driver = Selenium.driver
        return self.driver

    def find_element(self, xpath:str) -> selenium.webdriver.remote.webelement.WebElement:
        """Shortcut for finding xpath element."""
        return self.driver.find_element(By.XPATH, xpath)

    def find_elements(self, xpath:str) -> 'list[selenium.webdriver.remote.webelement.WebElement]':
        """Shortcut for finding xpath elements."""
        return self.driver.find_elements(By.XPATH, xpath)

    def _answer_question_select_column(self):
        pass

    def _answer_question_select_row(self):
        pass

    def _answer_question_get_index(self, headings:'list[str]', answer:'int|str')->int:
        if isinstance(answer, str):
            # Select radio button according to header
            index = headings.index(answer)
        elif isinstance(answer, int):
            # Select radio button according to position
            index = answer
        else:
            AttributeError("You dont have an index.")
        return index

    def _answer_question_radiobutton_group(self, answer_container:Container, question_element:'selenium.webdriver.remote.webelement.WebElement'):
        """Abstraction level for evaluating 'answer_question' 
        for radiobutton group.
        """
        # Get header texts
        header_element = question_element.find_elements(By.XPATH, '.'+XPATH_RADIOGROUP_HEADER)
        spans = header_element.find_elements(By.XPATH, '.'+XPATH_SPAN)
        headings = [span.text for span in spans]
        # Get radio button groups
        radiogroup_elements = question_element.find_elements(By.XPATH, '.'+XPATH_RADIOGROUP)
        # Select rows based on container 'answer_container'.
        if isinstance(answer_container, Sequence):
            """Each list element deals with a row, in order."""
            pairs = zip(radiogroup_elements, answer_container)
            for radiogroup_element, answer_option in pairs:
                # Get column radiobutton
                index = self._answer_question_get_index(headings, answer_option)
                radio_button = radiogroup_element.find_element(By.XPATH, '.'+XPATH_RADIOGROUP_BUTTON)[index]
                # Click radio button
                radio_button.click()
        elif isinstance(answer_container, Mapping):
            """Each row_header_key,answer_option pair deals with row header id, and table header selection"""
            for row_header_key, answer_option in answer_container.items():
                # Get row radiogroup by side header
                xpath_radiogroup_by_side_header = XPATH_RADIOGROUP_BY_SIDE_HEADER.format(row_header_key)
                radiogroup_element = question_element.find_element(By.XPATH, '.'+xpath_radiogroup_by_side_header)
                # Get column radiobutton
                index = self._answer_question_get_index(headings, answer_option)
                radio_button = radiogroup_element.find_element(By.XPATH, '.'+XPATH_RADIOGROUP_BUTTON)[index]
                # Click radio button
                radio_button.click()

    def _answer_question_checkbox_tick_accordingly(self, ticked:bool, tick_it:bool)->bool:
        return bool(ticked) != bool(tick_it)    # XOR logic gate

    def _answer_question_checkbox_group(self, answer_container:Container, question_element:'selenium.webdriver.remote.webelement.WebElement'):
        """Abstraction level for evaluating 'answer_question' 
        for checkbox group.
        """
        # Get check boxes
        element_checkboxes = question_element.find_elements(By.XPATH, '.'+XPATH_CHECKBOX)
        if isinstance(answer_container, Sequence):
            pairs = zip(element_checkboxes, answer_container)
            for element_checkbox, decision in pairs:
                # Verify checkbox value before clicking it.
                if self._answer_question_checkbox_tick_accordingly(element_checkbox.isSelected(), bool(decision)):
                    element_checkbox.click()
        elif isinstance(answer_container, Mapping):
            # For each label, if there is a matching answer_container element, check it and tick checkbox accordingly.
            label_texts = [element_checkbox.value for element_checkbox in element_checkboxes]
            container_keys = list(answer_container.keys())
            for i, label_text in enumerate(label_texts):
                # Match conatiner key to label text
                matches = [key for key in container_keys if label_text.lower() in key.lower()]
                if matches:
                    # Click checkbox if answer suggests that.
                    match_key = matches[0]
                    match_answer = answer_container[match_key]
                    # Get checkbox
                    element_checkbox = element_checkboxes[i]
                    # Evaluate whether to click the button.
                    if self._answer_question_checkbox_tick_accordingly(element_checkbox.isSelected(), bool(match_answer)):
                        element_checkbox.click()
                else:
                    raise AttributeError("Something wrong")

    def answer_question(self, value:Container|str):
        """Select/input an answer value for the element according to its element type."""
        # Get question (by label/index)
        xpath1 = ""
        if self.question_no:
            xpath1 = XPATH_QUESTION_BY_NUMBER.format(self.question_no)
        elif self.label:
            xpath1 = XPATH_QUESTION_BY_LABEL.format(self.label)
        else:
            # NB: May not be the proper error raised.
            raise AttributeError("There isn't a parameter to select question.")
        # Get question element
        question_element = self.find_element(xpath1)
        if self.element_type == ELEMENT_TYPE.TEXT:
            # Get input element
            element = question_element.find_element(By.XPATH, '.'+XPATH_TEXTINPUT)
            element.send_keys(value)
        elif self.element_type == ELEMENT_TYPE.DROPDOWN:
            # Get dropdown element and open dropdown
            element_dropdown = question_element.find_element(By.XPATH, '.'+XPATH_DROPDOWN)
            element_dropdown.click()
            # Select dropdown
            if isinstance(value, int):
                # Select by order of dropdown
                element = question_element.find_element(By.XPATH, '.'+XPATH_DROPDOWN_OPTION_INDEX)
            elif isinstance(value, str):
                # Select by text of dropdown option
                element = question_element.find_element(By.XPATH, '.'+XPATH_DROPDOWN_OPTION_TEXT)
            # Select the option
            element.click()
        elif self.element_type == ELEMENT_TYPE.TEXTAREA:
            # Get textarea (should only have 1 textarea in entire page 1. Still explicit)
            element = question_element.find_element(By.XPATH, '.'+XPATH_TEXTAREA)
            element.send_keys(value)
        elif self.element_type == ELEMENT_TYPE.RADIO_BUTTON:
            pass
        elif self.element_type == ELEMENT_TYPE.RADIO_BUTTON_GROUP:
            self._answer_question_radiobutton_group(value, question_element)
        elif self.element_type == ELEMENT_TYPE.CHECK_BUTTON:
            pass
        elif self.element_type == ELEMENT_TYPE.CHECK_BUTTON_GROUP:
            self._answer_question_checkbox_group(value, question_element)


class Selenium:
    """Use Selenium to traverse the form."""
    driver = None

    def __init__(self):
        if Selenium.driver is None:
            # self.driver = selenium.webdriver.Firefox()
            self.driver = selenium.webdriver.Chrome()

    def is_open(self) -> bool:
        """Checks whether driver window is open."""
        # https://www.codegrepper.com/code-examples/python/selenium+check+if+driver+is+open+python
        return bool(self.driver.session_id)

    def main_instructions(self, submit=True, continue_it=True, mold_odor=False, close=False, option=1):
        """Instruction set to carry out to fill out form."""
        if option == 1:
            # Load webpage with form
            self.driver.get(website_url)
            # assert 'mold' in self.driver.title.lower()
            # Enter Date:
            date_input = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/input[1]')
            # date_input.send_keys(today_date())
            date_input.send_keys(Inputs.date)
            # Enter Observer name:
            observer_input = self.driver.find_element(By.CSS_SELECTOR, ".office-form-question-textbox.office-form-textfield-input.form-control.office-form-theme-focus-border.border-no-radius")
            observer_input.send_keys(observer_name)
            # Select Faculty/Office/Unit
            self.driver.find_element(By.ID, "SelectId_0_placeholder").click()
            self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Faculty of Engineering"]').click()
            # Select Building
            self.driver.find_elements(By.CLASS_NAME, "select-placeholder-text")[-1].click()
            building_text = BUILDINGS[Inputs.building_id]
            self.driver.find_element(By.CSS_SELECTOR, '[aria-label="{}"]'.format(building_text)).click()
            # Select Floor
            self.driver.find_element(By.ID, "SelectId_2_placeholder").click()
            floor_text = FLOORS[Inputs.floor_id]
            self.driver.find_element(By.CSS_SELECTOR, '[aria-label="{}"]'.format(floor_text)).click()
            # Room / Area Identification
            room_input = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[7]/div/div[2]/div/div/input')
            room_input.send_keys(Inputs.room_name)
            # Room/Area Type
            self.driver.find_element(By.ID, "SelectId_3_placeholder").click()
            rm_typ_id = Inputs.room_type_id + 1
            self.driver.find_element(By.XPATH, '//*[@id="SelectId_3"]/div[2]/div[{}]'.format(rm_typ_id)).click()
            # Mold Odor
            self.driver.find_element(By.ID, "SelectId_4_placeholder").click()
            self.driver.find_element(By.CSS_SELECTOR, '[aria-label="None"]').click()
            # Select all N/A
            # Damage or Stains
            for i in range(2,2+8):
                self.driver.find_element(By.XPATH, '    /div/div/div[1]/div/div[1]/div[2]/div[2]/div[10]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
            # Visible Mold
            for i in range(2,2+8):
                self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[12]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
            # Wet or Damp
            for i in range(2,2+8):
                self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[14]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
            # Within 3 feet of exterior wall?: 'No [whatever]' by default
            # Damage or Stains
            self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[11]/div/div[2]/div/div[11]/div/label/input').click()
            # Visible Mold
            self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[13]/div/div[2]/div/div[11]/div/label/input').click()
            # Wet or Damp
            self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[15]/div/div[2]/div/div[11]/div/label/input').click()
            if mold_odor:
                # Select potency of mold odor
                # Open options
                self.driver.find_element(By.ID, "SelectId_4_placeholder").click()
                # Select option
                str1 = '[aria-label="{}"]'.format("Strong")
                self.driver.find_element(By.CSS_SELECTOR, str1).click()
            # Press submit button
            self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button/div').click()
            
            # Now, put in mold odor info
            # PAGE 2
            # Select all N/A by default, Select last input 'N/A' 7 times
            for _ in range(7):
                n_a = self.driver.find_elements_by_css_selector("input[value='N/A']")[-1].click()
                # n_a = self.driver.find_elements_by_xpath("//input[@value='N/A']")[-1].click()
            # Individual options
            # Ceiling
            # self.driver.find_element_by_xpath
            # Walls
            # Floor
            # Windows
            # Furnishings
            # HVAC System
            # Supplies and Materials
            # Supplies and Materials Description?
            # Additional Comments?

            # Press submit button
            submit_button = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button[2]/div')
            if submit:
                submit_button.click()
            # Next Page
                # Submit another form
                submit_link = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[2]/div[2]/div[2]/a')
                if continue_it:
                    submit_link.click()
            if close:
                # The End
                self.driver.quit()
                print("that's the end of the main instruction set.")
        
        elif option == 2:
            pass