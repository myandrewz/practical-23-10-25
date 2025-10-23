# ZeroEvenOdd Threading Solution

A Python implementation of a multi-threaded synchronization problem where three threads print numbers in a specific pattern: `010203040506...`

## 🎯 Problem Statement

You have the function `printNumber` that can be called with an integer parameter and prints it to the console.

- Thread A calls `zero()` which should output only zeros  
- Thread B calls `even()` which should output only even numbers  
- Thread C calls `odd()` which should output only odd numbers  

Each thread has access to the same instance of `ZeroEvenOdd`. The threads should print the numbers in order: `0102030405...`

### Example:
- **Input**: `n = 5`
- **Output**: `0102030405`
- **Pattern**: Zero, One, Zero, Two, Zero, Three, Zero, Four, Zero, Five

## 🚀 Features

- **Thread Synchronization**: Uses semaphores for precise thread coordination
- **Race Condition Prevention**: Ensures correct ordering without race conditions
- **Scalable Design**: Works with any positive integer `n`
- **Type Hints**: Full type annotation support
- **Comprehensive Testing**: Multiple test cases with verification
- **Clean API**: Simple interface following the problem specification

## 📋 Requirements

- Python 3.6+ (for type hints)
- No external dependencies (uses only built-in `threading` module)

## 🛠️ Installation & Usage

### 1. Navigate to the Directory

```bash
cd qn2
```

### 2. Run the Solution

```bash
python ZeroEvenOdd.py
```

### 3. Using as a Module

```python
from ZeroEvenOdd import ZeroEvenOdd
import threading

def print_number(x):
    print(x, end='')

# Create instance
zeo = ZeroEvenOdd(5)

# Create threads
thread_zero = threading.Thread(target=zeo.zero, args=(print_number,))
thread_even = threading.Thread(target=zeo.even, args=(print_number,))
thread_odd = threading.Thread(target=zeo.odd, args=(print_number,))

# Start threads
thread_zero.start()
thread_even.start()
thread_odd.start()

# Wait for completion
thread_zero.join()
thread_even.join()
thread_odd.join()
```

## 🔧 Class and Methods

### `ZeroEvenOdd(n: int)`
**Main class for thread synchronization**

#### Parameters:
- `n` (int): The upper limit for numbers to print (1 to n)

#### Methods:

##### `zero(print_number: Callable[[int], None]) -> None`
- **Purpose**: Prints zeros in the sequence
- **Thread**: Should be called by Thread A
- **Behavior**: Prints `0` before each number in the sequence
- **Parameters**: `print_number` - Function that prints the given number

##### `even(print_number: Callable[[int], None]) -> None`
- **Purpose**: Prints even numbers in the sequence
- **Thread**: Should be called by Thread B  
- **Behavior**: Prints even numbers (2, 4, 6, ...)
- **Parameters**: `print_number` - Function that prints the given number

##### `odd(print_number: Callable[[int], None]) -> None`
- **Purpose**: Prints odd numbers in the sequence
- **Thread**: Should be called by Thread C
- **Behavior**: Prints odd numbers (1, 3, 5, ...)
- **Parameters**: `print_number` - Function that prints the given number

## 📊 Algorithm Explanation

### Synchronization Strategy

The solution uses **semaphores** to coordinate three threads:

```python
self.zero_sem = threading.Semaphore(1)  # Zero starts first
self.even_sem = threading.Semaphore(0)  # Even waits
self.odd_sem = threading.Semaphore(0)   # Odd waits
```

### Execution Flow:

1. **Zero Thread**: 
   - Starts first (semaphore initialized to 1)
   - Prints `0`
   - Determines next thread based on current number (odd/even)
   - Releases appropriate semaphore

2. **Odd/Even Threads**:
   - Wait for their respective semaphores
   - Print their number
   - Increment current counter
   - Release zero semaphore for next iteration

### Key Synchronization Points:

