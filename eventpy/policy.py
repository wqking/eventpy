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

