import datetime
import time
import dataclasses
import enum
import csv

from pynput import keyboard
from pynput.keyboard import Key, Controller
import selenium
import selenium.webdriver

import PARAM


keyboardController = Controller()


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
            time.sleep(5)
            self.driver.quit()

    def main_instructions(self):
        """Instruction set to carry out to fill out form."""
        self.driver.get()
        self.driver.get(website_url)
        self.driver.quit()


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


def k_type(str1 : str):
    """Type a string 'str1' with the keyboard."""
    keyboardController.type(str1)

def k_press(key : Key, dt=press_dt, release_time=False):
    """Press a single key. """
    keyboardController.press(key)
    time.sleep(dt)
    keyboardController.release(key)
    if release_time:
        if isinstance(release_time, (int, float)):
            time.sleep(release_time)
        else:
            time.sleep(dt)

def today_date(option="chrome") -> str:
    "Returns today's date for form."
    now = datetime.datetime.now()
    if option == 'mozilla':
        str1 = now.strftime('%d/%m/%Y')
    else:
        str1 = now.strftime('%m/%d/%Y')
    print("Today's date is|", str1)
    return str1


def when_you_are_ready_callback(key:Key):
    """Callback function to call when user is ready to go."""
    # Press space:
    if key == Key.space:
        return False


#INSTRUCTIONS
@dataclasses.dataclass
class Section():
    """Instructions section separation."""

    class Interludes(enum.Enum):
        IGNORE = enum.auto()
        PASS = enum.auto()
        WAIT = enum.auto()
        SLEEP = enum.auto()

        @classmethod
        def create_listener(cls) -> keyboard.Listener:
            """Creates a keyboard listener that carries out your input command"""
            return keyboard.Listener(on_release=cls.command)

        @classmethod
        def command(cls, key:Key):
            """Keyboard commands for interlude."""
            if key == Key.q:
                global end
                end = True
            elif key == Key.space:
                # Stop Listener
                return False

    name : str
    description : str = ""

    interlude_type = Interludes.IGNORE

    def __post_init__(self):
        # Call the following at interlude of instructions.
        self.section_interlude()
        # Print description if exists.
        if self.description: print(self)#print(self.decription)
        # Check state changes
        state_check()

    def section_interlude(self):
        if self.interlude_type == self.Interludes.IGNORE:
            pass
        elif self.interlude_type == self.Interludes.PASS:
            pass
        elif self.interlude_type == self.Interludes.WAIT:
            listener = self.Interludes.create_listener()
            with listener as lsnr:
                print(PARAM.interlude_listener_options)
                lsnr.join()
        elif self.interlude_type == self.Interludes.SLEEP:
            time.sleep(def_sleep)


@dataclasses.dataclass
class Page(Section):
    """Instructions page separation."""
    interlude_type = Section.Interludes.SLEEP


def press_amount(key:Key, amount:int=1):
    """Press 'key' 'amount' times."""
    for _ in range(amount):
        k_press(key, release_time=True)
    state_check()


def tab(amount : int = 1):
    """Press 'Tab' 'amount' times."""
    press_amount(Key.tab, amount=amount)

def enter(amount : int = 1):
    """Press 'Enter' 'amount' times."""
    press_amount(Key.enter, amount=amount)

def down(amount : int = 1):
    """Press down arrow 'amount' times."""
    press_amount(Key.down, amount=amount)
    
def left(amount : int = 1):
    """Press left arrow 'amount' times."""
    press_amount(Key.left, amount=amount)

def space(amount : int = 1):
    """Press 'Space' 'amount' times."""
    press_amount(Key.space, amount=amount)


def press_keys_amount(keys:'list[callable]', amount:int=1):
    for _ in range(amount):
        for ele in keys:
            # function
            if callable(ele):
                ele()
            # Key
            elif isinstance(ele, Key):
                press_amount(ele)
            else:
                raise AttributeError("Wrong key:", ele)


def main_instructions():
    """Execute all of the following functions to fill out the form."""
    Page("Start")
    tab()
    Section("Date")
    tab(), k_type(today_date())
    Section("Observer")
    tab(), k_type(observer_name)
    Section('Faculty')
    tab(), enter(), down(6), enter()
    Section("Building")
    tab(), enter(), down(Inputs.building_id), enter()
    Section("Floor")
    tab(), enter(), down(Inputs.floor_id), enter()
    Section("Room Name")
    tab(), k_type(Inputs.room_name)
    Section("Room Type")
    tab(), enter(), down(Inputs.room_type_id), enter()
    Section("Odor")
    tab(), enter(), enter()
    # tab(), enter(), down(3), enter()
    Section("")
    press_keys_amount((tab, space,), 8)
    tab(10), space()
    Section("Visible Mold", description="Select all as 'N/A'.")
    tab(2)
    press_keys_amount((left, tab,), 8)
    Section("Question 12", description="No Visible Mold selected.")
    tab(10)
    Section("Question 13 | Wet or Damp", description="Selected all 'N/A'.")
    press_keys_amount((tab, left,), 8)
    Section()
    tab(), tab(10), space()
    tab(), enter(),
    Page("Page 2")
    tab(2)
    tab(6), space()
    tab(7), space()
    tab(6), space()
    tab(4), space()
    tab(6), space()
    tab(5), space()
    tab(4), space()
    return
    tab(7), enter(), #Submit
    Page("Submit")
    enter(),
    Page("End")


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