```python
# Zero thread logic
self.zero_sem.acquire()  # Wait for turn
print_number(0)          # Print zero
if self.current % 2 == 1:
    self.odd_sem.release()   # Next is odd
else:
    self.even_sem.release()  # Next is even

# Odd/Even thread logic  
self.odd_sem.acquire()       # Wait for turn
print_number(self.current)   # Print number
self.current += 1            # Move to next
self.zero_sem.release()      # Give turn back to zero
```

## 🧪 Test Cases

The solution includes comprehensive test cases:

| Test Case | n | Expected Output | Description |
|-----------|---|-----------------|-------------|
| Basic | 5 | `0102030405` | Standard example |
| Small | 3 | `010203` | Minimal case |
| Medium | 7 | `01020304050607` | Medium complexity |
| Larger | 10 | `0102030405060708091010` | Larger sequence |

### Running Tests

```bash
python ZeroEvenOdd.py
```

**Expected Output:**
```
==================================================
ZERO EVEN ODD THREADING TEST
==================================================
Testing ZeroEvenOdd with n=5
Expected output: 0102030405
Actual output:   0102030405
Output as list: ['0', '1', '0', '2', '0', '3', '0', '4', '0', '5']
Test PASSED!

==================================================
Testing with different values of n
==================================================

Testing with n=3:
Output: 010203

Testing with n=7:
Output: 01020304050607

Testing with n=10:
Output: 0102030405060708091010
```

## ⚡ Performance Analysis

### Time Complexity
- **Per Thread**: O(n) - each thread processes at most n/2 + 1 numbers
- **Total Operations**: O(n) - 2n total prints (n zeros + n numbers)

### Space Complexity
- **Memory Usage**: O(1) - constant space for semaphores and counters
- **Thread Stack**: O(1) per thread - no recursive calls

### Synchronization Overhead
- **Semaphore Operations**: Each print requires 1 acquire + 1 release
- **Context Switching**: Minimal due to efficient semaphore implementation
- **Deadlock Prevention**: Careful semaphore ordering prevents deadlocks

## 🔒 Threading Concepts Demonstrated

### 1. **Semaphores**
- **Purpose**: Control access to shared resources
- **Advantage**: More flexible than locks for this use case
- **Implementation**: `threading.Semaphore(initial_value)`

### 2. **Thread Coordination**
- **Pattern**: Producer-consumer with multiple producers
- **Synchronization**: Turn-based execution using semaphores
- **Order Guarantee**: Ensures deterministic output sequence

### 3. **Race Condition Prevention**
- **Problem**: Multiple threads accessing shared state
- **Solution**: Semaphores ensure atomic operations
- **Result**: Predictable, correct output every time

## 🔍 Design Decisions

### Why Semaphores Over Locks?
1. **Turn-based Access**: Semaphores naturally model turn-taking
2. **Multiple States**: Need to coordinate 3 different thread states
3. **Flexibility**: Easy to signal specific threads
4. **No Busy Waiting**: Threads block efficiently until their turn

### Why Track Current Number?
1. **Odd/Even Decision**: Zero thread needs to know which number is next
2. **Increment Logic**: Odd/even threads increment after printing
3. **State Management**: Clean separation of concerns

### Thread Safety Considerations:
- **Atomic Operations**: Each semaphore operation is atomic
- **No Shared Variables**: Only `current` is shared, protected by semaphores
- **Deterministic Order**: Semaphore ordering guarantees correct sequence

## 🚨 Common Pitfalls Avoided

### 1. **Deadlock Prevention**
```python
# WRONG: Could cause deadlock
lock1.acquire()
lock2.acquire()

# RIGHT: Use semaphores with proper ordering
self.zero_sem.acquire()
# ... work ...
self.odd_sem.release()  # Always release different semaphore
```

### 2. **Race Conditions**
```python
# WRONG: Race condition on shared counter
if counter % 2 == 1:  # Could change between check and use
    
# RIGHT: Use protected current variable
if self.current % 2 == 1:  # Protected by semaphore ordering
```

### 3. **Busy Waiting**
```python
# WRONG: Wastes CPU cycles
while not my_turn:
    time.sleep(0.001)
    


