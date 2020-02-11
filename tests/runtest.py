import sys
sys.path.append('../')

from internal import test_linkedlist
import test_callbacklist_basic
import test_callbacklist_multithread
import test_eventdispatcher_basic
import test_eventdispatcher_multithread
import test_eventqueue_basic
import test_eventqueue_multithread

def doTest() :
    test_linkedlist.test_empty()
    test_linkedlist.test_append()
    test_linkedlist.test_prepend()
    test_linkedlist.test_insert()

    test_callbacklist_basic.test_noParams()
    test_callbacklist_basic.test_hasParams()
    test_callbacklist_basic.test_forEach()
    test_callbacklist_basic.test_forEachIf()
    test_callbacklist_basic.test_nestedCallbacks_newCallbacksShouldNotBeTriggered()
    test_callbacklist_basic.test_removeInsideCallback()
    
    test_callbacklist_multithread.test_append()
    test_callbacklist_multithread.test_remove()
    test_callbacklist_multithread.test_doubleRemove()
    test_callbacklist_multithread.test_appendDoubleRemove()
    test_callbacklist_multithread.test_insert()

    test_eventdispatcher_basic.test_noParams1()
    test_eventdispatcher_basic.test_noParams2()
    test_eventdispatcher_basic.test_noParams3()
    test_eventdispatcher_basic.test_hasParams()
    test_eventdispatcher_basic.test_hasParams_includeEvent()
    test_eventdispatcher_basic.test_forEach()
    test_eventdispatcher_basic.test_forEachIf()
    
    test_eventdispatcher_multithread.test_multiThreading()
    
    test_eventqueue_basic.test_noParams1()
    test_eventqueue_basic.test_hasParams()
    test_eventqueue_basic.test_processOne()
    test_eventqueue_basic.test_customizedEvent()
    test_eventqueue_basic.test_clearEvents()
    test_eventqueue_basic.test_processIf()
    
    test_eventqueue_multithread.test_multiThreading()
    test_eventqueue_multithread.test_oneThreadWaits()
    test_eventqueue_multithread.test_manyThreadsWait()

if __name__ == "__main__":
    doTest()
    