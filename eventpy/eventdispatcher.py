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
import eventpy.callbacklist as callbacklist
import eventpy.internal.lockguard as lockguard

class EventDispatcher :
    def __init__(self, policy = eventpy.policy.defaultPolicy) :
        self._policy = policy.clone()
        self._eventCallbackListMapLock = self._policy.lockClass()
        self._eventCallbackListMap = {}
        if self._policy.argumentPassingMode == eventpy.policy.argumentPassingExcludeEvent :
            self.dispatch = self._dispatchExcludeEvent
        else :
            self.dispatch = self._dispatchIncludeEvent
        
    def appendListener(self, event, callback) :
        return self._getCallbackList(event).append(callback)

    def prependListener(self, event, callback) :
        return self._getCallbackList(event).prepend(callback)

    def insertListener(self, event, callback, beforeHandle) :
        return self._getCallbackList(event).insert(callback, beforeHandle)
        
    def removeListener(self, event, handle) :
        callableList = self._doFindCallableList(event)
        if callableList is not None :
            return callableList.remove(handle)
        return False
        
    def forEach(self, event, func) :
        callableList = self._doFindCallableList(event)
        if callableList is not None :
            return callableList.forEach(func)

    def forEachIf(self, event, func) :
        callableList = self._doFindCallableList(event)
        if callableList is not None :
            return callableList.forEachIf(func)
        return True

	# Bypass any getEvent policy. The first argument is the event type.
	# Most used for internal purpose.
    def directDispatch(self, event, *args, **kwargs) :
        callableList = self._doFindCallableList(event)
        if callableList is not None :
            callableList(*args, **kwargs)

    def _dispatchIncludeEvent(self, *args, **kwargs) :
        event = self._policy.getEvent(*args, **kwargs)
        self.directDispatch(event, *args, **kwargs)

    def _dispatchExcludeEvent(self, e, *args, **kwargs) :
        event = self._policy.getEvent(e, *args, **kwargs)
        self.directDispatch(event, *args, **kwargs)

    def _getCallbackList(self, event) :
        with lockguard.LockGuard(self._eventCallbackListMapLock) :
            if event not in self._eventCallbackListMap :
                self._eventCallbackListMap[event] = callbacklist.CallbackList(self._policy)
            return self._eventCallbackListMap[event]
    
    def _doFindCallableList(self, event) :
        with lockguard.LockGuard(self._eventCallbackListMapLock) :
            if event in self._eventCallbackListMap :
                return self._eventCallbackListMap[event]
        return None
