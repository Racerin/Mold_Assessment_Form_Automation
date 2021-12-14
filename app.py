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

    elif option == 4:
        tests.TestInputs.set_test_values()
        runner = Runner(
            sleep_time=20,
            sleep_yields=[YIELD.BEFORE_NEXT_PAGE,]
        )
        runner.run(obj)

def fill_out_forms(pause_at_form_end=False):
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
@click.option('--interact', '-i', is_flag=True, default=False, help="Respond to prompts for more detailed information.")
def app_automate(observer, date, excel_load_file, ignore_completed, interact):
    """ Run a terminal app to automatically submit
    user inputs from the spreadsheet
    onto the online Microsoft form. 
    """

    # Instantiation
    config = Config()
    # pause_at_form_end = False

    # Interaction, TOTEST, TODO
    if interact:
        # Get an observer name if nothing from config > command line
        if not Inputs.observer_name:
            click.echo("The observer's name could not be found.")
            observer = click.prompt(PROMPT_OBSERVER_NAME).strip()

        # Inform user of date
        if not Inputs.date:
            click.echo("The date will be today's date: {}".format(today_date()))
            Inputs.date = today_date()

        # Get a file from the various files in working directory.
        if not excel_load_file:
            pwd = os.getcwd()
            file_names = [f for f in os.listdir(pwd) if os.path.isfile(os.path.join(pwd, f))]
            excel_file_names = [f for f in file_names if re.match(RE_EXCEL_FILE_EXT, f)]
            if excel_file_names:
                file_name = best_match(excel_file_names, FILE_EXAMPLE_TEMPLATE)
                # Send message
                click.echo("Select the file name by its number below.")
                for i, excel_file_name in enumerate(excel_file_names):
                    click.echo("{}: {}".format(i, excel_file_name))
                try:
                    ans = click.prompt().strip(type=int)
                    excel_file_name[ans]
                except (ValueError, IndexError):
                    click.echo("This is an incorrect input. A Default file name '{}' was selected.".format(file_name))
            else:
                raise FileNotFoundError("Spreadsheet file cannot be found.")

        # Do you ignore completed forms?
        ignore_completed = click.confirm(PROMPT_IGNORE_COMPLETED)

        # Pause at the end of each form
        pause_at_form_end = click.confirm(PROMPT_PAUSE_AT_FORM_END)
    
    # Assign the values to the properties
    click.echo("This is observer: {}".format(observer))
    library.Inputs.observer_name = observer
    library.Inputs.date = date
    library.excel_load_file = excel_load_file
    library.Inputs._ignore_completed = ignore_completed
    # setattr(library.Inputs, '_ignore_completed', ignore_completed)

    # Start form automation
    click.echo("Form automation started.")
    
    # Run through forms
    fill_out_forms()

    click.echo("Form automation ended.")


if __name__ == "__main__":
    # one_form()
    app_automate()