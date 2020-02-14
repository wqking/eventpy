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

from . import lockguard

class LinkedListNode :
    def __init__(self, data = None) :
        self._data = data
        self._previous = None
        self._next = None
        self._list = None
        
    def getData(self) :
        return self._data
        
    def getNext(self) :
        return self._next

# need Lock        
class LinkedList :
    def __init__(self, lock) :
        self._lock = lock
        self._head = None
        self._tail = None
        
    def getHead(self) :
        return self._head
        
    def getTail(self) :
        return self._tail
        
    def empty(self) :
        return self._head == None
    
    def append(self, node) :
        with lockguard.LockGuard(self._lock) :
            if node._list is not None :
                if node._list == self :
                    return
                node._list.remove(node)
            node._list = self

            if self._head == None :
                self._head = node
                self._tail = node
            else :
                node._previous = self._tail
                self._tail._next = node
                self._tail = node

    def prepend(self, node) :
        with lockguard.LockGuard(self._lock) :
            if node._list is not None :
                if node._list == self :
                    return
                node._list.remove(node)
            node._list = self

            if self._head == None :
                self._head = node
                self._tail = node
            else :
                node._next = self._head
                self._head._previous = node
                self._head = node

    def insert(self, node, beforeNode) :
        with lockguard.LockGuard(self._lock) :
            if node._list is not None :
                if node._list == self :
                    return
                node._list.remove(node)
            node._list = self

            node._previous = beforeNode._previous
            node._next = beforeNode
            if beforeNode._previous is not None :
                beforeNode._previous._next = node
            beforeNode._previous = node
            if beforeNode == self._head :
                self._head = node

    def remove(self, node, postProcess = None) :
        with lockguard.LockGuard(self._lock) :
            if node._list is None :
                return
            if node._list != self :
                return
            node._list = None

            if node._next is not None :
                node._next._previous = node._previous
            
            if node._previous is not None :
                node._previous._next = node._next
                
            if self._head == node :
                self._head = node._next
                
            if self._tail == node :
                self._tail = node._previous
            
            if postProcess is not None :
                postProcess(node)

