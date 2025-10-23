class ZeroEvenOdd:
    def __init__(self, n):
        self.__n = n
    
    def zero(self):

        print(0, end='')
    
    def even(self, num):
        print(num, end='')
    
    def odd(self, num):
        print(num, end='')
    
    def printNumber(self, num):
        print(self.__n)

    def print_sequence(self):
        
        odd_num = 1
        even_num = 2
        
        for i in range(1, self.__n + 1):
            self.zero()
            self.odd(odd_num)
            odd_num += 2
            
            self.zero()
            self.even(even_num)
            even_num += 2
        
        print()


