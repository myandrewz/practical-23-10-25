package org.example;

import java.util.concurrent.Semaphore;
import java.util.function.IntConsumer;

/**
 * Question2: Implement ZeroEvenOdd to print the sequence 01020304... with total length 2n.
 *
 * The same instance is used by three threads:
 *  - zero(): prints only 0s, exactly n times
 *  - even(): prints even numbers in ascending order
 *  - odd(): prints odd numbers in ascending order
 *
 * Expected combined output: 0 1 0 2 0 3 0 4 ... (without spaces)
 */
public class ZeroEvenOdd {
    private final int n;

    // Semaphores to coordinate order: zero -> (odd|even) -> zero -> ...
    private final Semaphore zeroSem = new Semaphore(1);
    private final Semaphore oddSem = new Semaphore(0);
    private final Semaphore evenSem = new Semaphore(0);

    public ZeroEvenOdd(int n) {
        this.n = n;
    }

    // printNumber.accept(x) outputs "x", where x is an integer.
    public void zero(IntConsumer printNumber) throws InterruptedException {
        for (int i = 1; i <= n; i++) {
            zeroSem.acquire();
            printNumber.accept(0);
            // signal the next appropriate number printer
            if ((i & 1) == 1) {
                oddSem.release();
            } else {
                evenSem.release();
            }
        }
    }

    public void even(IntConsumer printNumber) throws InterruptedException {
        for (int i = 2; i <= n; i += 2) {
            evenSem.acquire();
            printNumber.accept(i);
            zeroSem.release();
        }
    }

    public void odd(IntConsumer printNumber) throws InterruptedException {
        for (int i = 1; i <= n; i += 2) {
            oddSem.acquire();
            printNumber.accept(i);
            zeroSem.release();
        }
    }
}
