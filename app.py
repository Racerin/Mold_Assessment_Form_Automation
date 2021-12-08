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

def fill_out_forms():
    """ Fill-out forms according to data in input excel file. """

    selenium = Selenium()
    runner = Runner(
        return_yields=[],
    )

    # Load input files
    Inputs.load_user_inputs()
    Inputs.load_completed()

    # Go through each user input form submission
    try:
        success = True
        while success:
            success = Inputs.load_user_input()
            runner.run(selenium)
    except Exception as err:    
        # Save the completed forms before raising error.
        Inputs.save_completed()
        raise err from err

    # Save the completed forms at the end.
    Inputs.save_completed()


if __name__ == "__main__":
    one_form()