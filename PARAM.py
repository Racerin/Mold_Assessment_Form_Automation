import enum

CONFIG_FILE = "config.json"

TSV_HEADER = ["Room Name", "Floor ID", "Room Type ID", "Building ID", "FUTURE"]

ROOM_NAME_PROMPT = "Enter the Room/Area name: "

FLOOR_PROMPT = """Enter the corresponding number for the Floor.
0. Basement
1. Ground
2. Floor 1
3. Floor 2
4. Floor 3
5. Floor 4
6. Floor 5
"""

ROOM_TYPE_PROMPT = """Enter the corresponding number for the Room/Area type.
0. Office, 1. Classroom, 2. Kitchen, 3. Workshop, 4. Lab, 
5. Store Room, 6. Washroom, 7. Conference Room, 
8. Meeting Room, 9. Changing/Locker Room, 10. Electrical Room
"""

BUILDING_PROMPT = """Enter the corresponding number for the Building that the room is in.
0. Geomatics Engineering and Land Management, 
1. George Moonsammy Building (Block 9), 
2. Systems Lab (Block 11), 
3. Block 13 (Max Richards Building), 
4. Kenneth S. Julien Building (Block 1), 
5. Block 2 Civil Building, 
6. Civil/Chemical/Mechanical Labs
"""

OBSERVER_NAME_PROMPT = """What was the obeserver's name?
"""

INTERLUDE_LISTENER_OPTIONS = """q:quit, space:next,
"""


class ELEMENT_TYPE(enum.Enum):
    NONE = enum.auto()
    TEXT = enum.auto()
    DROPDOWN = enum.auto()
    TEXTAREA = enum.auto()
    RADIO_BUTTON = enum.auto()
    RADIO_BUTTON_GROUP = enum.auto()
    CHECK_BUTTON = enum.auto()
    CHECK_BUTTON_GROUP = enum.auto()


class PAUSE(enum.Enum):
    NONE = enum.auto()
    START = enum.auto()
    FIRST_PAGE_UPDATE = enum.auto()
    FIRST_CHECKBOX = enum.auto()
    MOLD_ODOR = enum.auto()

    BEFORE_NEXT_PAGE = enum.auto()
    NEXT_PAGE = enum.auto()
    PAGE_ONE = enum.auto()
    PAGE_TWO = enum.auto()
    PAGE_THREE = enum.auto()

    SUBMIT = enum.auto()
    NEXT_FORM = enum.auto()


# Regular Expressions
RE_TRAILING_DASH = r'^/+'


# Selenium Answers
ANS_RADIOGROUPS_DEFAULT = ['N/A'] * 8
ANS_CHECKBOXES_DEFAULT = [11]
ANS_RADIOGROUP_DEFAULT = 'N/A'
ANS_CHECKBOX2_DEFAULT = ['N/A']
ANS_CHECKBOX_OTHER_DEFAULT = []


