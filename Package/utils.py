from .linear import Vector, Matrix
from .raymarching import rayMarch, getLight


class Screen():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fragCoord = Matrix(
            [[Vector([j + 0.5, i + 0.5]) for j in range(width)]
             for i in range(height - 1, -1, -1)])
        self.resolution = Vector([self.width, self.height])
        self.fragColor = Matrix([[Vector([0]) for j in range(width)]
                                 for i in range(height)])

        self.uv = self.fragCoord
        for i in range(height):
            for j in range(width):
                self.uv.array[i][j] = Vector.divVec(
                    self.fragCoord.array[i][j] - (self.resolution * 0.5),
                    self.resolution)

    def calc(self):
        for i in range(self.height):
            for j in range(self.width):
                uv = self.uv.array[i][j]
                color = Vector([0, 0, 0])
                ro = Vector([0, 1, 0])
                rd = Vector([uv.array[0], uv.array[1], 1.]).normalize()

                d = rayMarch(ro, rd)

                p = ro + rd * d
                dif = getLight(p)

                color = Vector([dif])
                self.fragColor.array[i][j] = color

    def calcPart(self, start, end):
        result = Matrix([[Vector([0]) for j in range(self.width)]
                         for i in range(self.height)])
        for i in range(start, end):
            for j in range(self.width):
                uv = self.uv.array[i][j]
                color = Vector([0, 0, 0])
                ro = Vector([0, 1, 0])
                rd = Vector([uv.array[0], uv.array[1], 1.]).normalize()

                d = rayMarch(ro, rd)

                p = ro + rd * d
                dif = getLight(p)

                color = Vector([dif])
                result.array[i][j] = color
        return result

    def calcMul(self, processorNum):
        from multiprocessing import Pool
        start, interval = 0, int(self.height / processorNum)
        pool = Pool(processes=processorNum)
        processes = []

        for _ in range(processorNum):
            processes.append(
                pool.apply_async(self.calcPart, (start, start + interval)))
            start += interval
        pool.close()
        pool.join()

        for process in processes:
            self.fragColor += process.get()

    def turn2Chara(self, number):
        charas = list('''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxr\
        jft/\\|()1{}[]?-_+~<>i!lI;:,"^`'. ''')
        charas_len = len(charas)

        chara = charas[int(number * charas_len)]
        return chara

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                chara = self.turn2Chara(self.fragColor.array[i][j].array[0])
                print(chara + " ", end='')
            print("")

    def printToFile(self):
        result = open("result.txt", mode='w')
        for i in range(self.height):
            for j in range(self.width):
                chara = self.turn2Chara(self.fragColor.array[i][j].array[0])
                result.write(chara + " ")
            result.write("\n")
