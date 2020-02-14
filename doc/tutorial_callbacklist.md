# Tutorials of CallbackList

<!--toc-->

## Tutorials

### CallbackList tutorial 1, basic

**Code**  
```python
from eventpy.callbacklist import CallbackList

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
```

**Output**  
> Got callback 1.  
> Got callback 2.  

**Remarks**  
First let's define a callback list.
```python
callbackList = CallbackList()
```
Now let's add a callback.  
```python
callbackList.append(lambda : print("Got callback 1."))
```
Function `append` takes one arguments, the *callback*.  
The *callback* can be any callback target -- functions, lambda expressions, or callable objects that defined `__call__`.   
In the tutorial, we also add another callback.  

Now let's invoke the callbackList.
```python
callbackList();
```
During the invoking, all callbacks will be invoked one by one in the order of they were added.

### CallbackList tutorial 2, callback with parameters

**Code**  
```python
# create a CallbackList
callbackList = CallbackList()
callbackList.append(lambda s, b : print("Got callback 1, s is %s b is %d" % (s, b)))
def anotherCallback(s, b) :
	print("Got callback 2, s is %s b is %d" % (s, b))
callbackList.append(anotherCallback)
# Invoke the callback list
callbackList("Hello world", True)
```

**Output**  
> Got callback 1, s is Hello world b is 1  
> Got callback 2, s is Hello world b is 1  

**Remarks**  

### CallbackList tutorial 3, remove

**Code**  
```python
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
```

**Output**  
> Got callback 1.  
> Got callback 3.  

**Remarks**  

### CallbackList tutorial 4, for each

**Code**  
```python
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
```

**Output**  
> Got callback 1.  
> Got callback 3.  

**Remarks**  
