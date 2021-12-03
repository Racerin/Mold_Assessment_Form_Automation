import datetime
import logging
from os import remove, environ
import time
import dataclasses
import enum
import csv
import string
import json
import re
import pydoc
import typing
from collections.abc import Sequence, Mapping, Container
from numbers import Number
from functools import partial

import openpyxl
from pynput import keyboard
from pynput.keyboard import Key
from Levenshtein import jaro
from Levenshtein import ratio as l_ratio

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

def switch_date_format(date:str) -> str:
    """ Switch around the day ad month in date. """
    # Match the regex groups for day and month 
    match = re.match(RE_DATE_SWITCH, date)
    if match:
        # Construct new string with switched around values
        ans = "{xx}/{ww}/{yyyy}".format(**match.groupdict())
        return ans
    else:
        raise ValueError("Cannot match date format to 'date' string.")

def load_tsv_file(filename, ignore_header_regex:str=None) -> list:
    """Extract row information from a tsv file.
    ignore_header_regex : A regular expression string to ignore the 1st header
    string if it matches.
    """
    ans_list = list()
    with open(filename, mode="r") as fd:
        rd = csv.reader(fd, delimiter='\t')
        for i, row in enumerate(rd):
            if i==0 and ignore_header_regex is not None:
                # Ignore the first row if its 1st element matches regular expression
                first_header = row[0]
                if re.search(ignore_header_regex, first_header):
                    continue
            ans_list.append(row)
    return ans_list

def save_tsv_file(filename, rows:Sequence):
    """Save rows of a sequence as rows in a tsv file.
    ans_row_strs : Sequence of strings that need be be joined to create last str.
    ans_str : string to save into tsv file.
    """
    with open(filename, mode='w+') as fd:
        ans_row_strs = list()
        for row in rows:
            # Convert each row to a str.
            if isinstance(row, Sequence):
                # Row data is separated by tabs.
                row_str = '\t'.join(row)
            else:
                row_str = str(row)
            ans_row_strs.append(row_str)
        ans_str = '\n'.join(ans_row_strs)
        fd.write(ans_str)

def load_excel_file(filename, ignore_header_regex:str=None) -> list:
    """ Reminiscent of 'load_tsv_file'. """
    # Open the excel file
    excel = openpyxl.load_workbook(filename)
    # Open the active/first sheet
    sheet = excel.active
    # Get rows
    rows = sheet.rows
    # Place each cell of row into a list, and place lists into a bigger list
    ans = list()
    for i, row in enumerate(rows):
        row_list = list()
        # Skip header row
        if i==0 and isinstance(ignore_header_regex, str):
            first_cell = row[0]
            matched_header = re.search(ignore_header_regex, first_cell.value)
            if matched_header: continue
        for cell in row:
            row_list.append(cell.value)
        ans.append(row_list)
    return ans

def match_strings(str1:str, str2:str) -> float:
    """Return the match ratio between strings based on string length.
    """
    ans = l_ratio(str1, str2)
    return ans

def str_to_key(str1:str) -> str:
    """Convert a string to a string usable as a key"""
    # Remove any trailing white space
    str1 = str1.strip()

    # Add underscore if 1st character is a number
    if str1[0].isdigit():
        str1 = '_' + str1
    
    # Replace any non-letters with '_'
    _strings = [t if t in string.ascii_letters + string.digits else '_' for t in str1]
    ans = "".join(_strings)
    return ans


def get_keys_and_values_strs_dict(dict1:dict) -> dict:
    """Creates dictionary of dictionary 
    where the values and keys are keys of type 'str' to its mapped value.
    """
    ans = dict()
    # Add keys and values
    for k,v in dict1.items():
        ans.update(
                {
                str_to_key(str(k)) : v,
                str_to_key(str(v)) : v,
                }
            )
    return ans

def best_match(container:Container, to_match:str) -> typing.Any:
    """Returns the value of container whose key best matches 'to_match'.
    Dict: The key with the highest score returns its mapped value.
        In essence, you could maybe set the default value by key of None
    List: The value with the highest score is returned.
    """
    best_score = 0
    if isinstance(container, Mapping):
        best_key = None
        for key in container:
            # Lavenshtein match the keys as a string
            score = match_strings(str(key), to_match)
            if score > best_score:
                best_key = key
                best_score = score
        try:
            best_value = container[best_key]
            return best_value
        except KeyError as err:
            raise KeyError(
                "There was no match for '{}' in the dictionary '{}'.".format(to_match, dict1)
                ) from err
    elif isinstance(container, Container):
        best_value = None
        for value in container:
            score = match_strings(str(value), to_match)
            if score > best_score:
                best_value = value
                best_score = score
        return best_value


## Global Configure

# Files
tsv_save_file = "completed.tsv"
excel_load_file = "file.xlsx"
excel_save_file = "completed.xlsx"

# Website url (NB. By default, a secret to remote repository)
website_url = environ.get('WEBSITE_URL', None)
if website_url is None:
    ValueError("You must assign a url for the form as an 'environment variable' [WEBSITE_URL]")


