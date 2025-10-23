using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace QN_one
{
    public class ZeroEvenOdd
    {
        int n;
        public ZeroEvenOdd(int value) {
          this.n = value;
        }

        private void zero(int x) =>this.printNumber(0);

        private void even(int x)
        {
            if (x % 2 == 0) this.printNumber(x);

        }
        private void odd(int x)
        {
            if (x % 2 > 0) this.printNumber(x);
        }

        private void printNumber(int x) => Console.Write(x);

        public void series()
        {
           
            for (int i = 1; i < this.n; i++)
            {
                this.zero(i);
                if( i % 2 == 0)this.even(i);
                else this.odd(i);
            }
        }

    }
}
