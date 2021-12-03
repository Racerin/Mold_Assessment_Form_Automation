# Automate Fillinf-out forms
from library import *
import tests

import click


def one_form(option=4):
    """Fill out one form."""
    obj = Selenium()

    if option == 1:
        # Prompt user inputs
        Inputs.user_input_prompt()
        obj.main_instructions(submit=False, mold_odor=True)

    elif option == 2:
        # Get inputs from tsv file
        rows = Inputs.get_user_inputs()
        # Assign only the 1st row
        Inputs.row_update(rows[0])
        obj.main_instructions(submit=False, mold_odor=True)

    elif option == 3:
        tests.TestInputs.set_test_values()
        obj.main_instructions(submit=False, mold_odor=True)

    elif option == 4:
        tests.TestInputs.set_test_values()
        runner = Runner(
            sleep_time=20,
            sleep_yields=[YIELD.BEFORE_NEXT_PAGE,]
        )
        runner.run(obj)


if __name__ == "__main__":
    one_form()