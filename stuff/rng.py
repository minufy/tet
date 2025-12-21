import math

class RNG:
    def __init__(self, seed):
        self.t = seed % 2147483647

        if self.t == 0:
            self.t += 2147483646

    def next(self):
        self.t = 16807 * self.t % 2147483647
        return self.t
    
    def nextFloat(self):
        return (self.next() - 1) / 2147483646

    def shuffleArray(self, array):
        if len(array) == 0:
            return array

        for i in range(len(array)-1, 0, -1):
            r = math.floor(self.nextFloat() * (i+1))
            array[i], array[r] = array[r], array[i]

        return array