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

