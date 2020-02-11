from eventpy.eventqueue import EventQueue
import eventpy.policy as eventPolicy

import sys

def test_noParams1() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    queue = EventQueue()
    queue.appendListener('hello', cb1)
    queue.appendListener('world', cb2)
    queue.appendListener('hello', cb3)

    dataList = []
    queue.enqueue('hello')
    assert dataList == []
    queue.process()
    assert dataList == [ 1, 3 ]
    dataList = []
    queue.process()
    assert dataList == []

def test_hasParams() :
    dataList = []

    def cb1(s, i) :
        dataList.append(s + str(i + 1))
    def cb2(s, i) :
        dataList.append(s + str(i + 2))
    def cb3(s, i) :
        dataList.append(s + str(i + 3))

    queue = EventQueue()
    queue.appendListener(11, cb1)
    queue.appendListener(12, cb2)
    queue.appendListener(13, cb3)

    dataList = []
    queue.enqueue(1)
    queue.enqueue(2, 'a', 5)
    queue.process()
    assert dataList == [ ]

    dataList = []
    queue.enqueue(11, 'a', 1)
    queue.process()
    assert dataList == [ 'a2' ]

    dataList = []
    queue.enqueue(12, 'b', 2)
    queue.process()
    assert dataList == [ 'b4' ]

    dataList = []
    queue.enqueue(13, 'c', 3)
    queue.process()
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

    assert queue.processOne()
    assert dataList == [ 2, 8 ]
    
    assert not queue.processOne()

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
    
def doTest_peekEvent_takeEvent_dispatch(testIndex) :
    class SP :
        def __init__(self, value) :
            self.value = value

    queue = EventQueue()
    wpList = []
    itemCount = 3
    dataList = [ 0 for x in range(itemCount) ]
    
    def listener(sp) :
        dataList[sp.value] += 1
    queue.appendListener(3, listener)
    
    def add(e, n) :
        sp = SP(n)
        queue.enqueue(e, sp)
        wpList.append(sp)
    add(3, 0)
    add(3, 1)
    add(3, 2)
    
    def testPeek() :
        event = queue.peekEvent()
        assert event != None
        assert event.event == 3
        assert event.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4

    def testPeekPeek() :
        event = queue.peekEvent()
        assert event != None
        assert event.event == 3
        assert event.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
        event2 = queue.peekEvent()
        assert event2.event == 3
        assert event2.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
    def testPeekTake() :
        event = queue.peekEvent()
        assert event != None
        assert event.event == 3
        assert event.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
        event2 = queue.takeEvent()
        assert event2.event == 3
        assert event2.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4

    def testPeekTakePeek() :
        event = queue.peekEvent()
        assert event != None
        assert event.event == 3
        assert event.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
        event2 = queue.takeEvent()
        assert event2.event == 3
        assert event2.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4

        event3 = queue.peekEvent()
        assert event3 != None
        assert event3.event == 3
        assert event3.args[0].value == 1
        assert sys.getrefcount(wpList[1]) == 4
        
    def testPeekDispatchPeekDispatchAgain() :
        event = queue.peekEvent()
        assert event != None
        assert event.event == 3
        assert event.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
        queue.dispatchEvent(event)
        event2 = queue.peekEvent()
        assert event2 != None
        assert event2.event == 3
        assert event2.args[0].value == 0
        assert sys.getrefcount(wpList[0]) == 4
        
        assert dataList == [ 1, 0, 0 ]

        queue.dispatchEvent(event)
        assert dataList == [ 2, 0, 0 ]
        
    def testProcess() :
        assert dataList == [ 0, 0, 0 ]
        queue.process()
        assert dataList == [ 1, 1, 1 ]
        
    def takeAllProcess() :
        for i in range(itemCount) :
            event = queue.takeEvent()
            assert event != None
        assert queue.peekEvent() == None
        assert queue.takeEvent() == None

        assert dataList == [ 0, 0, 0 ]
        queue.process()
        assert dataList == [ 0, 0, 0 ]
        
    testList = [
        testPeek,
        testPeekPeek,
        testPeekTake,
        testPeekTakePeek,
        testPeekDispatchPeekDispatchAgain,
        testProcess,
        takeAllProcess
    ]
    testList[testIndex]()

def test_peekEvent_takeEvent_dispatch() :
    doTest_peekEvent_takeEvent_dispatch(0)
    doTest_peekEvent_takeEvent_dispatch(1)
    doTest_peekEvent_takeEvent_dispatch(2)
    doTest_peekEvent_takeEvent_dispatch(3)
    doTest_peekEvent_takeEvent_dispatch(4)
    doTest_peekEvent_takeEvent_dispatch(5)
    doTest_peekEvent_takeEvent_dispatch(6)

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
    assert(queue.processIf(func))
    assert dataList == [ 3, 2, 4 ]
    # Now the queue contains 5, 6, 6

    assert callbackCounters[5] == 1
    assert callbackCounters[6] == 2
    assert callbackCounters[7] == 3

    queue.process();
    assert dataList == [ 4, 4, 4 ]

    assert(not queue.processIf(None))
