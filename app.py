# Automate Fillinf-out forms
from library import *
import tests

import click


@click.command()
@click.option("--observer_name", default=observer_name, help="The person that filled out the doc.")
def main_event():
    main_event_listener.start()
    # Get user inputs
    get_user_inputs()
    # Enter Main event loop
    for _ in range(1e4):
        if end:
            # End of event loop
            quit()
            exit()
        else:
            # Main event loop
            pass


def one_form(option=4):
    """Fill out one form."""
    obj = Selenium()
    # Input
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
        runner = Runner(
            sleep_time=20,
            sleep_pauses=[PAUSE.BEFORE_NEXT_PAGE,]
        )
        runner.run(obj)
        # obj.main_instructions(submit=False, option=2)


if __name__ == "__main__":
    # main_event()
    one_form()