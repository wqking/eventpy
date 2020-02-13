import eventpy.eventqueue as eventqueue
import eventpy.policy as eventPolicy

import threading
import time

def test_tutorial_1_basic() :
    print("EventQueue tutorial 1, basic")

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

def test_tutorial_2_multipleThreading() :
    print("EventQueue tutorial 2, multiple threading")

    # create an EventQueue
    queue = eventqueue.EventQueue()
    
    stopEvent = 1
    otherEvent = 2
    
    def threadFunc() :
        shouldStop = False
        def stopCallback(index) :
            nonlocal shouldStop
            shouldStop = True
        queue.appendListener(stopEvent, stopCallback)
        queue.appendListener(otherEvent, lambda index : print("Got event, index is %d" % (index)))
        while not shouldStop :
            queue.wait()
            queue.process()
    # Start a thread to process the event queue.
    # All listeners are invoked in that thread.
    thread = threading.Thread(target = threadFunc)
    thread.start()

    # Enqueue an event from the main thread. After sleeping for 10 milliseconds,
    # the event should have be processed by the other thread.
    queue.enqueue(otherEvent, 1)
    time.sleep(0.01)
    print("Should have triggered event with index = 1")

    queue.enqueue(otherEvent, 2)
    time.sleep(0.01)
    print("Should have triggered event with index = 2")
    
    # eventqueue.DisableQueueNotify is a resource management class that
    # disables waking up any waiting threads.
    # So no events should be triggered in this code block.
    # DisableQueueNotify is useful when adding lots of events at the same time
    # and only want to wake up the waiting threads after all events are added.
    with eventqueue.DisableQueueNotify(queue) :
        queue.enqueue(otherEvent, 10)
        time.sleep(0.01)
        print("Should NOT trigger event with index = 10")
        queue.enqueue(otherEvent, 11)
        time.sleep(0.01)
        print("Should NOT trigger event with index = 11")
    
    # The DisableQueueNotify object is destroyed here, and has resumed
    # waking up waiting threads. So the events should be triggered.
    time.sleep(0.01)
    print("Should have triggered events with index = 10 and 11")

    queue.enqueue(stopEvent, 1)
    thread.join()

