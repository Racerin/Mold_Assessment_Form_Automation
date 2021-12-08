import unittest
import os
import datetime
import tempfile
import uuid
import string
import random
from random import randrange
import logging

import openpyxl

import library
from library import *

logging.basicConfig(
    filename="test.log", 
    # level=logging.INFO,
    filemode='w',
    # encoding='utf-8',
    format=LOGGER_FORMAT_TEST,
    )
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def randstr(length=randrange(1,20)):
    """Create a string containing random characters."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_rand_str() -> str:
    """Create a string containing random characters."""
    str1 = str(uuid.uuid4().hex)
    str1 = datetime.datetime.now().strftime("%y%m%d_%H%M%S%f")
    return str1


def extract_xlsx_data(filename:str) -> Container:
    """Create a list of rows then columns from an xlsx/xltx file.
    """
    ## opening the xlsx file
    xlsx = openpyxl.load_workbook(filename)

    ## opening the active sheet
    sheet = xlsx.active

    ## getting the data from the sheet
    data = sheet.rows

    # Return object data
    return data


class Tsv_Example_Template:
    """Create a 'TemporaryFile' context manager
    that connects to 'example template.xltx' 
    as a tsv file.
    """
    def __enter__(self):
        # Obtain xlsx/xltx file data
        data = extract_xlsx_data(FILE_EXAMPLE_TEMPLATE)

        # Open the tsv temporary file
        self.tsv_file = tempfile.TemporaryFile(suffix='.tsv')
        
        # Write data to tsv file. https://www.studytonight.com/post/converting-xlsx-file-to-csv-file-using-python
        for row in data:
            row_list = list(row)
            n_col = len(row_list)
            for i in range(n_col):
                str_col = str(row_list[i].value)
                if i == n_col - 1:
                    self.tsv_file.write(str_col)
                else:
                    self.tsv_file.write(str_col + '\t')
            self.tsv_file.write('\n')

        # Return the file object
        return self.tsv_file

    def __exit__(self, *exc):
        # Explicitly close temporary file
        self.tsv_file.close()


class TestKeyboard(unittest.TestCase):
    """ All to do with testing KeyboardManager. """

    def test_logging(self):
        """ Interactive/engaging unittest of keyboard with interrupts. """

        kb = KeyboardManager()

        # Start test
        logger.debug("Started.")
        kb.start()
        for _ in range(5):
            time.sleep(5)
        logger.debug("Finished.")


class TestInputs(unittest.TestCase):

    @classmethod
    def set_test_values(cls):
        """Set values for input to test with."""
        row = get_rand_str(), randrange(1, 5), randrange(1, 3), randrange(1, 3), randrange(0,4)
        kwa = {
            'mold_odor_desc':randstr(20),
            'supplies_and_materials_desc':["Lunch kit", 'box', 0],
            }
        Inputs.set_user_input(row, **kwa)

    def test_tsv(self):
        """Test the saving and loading of completed tsv files."""

        container = [
            [1, 2, 3, 4, 5],
            ['a', 'b', 'c', 'd'],
        ]

        try:
            _, filename = tempfile.mkstemp(suffix='.tsv', dir=os.getcwd())
            library.tsv_complete_file = filename
            
            # Save file
            Inputs.completed_row_inputs = container
            Inputs.save_completed()

            # Load file
            Inputs.load_completed()
            from_complete = Inputs.completed_row_inputs
                
            # Checks
            assert len(from_complete) == len(container), from_complete
            assert container[1][0] in from_complete[1], from_complete
            assert container[1] == from_complete[1], from_complete

        finally:
            # Clean-up
            if os.path.exists(filename):
                os.remove(filename)


class TestSelenium(unittest.TestCase):
    def t5est_open_form(self):
        """Just open the window on form."""
        obj = Selenium()
        obj.driver.get(website_url)
        obj.hold_open()
        # time.sleep(60)

    def test_main_instructions_mold(self):
        """Test whether main_instructions mold input clicks button."""
        # Get inputs
        TestInputs.set_test_values()
        # Start your engines
        obj = Selenium()
        obj.main_instructions(submit=False, continue_it=False,  mold_odor=True)

    def test_progressively(self):
        """This unittest is used often to help build the app itself."""
        obj = Selenium()
        TestInputs.set_test_values()
        runner = Runner(
            sleep_time=1,
            sleep_yields={YIELD.BEFORE_NEXT_PAGE:None, },
        )
        runner.run(obj)


class TestRegularExpression(unittest.TestCase):
    def test_section_content(self):
        """Test regular expression match groupdicts."""
        # Test Section:Content regular expression
        inputs = [
            'MO:Something in here.',
            'Mold Odor:Moderate',
            'SP: Space before and after. ',
            ' OS :Other space before and after.',
        ]
        outputs = [
            ('MO', 'Something in here.'),
            ('Mold Odor', 'Moderate'),
            ('SP', 'Space before and after. '),
            ('OS','Other space before and after.'),
        ]
        for i, tup in enumerate(zip(inputs, outputs)):
            text, output = tup
            section, content = output
            match = re.match(RE_SECTION_CONTENT_GROUPDICT, text)
            assert isinstance(match, re.Match), (type(match), 'index:', i)
            dict1 = match.groupdict()
            assert 'section' in dict1
            assert 'content' in dict1
            assert dict1['section'] == section, (dict1['section'], )
            assert dict1['content'] == content, (dict1['content'], )

    def test_groupdict(self):
        """Test groupdict of regular expression match."""
        pass


class TestStringMatch(unittest.TestCase):
    def test_ratio(self):
        """Test 'Levenshtein.ratio' for my own closure."""
        # Test small strings
        small = l_ratio('AA', 'AB')
        assert isinstance(small, float)
        assert small < 1, small
        small_to_long = l_ratio('AB', 'ABra Cadabra')
        assert isinstance(small_to_long, float)
        assert small < 1, small_to_long
        # Test commutative match
        forward = l_ratio('Snake', 'Hibiscus flower')
        backward = l_ratio('Hibiscus flower', 'Snake')
        assert forward == backward, (forward, backward)


class TestExampleTemplate(unittest.TestCase):
    """Test the values of 'example template.xltx' """

    @classmethod
    def setUpClass(cls):
        cls.example_template_file = Tsv_Example_Template()

    def test_process(self):
        """ Test the entire process of extract information from 'example template'
        to before filling-out form.
        """

        # Load Inputs
        Inputs.load_user_inputs(filename=FILE_EXAMPLE_TEMPLATE)
        assert isinstance(Inputs.user_rows_inputs, list)
        assert len(Inputs.user_rows_inputs) == 1, len(Inputs.user_rows_inputs)
        
        # Now, load a user input
        Inputs.load_user_input()
        assert len(Inputs.current_row_inputs) > 0, Inputs.current_row_inputs
        assert "Main Classroom" in Inputs.current_row_inputs[0], Inputs.current_row_inputs[0]
        assert Inputs.mold_odor_id is None, Inputs.mold_odor_id
        assert re.match(RE_DATE, Inputs.date), Inputs.date
        # Assert 'Ceiling' was not selected
        assert Inputs.damage_or_stains[0] == 'N/A' or \
            DSVMWD[0] not in Inputs.damage_or_stains, \
                Inputs.damage_or_stains
        # Assert 'Walls' was selected
        assert Inputs.damage_or_stains[1] == '2' or \
            DSVMWD[1] in Inputs.damage_or_stains, \
                Inputs.damage_or_stains
        # Assert 'Window' is external
        assert DSVMWD[3] in Inputs.damage_or_stains_exterior, \
            Inputs.damage_or_stains_exterior

    def test_fill_out_form(self):
        """ Test the filling out of form using the data from 'example template'. 
        """
        # Load web form
        selenium = Selenium()
        runner = Runner()
        runner.__sleep_callback = lambda *a: time.sleep(2)

        # Load 'Inputs' class
        Inputs.load_user_inputs(filename=FILE_EXAMPLE_TEMPLATE)

        # Load 1st form
        Inputs.load_user_input()
        runner.run(selenium=selenium)

        # Load 2nd form
        Inputs.load_user_input()
        runner.run(selenium=selenium)


class TestLibrary(unittest.TestCase):
    """ General static functions to unit test. """

    def test_str_to_key(self):
        """ Test the function 'str_to_key'. """
        input1 = "Bad Bat."
        ans1 = str_to_key(input1)
        assert ans1 == "Bad_Bat_", (input1, ans1)
        input2 = "10"
        ans2 = str_to_key(input2)
        assert ans2 == "_10", (input2, ans2)

    def test_switch_date_format(self):
        """ Test the function 'switch_date_format'. """
        
        # Normal date
        input1 = "28/02/2010"
        ans1 = switch_date_format(input1)
        assert ans1 == "02/28/2010", (input1, ans1)

        # Check Error strings
        error_input_strings = [
            "a",
            "111/11/1111",
        ]
        for error_input in error_input_strings:
            with self.assertRaises(ValueError):
                switch_date_format(error_input)