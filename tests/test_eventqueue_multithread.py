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

from eventpy.eventqueue import *

import threading
import random
import time
import itertools

def test_multiThreading() :
    threadCount = 64
    dataCountPerThread = 1024
    itemCount = threadCount * dataCountPerThread

    eventList = [ x for x in range(itemCount) ]
    random.shuffle(eventList)
  
    queue = EventQueue()
    dataList = [ 0 for x in range(itemCount) ]
    for i in range(itemCount) :
        def cb(d, i = i) :
            dataList[i] += d
        queue.appendListener(eventList[i], cb)

    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * dataCountPerThread, (i + 1) * dataCountPerThread) :
                queue.enqueue(k, 3)
            for k in range(10) :
                queue.process()
        threadList.append(threading.Thread(target = cb))
    
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()
        
    compareList = [ 3 for x in range(itemCount) ]
    assert dataList == compareList
    
def doOneThreadWaits(testIndex) :
    # note, all events will be process from the other thread instead of main thread
    stopEvent = 1
    otherEvent = 2

    queue = EventQueue()
    
    itemCount = 5
    dataList = [ 0 for x in range(itemCount) ]
    threadProcessCount = 0
    
    def threadCb() :
        nonlocal threadProcessCount
        shouldStop = False
        def listener1(index) :
            nonlocal shouldStop
            shouldStop = True
        def listener2(index) :
            dataList[index] += index + 1
        queue.appendListener(stopEvent, listener1)
        queue.appendListener(otherEvent, listener2)
        while not shouldStop :
            queue.wait()
            threadProcessCount += 1
            queue.process()
    thread = threading.Thread(target = threadCb)
    
    assert threadProcessCount == 0
    
    def waitUntilQueueEmpty() :
        while queue.waitFor(0.001) :
            pass
        
    def testEnqueueOneByOne() :
        queue.enqueue(otherEvent, 1)
        waitUntilQueueEmpty()
        assert threadProcessCount == 1
        assert queue.emptyQueue()
        assert dataList == [ 0, 2, 0, 0, 0 ]

        queue.enqueue(otherEvent, 3)
        waitUntilQueueEmpty()
        assert threadProcessCount == 2
        assert queue.emptyQueue()
        assert dataList == [ 0, 2, 0, 4, 0 ]
        
    def testEnqueueTwo() :
        queue.enqueue(otherEvent, 1)
        time.sleep(0.01)
        assert threadProcessCount == 1
        assert queue.emptyQueue()

        queue.enqueue(otherEvent, 3)
        waitUntilQueueEmpty()
        assert threadProcessCount == 2
        assert dataList == [ 0, 2, 0, 4, 0 ]
        
    def testBatchingEnqueue() :
        with DisableQueueNotify(queue) :
            queue.enqueue(otherEvent, 2)
            time.sleep(0.01)
            assert(threadProcessCount == 0)
            assert not queue.emptyQueue()

            queue.enqueue(otherEvent, 4)
            time.sleep(0.01)
            assert(threadProcessCount == 0)
            assert not queue.emptyQueue()
        waitUntilQueueEmpty()
        assert threadProcessCount == 1
        assert dataList == [ 0, 0, 3, 0, 5 ]

    thread.start()

    testList = [ testEnqueueOneByOne, testEnqueueTwo, testBatchingEnqueue ]
    testList[testIndex]()

    queue.enqueue(stopEvent, 1)
    thread.join()

def test_oneThreadWaits() :
    doOneThreadWaits(0)
    doOneThreadWaits(1)
    doOneThreadWaits(2)

def test_manyThreadsWait() :
    queue = EventQueue()
    
    stopEvent = 1
    otherEvent = 2
    
    unit = 3
    itemCount = 30 * unit

    dataList = [ 0 for x in range(itemCount) ]
    shouldStop = False
    
    def listener1() :
        nonlocal shouldStop
        shouldStop = True

    def listener2(index) :
        dataList[index] += 1
        
    queue.appendListener(stopEvent, listener1)
    queue.appendListener(otherEvent, listener2)

    threadList = []
    for i in range(itemCount) :
        def cb(i = i) :
            while True :
                while not queue.waitFor(0.01) and not shouldStop :
                    pass
                if shouldStop :
                    break
                queue.process()
        threadList.append(threading.Thread(target = cb))
    
    for thread in threadList :
        thread.start()
    
    for i in range(itemCount) :
        queue.enqueue(otherEvent, i)
        time.sleep(0)
        
    for i in range(0, itemCount, unit) :
        with DisableQueueNotify(queue) :
            for k in range(unit) :
                queue.enqueue(otherEvent, i)
                time.sleep(0)
    queue.enqueue(stopEvent)
        
    for thread in threadList :
        thread.join()
        
    all = list(itertools.accumulate(dataList))[-1]
    assert all == itemCount * 2
        
