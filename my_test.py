from library import *
import app

options = 7
option = None
# option = input("What option do you want?\n")
options = int(option) if option else options

if options == 0:
    today_date()
elif options == 1:
    with keyboard.Listener(on_press=lambda a:print("Im going down."), on_release=lambda a:print("Im coming up.")) as listener:
        print("This will print once the keyboard even is set up.")
        listener.join()
        print("If i cancel the program, this would never print.")
elif options == 2:
    listener = keyboard.Listener(on_press=lambda a:print("Im going down."), on_release=lambda a:print("Im coming up."))
    listener.start()
    time.sleep(3)
elif options == 3:
    # Evaluation direction
    print("1st"), print("2nd")
elif options == 4:
    press_keys_amount((tab, enter,), 4)
elif options == 5:
    # Test main_event_listener
    main_event_listener.start()
    print("Go ahead and start.\n")
    time.sleep(5)
elif options == 6:
    obj = Selenium()
    obj.test(2)
elif options == 7:
    inputs = Inputs.get_user_inputs()
    Inputs.set_user_input(inputs[0])
    obj = Selenium()
    obj.main_instructions()
elif options == 1:
    pass
elif options == 1:
    pass
else:
    print("Nothing happen.")