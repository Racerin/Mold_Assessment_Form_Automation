import unittest
import os
import datetime
import uuid
import string
import random
from random import randrange

from library import *


def randstr(length=randrange(1,20)):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_rand_str() -> str:
    str1 = str(uuid.uuid4().hex)
    str1 = datetime.datetime.now().strftime("%y%m%d_%H%M%S%f")
    return str1


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

    def test_progressively(self):
        """This unittest is used often to help build the app itself."""
        obj = Selenium()
        TestInputs.set_test_values()
        runner = Runner(
            sleep_time=1,
            sleep_pauses={PAUSE.BEFORE_NEXT_PAGE:None, },
        )
        runner.run(obj)


class TestKeyboardManager(unittest.TestCase):
    pass