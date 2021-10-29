import unittest
import os
import datetime
import uuid
from random import randrange

from library import *

class TestInputs(unittest.TestCase):
    @classmethod
    def set_test_values(cls):
        """Set values for input to test with."""
        row = get_rand_str(), randrange(1, 5), randrange(1, 3), randrange(1, 3)
        Inputs.set_user_input(row)

    def test_tsv(self):
        """Test the saving and loading of tsv files function."""
        # Inputs
        # filename = os.path.join(os.getcwd(), 'trash', '{}.txt'.format(get_rand_str()), )
        filename = 'trash/{}.txt'.format(get_rand_str())
        container = [
            [1, 2, 3, 4],
            ['a', 'b', 'c', 'd'],
        ]
        # Save file
        Inputs.save_tsv(container, filename=filename)
        # Load file
        loaded_container = Inputs.load_tsv(filename=filename)
        # Checks
        assert container[1] in loaded_container
        assert [str(ele) for ele in container[0]] in loaded_container


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


class TestKeyboardManager(unittest.TestCase):
    pass


def get_rand_str() -> str:
    str1 = str(uuid.uuid4().hex)
    str1 = datetime.datetime.now().strftime("%y%m%d_%H%M%S%f")
    return str1