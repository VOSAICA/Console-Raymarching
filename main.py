from Package.utils import Screen


if __name__ == '__main__':
    screen = Screen(256, 208)  # resolution as 256*208

    # It will be faster to use multiprocessing, but without it is also ok
    # For using multiprocessing, change the screen.calc() to screen.calcMul()

    # Change the argument if there are more than 8 cores in your CPU
    screen.calcMul(8)

    # screen.calc()

    # Print the result to console
    screen.show()

    # Print the result to a text file
    screen.printToFile()
