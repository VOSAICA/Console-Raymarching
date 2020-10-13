from Package.utils import Screen
# from multiprocessing import Pool


if __name__ == '__main__':

    screen = Screen(256, 208)  # resolution as 256*208

    # It will be faster to use multiprocessing, but without it is also ok

    # Comment the screen.calc() and uncomment the next part to do calculation
    # with multiprocessing

    # Change the processorNum if there are more than 4 cores in your CPU
    '''
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
    '''

    # Do calculation
    screen.calc()

    # Print the result to console
    screen.show()

    # Print the result to a text file
    screen.printToFile()
