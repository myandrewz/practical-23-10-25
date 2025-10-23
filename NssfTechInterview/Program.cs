
using NssfTechInterview.BusinessLogic;


int n = 9;
ZeroEvenOdd zeroEvenOdd = new ZeroEvenOdd(n);

// Run all threads in parallel
Task t1 = Task.Run(() => zeroEvenOdd.Zero(Console.Write));
Task t2 = Task.Run(() => zeroEvenOdd.Even(Console.Write));
Task t3 = Task.Run(() => zeroEvenOdd.Odd(Console.Write));

Task.WaitAll(t1, t2, t3);
Console.WriteLine(); // Move to next line after output