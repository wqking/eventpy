# eventpy library
# Copyright (C) 2020 Wang Qi (wqking)
# Github: https://github.com/wqking/eventpy
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from eventpy.callbacklist import CallbackList
import eventpy.policy as policy

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

    callbackList._currentCounter = -2 # trigger _currentCounter overflow
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
        return 1
    def cb2() :
        return 2
    def cb3() :
        return 3
        
    callbackList = CallbackList(policy.singleThreadPolicy)
    callbackList.append(cb1)
    callbackList.append(cb2)
    callbackList.append(cb3)

    i = 1
    def func1(cb) :
        nonlocal i
        assert cb() == i
        i += 1
    callbackList.forEach(func1)

    i = 1
    def func2(handle, cb) :
        nonlocal i
        assert cb() == i
        i += 1
        callbackList.remove(handle)
    callbackList.forEach(func2)

    assert callbackList.empty()

def test_forEachIf() :
    dataList = [ 0 for x in range(3) ]
    def cb1() :
        dataList[0] += 1
    def cb2() :
        dataList[1] += 2
    def cb3() :
        dataList[2] += 3
        
    callbackList = CallbackList()
    callbackList.append(cb1)
    callbackList.append(cb2)
    callbackList.append(cb3)
    
    assert dataList == [ 0, 0, 0 ]
    
    i = 0
    def func1(cb) :
        nonlocal i
        cb()
        i += 1
        return i != 2
    result = callbackList.forEachIf(func1)
    
    assert not result
    assert dataList == [ 1, 2, 0 ]

def test_nestedCallbacks_newCallbacksShouldNotBeTriggered() :
    a = 0
    b = 0
    callbackList = CallbackList()

    def cb1() :
        nonlocal b
        b += 1
        callbackList.append(cbIncB)
        h2 = callbackList.append(cb2)
        callbackList.append(cbIncB)
        callbackList.insert(cbIncB, h2)
        callbackList.prepend(cbIncB)
        
    def cb2() :
        nonlocal b
        b += 1
        
    def cbIncB() :
        nonlocal b
        b += 1
        callbackList.append(cbIncB)

    def cb0() :
        nonlocal a
        a = 1
        h1 = callbackList.append(cb1)
        callbackList.prepend(cbIncB)
        callbackList.insert(cbIncB, h1)
        
    callbackList.append(cb0)
    
    assert a == 0
    assert b == 0

    callbackList()
    assert a == 1
    assert b == 0

    callbackList()
    assert a == 1
    assert b == 3 # there are 3 new top level callback

    b = 0
    callbackList()
    assert a == 1
    assert b > 3
    
class RemovalTester :
    def __init__(self, callbackCount, removerIndex, indexesToBeRemoved) :
        self._callbackCount = callbackCount
        self._removerIndex = removerIndex
        self._indexesToBeRemoved = indexesToBeRemoved
        
    def test(self) :
        callbackList = CallbackList()

        handleList = []
        dataList = []
        compareList = []

        for i in range(self._callbackCount) :
            handleList.append(None)
            dataList.append(0)
            compareList.append(i + 1)
            
        def createNormalCallback(index) :
            def cb() :
                dataList[index] = index + 1
            return cb
            
        def createRemovalCallback(index) :
            def cb() :
                dataList[index] = index + 1
                for i in self._indexesToBeRemoved :
                    callbackList.remove(handleList[i])
            return cb

        for i in range(self._callbackCount) :
            if i == self._removerIndex :
                handleList[i] = callbackList.append(createRemovalCallback(i))
            else :
                handleList[i] = callbackList.append(createNormalCallback(i))
        
        callbackList()
        
        for i in self._indexesToBeRemoved :
            if i > self._removerIndex :
                compareList[i] = 0
                
        assert dataList == compareList

def test_removeInsideCallback() :
    RemovalTester(7, 3, [ 0 ]).test()
    RemovalTester(7, 3, [ 1 ]).test()
    RemovalTester(7, 3, [ 2 ]).test()
    RemovalTester(7, 3, [ 3 ]).test()
    RemovalTester(7, 3, [ 4 ]).test()
    RemovalTester(7, 3, [ 5 ]).test()
    RemovalTester(7, 3, [ 6 ]).test()

    RemovalTester(7, 3, [ 0, 3 ]).test()
    RemovalTester(7, 3, [ 3, 0 ]).test()
    RemovalTester(7, 3, [ 1, 3 ]).test()
    RemovalTester(7, 3, [ 3, 1 ]).test()
    RemovalTester(7, 3, [ 2, 3 ]).test()
    RemovalTester(7, 3, [ 3, 2 ]).test()
    RemovalTester(7, 3, [ 3, 4 ]).test()
    RemovalTester(7, 3, [ 4, 3 ]).test()
    RemovalTester(7, 3, [ 3, 5 ]).test()
    RemovalTester(7, 3, [ 5, 3 ]).test()
    RemovalTester(7, 3, [ 3, 6 ]).test()
    RemovalTester(7, 3, [ 6, 3 ]).test()

    RemovalTester(7, 3, [ 2, 4 ]).test()
    RemovalTester(7, 3, [ 4, 2 ]).test()
    RemovalTester(7, 3, [ 0, 6 ]).test()
    RemovalTester(7, 3, [ 0, 0 ]).test()

    RemovalTester(7, 3, [ 4, 5 ]).test()
    RemovalTester(7, 3, [ 5, 4 ]).test()

    RemovalTester(7, 3, [ 3, 4, 5 ]).test()
    RemovalTester(7, 3, [ 3, 5, 4 ]).test()

    RemovalTester(7, 3, [ 0, 1, 2, 3, 4, 5, 6 ]).test()
    RemovalTester(7, 3, [ 6, 5, 4, 3, 2, 1, 0 ]).test()
    RemovalTester(7, 3, [ 0, 2, 1, 3, 5, 4, 6 ]).test()
    RemovalTester(7, 3, [ 6, 4, 5, 3, 1, 2, 0 ]).test()