class Config():
    """ This class when instantiated;
    1. Loads information from 'config.json' file.
    # 2. Assigns the variables to it's class according to its name
    # 3. Assigns all other variables globally.
     """
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
        for _class in classes:

            # Get class dict
            class_name = _class.__name__
            if class_name in self.data:

            # Pop dict according to class from config's data
                dict1 = self.data.pop(class_name)

            # Assign variables of dict to class
                if isinstance(dict1, Mapping):
                    for k,v in dict1.items():
                        setattr(_class, k, v)
                else:
                    logging.error("You cannot assign a non-dictionary to the class {}.".format(class_name))

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
            intensity_option = best_match(MOLD_ODOR, intensity)
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

    class Parser:
        inputs = dict()

        def __get_best_section(self, section_input : str) -> OTHERS_SECTION:
            """Ge the best section from the user's input string."""
            section_matches = list()

            # Go through each section key[word] to get a matching score
            for section_keys_tup in OTHERS_SECTION.EVERYONE:
                for key in section_keys_tup:
                    score = match_strings(key, section_input)
                    tup = (score, section_keys_tup)
                    section_matches.append(tup)

            # Select the section_keys with the highest correlation (Last one when sorted)
            section_matches.sort()
            __score, section = section_matches[-1]
            return section

        def __get_intensity_for_DSVMWD_option(self, option_input) -> 'int|None':
            """Returns the number corresponding to the 
            size of the affected area (page 1).
            """
            # Return index for area size if it is in the user's option-input
            for sz_index in AFFECTED_AREA_SIZE_STR:
                if sz_index in option_input:
                    return int(sz_index)
            else:
                # Return default
                return 0

        def __get_inputs_value(self, section:OTHERS_SECTION, content_str:str, inputs_attribute:str) -> typing.Any:
            """Create values that are passable to Selenium to answer questions.
            NB: Contains unpredictable data flow inside
            """

            # Split-up content-input-string to get input-option-strings
            options_input = [option.strip() for option in content_str.split(',')]

            # Remove any empty strings
            options_input = [x for x in options_input if bool(x)]

            # Get respective standard dictionary
            params = OTHERS_SECTION_MAPPING[section]

            ## Match each option in content
            # Checkbox string matching
            if section in OTHERS_SECTION.CHECKBOX_WITH_OTHER:
                inputs_value = options_input

            # Check for DS, VM, WD
            elif section in OTHERS_SECTION.EXTERIOR_WALL:
                # Setup
                k_v_string_dict = get_keys_and_values_strs_dict(params)
                DSVMWD_values = dict()
                exteriors_values = list()
                
                # Parse through each 
                for option_input in options_input:
                    # Check with keys and values
                    best_option = best_match(k_v_string_dict, option_input)
                    area_size_index = self.__get_intensity_for_DSVMWD_option(option_input)
                    # Add values for 'Inputs'
                    DSVMWD_values.update({best_option:area_size_index})
                    # Check for exterior in input_option
                    if '+' in option_input:
                        exteriors_values.append(best_option)

                #Now, Assign values for inputs
                inputs_value = DSVMWD_values
                if exteriors_values:
                    """BAD data flow BUT, soo much easier. 
                    This will be taken out of inputs_value in 
                    '__get_inputs_exterior_wall_filter'
                    """
                    inputs_value.update({'exterior':exteriors_values})
            elif section in OTHERS_SECTION.RADIO_BUTTON_OPTIONS:
                # Get all options as keys to match with value
                k_v_string_dict = get_keys_and_values_strs_dict(params)
                # Get best matching value of param
                best_option = best_match(k_v_string_dict, content_str)
                # inputs_value
                inputs_value = best_option
            elif section in OTHERS_SECTION.TEXTINPUTS:
                assert isinstance(content_str, str), content_str
                inputs_value = content_str
            return inputs_value

        
        def __assign_inputs_exterior_wall_filter(self, inputs_value:dict, inputs_attribute:str, obj_class) -> dict:
            """ Extracts exterior value from dict and assigns it to class. """
            if isinstance(inputs_value, Mapping):
                exteriors = inputs_value.pop('exterior', None)
                if isinstance(exteriors, Sequence):
                    # Add '_exterior' to 'inputs_attribute' to create the exterior 'Inputs' attribute
                    new_inputs_attribute = STR_INPUTS_EXTERIOR.format(inputs_attribute)  #eg. damage_or_stain_exterior
                    # Now, Assign the value to class
                    setattr(obj_class, new_inputs_attribute, exteriors)

        def parse_others_cell(self, others_cell:str):
            """Factory method for parsing a string of 'Others'.
            """
            # Get the section:content of the input string
            m = re.match(RE_SECTION_CONTENT_GROUPDICT, others_cell)
            if m:
                dict_section_content = m.groupdict()
                section_str_input, content_str_input = dict_section_content['section'].strip(), dict_section_content['content'].strip()

                # Determine 'section' selected in cell
                section = self.__get_best_section(section_str_input)

                # Get in str form 'inputs_attribute' for attribute in 'Inputs' to use as a key.
                inputs_attribute = OTHERS_SECTION_INPUTS_MAPPING[section]

                # Get value for 'inputs_attribute'
                inputs_value = self.__get_inputs_value(section, content_str_input, inputs_attribute)

                # Add new key:values, attribute:values for defined inputs
                self.inputs.update({inputs_attribute:inputs_value})
            else:
                raise ValueError("The 'others_cell' value is not valid.")

        def assign_to_inputs_cls(self, input_cls, to_global=True):
            """Assign to 'Inputs' class if already an attribute else globally.
            Also deals with assigning DS,VM,WD exterior values.
            """
            for inputs_attribute, inputs_value in self.inputs.items():
                if inputs_attribute in OTHERS_SECTION_INPUTS_MAPPING.values():
                    # Filter function for DS,VM,WD exterior walls
                    self.__assign_inputs_exterior_wall_filter(inputs_value, inputs_attribute, input_cls)
                    # Just assign
                    setattr(input_cls, inputs_attribute, inputs_value)

                # If not in 'Inputs', assign 'inputs_value' to global variables
                elif to_global:
                    setattr(globals(), inputs_attribute, inputs_value)

                else:
                    raise AttributeError("Attribute '{}' cannot be found in '{}'.".format(input_name, input_cls))

    observer_name : str = "John Doe"
    date : str = today_date()

    room_name : str = ""
    floor_id : int = None
    room_type_id : int = None
    building_id : int = None

    others_arguments = list()
    parser_for_other_arguments = list()

    # mold_odor_id = None
    mold_odor_id = 'None'
    mold_odor_desc : str = ""

    damage_or_stains = ANS_RADIOGROUPS_DEFAULT
    damage_or_stains_exterior = ANS_CHECKBOXES_DEFAULT
    visible_mold = ANS_RADIOGROUPS_DEFAULT
    visible_mold_exterior = ANS_CHECKBOXES_DEFAULT
    wet_or_damp = ANS_RADIOGROUPS_DEFAULT
    wet_or_damp_exterior = ANS_CHECKBOXES_DEFAULT

    ceiling_materials = ANS_RADIOGROUP_DEFAULT
    wall_materials = ANS_RADIOGROUP_DEFAULT
    floor_materials = ANS_RADIOGROUP_DEFAULT
    windows_materials = ANS_RADIOGROUP_DEFAULT
    furnishing_materials = ANS_RADIOGROUP_DEFAULT
    hvac_materials = ANS_RADIOGROUP_DEFAULT
    supplies_and_materials = ANS_CHECKBOX2_DEFAULT
    supplies_and_materials_desc = ANS_CHECKBOX_OTHER_DEFAULT
    additional_comments : str = ""

    user_rows_inputs = list()
    current_row_inputs = list()
    completed_row_inputs = list()

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
    def load_user_inputs(cls, extend=False, filename=excel_load_file) -> list:
        """Load user input data into memory.
        Have the option to extend previous values with new values.
        """
        ans_list = load_excel_file(filename, ignore_header_regex='Room ')
        if extend:
            cls.user_rows_inputs.extend(ans_list)
        else:
            cls.user_rows_inputs = ans_list

    @classmethod
    def save_completed(cls):
        """Saves completed rows into a file"""
        save_tsv_file(tsv_save_file, cls.completed_row_inputs)

    @classmethod
    def load_completed(cls):
        """Loads row files into memory"""
        cls.completed_row_inputs = load_excel_file(excel_save_file)

    @classmethod
    def set_default_values(cls, include:Container=[], exclude:Container=[]):
        """ Set the default values for this class 'Inputs'.
        Attributes; observer_name, date,
        user_rows_inputs, current_row_inputs, completed_row_inputs,
        are automatically excluded.

        Attributes not defined in the class construct are also excluded.

        N.B to myself: If 'Inputs' was setup to use instances of it, you wouldn't have to use this method.
        Also, REMEMBER TODO to update this method whenever the default value of the class changes.
        """
        
        # Set the defaults on the following attributes
        cls.room_name = ""
        cls.floor_id = None
        cls.room_type_id = None
        cls.building_id = None

        cls.others_arguments = list()
        cls.parser_for_other_arguments = list()

        cls.mold_odor_id = 'None'
        cls.mold_odor_desc = ""

        cls.damage_or_stains = ANS_RADIOGROUPS_DEFAULT
        cls.damage_or_stains_exterior = ANS_CHECKBOXES_DEFAULT
        cls.visible_mold = ANS_RADIOGROUPS_DEFAULT
        cls.visible_mold_exterior = ANS_CHECKBOXES_DEFAULT
        cls.wet_or_damp = ANS_RADIOGROUPS_DEFAULT
        cls.wet_or_damp_exterior = ANS_CHECKBOXES_DEFAULT

        cls.ceiling_materials = ANS_RADIOGROUP_DEFAULT
        cls.wall_materials = ANS_RADIOGROUP_DEFAULT
        cls.floor_materials = ANS_RADIOGROUP_DEFAULT
        cls.windows_materials = ANS_RADIOGROUP_DEFAULT
        cls.furnishing_materials = ANS_RADIOGROUP_DEFAULT
        cls.hvac_materials = ANS_RADIOGROUP_DEFAULT
        cls.supplies_and_materials = ANS_CHECKBOX2_DEFAULT
        cls.supplies_and_materials_desc = ANS_CHECKBOX_OTHER_DEFAULT
        cls.additional_comments = ""


    @classmethod
    def __floor_roomtype_building(cls, floor, roomtype, building):
        """ Returning the official string for each property. """

        # Get 'Inputs' attributes
        floor_id = best_match(get_keys_and_values_strs_dict(FLOORS), floor)
        room_type_id = best_match(get_keys_and_values_strs_dict(ROOM_TYPES), roomtype)
        building_id = best_match(get_keys_and_values_strs_dict(BUILDINGS), building)

        # Return structured answer
        return floor_id, room_type_id, building_id

    @classmethod
    def set_user_input(cls, row=current_row_inputs, **kwargs):
        """Assign arguments to/in Inputs"""

        # Assign row variables
        cls.room_name, floor, room_type, building, *cls.others_arguments = row
        cls.floor_id, cls.room_type_id, cls.building_id = cls.__floor_roomtype_building(floor, room_type, building)

        # Assign mapped variables
        cls_dir = dir(cls)
        for k,v in kwargs.items():
            if k in cls_dir:
                setattr(cls, k, v)

        # Create object parsers of other_arguments
        cls.parse_other_arguments()

    @classmethod
    def parse_other_arguments(cls):
        """Use factory method to parse arguments. Assign values to class immediately.
        Use the 'Inputs.Parser' class to parse through the other arguments.
        """
        # Filter None values
        cls.others_arguments = [x for x in cls.others_arguments if bool(x)]

        # Now, parse the arguments
        for arg_str in cls.others_arguments:
            parser = cls().Parser()
            parser.inputs.clear()
            parser.parse_others_cell(arg_str)
            parser.assign_to_inputs_cls(cls, to_global=False)

    @classmethod
    def load_user_input(cls, index=0, task_completed:bool=True):
        """Loads one row of user inputs into memory.
        Keeps account of inputs for forms filled-out.
        task_completed: States whether the current_row_inputs were used to complete a form.
        """
        # Set defaults
        cls.set_default_values(include=[])

        # Move current user inputs over to completed
        if cls.current_row_inputs and task_completed:
            cls.completed_row_inputs.append(cls.current_row_inputs)

        # Get next current_row_inputs
        cls.current_row_inputs = cls.user_rows_inputs.pop(index)
        assert len(cls.current_row_inputs) > 4, cls.current_row_inputs
        
        # Set and parse user inputs if not in 'completeed_row_inputs'
        if cls.current_row_inputs not in cls.completed_row_inputs:
            cls.set_user_input(row=cls.current_row_inputs)


