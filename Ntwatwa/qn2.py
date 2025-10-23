class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n

    def zero(self, printNumber):
        printNumber(0)

    def even(self, printNumber, i):
        if i % 2 == 0:
            printNumber(i)

    def odd(self, printNumber, i):
        if i % 2 == 1:
            printNumber(i)

    def run(self, printNumber):
        for i in range(1, self.n + 1):
            self.zero(printNumber)
            if i % 2 == 0:
                self.even(printNumber, i)
            else:
                self.odd(printNumber, i)


def printNumber(x):
    print(x, end='')

n = int(input(f"Enter the value of n : "))

zeo = ZeroEvenOdd(n)
zeo.run(printNumber)
print("\n")
