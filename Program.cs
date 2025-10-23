

Run();
static void Run()
{
    var zeo = new ZeroEvenOdd(17);

    //delegate to print number
    static void printNumber(int x) => Console.Write(x);

    //thread A calls zeo.Zero()
    new Thread(() => zeo.Zero(printNumber)).Start();
    //thread B calls zeo.Even()
    new Thread(() => zeo.Even(printNumber)).Start();
    //thread C calls zeo.Odd()
    new Thread(() => zeo.Odd(printNumber)).Start();

    Thread.Sleep(100);
}

public class ZeroEvenOdd
{
    //indicates the length of the output string
    private int outputLength;

    //synchronization flag to indicate whose turn it is to print
    // 0 = zero, 1 = odd, 2 = even
    private int turn = 0;

    //this is the current number to print
    private int num = 1;

    public ZeroEvenOdd(int n)
    {
        //initialize n to the input value
        this.outputLength = n;
    }

    /// <summary>
    /// prints zeroes before each odd/even number
    /// </summary>
    /// <param name="printNumber"></param>
    public void Zero(Action<int> printNumber)
    {
        for (int i = 0; i < outputLength; i++)
        {
            while (turn != 0) { }
            printNumber(0);

            turn = (num % 2 == 1) ? 1 : 2;
        }
    }

    /// <summary>
    /// prints even numbers
    /// </summary>
    /// <param name="printNumber"></param>
    public void Even(Action<int> printNumber)
    {
        for (int i = 2; i <= outputLength; i += 2)
        {
            //poll for turn to print even
            while (turn != 2) { }
            printNumber(num++);
            turn = 0;
        }
    }

    /// <summary>
    /// prints odd numbers
    /// </summary>
    /// <param name="printNumber"></param>
    public void Odd(Action<int> printNumber)
    {
        for (int i = 1; i <= outputLength; i += 2)
        {
            //poll for turn to print even
            while (turn != 1) { }
            printNumber(num++);
            turn = 0;
        }
    }
}


