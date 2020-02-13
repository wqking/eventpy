from eventpy.callbacklist import CallbackList
import eventpy.policy as policy

def test_tutorial_1_basic() :
    print("CallbackList tutorial 1, basic")
    # create a CallbackList
    callbackList = CallbackList()
    # Add a callback.
    # Lambda is not required, any function or callable object is fine
    callbackList.append(lambda : print("Got callback 1."))
    def anotherCallback() :
        print("Got callback 2.")
    callbackList.append(anotherCallback)
    # Invoke the callback list
    callbackList()

def test_tutorial_2_callbackWithParameters() :
    print("CallbackList tutorial 2, callback with parameters")
    # create a CallbackList
    callbackList = CallbackList()
    callbackList.append(lambda s, b : print("Got callback 1, s is %s b is %d" % (s, b)))
    def anotherCallback(s, b) :
        print("Got callback 2, s is %s b is %d" % (s, b))
    callbackList.append(anotherCallback)
    # Invoke the callback list
    callbackList("Hello world", True)

def test_tutorial_3_remove() :
    print("CallbackList tutorial 3, remove")
    # create a CallbackList
    callbackList = CallbackList()
    
    # Add some callbacks.
    callbackList.append(lambda : print("Got callback 1."))
    handle2 = callbackList.append(lambda : print("Got callback 2."))
    callbackList.append(lambda : print("Got callback 3."))
    
    callbackList.remove(handle2)
    
    # Invoke the callback list
    # The "Got callback 2" callback should not be triggered.
    callbackList()

def test_tutorial_4_forEach() :
    print("CallbackList tutorial 4, forEach")
    # create a CallbackList
    callbackList = CallbackList()
    
    # Add some callbacks.
    callbackList.append(lambda : print("Got callback 1."))
    callbackList.append(lambda : print("Got callback 2."))
    callbackList.append(lambda : print("Got callback 3."))
    
    # Now call forEach to remove the second callback
    # The forEach callback prototype is func(handle, callback)
    index = 0
    def func(handle, callback) :
        nonlocal index
        print("forEach(Handle, Callback), invoked ", index)
        if index == 1 :
            callbackList.remove(handle)
            print("forEach(Handle, Callback), removed second callback")
        index += 1
    callbackList.forEach(func)

    # The forEach callback prototype can also be func(callback)
    callbackList.forEach(lambda callback : print("forEach(Callback), invoked"))

    # Invoke the callback list
    # The "Got callback 2" callback should not be triggered.
    callbackList()
