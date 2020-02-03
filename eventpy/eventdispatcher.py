import eventpy.lock as lock
import eventpy.callbacklist as callbacklist
import eventpy.internal.lockguard as lockguard

class EventDispatcher :
    def __init__(self, lockClass = lock.Lock) :
        self._lockClass = lockClass
        self._lock = self._lockClass()
        self._eventCallbackListMap = {}
        
    def appendListener(self, event, callback) :
        return self._getCallbackList(event).append(callback)

    def prependListener(self, event, callback) :
        return self._getCallbackList(event).prepend(callback)

    def insertListener(self, event, callback, beforeHandle) :
        return self._getCallbackList(event).insert(callback, beforeHandle)
        
    def removeListener(self, event, handle) :
        callableList = self._doFindCallableList(event)
        if callableList != None :
            return callableList.remove(handle)
        return False
        
    def forEach(self, event, func) :
        callableList = self._doFindCallableList(event)
        if callableList != None :
            return callableList.forEach(func)

    def forEachIf(self, event, func) :
        callableList = self._doFindCallableList(event)
        if callableList != None :
            return callableList.forEachIf(func)
        return True
        
    def dispatch(self, event, *args, **kwargs) :
        callableList = self._doFindCallableList(event)
        if callableList != None :
            callableList(*args, **kwargs)

    def _getCallbackList(self, event) :
        with lockguard.LockGuard(self._lock) :
            if event not in self._eventCallbackListMap :
                self._eventCallbackListMap[event] = callbacklist.CallbackList(self._lockClass)
            return self._eventCallbackListMap[event]
    
    def _doFindCallableList(self, event) :
        with lockguard.LockGuard(self._lock) :
            if event in self._eventCallbackListMap :
                return self._eventCallbackListMap[event]
        return None
