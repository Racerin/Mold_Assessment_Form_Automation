import unittest
import datetime
import uuid

from library import *

class TestInputs(unittest.TestCase):
    def test_tsv(self):
        """Test the saving and loading of tsv files function."""
        # Inputs
        filename = 'test/{}.txt'.format(get_rand_str())
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


class TestSelenium(unittest.TestCase):
    pass


class TestKeyboardManager(unittest.TestCase):
    pass


def get_rand_str() -> str:
    str1 = str(uuid.uuid4().hex)
    str1 = datetime.datetime.now().strftime("%y%m%d_%H%M%S%f")
    return str1