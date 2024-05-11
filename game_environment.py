from config import Configuration as C

grassblockHeight = 70
grassblockWidth = 71

groundHeight = C.HEIGHT - grassblockHeight

numPlatforms = 5
platformY = [100, 200, 300, groundHeight, groundHeight]
platformX = [100, 800, 500, 0, 781]
platformWidth = [3, 3, 3, 8, 6]

def drawEnvironment(screen):
    for y in range(numPlatforms):
        for x in range(platformWidth[y]):
            screen.blit('grassblock', (platformX[y] + x*grassblockWidth, platformY[y]))


def getGround(x, y):
    for i in range(numPlatforms):
        if y <= platformY[i]+grassblockHeight/2:
            if x > platformX[i] - C.PLAYERWIDTH/4 and x < platformX[i] + platformWidth[i]*grassblockWidth + C.PLAYERWIDTH/4:
                return platformY[i]
    return C.HEIGHT