class Xpath:
    @classmethod
    def xpath_index(cls, xpath:str, index:int=None, xpath_indexQ=True, encapsulate=False) -> str:
        """Returns an xpath of index of nodes"""

        # Convert 'index' from programming/Python index to xpath index
        if xpath_indexQ: index += 1
        if index is None:
            if encapsulate:
                str1 = "({})[]".format(xpath)
            else:
                str1 = "{}[]".format(xpath)
        else:
            if encapsulate:
                str1 = "({})[{}]".format(xpath, index)
            else:
                str1 = "{}[{}]".format(xpath, index)
        return str1

    @classmethod
    def ancestor(cls, xpath_current:str, xpath_ascending_to:str, remove_trailings=True) -> str:
        """Formulate and return xpath of self node and ancestor xpath"""
        # Remove '//' at the start of the extending xpath
        if remove_trailings:
            xpath_ascending_to = re.sub(RE_TRAILING_DASH, '', xpath_ascending_to)
        str1 = "{}/ancestor::{}".format(xpath_current, xpath_ascending_to)
        return str1

    @classmethod
    def descendant(cls, xpath_current:str, xpath_descending_to:str, remove_trailings=True) -> str:
        """Formulate and return xpath of self node and descendant xpath"""
        # Remove '//' at the start of the extending xpath
        if remove_trailings:
            xpath_descending_to = re.sub(RE_TRAILING_DASH, '', xpath_descending_to)
        str1 = "{}/descendant::{}".format(xpath_current, xpath_descending_to)
        return str1

    @classmethod
    def get_xpath_format_to_input_type(self, mappings:dict, key:typing.Any) -> str:
        """Returns appropriate xpath based on type of input.
        NB: Python may turns key 'typ' into a string (dict constructor). 
        Key is reverted to type with pydoc if needed.
        """
        for typ_str, xpath_to_format in mappings.items():
            # Ensure 'type' is a type(i.e. str, int, float, etc.) and not a str itself
            typ = pydoc.locate(typ_str) if isinstance(typ_str, str) else typ_str
            if isinstance(key, typ):
                xpath = xpath_to_format.format(key)
                return xpath
        else:
            # Raise error
            types = tuple(mappings.keys())
            types_str = ', '.join(types)
            raise AttributeError("Key not of proper format({}).".format(types_str))


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

    def answer_question(self, value:'Container|str'):
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


