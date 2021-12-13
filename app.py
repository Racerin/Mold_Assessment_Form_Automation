# Automate Fillinf-out forms
from library import *
import library
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


@click.command()
@click.option('--observer', '-o', default=Inputs.observer_name, help="The name of the person who conducted the Mold Assessment.", )
@click.option('--date', '-d', default=Inputs.date, help="The date (format: mm/dd/yyyy) that ALL the mold assessments were conducted (Do not use if the mold accessment was conducted different days.).", )
@click.option('--excel-load-file', default=excel_load_file, show_default=True, help="The excel preadsheet file the user filled-out.", )
@click.option('--ignore-completed', is_flag=True, default=Inputs._ignore_completed, help="Ignore a user input if it was submitted before.", )
def app_automate(observer, date, excel_load_file, ignore_completed):
    """ Run a terminal app to automatically submit
    user inputs from the spreadsheet
    onto the online Microsoft form. 
    """

    click.echo("Form automation started.")
    config = Config()
    
    # Assign the values to the properties
    click.echo("This is observer: {}".format(observer))
    library.Inputs.observer_name = observer
    library.Inputs.date = date
    library.excel_load_file = excel_load_file
    library.Inputs._ignore_completed = ignore_completed
    # setattr(library.Inputs, '_ignore_completed', ignore_completed)

    # Run through forms
    # fill_out_forms()

    click.echo("Form automation ended.")


if __name__ == "__main__":
    # one_form()
    app_automate()