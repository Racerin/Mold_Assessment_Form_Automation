import datetime
import time
import dataclasses
import enum
import csv

from pynput import keyboard
from pynput.keyboard import Key, Controller

import selenium
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import PARAM


keyboardController = Controller()


buildings = {
    0:"Geomatics Engineering and Land Management",
    1:"George Moonsammy Building",
    2:"Systems Laboratory",
    3:"Max Richards Building",
    4:"Kenneth S. Julien Building",
    5:"IDC Imbert Building",
    6:"Civil, Chemical and Mechanical Engineering Laboratories",
}


floors = {
    0:"Basement",
    'b':"Basement",
    1:"Ground",
    'g':"Ground",
    2:1,
    3:2,
    4:3,
    5:4,
    6:5,
}

room_types = {
    0:"Office",
    1:"Classroom",
    2:"Kitchen",
    3:"Workshop",
    4:"Lab",
    5:"Store Room",
    6:"Washroom",
    7:"Conference room",
}

effect_zones = {
    0:"Ceiling",
    1:"Walls",
    2:"Floor",
    3:"Windows",
    4:"Furnishings",
    5:"HVAC systems",
    6:"Supplies & Materials",
    7:"Pipes",
    8:"All components are more than 3 feet away from Exterior Wall",
    9:"No Exterior Walls",
    10:"No Effect/Zone",
}

ceiling_material = {
    0:"Ceiling Tile",
    1:"Plaster",
    2:"Concrete",
    3:"Sheet rock",
    4:"Metal",
    5:"Wood",
    6:"N/A",
}

wall_materials = {
    0:"Sheet rock",
    1:"Plaster",
    2:"Concrete",
    3:"Block",
    4:"Tile",
    5:"Wood",
    6:"N/A",
}

floor_material = {
    0:"Wood",
    1:"Carpet",
    2:"Vinyl",
    3:"Ceramic",
    4:"Concrete",
    5:"N/A",
}

windows_material = {
    0:"Exterior",
    1:"Interior",
    2:"skylight",
    3:"N/A",
}

furnishing = {
    0:"Furniture",
    1:"Mechanical",
    2:"Sink",
    3:"Toilet",
    4:"Copier",
    5:"N/A",
}

hvac_material = {
    0:"Forced Air",
    1:"Fan",
    2:"Unit Ventilator",
    3:"Window Unit",
    4:"N/A",
}

supplies_and_materials = {
    0:"Books",
    1:"Boxes",
    2:"Equipment",
    3:"N/A",
}

supplies_and_materials_desc = {
    0:"Wrinkled pages",
    1:"Crumpled boxes",
    2:"Other",
}

#Configure
key_cmd_dt = 1  #delay time between inputs
press_dt = 1e-1 #delay time to press and release key
def_sleep = 5
observer_name : str = "Darnell Baird"
tsv_file = 'file.tsv'
website_url = "https://forms.office.com/pages/responsepage.aspx?id=KupABOviREat2LyPNxBbYeaRdFMG3AdBl5FpMuhBKwdUOTlWWUlCVUxHUFU3TENVUUVaMDlMUkw3USQlQCN0PWcu"

#Flags
end = False
pause = False

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
    def get_user_inputs(cls) -> 'list[tuple[4]]':
        """Use tsv file to load in user inputs."""
        ans = []
        with open(tsv_file) as fd:
            rd = csv.reader(fd, delimiter="\t")
            for row in rd:
                row_with_type = [int(str1) if str1.isdigit() else str1 for str1 in row ]
                ans.append(row_with_type)
                print("this is row:", row_with_type)
        return ans

    @classmethod
    def set_user_input(cls, row):
        cls.room_name, cls.floor_id, cls.room_type_id, cls.building_id = row


class Selenium:
    """Use Selenium to traverse the form."""
    # driver = selenium.webdriver.Firefox()
    driver = selenium.webdriver.Chrome()

    def test(self, option=1):
        if option == 1:
            self.driver.get('http://www.google.com/')
            time.sleep(5) # Let the user actually see something!
            search_box = self.driver.find_element_by_name('q')
            search_box.send_keys('ChromeDriver')
            search_box.submit()
            time.sleep(5) # Let the user actually see something!
            self.driver.quit()
        elif option == 2:
            self.driver.get("https://google.co.in")
            print("Dir of driver.", dir(self.driver))
            print("vars of driver.:", vars(self.driver))
            print("Title:", self.driver.title)
            time.sleep(5)
            self.driver.quit()
        print("Good bye.")

    def dt(self):
        """Give the viewer some time to process."""
        time.sleep(1)

    def click(self, xpath:str, *args) -> selenium.webdriver.remote.webelement.WebElement:
        """ NOT USED AS YET.
        Click on an element with xpath.
        args: optional arguments for text formatting
        """
        ele = self.driver.find_element_by_xpath(xpath.format(*args))
        ele.click()
        return ele

    def main_instructions(self, submit=True, continue_it=True, close=False):
        """Instruction set to carry out to fill out form."""
        # Load webpage with form
        self.driver.get(website_url)
        # assert 'mold' in self.driver.title.lower()
        self.dt()
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
        building_text = buildings[Inputs.building_id]
        self.driver.find_element_by_css_selector('[aria-label="{}"]'.format(building_text)).click()
        # Select Floor
        self.driver.find_element_by_id("SelectId_2_placeholder").click()
        floor_text = floors[Inputs.floor_id]
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
        # Press submit button
        self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button/div').click()
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
        if submit:
            self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button[2]/div').click()

        # Submit another form
        if continue_it:
            self.driver.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[2]/div[2]/div[2]/a').click()
        # The End
        if close:
            self.driver.quit()
            print("that's the end of the main instruction set.")


def unpause_callback(key):
    try:
        if key.char == 'p':
            global pause
            pause = True
    except AttributeError:
        pass


def state_check():
    global end, pause
    if end:
        quit()
        exit()
    if pause:
        while(pause):
            with keyboard.Listener(on_release=unpause_callback) as lsnr:
                lsnr.join()
        else:
            print("Unpaused.")


def today_date(option="mozilla") -> str:
    "Returns today's date for form."
    now = datetime.datetime.now()
    if option == 'mozilla':
        str1 = now.strftime('%d/%m/%Y')
    else:
        str1 = now.strftime('%m/%d/%Y')
    print("Today's date is|", str1)
    return str1


def main_on_release(key : Key):
    try:
        if key.char == 'q':
            global end
            end = True
            print("Quit.")
        if key.char == 'p':
            # print("I am printing.")
            global pause
            pause = True
            print("Paused.")
    except AttributeError:
        pass


main_event_listener = keyboard.Listener(on_release=main_on_release)