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

import threading
import random

def test_multiThreading() :
    threadCount = 64
    eventCountPerThread = 1024
    itemCount = threadCount * eventCountPerThread
    
    eventList = [ x for x in range(itemCount) ]
    random.shuffle(eventList)
    
    dataList = [ 0 for x in range(itemCount) ]
    handleList = [ None for x in range(itemCount) ]

    policy = eventPolicy.defaultPolicy.clone()
    policy.argumentPassingMode = eventPolicy.argumentPassingIncludeEvent
    dispatcher = EventDispatcher(policy)

    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * eventCountPerThread, (i + 1) * eventCountPerThread) :
                def listener(e, k = k) :
                    dataList[k] += e
                    dispatcher.removeListener(eventList[k], handleList[k])
                handleList[k] = dispatcher.appendListener(eventList[k], listener)
        threadList.append(threading.Thread(target = cb))
    
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()
        
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * eventCountPerThread, (i + 1) * eventCountPerThread) :
                dispatcher.dispatch(eventList[k])
        threadList.append(threading.Thread(target = cb))
    
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()
        
    eventList.sort()
    dataList.sort()
    assert eventList == dataList
        
