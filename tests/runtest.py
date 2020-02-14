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

import sys
sys.path.append('../')

from internal import test_linkedlist
import tutorial_callbacklist
import tutorial_eventdispatcher
import tutorial_eventqueue
import test_callbacklist_basic
import test_callbacklist_multithread
import test_eventdispatcher_basic
import test_eventdispatcher_multithread
import test_eventqueue_basic
import test_eventqueue_multithread

def doTest() :
    tutorial_callbacklist.test_tutorial_1_basic()
    tutorial_callbacklist.test_tutorial_2_callbackWithParameters()
    tutorial_callbacklist.test_tutorial_3_remove()
    tutorial_callbacklist.test_tutorial_4_forEach()
    
    tutorial_eventdispatcher.test_tutorial_1_basic()
    tutorial_eventdispatcher.test_tutorial_2_listenerWithParameters()
    tutorial_eventdispatcher.test_tutorial_3_customizedEventClass()
    tutorial_eventdispatcher.test_tutorial_4_eventCanceling()
    
    tutorial_eventqueue.test_tutorial_1_basic()
    tutorial_eventqueue.test_tutorial_2_multipleThreading()

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
    