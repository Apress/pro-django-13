class FibonacciIterator(object):
    def __init__(self, count):
        self.a = 0
        self.b = 1
        self.count = count
        self.current = 0

    def __next__(self):
        self.current += 1
        if self.current > self.count:
            raise StopIteration
        if self.current < 3:
            return self.current - 1
        c = self.a + self.b
        self.a = self.b
        self.b = c
        return c
    next = __next__

    def __iter__(self):
        # Since it's already an iterator, this can return itself.
        return self


class Fibonacci(object):
    def __init__(self, count):
        self.count = count

    def __iter__(self):
        return FibonacciIterator(self.count)

    def __len__(self):
        return self.count


if __name__ == '__main__':
    eight = Fibonacci(8)
    assert list(eight), [0, 1, 1, 2, 3, 5, 8, 13]
    assert len(eight), 8
