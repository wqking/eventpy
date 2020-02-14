# eventpy library
# Copyright (C) 2020 Wang Qi (wqking)
# Github: https://github.com/wqking/eventpy
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from eventpy.eventdispatcher import EventDispatcher
import eventpy.policy

def test_tutorial_1_basic() :
    print("EventDispatcher tutorial 1, basic")

    # create an EventDispatcher
    dispatcher = EventDispatcher()

    # Add a listener.
    # here 3 and 5 is the event type,
    # Lambda is not required, any function or callable object is fine
    dispatcher.appendListener(3, lambda : print("Got event 3."))
    dispatcher.appendListener(5, lambda : print("Got event 5."))
    dispatcher.appendListener(5, lambda : print("Got another event 5."))

    # Dispatch the events, the first argument is always the event type.
    dispatcher.dispatch(3)
    dispatcher.dispatch(5)

def test_tutorial_2_listenerWithParameters() :
    print("EventDispatcher tutorial 2, listener with parameters")

    # create an EventDispatcher
    dispatcher = EventDispatcher()

    dispatcher.appendListener(3, lambda s, b : print("Got event 3, s is %s b is %d" % (s, b)))
    dispatcher.appendListener(5, lambda s, b : print("Got event 5, s is %s b is %d" % (s, b)))
    dispatcher.appendListener(5, lambda s, b : print("Got another event 5, s is %s b is %d" % (s, b)))

    # Dispatch the events, the first argument is always the event type.
    dispatcher.dispatch(3, "Hello", True)
    dispatcher.dispatch(5, "World", False)

def test_tutorial_3_customizedEventClass() :
    print("EventDispatcher tutorial 3, customized Event class")
    
    # Define an Event to hold all parameters.
    # Instead of class, other data types such as dictionary can be used
    class MyEvent :
        def __init__(self, type, message, param) :
            self.type = type
            self.message = message
            self.param = param

    def getEvent(e, b) :
        return e.type

    # Define policies to let the dispatcher knows how to
    # extract the event type.
    # Note we should clone the defaultPolicy, otherwise, the defaultPolicy will be modified.
    myPolicy = eventpy.policy.defaultPolicy.clone()
    myPolicy.getEvent = getEvent
    # Change argumentPassingMode to include the first argument (which is MyEvent) during dispatch
    myPolicy.argumentPassingMode = eventpy.policy.argumentPassingIncludeEvent
    
    # create an EventDispatcher
    # pass the new policies to the constructor
    dispatcher = EventDispatcher(myPolicy)
    
    # Add a listener
    # Note the first argument is the event type, not MyEvent
    dispatcher.appendListener(3, lambda e, b : print(
        "Got event 3, type is %d, message is %s, param is %d, b is %d" % (e.type, e.message, e.param, b)
    ))
    
    # Dispatch the event
    dispatcher.dispatch(MyEvent(3, "Hello world", 38), True)

def test_tutorial_4_eventCanceling() :
    print("EventDispatcher tutorial 4, event canceling")
    
    # Define an Event to hold all parameters.
    # Instead of class, other data types such as dictionary can be used
    class MyEvent :
        def __init__(self, type = 0) :
            self.type = type
            self.canceled = False

    def getEvent(e) :
        return e.type
        
    def canContinueInvoking(e) :
        return not e.canceled

    # Define policies to let the dispatcher knows how to
    # extract the event type.
    # Note we should clone the defaultPolicy, otherwise, the defaultPolicy will be modified.
    myPolicy = eventpy.policy.defaultPolicy.clone()
    myPolicy.getEvent = getEvent
    myPolicy.canContinueInvoking = canContinueInvoking
    # Change argumentPassingMode to include the first argument (which is MyEvent) during dispatch
    myPolicy.argumentPassingMode = eventpy.policy.argumentPassingIncludeEvent
    
    # create an EventDispatcher
    # pass the new policies to the constructor
    dispatcher = EventDispatcher(myPolicy)
    
    # Add a listener
    # Note the first argument is the event type, not MyEvent
    def cb1(e) :
        print("Got event %d" % (e.type))
        e.canceled = True
    dispatcher.appendListener(3, cb1)
    dispatcher.appendListener(3, lambda e : print("Should not get this event 3"))
    
    # Dispatch the event
    dispatcher.dispatch(MyEvent(3))

