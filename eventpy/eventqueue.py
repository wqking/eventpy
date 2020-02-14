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

import eventpy.policy
import eventpy.lock as lock
import eventpy.eventdispatcher as eventdispatcher
import eventpy.internal.lockguard as lockguard

import time

class DisableQueueNotify :
    def __init__(self, queue) :
        self._queue = queue

    def __enter__(self) :
        self._queue._queueNotifyCounter += 1
        return self

    def __exit__(self, type, value, traceBack) :
        self._queue._queueNotifyCounter -= 1
        if self._queue._doCanNotifyQueueAvailable() and not self._queue.emptyQueue() :
            with lockguard.LockGuard(self._queue._queueListMutex) :
                self._queue._queueListConditionVariable.notify();

class QueuedEvent :
    def __init__(self, event, args, kwargs) :
        self.event = event
        self.args = args
        self.kwargs = kwargs

class EventQueue(eventdispatcher.EventDispatcher) :
    def __init__(self, policy = eventpy.policy.defaultPolicy) :
        super().__init__(policy)
        
        self._policy = policy.clone()
        self._queueListLock = self._policy.lockClass()
        self._queueNotifyCounter = 0
        self._queueEmptyCounter = 0
        self._queueList = []
        self._queueListMutex = self._policy.lockClass()
        self._queueListConditionVariable = self._policy.conditionClass(self._queueListMutex)

    def enqueue(self, *args, **kwargs) :
        event = self._policy.getEvent(*args, **kwargs)
        if self._policy.argumentPassingMode == eventpy.policy.argumentPassingExcludeEvent :
            args = args[1:]
        queuedEvent = QueuedEvent(event, args, kwargs)
        with lockguard.LockGuard(self._queueListLock) :
            self._queueList.append(queuedEvent)
        if self._doCanProcess() :
            with lockguard.LockGuard(self._queueListMutex) :
                self._queueListConditionVariable.notify()

    def emptyQueue(self) :
        return (not self._queueList) and (self._queueEmptyCounter == 0)

    def clearEvents(self) :
        with lockguard.LockGuard(self._queueListLock) :
            self._queueList = []
            
    def process(self) :
        if self._queueList :
            with lockguard.LockGuard(self._queueListLock) :
                tempList = self._queueList
                self._queueList = []
            if tempList :
                for queuedEvent in tempList :
                    self.directDispatch(queuedEvent.event, *queuedEvent.args, **queuedEvent.kwargs)
                return True
        return False
        
    def processOne(self) :
        if self._queueList :
            queuedEvent = None
            with lockguard.LockGuard(self._queueListLock) :
                if self._queueList :
                    queuedEvent = self._queueList[0]
                    self._queueList = self._queueList[1:]
            if queuedEvent is not None :
                self.directDispatch(queuedEvent.event, *queuedEvent.args, **queuedEvent.kwargs)
                return True
        return False

    def processIf(self, func) :
        if self._queueList :
            with lockguard.LockGuard(self._queueListLock) :
                tempList = self._queueList
                self._queueList = []
            if tempList :
                for queuedEvent in tempList :
                    if func(*queuedEvent.args, **queuedEvent.kwargs) :
                        self.directDispatch(queuedEvent.event, *queuedEvent.args, **queuedEvent.kwargs)
                    else :
                        self._queueList.append(queuedEvent)
                return True
        return False
        
    def wait(self) :
        with lockguard.LockGuard(self._queueListMutex) :
            while True :
                self._queueListConditionVariable.wait(0.001)
                if self._doCanProcess() :
                    break
        
    def waitFor(self, seconds) :
        with lockguard.LockGuard(self._queueListMutex) :
            startSeconds = time.time()
            while True :
                self._queueListConditionVariable.wait(0.001)
                if self._doCanProcess() :
                    return True
                if time.time() - startSeconds >= seconds :
                    return False
                    
    def dispatchEvent(self, queuedEvent) :
        self.directDispatch(queuedEvent.event, *queuedEvent.args, **queuedEvent.kwargs)
        
    def peekEvent(self) :
        if self._queueList :
            with lockguard.LockGuard(self._queueListLock) :
                if self._queueList :
                    return self._queueList[0]
        return None
        
    def takeEvent(self) :
        if self._queueList :
            with lockguard.LockGuard(self._queueListLock) :
                if self._queueList :
                    queuedEvent = self._queueList[0]
                    self._queueList = self._queueList[1:]
                    return queuedEvent
        return None
        
    def _doCanProcess(self) :
        return not self.emptyQueue() and self._doCanNotifyQueueAvailable()
        
    def _doCanNotifyQueueAvailable(self) :
        return self._queueNotifyCounter == 0

