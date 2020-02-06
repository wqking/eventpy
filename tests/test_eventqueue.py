from eventpy.eventqueue import EventQueue
import eventpy.policy as eventPolicy

def test_noParams1() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    eventQueue = EventQueue()
    eventQueue.appendListener('hello', cb1)
    eventQueue.appendListener('world', cb2)
    eventQueue.appendListener('hello', cb3)

    dataList = []
    eventQueue.enqueue('hello')
    assert dataList == []
    eventQueue.process()
    assert dataList == [ 1, 3 ]
    dataList = []
    eventQueue.process()
    assert dataList == []

def test_hasParams() :
    dataList = []

    def cb1(s, i) :
        dataList.append(s + str(i + 1))
    def cb2(s, i) :
        dataList.append(s + str(i + 2))
    def cb3(s, i) :
        dataList.append(s + str(i + 3))

    eventQueue = EventQueue()
    eventQueue.appendListener(11, cb1)
    eventQueue.appendListener(12, cb2)
    eventQueue.appendListener(13, cb3)

    dataList = []
    eventQueue.enqueue(1)
    eventQueue.enqueue(2, 'a', 5)
    eventQueue.process()
    assert dataList == [ ]

    dataList = []
    eventQueue.enqueue(11, 'a', 1)
    eventQueue.process()
    assert dataList == [ 'a2' ]

    dataList = []
    eventQueue.enqueue(12, 'b', 2)
    eventQueue.process()
    assert dataList == [ 'b4' ]

    dataList = []
    eventQueue.enqueue(13, 'c', 3)
    eventQueue.process()
    assert dataList == [ 'c6' ]

def test_processOne() :
    dataList = [ 1, 5 ]

    def cb1() :
        dataList[0] += 1
    def cb2() :
        dataList[1] += 3

    queue = EventQueue()
    queue.appendListener(3, cb1)
    queue.appendListener(5, cb2)

    queue.enqueue(3)
    queue.enqueue(5)
    assert dataList == [ 1, 5 ]

    queue.processOne()
    assert dataList == [ 2, 5 ]

    queue.processOne()
    assert dataList == [ 2, 8 ]

def test_customizedEvent() :
    policy = eventPolicy.defaultPolicy.clone()
    policy.getEvent = lambda e, s : e['type']
    policy.argumentPassingMode = eventPolicy.argumentPassingIncludeEvent
    queue = EventQueue(policy)
    dataList = []
    def cb1(e, s) :
        dataList.append(str(e['type'] + e['message'] + s))
    def cb2(e, s) :
        dataList.append(str(e['type'] + e['message'] + s))
    def cb3(e, s) :
        dataList.append(str(e['type'] + e['message'] + s))
    queue.appendListener('First', cb1)
    queue.appendListener('Second', cb2)
    queue.appendListener('Third', cb3)
    queue.enqueue({ 'type' : 'First', 'message' : 'Hello' }, 'what')
    queue.enqueue({ 'type' : 'Second', 'message' : 'World' }, 'how')
    queue.enqueue({ 'type' : 'Third', 'message' : 'Good' }, 'why')
    queue.process()
    assert dataList == [ 'FirstHellowhat', 'SecondWorldhow', 'ThirdGoodwhy' ]

def test_clearEvents() :
    dataList = [ 1, 5 ]

    def cb1() :
        dataList[0] += 1
    def cb2() :
        dataList[1] += 3

    queue = EventQueue()
    queue.appendListener(3, cb1)
    queue.appendListener(3, cb2)
    assert dataList == [ 1, 5 ]

    queue.enqueue(3)
    queue.process()
    assert dataList == [ 2, 8 ]

    queue.enqueue(3)
    queue.clearEvents()
    queue.process()
    assert dataList == [ 2, 8 ]

def test_processIf() :
    dataList = [ 0, 0, 0 ]

    def cb1(e) :
        dataList[0] += 1
    def cb2(e) :
        dataList[1] += 1
    def cb3(e) :
        dataList[2] += 1

    policy = eventPolicy.defaultPolicy.clone()
    policy.argumentPassingMode = eventPolicy.argumentPassingIncludeEvent
    queue = EventQueue(policy)
    queue.appendListener(5, cb1)
    queue.appendListener(6, cb2)
    queue.appendListener(7, cb3)
    assert dataList == [ 0, 0, 0 ]

    queue.enqueue(5)
    queue.enqueue(6)
    queue.enqueue(7)
    queue.process();
    assert dataList == [ 1, 1, 1 ]

    queue.enqueue(5)
    queue.enqueue(6)
    queue.enqueue(7)
    queue.processIf(lambda event : event == 6)
    assert dataList == [ 1, 2, 1 ]
    # Now the queue contains 5, 7

    queue.enqueue(5)
    queue.enqueue(6)
    queue.enqueue(7)
    queue.processIf(lambda event : event == 5)
    assert dataList == [ 3, 2, 1 ]
    # Now the queue contains 6, 7, 7

    # Ensure the callback in processIf is not called for unncessary times.
    # Veriy the internal loops in processIf is correct.
    callbackCounters = [ 0 for x in range(10) ]

    queue.enqueue(5)
    queue.enqueue(6)
    queue.enqueue(7)
    def func(event) :
        callbackCounters[event] += 1
        return event == 7
    queue.processIf(func)
    assert dataList == [ 3, 2, 4 ]
    # Now the queue contains 5, 6, 6

    assert callbackCounters[5] == 1
    assert callbackCounters[6] == 2
    assert callbackCounters[7] == 3

    queue.process();
    assert dataList == [ 4, 4, 4 ]
