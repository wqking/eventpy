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

import threading

argumentPassingIncludeEvent = 0
argumentPassingExcludeEvent = 1

Lock = threading.RLock
		
class NullLock :
    def acquire(self, blocking = 1) :
        return self

    def release(self) :
        pass
	
Condition = threading.Condition
		
class NullCondition :
    def __init__(self, lock) :
        pass

    def acquire(self, *args) :
        return self

    def release(self) :
        pass
	
    def wait(self, timeout = 0) :
        pass
        
    def notify(self, n = 1) :
        pass

    def notify_all(self) :
        pass
        
    def notifyAll(self) :
        pass

class Threading :
    def __init__(
        self,
        lockClass = Lock,
        conditionClass = Condition
    ) :
        self.lockClass = lockClass
        self.conditionClass = conditionClass

multipleThreading = Threading(
        lockClass = Lock,
        conditionClass = Condition
    )

singleThreading = Threading(
        lockClass = NullLock,
        conditionClass = NullCondition
    )

def getEvent(*args, **kwargs) :
    return args[0]

def canContinueInvoking(*args, **kwargs) :
    return True

class Policy :
    def __init__(
        self,
        threading = multipleThreading,
        getEvent = getEvent,
        canContinueInvoking = canContinueInvoking,
        argumentPassingMode = argumentPassingExcludeEvent
    ) :
        self.threading = threading
        self.lockClass = threading.lockClass
        self.conditionClass = threading.conditionClass
        self.getEvent = getEvent
        self.canContinueInvoking = canContinueInvoking
        self.argumentPassingMode = argumentPassingMode
        
    def clone(self) :
        return Policy(
            threading = self.threading,
            getEvent = self.getEvent,
            canContinueInvoking = self.canContinueInvoking,
            argumentPassingMode = self.argumentPassingMode
        )

defaultPolicy = Policy()
singleThreadPolicy = Policy(threading = singleThreading)

