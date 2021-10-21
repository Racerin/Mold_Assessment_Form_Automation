from library import *
import app

options = 7
option = None
# option = input("What option do you want?\n")
options = int(option) if option else options

if options == 3:
    # Evaluation direction
    print("1st"), print("2nd")
elif option == 1:
    pass
elif option == 1:
    pass
elif option == 1:
    pass
elif option == 1:
    pass
elif option == 1:
    pass
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
    # with keyboard.Listener(on_release=lambda k:False if k==Key.space else True ) as lsnr:
    #     lsnr.join()
    print("The End.")
elif options == 1:
    pass
elif options == 1:
    pass
else:
    print("Nothing happen.")