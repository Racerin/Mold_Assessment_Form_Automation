import datetime
import time
import dataclasses
import enum
import csv
import json

from pynput import keyboard
from pynput.keyboard import Key

import selenium
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import PARAM


from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


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

    def load_config(self, filename=PARAM.config_file):
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


#Inputs
@dataclasses.dataclass
class Inputs:
    room_name : str = ""
    floor_id : int = None
    room_type_id : int = None
    building_id : int = None

    @classmethod
    def user_input_prompt(cls):
        """Prompt user for input data."""
        # observer_name = input(PARAM.observer_name_prompt)
        cls.room_name = input(PARAM.room_name_prompt)
        cls.floor_id = int(input(PARAM.floor_prompt))
        cls.room_type_id = int(input(PARAM.room_type_prompt))
        cls.building_id = int(input(PARAM.building_prompt))

    @classmethod
    def row_update(cls, row):
        """Assign tsv file row to class variables."""
        cls.room_name, cls.floor_id, cls.room_type_id, cls.building_id = row

    @classmethod
    def save_tsv(cls, container:'list|tuple', filename=tsv_save_file):
        """Save container to tsv file."""
        with open(filename, mode="w") as fd:
            rd = csv.writer(fd, delimiter='\t')
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
    def set_user_input(cls, row:'list[4]'):
        cls.room_name, cls.floor_id, cls.room_type_id, cls.building_id = row


class Selenium:
    """Use Selenium to traverse the form."""

    def __init__(self):
        # self.driver = selenium.webdriver.Firefox()
        self.driver = selenium.webdriver.Chrome()

    def is_open(self) -> bool:
        """Checks whether driver window is open."""
        # https://www.codegrepper.com/code-examples/python/selenium+check+if+driver+is+open+python
        return bool(self.driver.session_id)

    def hold_open(self):
        """Pause script while window is open."""
        while(self.is_open()):
            time.sleep(1)

    def click(self, xpath:str, *args) -> selenium.webdriver.remote.webelement.WebElement:
        """ NOT USED AS YET.
        Click on an element with xpath.
        args: optional arguments for text formatting
        """
        ele = self.driver.find_element_by_xpath(xpath.format(*args))
        ele.click()
        return ele

    def main_instructions(self, submit=True, continue_it=True, mold_odor=False, close=False):
        """Instruction set to carry out to fill out form."""
        # Load webpage with form
        self.driver.get(website_url)
        # assert 'mold' in self.driver.title.lower()
        # Enter Date:
        date_input = self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/input[1]')
        date_input.send_keys(today_date())
        # Enter Observer name:
        observer_input = self.driver.find_element_by_css_selector(".office-form-question-textbox.office-form-textfield-input.form-control.office-form-theme-focus-border.border-no-radius")
        observer_input.send_keys(observer_name)
        # Select Faculty/Office/Unit
        self.driver.find_element_by_id("SelectId_0_placeholder").click()
        self.driver.find_element_by_css_selector('[aria-label="Faculty of Engineering"]').click()
        # Select Building
        self.driver.find_elements_by_class_name("select-placeholder-text")[-1].click()
        building_text = PARAM.buildings[Inputs.building_id]
        self.driver.find_element_by_css_selector('[aria-label="{}"]'.format(building_text)).click()
        # Select Floor
        self.driver.find_element_by_id("SelectId_2_placeholder").click()
        floor_text = PARAM.floors[Inputs.floor_id]
        self.driver.find_element_by_css_selector('[aria-label="{}"]'.format(floor_text)).click()
        # Room / Area Identification
        room_input = self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[7]/div/div[2]/div/div/input')
        room_input.send_keys(Inputs.room_name)
        # Room/Area Type
        self.driver.find_element_by_id("SelectId_3_placeholder").click()
        rm_typ_id = Inputs.room_type_id + 1
        self.driver.find_element_by_xpath('//*[@id="SelectId_3"]/div[2]/div[{}]'.format(rm_typ_id)).click()
        # Mold Odor
        self.driver.find_element_by_id("SelectId_4_placeholder").click()
        self.driver.find_element_by_css_selector('[aria-label="None"]').click()
        # Select all N/A
        # Damage or Stains
        for i in range(2,2+8):
            self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[10]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
        # Visible Mold
        for i in range(2,2+8):
            self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[12]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
        # Wet or Damp
        for i in range(2,2+8):
            self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[14]/div/div[2]/div/div[{}]/div[6]/input'.format(i)).click()
        # Within 3 feet of exterior wall?: 'No [whatever]' by default
        # Damage or Stains
        self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[11]/div/div[2]/div/div[11]/div/label/input').click()
        # Visible Mold
        self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[13]/div/div[2]/div/div[11]/div/label/input').click()
        # Wet or Damp
        self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[15]/div/div[2]/div/div[11]/div/label/input').click()
        if mold_odor:
            # Select potency of mold odor
            # Open options
            self.driver.find_element_by_id("SelectId_4_placeholder").click()
            # Select option
            str1 = '[aria-label="{}"]'.format("Strong")
            self.driver.find_element_by_css_selector(str1).click()
        # Press submit button
        self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button/div').click()
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
        submit_button = self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button[2]/div')
        if submit:
            submit_button.click()
        # Next Page
            # Submit another form
            submit_link = self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[2]/div[2]/div[2]/a')
            if continue_it:
                submit_link.click()
        if close:
            # The End
            self.driver.quit()
            print("that's the end of the main instruction set.")