namespace NssfTechInterview.BusinessLogic
{
    public class ZeroEvenOdd
    {
        private int n;

        // These events control which thread runs next
        private AutoResetEvent zeroEvent = new AutoResetEvent(true);   // Start with zero allowed
        private AutoResetEvent evenEvent = new AutoResetEvent(false);  // Even waits
        private AutoResetEvent oddEvent = new AutoResetEvent(false);   // Odd waits

        public ZeroEvenOdd(int n)
        {
            this.n = n;
        }

        // Prints 0 before every number
        public void Zero(Action<int> printNumber)
        {
            for (int i = 1; i <= n; i++)
            {
                zeroEvent.WaitOne();   // Wait for turn to print zero
                printNumber(0);        // Print zero

                // Decide whether to wake Odd or Even thread
                if (i % 2 == 1)
                    oddEvent.Set();    // Wake Odd thread
                else
                    evenEvent.Set();   // Wake Even thread
            }
        }

        // Prints even numbers (2, 4, 6, ...)
        public void Even(Action<int> printNumber)
        {
            for (int i = 2; i <= n; i += 2)
            {
                evenEvent.WaitOne();   // Wait for signal from Zero
                printNumber(i);        // Print even number
                zeroEvent.Set();       // Signal Zero to print next zero
            }
        }

        // Prints odd numbers (1, 3, 5, ...)
        public void Odd(Action<int> printNumber)
        {
            for (int i = 1; i <= n; i += 2)
            {
                oddEvent.WaitOne();    // Wait for signal from Zero
                printNumber(i);        // Print odd number
                zeroEvent.Set();       // Signal Zero to print next zero
            }
        }
    }
}
