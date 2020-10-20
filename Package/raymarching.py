from .linear import Vector

SURFACE_DIST = 0.01
MAX_DIST = 150.0
MAX_STEP = 100


def clamp(x, low, high):
    return min(max(x, low), high)


def getDist(p):
    s = Vector([0, 1, 6])
    sRadius = 1.0
    sphereDist = Vector.length(p - s) - sRadius

    planeDist = p.array[1]

    dist = min(sphereDist, planeDist)
    return dist


def rayMarch(ro, rd):
    depth = 0
    for _ in range(MAX_STEP):
        pos = ro + rd * depth
        dist = getDist(pos)
        depth += dist
        if dist < SURFACE_DIST or depth > MAX_DIST:
            break
    return depth


def getNormal(p):
    dx = Vector([0.01, 0.0, 0.0])
    dy = Vector([0.0, 0.01, 0.0])
    dz = Vector([0.0, 0.0, 0.01])
    dist = getDist(p)
    n = Vector([
        dist - getDist(p - dx), dist - getDist(p - dy), dist - getDist(p - dz)
    ])
    return (n.normalize())


def getLight(p):
    lightPos = Vector([3, 5, -1])
    li = Vector.normalize(lightPos - p)
    n = getNormal(p)

    dif = clamp(Vector.innerProd(n, li), 0, 1)

    if p.array[1] < 0.1:
        dif *= float(int(p.array[0] + 100) % 2
                     ^ int(p.array[2] + 100) % 2) * 0.9

    d = rayMarch(p + n * (SURFACE_DIST * 2), li)
    if d < Vector.length(lightPos - p):
        dif *= 0.1
    return dif
