import concurrent.futures
import time
import random

start = time.perf_counter()

processPools = []

class Trapezoid:
    def __init__(self, trap):
        self.a = min(trap)
        self.b = max(trap)
        self.h = sum(trap) - self.a - self.b

    def area(self):
        return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        return False

    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() - other.area()
        return False

    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() % other.area()
        return False


def threads(arr):
    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(trapezoid_area, [arr[i:i+50] for i in range(0, len(arr), 50)])
    finish_time = time.perf_counter()
    print('threads Finished in: ', round(finish_time - start_time, 2), 'second(s)')
    return 'pass'


def multiprocess(arr):
    start_time = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pp in range(0, 8):
            processPools.append(executor.submit(trapezoid_area, arr[(pp * len(arr) // 8):((pp+1) * len(arr))]))
        for pp in range(0, 8):
            (processPools[pp].result())
    finish_time = time.perf_counter()
    print('multiprocess Finished in: ', round(finish_time - start_time, 2), 'second(s)')
    return 'pass'


def thread_pool_run(pp, arr):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(trapezoid_area, arr[(pp * 20):((pp * 20) + 20)])
    return 'pass'


def mixed(arr):
    start_time = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pp in range(0, 5):
            processPools.append(executor.submit(thread_pool_run, pp, arr))
        for pp in range(0, 5):
            (processPools[pp].result())

    finish_time = time.perf_counter()
    print('mixed: ', round(finish_time - start_time, 2), 'second(s)')


def trapezoid_area(arr):
    for item in arr:
        trapezoid = Trapezoid(item)
        trapezoid.area()


def default(arr):
    start_time = time.perf_counter()
    trapezoid_area(arr)
    finish_time = time.perf_counter()
    print('default Finished in: ', round(finish_time - start_time, 2), 'second(s)')


if __name__ == "__main__":
    trapezoid_dimensions = [[random.randint(1, 200), random.randint(
        1, 200), random.randint(1, 200)] for _ in range(1000000)]
    # 0.08 second(s)
    default(trapezoid_dimensions)
    # 0.13 second(s)
    threads(trapezoid_dimensions)
    # 0.77 second(s)
    multiprocess(trapezoid_dimensions)
    # 0.68 second(s)
    mixed(trapezoid_dimensions)
