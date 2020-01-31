from eventpy.callbacklist import CallbackList

def test_noParams() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    callbackList = CallbackList()
    assert callbackList.empty()

    h1 = callbackList.append(cb1)
    assert not callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ 1 ]

    h2 = callbackList.append(cb2)
    assert not callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ 1, 2 ]

    h3 = callbackList.insert(cb3, h2)
    assert not callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ 1, 3, 2 ]

    callbackList.remove(h2)
    assert not callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ 1, 3 ]

    h2 = callbackList.prepend(cb2)
    assert not callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ 2, 1, 3 ]

    callbackList.remove(h1)
    callbackList.remove(h2)
    callbackList.remove(h3)
    assert callbackList.empty()
    dataList = []
    callbackList()
    assert dataList == [ ]

def test_hasParams() :
    dataList = []

    def cb1(s, i) :
        dataList.append(s + str(i + 1))
    def cb2(s, i) :
        dataList.append(s + str(i + 2))
    def cb3(s, i) :
        dataList.append(s + str(i + 3))

    callbackList = CallbackList()
    assert callbackList.empty()

    h1 = callbackList.append(cb1)
    assert not callbackList.empty()
    dataList = []
    callbackList('hello', 5)
    assert dataList == [ 'hello6' ]

    h2 = callbackList.append(cb2)
    assert not callbackList.empty()
    dataList = []
    callbackList('hello', 5)
    assert dataList == [ 'hello6', 'hello7' ]

    h3 = callbackList.insert(cb3, h2)
    assert not callbackList.empty()
    dataList = []
    callbackList('hello', 5)
    assert dataList == [ 'hello6', 'hello8', 'hello7' ]

def test_forEach() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass
    callbackList = CallbackList()
    callbackList.append(cb1)
    callbackList.append(cb2)
    callbackList.append(cb3)

    cbList = []
    callbackList.forEach(lambda cb : cbList.append(cb))
    assert cbList == [ cb1, cb2, cb3 ]

def test_forEachIf() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass
    callbackList = CallbackList()
    callbackList.append(cb1)
    callbackList.append(cb2)
    callbackList.append(cb3)
    
    def forEachCallback(cb) :
        cbList.append(cb)
        return cb != cb2

    cbList = []
    callbackList.forEachIf(forEachCallback)
    assert cbList == [ cb1, cb2 ]
