class LockGuard :
    def __init__(self, lock) :
        self._lock = lock

    def __enter__(self) :
        self.lock()
        return self

    def __exit__(self, type, value, traceBack) :
        self.unlock()
	
    def lock(self) :
        self._lock.acquire()

    def unlock(self) :
        self._lock.release()
		
class NullLocker :
    def __init__(self, lock = None) :
        pass

    def __enter__(self) :
        return self

    def __exit__(self, type, value, traceBack) :
        pass
	
