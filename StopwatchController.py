"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from Displays import *
from Lights import *
from Buzzer import *

"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class StopwatchController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button1 = Button(17, "start", buttonhandler=None)
        self._button2 = Button(16, "stop", buttonhandler=None)
        self._timekeeper = TimeKeeper()
        self._display = LCDDisplay (sda=0, scl=1, i2cid=0)

        """ Adding LEDs to Work with Buttons """
        self._lightr = Light (18, "Red LED")
        self._lightg = Light (19, "Green LED")
        """Implementing Buzzer """
        self._buzzer = PassiveBuzzer(15)

        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(3, self, debug=True)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN2_PRESS], 2)
        self._model.addTransition(2, [BTN2_PRESS], 0)
        # etc.
    
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
            
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            pass
        elif state == 1:
            # State1 do/actions
            # You can check your sensors here and perform transitions manually if needed
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # if self.motionsensor.tripped():
            # 	gotoState(2)
            
            self._display.showText(str(self._timekeeper))

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            # entry actions for state 0
            print('State 0 entered')
            self._display.showText('Ready to go!')
            self._display.reset()


        elif state == 1:
            # entry actions for state 1
            print('State 1 entered')
            """Ligth Control #1"""
            self._lightg.on()
            self._timekeeper.start()

        elif state == 2: 
            print('State 2 entered')
            """Light Control #2"""
            self._lightg.off()
            self._lightr.on()
            self._timekeeper.stop()        
            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state, event):
        if state == 2:
            self._lightr.off()
            self._timekeeper.reset()
            """Display Reset Message"""
            self._display.reset()
            self._display.showText('Resetting...')
            """LED Light Dance"""
            self._lightg.blink()
            self._lightr.blink()
            self._lightg.blink()
            self._lightr.blink()
            """"Grand Finale"""
            self._buzzer.beep()

        
            
        
    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
    MyControllerTemplate().run()