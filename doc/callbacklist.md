# Class CallbackList reference

<a id="a2_1"></a>
## Description

CallbackList is the fundamental class in eventpy. The other classes EventDispatcher and EventQueue are built on CallbackList.  

CallbackList holds a list of callbacks. At the time of the call, CallbackList simply invokes each callback one by one. Consider CallbackList as the signal/slot system in Qt, or the callback function pointer in some Windows APIs (such as lpCompletionRoutine in `ReadFileEx`).  
The *callback* can be any callback target -- functions, member functions (methods), lambda, and any object defined `__call__`.  

<a id="a2_2"></a>
## API reference

<a id="a3_1"></a>
### Import

import eventpy.callbacklist

<a id="a3_4"></a>
### Member methods

#### constructor

```python
CallbackList(policy = eventpy.policy.defaultPolicy)
```

`policy`: the policy to configure and extend the callback list. The default value is `eventpy.policy.defaultPolicy`. See [document of policies](policies.md) for details.  

#### empty

```python
empty()
```
Return true if the callback list is empty.  
Note: in multi threading, this function returning true doesn't guarantee that the list is empty. The list may immediately become non-empty after the function returns true.

#### append

```python
append(callback)
```  
Add the *callback* to the callback list.  
The callback is added to the end of the callback list.  
Return a handle that represents the callback. The handle can be used to remove this callback or to insert additional callbacks before this callback.  
If `append` is called in another callback during the invoking of the callback list, the new callback is guaranteed not to be triggered during the same callback list invoking.  
The time complexity is O(1).

#### prepend

```python
prepend(callback)
```  
Add the *callback* to the callback list.  
The callback is added to the beginning of the callback list.  
Return a handle that represents the callback. The handle can be used to remove this callback or to insert additional callbacks before this callback.  
If `prepend` is called in another callback during the invoking of the callback list, the new callback is guaranteed not to be triggered during the same callback list invoking.  
The time complexity is O(1).

#### insert

```python
insert(callback, before)
```  
Insert the *callback* to the callback list before the callback handle *before*. If *before* is not found, *callback* is added at the end of the callback list.  
Return a handle that represents the callback. The handle can be used to remove this callback or to insert additional callbacks before this callback.  
If `insert` is called in another callback during the invoking of the callback list, the new callback is guaranteed not to be triggered during the same callback list invoking.  
The time complexity is O(1).  

#### remove
```python
remove(handle)
```  
Remove the callback *handle* from the callback list.  
Return true if the callback is removed successfully, false if the callback is not found.  
The time complexity is O(1).  

#### forEach
```python
forEach(func)
```  
Apply `func` to all callbacks.  
The `func` can be one of the two prototypes:  
```python
func(handle, callback)
func(callback)
```
`handle` is the handle returned by `append`, `prepend`, or `insert`.  
`callback` is the callback added in the callback list.

**Note**: the `func` can remove any callbacks, or add other callbacks, safely.

#### forEachIf

```python
forEachIf(func)
```  
Apply `func` to all callbacks. `func` must return a boolean value, and if the return value is false, forEachIf stops the looping immediately.  
Return `true` if all callbacks are invoked, or `event` is not found, `false` if `func` returns `false`.
`func` has the same prototype as in `forEach`.

#### invoking operator

```python
__call__(*args, **kwargs) const;
```  
Invoke each callbacks in the callback list.  
The callbacks are called with arguments `args` and `kwargs`.  
The callbacks are called in the thread same as the callee.

<a id="a2_3"></a>
## Nested callback safety
1. If a callback adds another callback to the callback list during a invoking, the new callback is guaranteed not to be triggered within the same invoking. This is guaranteed by an integer counter. This rule will be broken is the counter is overflowed to zero in a invoking, but this rule will continue working on the subsequence invoking.  
2. Any callbacks that are removed during a invoking are guaranteed not triggered.  
3. All above points are not true in multiple threading. That's to say, if one thread is invoking a callback list, the other thread add or remove a callback, the added or removed callback may be called during the invoking.


<a id="a2_4"></a>
## Time complexities
- `append`: O(1)
- `prepend`: O(1)
- `insert`: O(1)
- `remove`: O(1)

