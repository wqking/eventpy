from eventpy.eventdispatcher import EventDispatcher
import eventpy.lock as lock

def test_noParams1() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    eventDispatcher = EventDispatcher()
    eventDispatcher.appendListener(11, cb1)
    eventDispatcher.appendListener(12, cb2)
    eventDispatcher.appendListener(13, cb3)

    dataList = []
    eventDispatcher.dispatch(1)
    assert dataList == [ ]

    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 1 ]

    dataList = []
    eventDispatcher.dispatch(12)
    assert dataList == [ 2 ]

    dataList = []
    eventDispatcher.dispatch(13)
    assert dataList == [ 3 ]

def test_noParams2() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    eventDispatcher = EventDispatcher()
    eventDispatcher.appendListener(11, cb1)
    eventDispatcher.appendListener(12, cb1)
    eventDispatcher.appendListener(12, cb2)
    eventDispatcher.appendListener(13, cb3)
    eventDispatcher.appendListener(13, cb2)
    eventDispatcher.appendListener(13, cb1)

    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 1 ]

    dataList = []
    eventDispatcher.dispatch(12)
    assert dataList == [ 1, 2 ]

    dataList = []
    eventDispatcher.dispatch(13)
    assert dataList == [ 3, 2, 1 ]

def test_noParams3() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    eventDispatcher = EventDispatcher()
    h1 = eventDispatcher.appendListener(11, cb1)
    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 1 ]

    h2 = eventDispatcher.prependListener(11, cb2)
    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 2, 1 ]

    h3 = eventDispatcher.prependListener(11, cb3)
    eventDispatcher.removeListener(11, h2)
    eventDispatcher.removeListener(99, h1) # invalid event, no effect
    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 3, 1 ]

    h2 = eventDispatcher.insertListener(11, cb2, h1)
    dataList = []
    eventDispatcher.dispatch(11)
    assert dataList == [ 3, 2, 1 ]

def test_hasParams() :
    dataList = []

    def cb1(s, i) :
        dataList.append(s + str(i + 1))
    def cb2(s, i) :
        dataList.append(s + str(i + 2))
    def cb3(s, i) :
        dataList.append(s + str(i + 3))

    eventDispatcher = EventDispatcher()
    eventDispatcher.appendListener(11, cb1)
    eventDispatcher.appendListener(12, cb2)
    eventDispatcher.appendListener(13, cb3)

    dataList = []
    eventDispatcher.dispatch(1)
    eventDispatcher.dispatch(2, 'a', 5)
    assert dataList == [ ]

    dataList = []
    eventDispatcher.dispatch(11, 'a', 1)
    assert dataList == [ 'a2' ]

    dataList = []
    eventDispatcher.dispatch(12, 'b', 2)
    assert dataList == [ 'b4' ]

    dataList = []
    eventDispatcher.dispatch(13, 'c', 3)
    assert dataList == [ 'c6' ]

def test_forEach() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass

    eventDispatcher = EventDispatcher()
    eventDispatcher.appendListener(11, cb1)
    eventDispatcher.appendListener(12, cb1)
    eventDispatcher.appendListener(12, cb2)
    eventDispatcher.appendListener(13, cb3)
    eventDispatcher.appendListener(13, cb2)
    eventDispatcher.appendListener(13, cb1)

    cbList = []
    eventDispatcher.forEach(11, lambda cb : cbList.append(cb))
    assert cbList == [ cb1 ]

    cbList = []
    eventDispatcher.forEach(12, lambda cb : cbList.append(cb))
    assert cbList == [ cb1, cb2 ]

    cbList = []
    eventDispatcher.forEach(13, lambda cb : cbList.append(cb))
    assert cbList == [ cb3, cb2, cb1 ]

def test_forEachIf() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass
        
    eventDispatcher = EventDispatcher()
    eventDispatcher.appendListener(11, cb1)
    eventDispatcher.appendListener(11, cb2)
    eventDispatcher.appendListener(11, cb3)
    
    cbList = []
    def forEachCallback1(cb) :
        cbList.append(cb)
        return cb != cb2
    eventDispatcher.forEachIf(11, forEachCallback1)
    assert cbList == [ cb1, cb2 ]
    
    cbList = []
    def forEachCallback2(cb) :
        cbList.append(cb)
        return True
    eventDispatcher.forEachIf(11, forEachCallback2)
    assert cbList == [ cb1, cb2, cb3 ]

    cbList = []
    def forEachCallback3(cb) :
        cbList.append(cb)
        return False
    eventDispatcher.forEachIf(11, forEachCallback3)
    assert cbList == [ cb1 ]

    cbList = []
    eventDispatcher.forEachIf(99, forEachCallback3)
    assert cbList == []
