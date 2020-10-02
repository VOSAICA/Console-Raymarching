from linear import Vector

SURFACE_DIST = 0.01
MAX_DIST = 150.0
MAX_STEP = 100


def clamp(x, low, high):
    return min(max(x, low), high)


def getDist(p):
    s = Vector([0., 1., 6.])
    sRadius = 1.0
    sphereDist = Vector.length(p - s) - sRadius

    planeDist = p.array[1]

    dist = min(sphereDist, planeDist)

    return dist


def rayMarch(ro, rd):
    depth = 0.
    for _ in range(MAX_STEP):
        pos = ro + rd * depth
        dist = getDist(pos)
        depth += dist
        if dist < SURFACE_DIST or depth > MAX_DIST:
            break

    return depth


def getNormal(p):
    # e = Vector([0.01, 0.0])
    eXYY = Vector([0.01, 0.0, 0.0])
    eYXY = Vector([0.0, 0.01, 0.0])
    eYYX = Vector([0.0, 0.0, 0.01])
    dist = getDist(p)
    n = Vector([
        dist - getDist(p - eXYY), dist - getDist(p - eYXY),
        dist - getDist(p - eYYX)
    ])

    return (n.normalize())


def getLight(p):
    lightPos = Vector([0, 5, 9])

    li = Vector.normalize(lightPos - p)
    n = getNormal(p)

    dif = clamp(Vector.innerProd(n, li), 0.0, 1.0)

    d = rayMarch(p + n * (SURFACE_DIST * 2.0), li)
    if d < Vector.length(lightPos - p):
        dif *= 0.1

    return dif
