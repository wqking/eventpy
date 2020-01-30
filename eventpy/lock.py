import threading

Lock = threading.RLock
		
class NullLock :
    def acquire(self, blocking = 1) :
        return self

    def release(self) :
        pass
	