class Counter:
    _count = 0
    count_dict = dict()
    test_functions = []

    def get_count(self): 
        print("This is count '{}'.".format(self._count))
        return self._count
    def set_count(self, val):
        print("This is count '{}'.".format(val))
        if isinstance(val, int):
            self._count = val
        else: raise ValueError("Count must be of type 'int'.")
    count = property(get_count, set_count,)

    def __init__(self, count=count):
        self.count = count

    def add_key(self, key, number=1):
        """ Adds a key and the number it adds by. """
        if isinstance(number, int):
            self.count_dict.update({key:number})

    def add(self, toAdd=1) -> int:
        self.count += toAdd
        return self.count

    def then_add(self, toAdd=1) -> int:
        to_return = self.count
        self.count += toAdd
        return to_return

    def inside(self, key) -> int:
        """ If the key is in the dict 'count_dict',
        add 1 to count.
        """
        to_add = self.count_dict.get(key, 0)
        return self.add(to_add)


class Selenium:
    """Use Selenium to traverse the form."""
    driver = None

    def create_driver(self, force=False):
        if Selenium.driver is None or force:
            self.driver = selenium.webdriver.Chrome()
            self.driver.maximize_window()

    def __init__(self):
        self.create_driver()

    def find_element(self, xpath:str) -> 'selenium.webdriver.remote.webelement.WebElement':
        """Shortcut for finding xpath element."""
        return self.driver.find_element(By.XPATH, xpath)

    def find_elements(self, xpath:str) -> 'list[selenium.webdriver.remote.webelement.WebElement]':
        """Shortcut for finding xpath elements."""
        return self.driver.find_elements(By.XPATH, xpath)

    @classmethod
    def get_question_xpath(cls, question_key:'int|str'):
        """Returns xpath for question."""
        mappings = dict(int=XPATH_QUESTION_BY_NUMBER, str=XPATH_QUESTION_BY_LABEL,)
        # Get the final xpath
        xpath_question = Xpath.get_xpath_format_to_input_type(mappings=mappings, key=question_key)
        return xpath_question

    @classmethod
    def get_dropdown_option_xpath(cls, option_key:'int|str'):
        """Returns xpath for dropdown options."""
        mappings = dict(int=XPATH_DROPDOWN_OPTION_INDEX, str=XPATH_DROPDOWN_OPTION_TEXT)
        # Get the final xpath
        xpath_dropdown_option = Xpath.get_xpath_format_to_input_type(mappings=mappings, key=option_key)
        return xpath_dropdown_option

    def answer_text_element(self, question_key:'int|str', input_answer:str, clear:bool=True):
        """Answer a text input question.
        question_key : Matches a question according to XPATH and respective key of question 
        (non-zero index or string match?.)
        """

        # Get xpath representation of html element
        xpath_question = self.get_question_xpath(question_key)
        xpath_input = Xpath.descendant(xpath_question, XPATH_INPUT)
        element_input = self.find_element(xpath_input)

        # Write to textinput element
        if clear:
            element_input.clear()
        element_input.send_keys(input_answer)


    def answer_textarea_element(self, question_key:'int|str', input_answer:str, clear:bool=True):
        """Answer a textarea question."""
        xpath_question = self.get_question_xpath(question_key)
        xpath_input = Xpath.descendant(xpath_question, XPATH_TEXTAREA)
        element_input = self.find_element(xpath_input)
        if clear:
            element_input.clear()
        element_input.send_keys(input_answer)

    def answer_dropdown_element(self, question_key:'int|str', option_answer:'int|str'):
        """Answer a dropdown menu question."""
        # Get/open dropdown menu
        xpath_question = self.get_question_xpath(question_key)
        xpath_dropdown = Xpath.descendant(xpath_question, XPATH_DROPDOWN)
        dropdown_element = self.find_element(xpath_dropdown)
        dropdown_element.click()
        # TODO: ensure dropdown menu is open
        # Select dropdown option
        xpath_dropdown_option = self.get_dropdown_option_xpath(option_answer)
        dropdown_option_element = self.find_element(xpath_dropdown_option)
        dropdown_option_element.click()

    def answer_radiogroups_element(self, question_key:'int|str', container_of_answers:'Sequence|Mapping', default=None):
        """Answer a group of radiogroups question.

        'pairs_container_answers' : A Sequence containing a pair of side_header and top_header values
        """
        xpath_question = self.get_question_xpath(question_key)
        xpath_radiogroup = Xpath.descendant(xpath_question, XPATH_RADIOGROUP)

        # Get top header string values
        xpath_header = Xpath.descendant(xpath_question, XPATH_RADIOGROUP_HEADER)
        xpath_header_span = Xpath.descendant(xpath_header, XPATH_SPAN)
        header_spans = self.find_elements(xpath_header_span)
        assert len(header_spans) > 0, xpath_header_span
        header_strs = [ele.text for ele in header_spans]

        # Get Side-Header string values
        xpath_radiogroup = Xpath.descendant(xpath_question, XPATH_RADIOGROUP)
        xpath_side_header = Xpath.descendant(xpath_radiogroup, XPATH_RADIOGROUP_BY_SIDE_HEADER)
        xpath_side_header_span = Xpath.descendant(xpath_side_header, XPATH_SPAN)
        side_headers_spans = self.find_elements(xpath_side_header_span)
        assert len(side_headers_spans) > 0, xpath_side_header_span
        side_header_strs = [ele.text for ele in side_headers_spans]

        pairs_container_answers = list()

        # Convert 'container_of_answers' to a sequence of answers if it is type 'Mapping'.
        if isinstance(container_of_answers, Mapping):
            used_side_headers = list()
            for key,val in container_of_answers.items():
                # Create the pairs of radiogroup's index and its answer
                if isinstance(key, int):
                    index = key
                elif isinstance(key, str):
                    index = best_match(side_header_strs, key)
                pairs_container_answers.append((index, val))
                used_side_headers.append(index)
            
            # Set 'default' for the rest of side headers
            if isinstance(default, str):
                default_val = best_match(header_strs, default)
                for index in side_header_strs:
                    if index not in used_side_headers:
                        used_side_headers.append(index)   #Dont need to do this but closure
                        pairs_container_answers.append((index, default_val,))

        # TODO: Needs to be updated like Mapping
        elif isinstance(container_of_answers, Sequence):
            raise SyntaxError("You need to fix this code 1st.")
            pairs_container_answers = enumerate(container_of_answers)

        # Now, Iterate through the radiogroups and their answers
        for radiogroup_index, option_response in pairs_container_answers:
            """ 'option_response' is either a str or an int.
            int: an answer corresponding to the header value
            str: an answer (may be imperfect) that suppose to match radio button value
            """
            if isinstance(option_response, int):
                # Choose header answer by index
                header_answer_index = option_response
            elif isinstance(option_response, str):
                # Choose header's answer's index by string matching
                answersQ = [header_str for header_str in header_strs if option_response in header_str]
                # answersQ = [side_header_str for side_header_str in side_header_strs if option_response in side_header_str]
                answersQ.sort()
                assert len(answersQ) > 0, (header_strs, option_response)
                answer = answersQ[0]
                header_answer_index = header_strs.index(answer)

            # Get index as an int?
            if isinstance(radiogroup_index, str):
                radiogroup_index = side_header_strs.index(radiogroup_index)

            # Select the correct radiobutton of the radiogroup
            xpath_radiogroup_index = Xpath.xpath_index(xpath_radiogroup, radiogroup_index)
            xpath_radiogroup_index_radiobutton = Xpath.descendant(xpath_radiogroup_index, XPATH_RADIOBUTTON)
            radiobuttons = self.find_elements(xpath_radiogroup_index_radiobutton)

            # Select the radio button with the answer according to index
            answer_radiobutton = radiobuttons[header_answer_index]
            answer_radiobutton.click()

    def answer_checkboxgroup_element(self, question_key:'int|str', container_of_answers:'Sequence|Mapping', default=None):
        """Answer a group of checkboxes.
        Reminiscent of 'answer_radiogroups_element'.
        """
        
        # Get checkbox labels
        xpath_question = self.get_question_xpath(question_key)
        xpath_checkbox_input = Xpath.descendant(xpath_question, XPATH_CHECKBOX)
        checkboxes = self.find_elements(xpath_checkbox_input)
        checkbox_label_strs = [checkbox.get_attribute('value') for checkbox in checkboxes]
        assert len(checkbox_label_strs) > 0, (xpath_checkbox_input,)

        # Pick default[s] if no answers are given
        if not container_of_answers:
            if isinstance(default, str):
                container_of_answers = [default,]
            elif isinstance(default, Container) and all((isinstance(x, str) for x in default)):
                container_of_answers = default
        
        # Convert 'container_of_answers' to a sequence of pairs of ...
        checkbox_answer_pairs = list()
        if isinstance(container_of_answers, Mapping):
            for label_str, answer in container_of_answers.items():
                # Get index of checkbox by string matching
                best_checkbox_label = best_match(checkbox_label_strs, label_str)
                checkbox_index = checkbox_label_strs.index(best_checkbox_label)
                """Turn the answer to a bool, EXCEPT if it's 'None'. 
                'None' is used to ignore checkbox."""
                bool_answer = bool(answer) if answer is not None else None
                # Add to paired sequence
                tup = checkbox_index, bool_answer
                checkbox_answer_pairs.append(tup)
        elif isinstance(container_of_answers, Sequence):
            for answer in container_of_answers:
                if isinstance(answer, int):
                    # Return index of checkbox with answer True
                    tup = answer, True
                    checkbox_answer_pairs.append(tup)
                elif isinstance(answer, str):
                    # Convert the label to index then do as above
                    # Each ele of sequence is a label string. Therefore label will correspond to True
                    best_checkbox_label = best_match(checkbox_label_strs, answer)
                    checkbox_index = checkbox_label_strs.index(best_checkbox_label) + 1
                    """Turn the answer to a bool, EXCEPT if it's 'None'. 
                    'None' is used to ignore checkbox."""
                    bool_answer = bool(answer) if answer is not None else None
                    # Add to paired sequence
                    tup = (checkbox_index, bool_answer, )
                    checkbox_answer_pairs.append(tup)
        
        # Set checkbox according
        for checkbox_index, bool_answer in checkbox_answer_pairs:
            # Ignore checkbox is an option
            if bool_answer is None:
                continue
            else:
                checkbox = checkboxes[checkbox_index - 1]
                # Make sure checkbox is active if answer is True
                if checkbox.is_selected() and bool_answer:
                    # Leave as is, checkbox is already activated
                    pass
                elif checkbox.is_selected() and not bool_answer:
                    # Deactivate checkbox
                    checkbox.click()
                elif not checkbox.is_selected() and bool_answer:
                    # Activate checkbox
                    checkbox.click()
                elif not checkbox.is_selected() and not bool_answer:
                    # Leave as is, checkbox is already deactivated
                    pass

    def ans_radiogroup_element(self, question_key:'int|str', answer:str):
        """Answer a group of radiobuttons.
        NOT to be confused with 'answer_radiogroups_element' (shorten and w/o an 's').
        Reminiscent of 'answer_checkboxgroup_element'.
        """

        # Get radiobutton labels as strings
        xpath_question = self.get_question_xpath(question_key)
        xpath_radiogroup = Xpath.descendant(xpath_question, XPATH_RADIOGROUP)
        xpath_radio_input = Xpath.descendant(xpath_radiogroup, XPATH_INPUT)
        input_radiobutton_elements = self.find_elements(xpath_radio_input)
        assert len(input_radiobutton_elements) > 0, xpath_radio_input
        radiobutton_label_strs = [ele.get_attribute("value") for ele in input_radiobutton_elements]

        # Now, match strings and choose best match as radiobutton
        best_match_str = best_match(radiobutton_label_strs, answer)
        best_match_index = radiobutton_label_strs.index(best_match_str)
        radiobutton = input_radiobutton_elements[best_match_index]
        radiobutton.click()

    def answer_checkboxgroup_other_element(self, question_key:'int|str', answers:Sequence, clear:bool=True):
        """Answer a group of checkboxes with an optional 'other'.
        Select checkboxes and fill-out 'other' based on type and content of answer of 'answers'.
        """
        # Setup variables
        others = []
        answers_indices = list()
        # Get basic xpath strings
        xpath_question = self.get_question_xpath(question_key)
        xpath_checkbox_input = Xpath.descendant(xpath_question, XPATH_CHECKBOX)
        xpath_other_input = Xpath.descendant(xpath_question, XPATH_INPUT_PLACEHOLDER_INPUT.format("Other"))
        checkbox_elements = self.find_elements(xpath_checkbox_input)
        label_strs = [ele.get_attribute('value') for ele in checkbox_elements]
        for ans in answers:
            if isinstance(ans, int):
                # Select checkbox of appropriate index
                pass
            elif isinstance(ans, str):
                # Select checkbox if 'ans' matches label, else put it for others
                best_matches = [lbl_str for lbl_str in label_strs if ans.lower() in lbl_str.lower()]
                n_best_matches = len(best_matches)
                if n_best_matches > 0:
                    # Set the checkbox as active
                    best_matches.sort() # Choose the smallest that matched
                    best_match = best_matches[0]
                    best_match_index = label_strs.index(best_match)
                    answers_indices.append(best_match_index)
                    # If checkbox already selected, add answer to 'other' list
                    checkbox = checkbox_elements[best_match_index]
                    if checkbox.is_selected():
                        others.append(ans)
                else:
                    # Just add to others
                    others.append(ans)
        # Now, Activate checkbox that have answers
        for index in answers_indices:
            checkbox = checkbox_elements[index]
            if checkbox.is_selected():
                pass
            else:
                checkbox.click()
        # Now, Input string to 'other' element textinput
        other_element = self.find_element(xpath_other_input)
        other_str = ','.join(others)
        if clear:
            other_element.clear()
        other_element.send_keys(other_str)

    def answer_date(self, question_key:'int|str', input_answer:str, clear:bool=True):
        """Answer a text input question for date.
        Must explicitely state key for question in the arguments.
        """
        # Get xpath representation of html element
        xpath_question = self.get_question_xpath(question_key)
        xpath_input = Xpath.descendant(xpath_question, XPATH_INPUT)
        element_input = self.find_element(xpath_input)

        # Get placeholder from html element to know which date format to use (M/d/yyyy or dd/MM/yyyy)
        placeholder_text = element_input.get_attribute('placeholder')
        if re.match(RE_DATE_PLACEHOLDER_WORLD_SHORT, placeholder_text):
            # Switch the day and month
            input_answer = switch_date_format(input_answer)
        # Assume date is already in USA format
        elif re.match(RE_DATE_PLACEHOLDER_USA_SHORT, placeholder_text): pass
        # Go with default
        else: pass

        # Write to textinput element
        if clear:
            element_input.clear()
        element_input.send_keys(input_answer)

    def is_open(self) -> bool:
        """Checks whether driver window is open."""
        # https://www.codegrepper.com/code-examples/python/selenium+check+if+driver+is+open+python
        return bool(self.driver.session_id)

    def get_element_question(self, key:'str|int'):
        """Get element question in webpage.
        NB: key|int is NOT zero-based. i.e. starts with 1
        """
        if isinstance(key, int):
            xpath = XPATH_QUESTION_BY_NUMBER.format(key)
        elif isinstance(key, str):
            xpath = XPATH_QUESTION_BY_LABEL.format(key)
        else:
            raise AttributeError("Key is not of the appriate type (str,int).")
        element_question = self.driver.find_element(By.XPATH, xpath)
        return element_question

    def main_instructions(self, submit=True, continue_it=True, mold_odor=False, close=False, yield_=False, option=2):
        """Instruction set to carry out to fill out form."""
        if option == 1:
            # Load webpage with form
            self.driver.get(website_url)
            # assert 'mold' in self.driver.title.lower()
            if yield_:
                yield YIELD.START
            # Enter Date:
            date_input = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/input[1]')
            # date_input.send_keys(today_date())
            date_input.send_keys(Inputs.date)
            # Enter Observer name:
            observer_input = self.driver.find_element(By.CSS_SELECTOR, ".office-form-question-textbox.office-form-textfield-input.form-control.office-form-theme-focus-border.border-no-radius")
            observer_input.send_keys(Inputs.observer_name)
            # Select Faculty/Office/Unit
            self.driver.find_element(By.ID, "SelectId_0_placeholder").click()
            self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Faculty of Engineering"]').click()
            if yield_:
                yield YIELD.FIRST_PAGE_UPDATE
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
            if yield_:
                yield YIELD.FIRST_CHECKBOX
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
            if yield_:
                yield YIELD.MOLD_ODOR
            if mold_odor:
                # Select potency of mold odor
                # Open options
                self.driver.find_element(By.ID, "SelectId_4_placeholder").click()
                # Select option
                str1 = '[aria-label="{}"]'.format("Strong")
                self.driver.find_element(By.CSS_SELECTOR, str1).click()
            if yield_:
                yield YIELD.BEFORE_NEXT_PAGE
            # Press next button
            self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button/div').click()
            
            # PAGE 2
            # Now, put in mold odor info
            if yield_:
                yield YIELD.NEXT_PAGE
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

            if yield_:
                yield YIELD.SUBMIT
                yield YIELD.BEFORE_NEXT_PAGE
            # Press submit button
            submit_button = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button[2]/div')
            if submit:
                submit_button.click()
                # Next Page
                if yield_:
                    yield YIELD.NEXT_PAGE
                # Submit another form
                submit_link = self.driver.find_element(By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[2]/div[2]/div[2]/a')
                if continue_it:
                    submit_link.click()
            if close:
                # The End
                self.driver.quit()
                print("that's the end of the main instruction set.")
        
        elif option == 2:
            # Load webpage form
            self.driver.get(website_url)

            # Set the zoom of the webpage
            # self.driver.execute_script("document.body.style.zoom='80%'")
            if yield_:
                yield YIELD.START
                yield YIELD.PAGE_ONE
                time.sleep(1)

            # Enter Date
            self.answer_date(1, Inputs.date)

            # Enter Observer name
            self.answer_text_element(2, Inputs.observer_name)

            # Select Faculty/Office/Unit
            self.answer_dropdown_element(3, 7)
            if yield_:
                yield YIELD.FIRST_PAGE_UPDATE

            # Select Building
            self.answer_dropdown_element(4, Inputs.building_id)

            # Select Floor
            self.answer_dropdown_element(5, Inputs.floor_id)

            # Enter Room/Area Identification
            self.answer_text_element(6, Inputs.room_name)

            # Enter Room/Area Type
            self.answer_dropdown_element(7, Inputs.room_type_id)

            # Mold Odor, set as 'None' for now in order to progress to the next question
            self.answer_dropdown_element(8, 'None')

            # Select Damage or Stains (DS)
            self.answer_radiogroups_element(9, Inputs.damage_or_stains, "N/A")

            # Select DS within range of external walls
            self.answer_checkboxgroup_element(10, Inputs.damage_or_stains_exterior, default="No Damage or Stains")

            # Select Visible Mold (VM)
            self.answer_radiogroups_element(11, Inputs.visible_mold, "N/A")

            # Select VM within range of external walls
            self.answer_checkboxgroup_element(12, Inputs.visible_mold_exterior, default="No Visible Mold")

            # Select Wet or Damp(WD)
            self.answer_radiogroups_element(13, Inputs.wet_or_damp, "N/A")

            # Select WD within range of external walls
            self.answer_checkboxgroup_element(14, Inputs.wet_or_damp_exterior, default="No Wet or Damp")

            # NOW, answer Mold Odor Option
            # mold_odor = MOLD_ODOR[Inputs.mold_odor_id]
            mold_odor_dict = get_keys_and_values_strs_dict(MOLD_ODOR)
            mold_odor = best_match(mold_odor_dict, Inputs.mold_odor_id)
            self.answer_dropdown_element(8, mold_odor)

            # If any answer other than 'None' a new question with textarea pops-up right after
            if Inputs.mold_odor_id != MOLD_ODOR[0]:
                self.answer_textarea_element(9, Inputs.mold_odor_desc)

            # Click 'Next' Button
            next_button = self.find_element(XPATH_NEXT_BUTTON)
            if yield_:
                yield YIELD.BEFORE_NEXT_PAGE
            next_button.click()

            # NEXT PAGE
            if yield_:
                yield YIELD.NEXT_PAGE
                yield YIELD.PAGE_TWO

            # counter = Counter(1)
            # counter.add_key('N/A')
            count = 0

            # Ceiling materials affected
            # self.ans_radiogroup_element(counter.then_add(), Inputs.ceiling_materials)
            self.ans_radiogroup_element(count+1, Inputs.ceiling_materials)
            count += 0 if Inputs.ceiling_materials=='N/A' else 1
            # counter.inside(Inputs.ceiling_materials)

            # Wall materials affected
            self.ans_radiogroup_element(count+2, Inputs.wall_materials)
            count += 0 if Inputs.wall_materials=='N/A' else 1
            # counter.inside(Inputs.wall_materials)

            # Floor materials affected
            self.ans_radiogroup_element(count+3, Inputs.floor_materials)
            count += 0 if Inputs.floor_materials=='N/A' else 1
            # counter.inside(Inputs.floor_materials)

            # Windows type affected
            self.ans_radiogroup_element(count+4, Inputs.windows_materials)
            count += 0 if Inputs.windows_materials=='N/A' else 1
            # counter.inside(Inputs.windows_materials)

            # Furnishings affected
            self.ans_radiogroup_element(count+5, Inputs.furnishing_materials)
            count += 0 if Inputs.furnishing_materials=='N/A' else 1
            # counter.inside(Inputs.furnishing_materials)

            # HVAC System affected
            self.ans_radiogroup_element(count+6, Inputs.hvac_materials)
            count += 0 if Inputs.hvac_materials=='N/A' else 1
            # counter.inside(Inputs.hvac_materials)

            # Supplies and Materials affected
            self.answer_checkboxgroup_element(count+7, Inputs.supplies_and_materials)

            # Supplies and Materials Description (Checkbox options with other)
            self.answer_checkboxgroup_other_element(count+8, Inputs.supplies_and_materials_desc)

            # Additional comments
            self.answer_textarea_element(count+9, Inputs.additional_comments)
            submit_button = self.find_element(XPATH_SUBMIT_BUTTON)
            if yield_:
                yield YIELD.BEFORE_NEXT_PAGE
                yield YIELD.SUBMIT
                print("Not suppose to reach here.")
            submit_button.click()

            # NEXT PAGE
            if yield_:
                yield YIELD.NEXT_PAGE
                yield YIELD.PAGE_THREE
                
            # Do another form
                yield YIELD.BEFORE_NEXT_PAGE


@dataclasses.dataclass
class Runner:
    """Responsible for handling running of Selenium's 'main_instruction'
    and handling interludes/pauses.
    The yields are grouped. If the yield falls within a specific group, respond accordingly.
    """
    submit : bool = False
    
    # Yield Groups
    continue_it_yields : list = dataclasses.field(default_factory=list)
    sleep_yields : dict = dataclasses.field(default_factory=dict)
    return_yields = [YIELD.SUBMIT]
    keyboard_yields : dict = dataclasses.field(default_factory=dict)

    sleep_time : float = 1

    def __continue_it_callback(self, yield_type, *args, **kwargs):
        """ Callback for 'continue_it'. """
        return None

    def __sleep_callback(self, yield_type, *args, **kwargs):
        """ Callback for 'sleep'. """
        duration = self.sleep_yields.get(yield_type, self.sleep_time)
        if isinstance(duration, (int,float)):
            time.sleep(duration)
        else:
            time.sleep(self.sleep_time)

    def __return_callback(self, yield_type, *args, **kwargs):
        """ Callback for 'return'. """
        """Quit generator
        Check 'run' method for better understanding
        """
        return None

    def __keyboard_callback(self, yield_type, *args, **kwargs):
        """ Callback for 'keyboard'. """
        key = self.keyboard_yields[yield_type]
        return None

    def yield_handler(self, yield_type:YIELD):
        """Responsible for actions based on the pause type and configuration."""
        
        # Yield for continue_it
        if yield_type in self.continue_it_yields:
            return self.__continue_it_callback(yield_type)
            
        # Yield for sleep
        if yield_type in self.sleep_yields:
            return self.__sleep_callback(yield_type)
            
        # Yield for return
        if yield_type in self.return_yields:
            return self.__return_callback(yield_type)
            
        # Yield for keyboard
        if yield_type in self.keyboard_yields:
            return self.__keyboard_callback(yield_type)

    def main_instruction_args(self) -> dict:
        """Returns args to apss into 'main_instruction' of 'Selenium'."""
        kwargs = dict(yield_=True, submit=self.submit, )
        return kwargs
    
    def run(self, selenium:Selenium):
        """Run 'Selenium' object according to config.
        Return control to Runner at each yield point and execute yield according to settings.
        """
        # Create a new session ad hoc
        selenium.create_driver(force=True)

        # Now iterate through each yield while processessing operations between each yield
        for _yield in selenium.main_instructions(**self.main_instruction_args()):
            self.yield_handler(_yield)
            
            # Return pause
            if _yield in self.return_yields: break


config = Config()