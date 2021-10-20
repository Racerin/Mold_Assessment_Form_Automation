# Automate Fillinf-out forms
from library import *


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

def one_form(option=2):
    """Fill out one form."""
    main_event_listener.start()
    # Input
    if option == 1:
        # Prompt user inputs
        Inputs.user_input_prompt()
    elif option == 2:
        # Get inputs from tsv file
        rows = Inputs.get_user_inputs()
        # Assign only the 1st row
        Inputs.row_update(rows[0])
    # Custom config for one form?
    print("Whe you are ready to go, press 'Space'.")
    with keyboard.Listener(on_release=when_you_are_ready_callback) as listener:
        listener.join()
    print("GO!!!")
    state_check()
    # Fill out one form
    main_instructions()

if __name__ == "__main__":
    # main_event()
    one_form()