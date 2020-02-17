# Class EventDispatcher reference
<!--begintoc-->
* [Description](#a2_1)
* [API reference](#a2_2)
  * [Import](#a3_1)
  * [Member functions](#a3_2)
* [Nested listener safety](#a2_3)
* [Time complexities](#a2_4)
<!--endtoc-->

<a id="a2_1"></a>
## Description

EventDispatcher is like a dictionary of <EventType, CallbackList>.

EventDispatcher holds a map of `<EventType, CallbackList>` pairs. On dispatching, EventDispatcher finds the CallbackList of the event type, then invoke the callback list. The invocation is always synchronous. The listeners are triggered when `EventDispatcher.dispatch` is called.  

<a id="a2_2"></a>
## API reference

<a id="a3_1"></a>
### Import

import eventpy.eventdispatcher

<a id="a3_2"></a>
### Member functions

#### constructors

```python
EventDispatcher(policy = eventpy.policy.defaultPolicy)
```

`policy`: the policy to configure and extend the event dispatcher. The default value is `eventpy.policy.defaultPolicy`. See [document of policies](policies.md) for details.  

#### appendListener

```python
appendListener(event, callback)
```  
Add the *callback* to the dispatcher to listen to *event*.  
The listener is added to the end of the listener list.  
Return a handle which represents the listener. The handle can be used to remove this listener or insert other listener before this listener.  
If `appendListener` is called in another listener during a dispatching, the new listener is guaranteed not triggered during the same dispatching.  
If the same callback is added twice, it results duplicated listeners.  
The time complexity is O(1).

#### prependListener

```python
prependListener(event, callback)
```  
Add the *callback* to the dispatcher to listen to *event*.  
The listener is added to the beginning of the listener list.  
Return a handle which represents the listener. The handle can be used to remove this listener or insert other listener before this listener.  
If `prependListener` is called in another listener during a dispatching, the new listener is guaranteed not triggered during the same dispatching.  
The time complexity is O(1).

#### insertListener

```python
insertListener(event, callback, before)
```  
Insert the *callback* to the dispatcher to listen to *event* before the listener handle *before*. If *before* is not found, *callback* is added at the end of the listener list.  
Return a handle which represents the listener. The handle can be used to remove this listener or insert other listener before this listener.  
If `insertListener` is called in another listener during a dispatching, the new listener is guaranteed not triggered during the same dispatching.  
The time complexity is O(1).  

#### removeListener

```python
removeListener(event, handle)
```  
Remove the listener *handle* which listens to *event* from the dispatcher.  
Return true if the listener is removed successfully, false if the listener is not found.  
The time complexity is O(1).  

#### forEach

```python
forEach(event, func);
```  
Apply `func` to all listeners of `event`.  
The `func` can be one of the two prototypes:  
```python
func(handle, callback)
func(callback)
```
`handle` is the handle returned by `appendListener`, `prependListener`, or `insertListener`.  
`callback` is the callback added in the event dispatcher.
**Note**: the `func` can remove any listeners, or add other listeners, safely.

#### forEachIf

```python
forEachIf(event, func)
```  
Apply `func` to all listeners of `event`. `func` must return a boolean value, and if the return value is false, forEachIf stops the looping immediately.  
Return `true` if all listeners are invoked, or `event` is not found, `false` if `func` returns `false`.
`func` has the same prototype as in `forEach`.

#### dispatch

```python
dispatch(event, *args, **kwargs);  
```  
Dispatch an event. The event type is deducted from the arguments of `dispatch`, usually the first argument is the event.   
The listeners are called with arguments `args` and `kwargs`.  
The function is synchronous. The listeners are called in the thread same as the caller of `dispatch`.

<a id="a2_3"></a>
## Nested listener safety
1. If a listener adds another listener of the same event to the dispatcher during a dispatching, the new listener is guaranteed not to be triggered within the same dispatching. This is guaranteed by an integer counter. This rule will be broken is the counter is overflowed to zero in a dispatching, but this rule will continue working on the subsequence dispatching.  
2. Any listeners that are removed during a dispatching are guaranteed not triggered.  
3. All above points are not true in multiple threading. That's to say, if one thread is invoking a callback list, the other thread add or remove a callback, the added or removed callback may be triggered during the invoking.

<a id="a2_4"></a>
## Time complexities
The time complexities being discussed here is about when operating on the listener in the underlying list, and `n` is the number of listeners. It doesn't include the event searching in the underlying `std::map` which is always O(log n).
- `appendListener`: O(1)
- `prependListener`: O(1)
- `insertListener`: O(1)
- `removeListener`: O(1)
- `enqueue`: O(1)

