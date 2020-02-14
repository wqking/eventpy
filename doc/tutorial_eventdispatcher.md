# Tutorials of EventDispatcher

<!--toc-->

## Tutorials

### Tutorial 1 -- Basic usage

**Code**  
```python
from eventpy.eventdispatcher import EventDispatcher

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
```

**Output**  
> Got event 3.  
> Got event 5.  
> Got another event 5.  

**Remarks**  
First let's define a dispatcher.
```python
dispatcher = EventDispatcher()
```

Now let's add a listener.  
```python
dispatcher.appendListener(3, lambda : print("Got event 3."))
```
Function `appendListener` takes at least two arguments. The first argument is the *event* of type *event type*, here is `int`. The second is the *callback*.  
The *callback* can be any callback target -- functions, lambda expressions, or callable objects that defined `__call__`.   
In the tutorial, we also add two listeners for event 5.  

Now let's dispatch some event.
```python
dispatcher.dispatch(3);
dispatcher.dispatch(5);
```
Here we dispatched two events, one is event 3, the other is event 5.  
During the dispatching, all listeners of that event will be invoked one by one in the order of they were added.

### Tutorial 2 -- Listener with parameters

**Code**  
```python
# create an EventDispatcher
dispatcher = EventDispatcher()

dispatcher.appendListener(3, lambda s, b : print("Got event 3, s is %s b is %d" % (s, b)))
dispatcher.appendListener(5, lambda s, b : print("Got event 5, s is %s b is %d" % (s, b)))
dispatcher.appendListener(5, lambda s, b : print("Got another event 5, s is %s b is %d" % (s, b)))

# Dispatch the events, the first argument is always the event type.
dispatcher.dispatch(3, "Hello", True)
dispatcher.dispatch(5, "World", False)
```

**Output**  
> Got event 3, s is Hello b is true  
> Got event 5, s is World b is false  
> Got another event 5, s is World b is false  

**Remarks**  

### Tutorial 3 -- Customized event struct

**Code**  
```python
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
```

**Output**  

> Got event 3  
> Event::type is 3  
> Event::message is Hello world  
> Event::param is 38  
> b is true  

**Remarks**
A common situation is an Event class is defined as the base class, all other events derive from Event, and the actual event type is a data member of Event (think QEvent in Qt). To let EventDispatcher knows how to get the event type from class Event, policies (the third template parameter) is used.  
