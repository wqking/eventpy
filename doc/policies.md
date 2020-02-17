# Policies
<!--begintoc-->
* [Introduction](#a2_1)
* [Policies](#a2_2)
  * [Function getEvent](#a3_1)
  * [Function canContinueInvoking](#a3_2)
  * [Object threading](#a3_3)
* [Object argumentPassingMode](#a2_3)
<!--endtoc-->

<a id="a2_1"></a>
## Introduction

eventpy uses policy based design to configure and extend each components' behavior. The only parameter in EventDispatcher, EventQueue, and CallbackList is the policies object. All those three classes have default policies class named `eventpy.policy.defaultPolicy`.  
A policy is an instance of `eventpy.policy.Policy`.  
The same policy mechanism applies to all three classes, EventDispatcher, EventQueue, and CallbackList, though not all classes requires the same policy.

<a id="a2_2"></a>
## Policies

<a id="a3_1"></a>
### Function getEvent

**Prototype**: `getEvent(*args, **kwargs)`. The function receives same arguments as `EventDispatcher.dispatch` and `EventQueue.enqueue`, and must return an event type.  
**Default value**: the default implementation returns the first argument `args[0]` of `getEvent`.  
**Apply**: EventDispatcher, EventQueue.

eventpy forwards all arguments of `EventDispatcher.dispatch` and `EventQueue.enqueue` (both has same arguments) to `getEvent` to get the event type, then invokes the callback list of the event type.  

Sample code

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

<a id="a3_2"></a>
### Function canContinueInvoking

**Prototype**: `canContinueInvoking(*args, **kwargs)`. The function receives same arguments as `EventDispatcher.dispatch` and `EventQueue.enqueue`, and must return true if the event dispatching or callback list invoking can continue, false if the dispatching should stop.  
**Default value**: the default implementation always returns true.  
**Apply**: CallbackList, EventDispatcher, EventQueue.

Sample code

```python
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
```

<a id="a3_3"></a>
### Object threading

**Default value**: `eventpy.policy.multipleThreading`.  
**Apply**: CallbackList, EventDispatcher, EventQueue.

`Threading` controls threading model. Default is 'multipleThreading'. Possible values:  
  * `multipleThreading`: the core data is protected with mutex. It's the default value. The library is safe in multiple threading.  
  * `singleThreading`: the core data is not protected and can't be accessed from multiple threads. The library is unsafe in multiple threading, but has better performance.  

<a id="a2_3"></a>
## Object argumentPassingMode

**Default value**: `argumentPassingExcludeEvent`.  
**Apply**: EventDispatcher, EventQueue.

`argumentPassingMode` is the argument passing mode. Default is `argumentPassingExcludeEvent`.

Let's see some examples. Assume we have the dispatcher  
```python
dispatcher.dispatch(3, "hello");
```

if `argumentPassingMode` is `argumentPassingExcludeEvent`, the listeners are called with argument `"hello"`, and `3` is the event type and is excluded.
if `argumentPassingMode` is `argumentPassingIncludeEvent`, the listeners are called with argument `3` and `"hello"`, and `3` is the event type and is included.

**Note**: the same rules also applies to `EventDispatcher<>::enqueue`, since `enqueue` has same parameters as `dispatch`.

