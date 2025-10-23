import threading
from typing import Callable


class ZeroEvenOdd:
    """
    A class that prints numbers in a specific pattern using three threads:
    - Thread A calls zero() which should output only zeros
    - Thread B calls even() which should output only even numbers  
    - Thread C calls odd() which should output only odd numbers
    """
    
    def __init__(self, n: int):
        """
        Initialize the ZeroEvenOdd class.
        
        Args:
            n (int): The upper limit for numbers to print (1 to n)
        """
        self.n = n
        
        # Semaphores for synchronization
        self.zero_sem = threading.Semaphore(1)  # Zero starts first
        self.even_sem = threading.Semaphore(0)  # Even waits
        self.odd_sem = threading.Semaphore(0)   # Odd waits
        
        # Track current number to print
        self.current = 1
    
    def zero(self, print_number: Callable[[int], None]) -> None:
        """
        Prints zeros in the sequence. Should be called by thread A.
        
        Args:
            print_number: Function that prints the given number
        """
        for i in range(self.n):
            self.zero_sem.acquire()  # Wait for zero's turn
            print_number(0)          # Print zero
            
            # Release the appropriate thread based on current number
            if self.current % 2 == 1:
                self.odd_sem.release()   # Next is odd
            else:
                self.even_sem.release()  # Next is even
    
    def even(self, print_number: Callable[[int], None]) -> None:
        """
        Prints even numbers in the sequence. Should be called by thread B.
        
        Args:
            print_number: Function that prints the given number
        """
        for i in range(2, self.n + 1, 2): 
            self.even_sem.acquire()      # Wait for even's turn
            print_number(self.current)   # Print current even number
            self.current += 1            # Move to next number
            self.zero_sem.release()      # Give turn back to zero
    
    def odd(self, print_number: Callable[[int], None]) -> None:
        """
        Prints odd numbers in the sequence. Should be called by thread C.
        
        Args:
            print_number: Function that prints the given number
        """
        for i in range(1, self.n + 1, 2):  # Odd numbers: 1, 3, 5, ...
            self.odd_sem.acquire()       # Wait for odd's turn
            print_number(self.current)   # Print current odd number
            self.current += 1            # Move to next number
            self.zero_sem.release()      # Give turn back to zero


def test_zero_even_odd():
    """
    Test the ZeroEvenOdd class with multiple threads.
    """
    import time
    
    # Test with n = 5
    n = 5
    zeo = ZeroEvenOdd(n)
    
    # Shared list to collect output
    output = []
    
    def print_number(x):
        output.append(str(x))
        print(x, end='')
    
    # Create threads
    thread_zero = threading.Thread(target=zeo.zero, args=(print_number,))
    thread_even = threading.Thread(target=zeo.even, args=(print_number,))
    thread_odd = threading.Thread(target=zeo.odd, args=(print_number,))
    
    # Start all threads
    print(f"Testing ZeroEvenOdd with n={n}")
    print("Expected output: 0102030405")
    print("Actual output:   ", end='')
    
    thread_zero.start()
    thread_even.start()
    thread_odd.start()
    
    # Wait for all threads to complete
    thread_zero.join()
    thread_even.join()
    thread_odd.join()
    
    print()  # New line
    print(f"Output as list: {output}")
    
    # Verify the output
    expected = ['0', '1', '0', '2', '0', '3', '0', '4', '0', '5']
    if output == expected:
        print("Test PASSED!")
    else:
        print(" Test FAILED!")
        print(f"Expected: {expected}")
        print(f"Got:      {output}")


if __name__ == "__main__":
    print("=" * 50)
    print("ZERO EVEN ODD THREADING TEST")
    print("=" * 50)
    
    test_zero_even_odd()
    
    print("\n" + "=" * 50)
    print("Testing with different values of n")
    print("=" * 50)
    
    # Test with different values
    for n in [3, 7, 10]:
        print(f"\nTesting with n={n}:")
        zeo = ZeroEvenOdd(n)
        output = []
        
        def print_num(x):
            output.append(x)
            print(x, end='')
        
        # Create and start threads
        t1 = threading.Thread(target=zeo.zero, args=(print_num,))
        t2 = threading.Thread(target=zeo.even, args=(print_num,))
        t3 = threading.Thread(target=zeo.odd, args=(print_num,))
        
        print("Output: ", end='')
        t1.start()
        t2.start()
        t3.start()
        
        t1.join()
        t2.join()
        t3.join()
        print()  # New line