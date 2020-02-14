# Introduction to eventpy library

eventpy includes three main classes, CallbackList, EventDispatcher, and EventQueue. Each class has a different purpose and usage.  

## Class CallbackList

CallbackList is the fundamental class in eventpy. The other classes EventDispatcher and EventQueue are built on CallbackList.  

CallbackList holds a list of callbacks. At the time of the call, CallbackList simply invokes each callback one by one. Consider CallbackList as the signal/slot system in Qt, or the callback function pointer in some Windows APIs (such as lpCompletionRoutine in `ReadFileEx`).  
The *callback* can be any callback target -- functions, lambda expressions, and any callable objects that defined `__call__`.  

CallbackList is ideal when there are very few kinds of events. Each event can have its own CallbackList, and each CallbackList can have a different prototype. For example,
```python
onStart = eventpy.CallbackList()
onStop = eventpy.CallbackList()
```
However, if there are many kinds of events, hundreds of to unlimited (this is quite common in GUI or game systems), it would be crazy to use CallbackList for each event. This is how EventDispatcher comes useful.  

## Class EventDispatcher

EventDispatcher is something like a dictionary of (EventType, CallbackList).

On dispatching, EventDispatcher finds the CallbackList of the event type, then invoke the callback list. The invocation is always synchronous. The listeners are triggered when `EventDispatcher.dispatch` is called.  

EventDispatcher is ideal when there are many kinds of events, or the number of events cannot be predetermined. Each event is distinguished by the event type. For example,
```python
dispatcher = eventpy.EventDispatcher();
dispatcher.appendListener(3, lambda s, b : print("Got event 3, s is %s b is %d" % (s, b)))
dispatcher.appendListener(5, lambda s, b : print("Got event 5, s is %s b is %d" % (s, b)))
dispatcher.dispatch(3, "Hello", True)
dispatcher.dispatch(5, "World", False)
```

## Class EventQueue

EventQueue includes all features of EventDispatcher and adds event queue features.  
EventQueue is asynchronous. Events are cached in the queue when `EventQueue.enqueue` is called, and dispatched later when `EventQueue.process` is called. `enqueue` and `process` can happen in the same thread, or in different threads.  
EventQueue is equivalent to the event system (QEvent) in Qt, or the message processing in Windows.  

```python
# create an EventQueue
queue = eventqueue.EventQueue()
queue.appendListener(3, lambda s, n : print("Got event 3, s is %s n is %d" % (s, n)))
queue.appendListener(5, lambda s, n : print("Got event 5, s is %s n is %d" % (s, n)))

# Enqueue the events, the first argument is always the event type.
# The listeners are not triggered during enqueue.
queue.enqueue(3, "Hello", 38)
queue.enqueue(5, "World", 58)

# Process the event queue, dispatch all queued events.
queue.process();
```

