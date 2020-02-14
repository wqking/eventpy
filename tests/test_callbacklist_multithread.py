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

import threading
import random

def test_append() :
    threadCount = 64
    taskCountPerThread = 1024
    itemCount = threadCount * taskCountPerThread

    callbackList = CallbackList()
    dataList = [ 0 for x in range(itemCount) ]
    taskList = []
    for i in range(itemCount) :
        def cb(i = i) :
            dataList[i] = i
        taskList.append(cb)
    random.shuffle(taskList)
    
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * taskCountPerThread, (i + 1) * taskCountPerThread) :
                callbackList.append(taskList[k])
        threadList.append(threading.Thread(target = cb))
    
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()
        
    taskList = []
    callbackList()
    
    dataList.sort()
    compareList = [ x for x in range(itemCount) ]
    assert dataList == compareList

def test_remove() :
    threadCount = 64
    taskCountPerThread = 1024
    itemCount = threadCount * taskCountPerThread

    callbackList = CallbackList()
    dataList = [ 0 for x in range(itemCount) ]
    taskList = []
    for i in range(itemCount) :
        def cb(i = i) :
            dataList[i] = i
        taskList.append(cb)
    random.shuffle(taskList)
    
    handleList = []
    for item in taskList :
        handleList.append(callbackList.append(item))
    
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * taskCountPerThread, (i + 1) * taskCountPerThread) :
                callbackList.remove(handleList[k])
        threadList.append(threading.Thread(target = cb))

    assert not callbackList.empty()
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()

    assert callbackList.empty()

def test_doubleRemove() :
    threadCount = 64
    taskCountPerThread = 1024
    itemCount = threadCount * taskCountPerThread

    callbackList = CallbackList()
    dataList = [ 0 for x in range(itemCount) ]
    taskList = []
    for i in range(itemCount) :
        def cb(i = i) :
            dataList[i] = i
        taskList.append(cb)
    random.shuffle(taskList)
    
    handleList = []
    for item in taskList :
        handleList.append(callbackList.append(item))
    
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            start = i
            end = i + 1
            if i > 0 :
                start -= 1
            elif i < threadCount - 1 :
                end += 1
            for k in range(start * taskCountPerThread, end * taskCountPerThread) :
                callbackList.remove(handleList[k])
        threadList.append(threading.Thread(target = cb))

    assert not callbackList.empty()
    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()

    assert callbackList.empty()

def test_appendDoubleRemove() :
    threadCount = 64
    taskCountPerThread = 1024
    itemCount = threadCount * taskCountPerThread

    callbackList = CallbackList()
    dataList = [ 0 for x in range(itemCount) ]
    taskList = []
    for i in range(itemCount) :
        def cb(i = i) :
            dataList[i] = i
        taskList.append(cb)
    random.shuffle(taskList)
    
    handleList = [ None for x in range(itemCount) ]
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            for k in range(i * taskCountPerThread, (i + 1) * taskCountPerThread) :
                handleList[k] = callbackList.append(taskList[k])
            start = i
            end = i + 1
            if i > 0 :
                start -= 1
            elif i < threadCount - 1 :
                end += 1
            for k in range(start * taskCountPerThread, end * taskCountPerThread) :
                callbackList.remove(handleList[k])
        threadList.append(threading.Thread(target = cb))

    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()

    assert callbackList.empty()

def test_insert() :
    threadCount = 64
    taskCountPerThread = 1024
    itemCount = threadCount * taskCountPerThread

    callbackList = CallbackList()
    dataList = [ 0 for x in range(itemCount) ]
    taskList = []
    for i in range(itemCount) :
        def cb(i = i) :
            dataList[i] = i
        cb.testData = i
        taskList.append(cb)
    random.shuffle(taskList)
    
    handleList = [ None for x in range(itemCount) ]
    threadList = []
    for i in range(threadCount) :
        def cb(i = i) :
            k = i * taskCountPerThread
            for k in range(k, i * taskCountPerThread + taskCountPerThread // 2) :
                handleList[k] = callbackList.append(taskList[k])
            offset = 0
            for k in range(k + 1, i * taskCountPerThread + taskCountPerThread // 2 + taskCountPerThread // 4) :
                handleList[k] = callbackList.insert(taskList[k], handleList[offset])
                offset += 1
            for k in range(k + 1, (i + 1) * taskCountPerThread) :
                handleList[k] = callbackList.insert(taskList[k], handleList[offset])
                offset += 1
        threadList.append(threading.Thread(target = cb))

    for thread in threadList :
        thread.start()
    for thread in threadList :
        thread.join()

    callbackList()
    dataList.sort()
    compareList = [ x for x in range(itemCount) ]
    assert dataList == compareList

