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

from eventpy.eventdispatcher import EventDispatcher
import eventpy.policy as eventPolicy

def test_noParams1() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    dispatcher = EventDispatcher()
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(12, cb2)
    dispatcher.appendListener(13, cb3)

    dataList = []
    dispatcher.dispatch(1)
    assert dataList == [ ]

    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 1 ]

    dataList = []
    dispatcher.dispatch(12)
    assert dataList == [ 2 ]

    dataList = []
    dispatcher.dispatch(13)
    assert dataList == [ 3 ]

def test_noParams2() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    dispatcher = EventDispatcher()
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(12, cb1)
    dispatcher.appendListener(12, cb2)
    dispatcher.appendListener(13, cb3)
    dispatcher.appendListener(13, cb2)
    dispatcher.appendListener(13, cb1)

    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 1 ]

    dataList = []
    dispatcher.dispatch(12)
    assert dataList == [ 1, 2 ]

    dataList = []
    dispatcher.dispatch(13)
    assert dataList == [ 3, 2, 1 ]

def test_noParams3() :
    dataList = []

    def cb1() :
        dataList.append(1)
    def cb2() :
        dataList.append(2)
    def cb3() :
        dataList.append(3)

    dispatcher = EventDispatcher()
    h1 = dispatcher.appendListener(11, cb1)
    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 1 ]

    h2 = dispatcher.prependListener(11, cb2)
    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 2, 1 ]

    h3 = dispatcher.prependListener(11, cb3)
    dispatcher.removeListener(11, h2)
    dispatcher.removeListener(99, h1) # invalid event, no effect
    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 3, 1 ]

    h2 = dispatcher.insertListener(11, cb2, h1)
    dataList = []
    dispatcher.dispatch(11)
    assert dataList == [ 3, 2, 1 ]

def test_hasParams() :
    dataList = []

    def cb1(s, i) :
        dataList.append(s + str(i + 1))
    def cb2(s, i) :
        dataList.append(s + str(i + 2))
    def cb3(s, i) :
        dataList.append(s + str(i + 3))

    dispatcher = EventDispatcher()
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(12, cb2)
    dispatcher.appendListener(13, cb3)

    dataList = []
    dispatcher.dispatch(1)
    dispatcher.dispatch(2, 'a', 5)
    assert dataList == [ ]

    dataList = []
    dispatcher.dispatch(11, 'a', 1)
    assert dataList == [ 'a2' ]

    dataList = []
    dispatcher.dispatch(12, 'b', 2)
    assert dataList == [ 'b4' ]

    dataList = []
    dispatcher.dispatch(13, 'c', 3)
    assert dataList == [ 'c6' ]

def test_hasParams_includeEvent() :
    dataList = []

    def cb1(e, s, i) :
        dataList.append(str(e) + s + str(i + 1))
    def cb2(e, s, i) :
        dataList.append(str(e) + s + str(i + 2))
    def cb3(e, s, i) :
        dataList.append(str(e) + s + str(i + 3))

    policy = eventPolicy.defaultPolicy.clone()
    policy.argumentPassingMode = eventPolicy.argumentPassingIncludeEvent
    dispatcher = EventDispatcher(policy)
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(12, cb2)
    dispatcher.appendListener(13, cb3)

    dataList = []
    dispatcher.dispatch(1)
    dispatcher.dispatch(2, 'a', 5)
    assert dataList == [ ]

    dataList = []
    dispatcher.dispatch(11, 'a', 1)
    assert dataList == [ '11a2' ]

    dataList = []
    dispatcher.dispatch(12, 'b', 2)
    assert dataList == [ '12b4' ]

    dataList = []
    dispatcher.dispatch(13, 'c', 3)
    assert dataList == [ '13c6' ]

def test_forEach() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass

    dispatcher = EventDispatcher()
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(12, cb1)
    dispatcher.appendListener(12, cb2)
    dispatcher.appendListener(13, cb3)
    dispatcher.appendListener(13, cb2)
    dispatcher.appendListener(13, cb1)

    cbList = []
    dispatcher.forEach(11, lambda cb : cbList.append(cb))
    assert cbList == [ cb1 ]

    cbList = []
    dispatcher.forEach(12, lambda cb : cbList.append(cb))
    assert cbList == [ cb1, cb2 ]

    cbList = []
    dispatcher.forEach(13, lambda cb : cbList.append(cb))
    assert cbList == [ cb3, cb2, cb1 ]

def test_forEachIf() :
    def cb1() :
        pass
    def cb2() :
        pass
    def cb3() :
        pass
        
    dispatcher = EventDispatcher()
    dispatcher.appendListener(11, cb1)
    dispatcher.appendListener(11, cb2)
    dispatcher.appendListener(11, cb3)
    
    cbList = []
    def forEachCallback1(cb) :
        cbList.append(cb)
        return cb != cb2
    dispatcher.forEachIf(11, forEachCallback1)
    assert cbList == [ cb1, cb2 ]
    
    cbList = []
    def forEachCallback2(cb) :
        cbList.append(cb)
        return True
    dispatcher.forEachIf(11, forEachCallback2)
    assert cbList == [ cb1, cb2, cb3 ]

    cbList = []
    def forEachCallback3(cb) :
        cbList.append(cb)
        return False
    dispatcher.forEachIf(11, forEachCallback3)
    assert cbList == [ cb1 ]

    cbList = []
    dispatcher.forEachIf(99, forEachCallback3)
    assert cbList == []
