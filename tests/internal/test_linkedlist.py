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

import eventpy.internal.linkedlist as linkedlist
import eventpy.lock as lock

def getAllData(linkedList) :
    result = []
    node = linkedList.getHead()
    while node != None :
        result.append(node.getData())
        node = node._next
    return result

def test_empty() :
    linkedList = linkedlist.LinkedList(lock.Lock())
    assert linkedList.getHead() is None
    assert linkedList.getTail() is None
    
def test_append() :
    linkedList = linkedlist.LinkedList(lock.Lock())

    linkedList.append(linkedlist.LinkedListNode(1))
    assert linkedList.getHead() == linkedList.getTail()
    assert getAllData(linkedList) == [ 1 ]

    linkedList.append(linkedlist.LinkedListNode(2))
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 1, 2 ]
    assert linkedList.getHead()._next == linkedList.getTail()

    linkedList.append(linkedlist.LinkedListNode(3))
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 1, 2, 3 ]
    assert linkedList.getHead()._next._next == linkedList.getTail()

def test_prepend() :
    linkedList = linkedlist.LinkedList(lock.NullLock())

    linkedList.prepend(linkedlist.LinkedListNode(1))
    assert linkedList.getHead() == linkedList.getTail()
    assert getAllData(linkedList) == [ 1 ]

    linkedList.prepend(linkedlist.LinkedListNode(2))
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 2, 1 ]
    assert linkedList.getHead()._next == linkedList.getTail()

    linkedList.prepend(linkedlist.LinkedListNode(3))
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 3, 2, 1 ]
    assert linkedList.getHead()._next._next == linkedList.getTail()

def test_insert() :
    linkedList = linkedlist.LinkedList(lock.NullLock())

    linkedList.append(linkedlist.LinkedListNode(1))
    assert linkedList.getHead() == linkedList.getTail()
    assert getAllData(linkedList) == [ 1 ]

    linkedList.insert(linkedlist.LinkedListNode(2), linkedList.getHead())
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 2, 1 ]
    assert linkedList.getHead()._next == linkedList.getTail()

    linkedList.insert(linkedlist.LinkedListNode(3), linkedList.getHead()._next)
    assert linkedList.getHead() != linkedList.getTail()
    assert getAllData(linkedList) == [ 2, 3, 1 ]
    assert linkedList.getHead()._next._next == linkedList.getTail()

