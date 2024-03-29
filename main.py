import os

from threading import Thread

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.Joystick import Joystick
#from joystick import Joystick

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
BUTTON_SCREEN_NAME = 'button'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

class buttonScreen(Screen):
    #joystick = Joystick(0, False).start()

    def __init__(self, **kwargs):
        Builder.load_file('buttonScreen.kv')
        super(buttonScreen, self).__init__(**kwargs)


    def pressed(self):
        SCREEN_MANAGER.current = 'main'

class MainScreen(Screen):

    counter = StringProperty("0")
    toggle = ObjectProperty(False)

    joystick = Joystick(0, False)
    X_axis = ObjectProperty(0.0)
    Y_axis = ObjectProperty(0.0)

    def joystick_thread(self):
        while 1:
            self.joystick.refresh()
            self.X_axis = self.joystick.get_axis('x')
            self.Y_axis = self.joystick.get_axis('y')
            #print(self.X_axis)

    def start_joystick_Thread(self):
        Thread(target=self.joystick_thread).start()

    """
    Class to handle the main screen and its associated touch events
    """
    def pressed_counter(self):
        tempCounter = int(self.counter)
        tempCounter += 1
        self.counter = str(tempCounter)

    def pressed_motor_toggle(self):
        self.toggle = not self.toggle

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        #PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='button', text="LOADING BUTTON SCREEN FOR YOU", pause_duration=2)

        #SCREEN_MANAGER.current = 'button'

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'



class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(buttonScreen(name=BUTTON_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()

