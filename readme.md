# eventpy -- Python library for event dispatcher and callback list

eventpy is a Python event library that provides tools that enable your application components to communicate with each other by dispatching events and listening for them. With eventpy you can easily implement signal/slot mechanism, or observer pattern.  
This library is the Python version rewritten from the C++ library [eventpp](https://github.com/wqking/eventpp), both are developed by the same developer.

## Facts and features

- **Powerful**
  - Supports synchronous event dispatching and asynchronous event queue.
  - Configurable and extensible with policies.
- **Robust**
  - Supports nested event. During the process of handling an event, a listener can safely dispatch event and append/prepend/insert/remove other listeners.
  - Thread safety. Supports multi-threading.
  - Well tested. Backed by unit tests.
- **Flexible and easy to use**
  - Listeners and events can be of any type and do not need to be inherited from any base class.
  - Requires Python 3. Tested with Python 3.7 and Cython.

## License

Apache License, Version 2.0  

## Version 0.1.0

eventpy is currently usable and stable.

## Source code

[https://github.com/wqking/eventpy](https://github.com/wqking/eventpy)

## Quick start

### Install

`pip install eventpy`

### Package

`eventpy`

### Using CallbackList
```python
# create a CallbackList
callbackList = CallbackList()
callbackList.append(lambda s, b : print("Got callback 1, s is %s b is %d" % (s, b)))
def anotherCallback(s, b) :
	print("Got callback 2, s is %s b is %d" % (s, b))
callbackList.append(anotherCallback)
# Invoke the callback list
callbackList("Hello world", True)
```

### Using EventDispatcher
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

### Using EventQueue
```python
# create an EventQueue
queue = eventqueue.EventQueue()
queue.appendListener(3, lambda s, n : print("Got event 3, s is %s n is %d" % (s, n)))
queue.appendListener(5, lambda s, n : print("Got event 5, s is %s n is %d" % (s, n)))
queue.appendListener(5, lambda s, n : print("Got another event 5, s is %s n is %d" % (s, n)))

# Enqueue the events, the first argument is always the event type.
# The listeners are not triggered during enqueue.
queue.enqueue(3, "Hello", 38)
queue.enqueue(5, "World", 58)

# Process the event queue, dispatch all queued events.
queue.process();
```

## Documentations

* [Overview](doc/introduction.md)
* [Tutorials of CallbackList](doc/tutorial_callbacklist.md)
* [Tutorials of EventDispatcher](doc/tutorial_eventdispatcher.md)
* [Tutorials of EventQueue](doc/tutorial_eventqueue.md)
* [Class CallbackList](doc/callbacklist.md)
* [Class EventDispatcher](doc/eventdispatcher.md)
* [Class EventQueue](doc/eventqueue.md)
* [Policies -- configure eventpy](doc/policies.md)
* There are runnable tutorials in the unit tests.

## Run the unit tests

Go to the root folder of eventpy, run `python -m pytest`

