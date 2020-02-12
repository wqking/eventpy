# Class EventQueue reference

<a id="a2_1"></a>
## Description

EventQueue includes all features of EventDispatcher and adds event queue features.  
EventQueue is asynchronous. Events are cached in the queue when `EventQueue.enqueue` is called, and dispatched later when `EventQueue.process` is called.  
EventQueue is equivalent to the event system (QEvent) in Qt, or the message processing in Windows API.  

<a id="a2_2"></a>
## API reference

<a id="a3_1"></a>
### Import

import eventpy.eventqueue

<a id="a3_4"></a>
### Member functions

#### constructor

```python
EventQueue(policy = eventpy.policy.defaultPolicy)
```

`policy`: the policy to configure and extend the event dispatcher. The default value is `eventpy.policy.defaultPolicy`. See [document of policies](policies.md) for details.  

#### enqueue

```python
enqueue(*args, **kwargs);
```  
Put an event into the event queue. The event type is deducted from the arguments of `enqueue`, usually the first argument is the event.  
`enqueue` wakes up any threads that are blocked by `wait` or `waitFor`.  
The time complexity is O(1).  

#### process

```python
process()
```  
Process the event queue. All events in the event queue are dispatched once and then removed from the queue.  
The function returns true if any events were processed, false if no event was processed.  
The listeners are called in the thread same as the caller of `process`.  
Any new events added to the queue during `process()` are not dispatched during current `process()`.  
`process()` is efficient in single thread event processing, it processes all events in the queue in current thread. To process events from multiple threads efficiently, use `processOne()`.  
Note: if `process()` is called from multiple threads simultaneously, the events in the event queue are guaranteed dispatched only once.  

#### processOne

```python
processOne()
```  
Process one event in the event queue. The first event in the event queue is dispatched once and then removed from the queue.  
The function returns true if one event was processed, false if no event was processed.  
The listener is called in the thread same as the caller of `processOne`.  
Any new events added to the queue during `processOne()` are not dispatched during current `processOne()`.  
If there are multiple threads processing events, `processOne()` is more efficient than `process()` because it can split the events processing to different threads. However, if there is only one thread processing events, 'process()' is more efficient.  
Note: if `processOne()` is called from multiple threads simultaneously, the events in the event queue are guaranteed dispatched only once.  

#### processIf

```python
processIf(func)
```
Process the event queue. Before processing an event, the event is passed to `func` and the event will be processed only if `func` returns true.  
`func` takes exactly the same arguments as `EventQueue.enqueue`, and returns a boolean value.  
`processIf` returns true if any event was dispatched, false if no event was dispatched.  
`processIf` has some good use scenarios:  
1. Process certain events in certain thread. For example, in a GUI application, the UI related events may be only desired to processed in the main thread.  
2. Process the events until certain time. For example, in a game engine, the event process may be limited to only several milliseconds, the remaining events will be process in next game loop.  

#### emptyQueue

```python
emptyQueue()
```
Return true if there is no any event in the event queue, false if there are any events in the event queue.  
Note: in multiple threading environment, the empty state may change immediately after the function returns.  

#### clearEvents

```python
clearEvents()
```
Clear all queued events without dispatching them.  

#### wait

```python
wait()
```
`wait` causes the current thread to block until there is new event arrives in the queue.  
`wait` is useful when a thread processes the event queue. A sampel usage is,
```python
while True :
    eventQueue.wait()
    eventQueue.process()
```
The code works event if it doesn't `wait`, but doing that will waste CPU power resource.

#### waitFor

```python
waitFor(seconds)
```
Wait for no longer than *seconds* time out.  
*seconds* is float number in second unit, so 0.01 is 10 milliseconds.
Return true if the queue is not empty, false if the return is caused by time out.  
`waitFor` is useful when a event queue processing thread has other condition to check. For example,
```python
shouldStop = False
while True :
    while not eventQueue.waitFor(0.01) and not shouldStop :
        if shouldStop :
            break
        eventQueue.process()
```

#### peekEvent

```python
peekEvent();
```
Retrieve an event from the queue.  
Return an object of `eventqueue.QueuedEvent`, None if there is no events.   
```python
class QueuedEvent :
    def __init__(self, event, args, kwargs) :
        self.event = event
        self.args = args
        self.kwargs = kwargs

```
`queuedEvent` is a eventqueue.QueuedEvent class. `event` is the event, `args` and `kwargs` are the arguments passed in `enqueue`.  
If the queue is empty, the function returns None, otherwise it returns an object of `eventqueue.QueuedEvent`.  
After the function returns, the original even is still in the queue.  

#### takeEvent

```python
takeEvent()
```
Take an event from the queue and remove the original event from the queue.  
If the queue is empty, the function returns None, otherwise it returns an object of `eventqueue.QueuedEvent`.  
After the function returns, the original even is removed from the queue.  

#### dispatchEvent

```python
dispatchEvent(queuedEvent)
```
Dispatch an event which was returned by `peekEvent` or `takeEvent`.  

<a id="a3_5"></a>
### Class eventqueue.DisableQueueNotify  

`eventqueue.DisableQueueNotify` is an exception safe class that temporarily prevents the event queue from waking up any waiting threads. When any `DisableQueueNotify` object exist using `with` keyword, calling `enqueue` doesn't wake up any threads that are blocked by `wait`. When the `DisableQueueNotify` object is out of scope, the waking up is resumed. If there are more than one `DisableQueueNotify` objects, the waking up is only resumed after all `DisableQueueNotify` objects are destroyed.  
`DisableQueueNotify` is useful to improve performance when batching adding events to the queue. For example, in a main loop of a game engine, `DisableQueueNotify` can be created on the start in a frame, then the game adding events to the queue, and the `DisableQueueNotify` is destroyed at the end of a frame and the events are processed.

To use `DisableQueueNotify`, construct it with an instance of event queue in `with` statement.

Sample code
```python
with DisableQueueNotify(queue) :
    # any blocking threads will not be waken up by the below two lines.
    queue.enqueue(otherEvent, 2)
    queue.enqueue(otherEvent, 4)
# any blocking threads are waken up here immediately.

# any blocking threads will be waken up by below line since there is no DisableQueueNotify.
queue.enqueue(3);
```