#XPaths
XPATH_QUESTIONS = r'//div[contains(@class, "__question__")]'
# XPATH_QUESTION_BY_LABEL = '//*[@class="office-form-question-title"]/span/span[@class="text-format-content" and text()="{}"]'
XPATH_QUESTION_BY_LABEL = '//*[@class="office-form-question-title"]/span/span[@class="text-format-content" and contains(text(),"{}")]'
# XPATH_QUESTION_BY_NUMBER = '(' + XPATH_QUESTIONS + ')[{}]'
XPATH_QUESTION_BY_NUMBER = XPATH_QUESTIONS + '[{}]'
XPATH_QUESTION_ELEMENT = '//*[@class="office-form-question-element"]'
XPATH_QUESTION_CONTENT = '//*[@class="office-form-question-content"]'
XPATH_SPAN = '//span'
XPATH_INPUT = '//input'
XPATH_INPUT_PLACEHOLDER_INPUT = '//input[@placeholder="{}"]'
XPATH_TEXTINPUT = XPATH_INPUT
# XPATH_DROPDOWN = '//span[contains(@class,"text-format-content")|contains(@class, "default")]'
XPATH_DROPDOWN = '//span[contains(@class, "select-placeholder-text")]'
# XPATH_DROPDOWN_OPTION = '//div[contains(@class, "select-option-content")]'
XPATH_DROPDOWN_OPTION = r'//div[@class="select-option-content"]'
XPATH_DROPDOWN_OPTION_TEXT = XPATH_DROPDOWN_OPTION+'/span[text()="{}"]'
XPATH_DROPDOWN_OPTION_INDEX = '('+XPATH_DROPDOWN_OPTION+')[{}]'
XPATH_LABEL = '//label'
XPATH_TEXTAREA = '//textarea'
XPATH_RADIO = '//input[@type="radio"]'
XPATH_RADIOBUTTON = '//input[@type="radio"]'
XPATH_RADIOGROUP = '//div[@role="radiogroup"]'
XPATH_RADIOGROUP_BUTTON = XPATH_RADIO
XPATH_RADIOGROUP_HEADER = '//div[@class="office-form-matrix-header"]'
XPATH_RADIOGROUP_BY_SIDE_HEADER_TEXT = '//span[@class="text-format-content" and contains(text(), "{}")]'
XPATH_RADIOGROUP_BY_SIDE_HEADER = 'div[@class="office-form-matrix-cell"]'
XPATH_RADIOGROUP_HEADER_TEXT = ''
XPATH_CHECKBOX = '//input[@type="checkbox"]'
XPATH_CHECKBOX_LABEL = '//div[@class="checkbox"]/label'
XPATH_NEXT_BUTTON = '//button[@role="button"]/div[text()="Next"]'
XPATH_SUBMIT_BUTTON = '//button[@role="button"]/div[text()="Submit"]'


BUILDINGS = {
    0:"Geomatics Engineering and Land Management",
    1:"George Moonsammy Building",
    2:"Systems Laboratory",
    3:"Max Richards Building",
    4:"Kenneth S. Julien Building",
    5:"IDC Imbert Building",
    6:"Civil, Chemical and Mechanical Engineering Laboratories",
}


FLOORS = {
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

ROOM_TYPES = {
    0:"Office",
    1:"Classroom",
    2:"Kitchen",
    3:"Workshop",
    4:"Lab",
    5:"Store Room",
    6:"Washroom",
    7:"Conference room",
    8:"Meeting Room",
    9:"Changing/Locker Room",
    10:"Electrical Room",
}

EFFECT_ZONES = {
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

CEILING_MATERIAL = {
    0:"Ceiling Tile",
    1:"Plaster",
    2:"Concrete",
    3:"Sheet rock",
    4:"Metal",
    5:"Wood",
    6:"N/A",
}

WALL_MATERIALS = {
    0:"Sheet rock",
    1:"Plaster",
    2:"Concrete",
    3:"Block",
    4:"Tile",
    5:"Wood",
    6:"N/A",
}

FLOOR_MATERIAL = {
    0:"Wood",
    1:"Carpet",
    2:"Vinyl",
    3:"Ceramic",
    4:"Concrete",
    5:"N/A",
}

WINDOWS_MATERIAL = {
    0:"Exterior",
    1:"Interior",
    2:"skylight",
    3:"N/A",
}

FURNISHING = {
    0:"Furniture",
    1:"Mechanical",
    2:"Sink",
    3:"Toilet",
    4:"Copier",
    5:"N/A",
}

HVAC_MATERIAL = {
    0:"Forced Air",
    1:"Fan",
    2:"Unit Ventilator",
    3:"Window Unit",
    4:"N/A",
}

SUPPLIES_AND_MATERIALS = {
    0:"Books",
    1:"Boxes",
    2:"Equipment",
    3:"N/A",
}

SUPPLIES_AND_MATERIALS_DESC = {
    0:"Wrinkled pages",
    1:"Crumpled boxes",
    2:"Other",
}

MOLD_ODOR = {
    0:"None",
    1:"Mild",
    2:"Moderate",
    3:"Strong",
}