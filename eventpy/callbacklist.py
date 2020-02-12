import eventpy.policy
import eventpy.internal.linkedlist as linkedlist
import eventpy.internal.lockguard as lockguard

import inspect

class CallbackList :
    class NodeData :
        def __init__(self, callback, counter) :
            self._callback = callback
            self._counter = counter

    def __init__(self, policy = eventpy.policy.defaultPolicy) :
        self._policy = policy.clone()
        self._lock = self._policy.lockClass()
        self._list = linkedlist.LinkedList(self._lock)
        self._currentCounter = 0

    def empty(self) :
        return self._list.empty()

    def append(self, callback) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.append(node)
        return node

    def prepend(self, callback) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.prepend(node)
        return node

    def insert(self, callback, before) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.insert(node, before)
        return node

    def remove(self, node) :
        if node is not None :
            def postProcess(n) :
                n.getData()._counter = 0
            self._list.remove(node, postProcess)
        
    def forEach(self, func) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        invoke = _selectForEachInvoke(func)
        while node is not None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                invoke(node)
            with lockguard.LockGuard(self._lock) :
                node = node._next

    def forEachIf(self, func) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        invoke = _selectForEachInvoke(func)
        while node is not None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                if not invoke(node) :
                    return False
            with lockguard.LockGuard(self._lock) :
                node = node._next
        return True
        
    def __call__(self, *args, **kwargs) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        while node is not None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                node.getData()._callback(*args, **kwargs)
            with lockguard.LockGuard(self._lock) :
                node = node._next

    def _getNextCounter(self) :
        self._currentCounter += 1
        result = self._currentCounter
        if result <= 0 : # overflow, let's reset all nodes' counters.
            with lockguard.LockGuard(self._lock) :
                node = self._list.getHead()
                while node is not None :
                    node.getData()._counter = 1
                    node = node.getNext()
            if self._currentCounter < 0 :
                self._currentCounter = 0
            self._currentCounter += 1
            result = self._currentCounter

        return result

def _selectForEachInvoke(func) :
    def _forEachInvoke1(node, func = func) :
        return func(node.getData()._callback)

    def _forEachInvoke2(node, func = func) :
        return func(node, node.getData()._callback)

    sig = inspect.signature(func)
    if len(sig.parameters) >= 2 :
        return _forEachInvoke2
    else :
        return _forEachInvoke1

