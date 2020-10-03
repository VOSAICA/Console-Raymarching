from .utils import Screen

# It will be faster to use multiprocessing, but without it is also ok
from multiprocessing import Pool

if __name__ == '__main__':

    screen = Screen(256, 208)  # resolution as 256*208

    # uncommet the next line to do calculation with single processor
    # screen.calc()

    # Do calculation with 4 processor
    # Change the processorNum if there are more than 4 cores in your CPU

    processorNum = 4

    start, interval = 0, int(screen.height / processorNum)
    pool = Pool(processes=processorNum)
    processes = []
    for _ in range(processorNum):
        processes.append(
            pool.apply_async(screen.calcPart, (start, start + interval)))
        start += interval
    pool.close()
    pool.join()

    for process in processes:
        screen.fragColor += process.get()

    # Print the result to console
    screen.show()

    # Print the result to a text file
    screen.printToFile()
