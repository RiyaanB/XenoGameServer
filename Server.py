from xenotables import Communicator as CC
from xenotables import XenoTable as XT
import time
from random import randint
from threading import Thread

serverIp = CC.myIP()

rows = []  # [y][x]
rows.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
rows.append([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0])
rows.append([0, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0])
rows.append([0, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0])
rows.append([0, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 0])
rows.append([0, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 0])
rows.append([0, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 0])
rows.append([0, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 0])
rows.append([0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0])
rows.append([0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 0])
rows.append([0, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0])
rows.append([0, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 0])
rows.append([0, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 0])
rows.append([0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0])
rows.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


def sleep(mil):
    time.sleep(mil / 1000.0)


def getGrid(x, y):
    global rows
    return rows[int(y)][int(x)]


xs = []
ys = []


def getEmpty():
    sprite = randint(1, 3)
    global xs
    global ys
    global rows
    while True:
        x = randint(0, 19)
        y = randint(0, 14)
        if getGrid(x, y) == 1 and not (y in ys) and not (x in xs):
            xs.append(x)
            ys.append(y)
            break
    return sprite, x, y


CC.debug = False
l = []


class opp:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = float(x)
        self.y = float(y)


players_who_have_left = []


def getOpps():
    global players_who_have_left
    print("entered getOpps()")
    num = z.get("players")
    opps = []
    for count in range(num):
        if count in players_who_have_left:
            pass
        else:
            while True:
                print("getting", count)
                info = z.get("player" + str(count))
                if info == 0:
                    players_who_have_left.append(count)
                else:
                    try:
                        int(info[0])
                        break
                    except ValueError:
                        pass
            opps.append(opp(info[0], info[1], info[2]))
    print("returned opps")
    return opps


def refreshGrid():
    opps = getOpps()
    for j in range(len(rows)):
        for k in range(len(rows[j])):
            if rows[j][k] == 3:
                rows[j][k] = 1
    for opp in opps:
        rows[round(opp.y)][round(opp.x)] = 3

    return opps


def getGrid(x, y):
    global rows
    print("Grids:", x, y)
    return rows[int(y)][int(x)]


def check(x, y, nx, ny):
    # Up    =  0,-1
    # Down  =  0, 1
    # Left  = -1, 0
    # Right =  1, 0
    print(x, y, nx, ny)
    if getGrid(x + nx, y + ny) == 1:
        return True
    else:
        return False


class npc(Thread):
    def __init__(self, x, y, dialogue, ids):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = "C_01/F/1.png"
        self.dialogue = dialogue
        self.free = True
        self.id = ids
        z.put("npc" + str(ids), (x, y, self.sprite))
        print("started", x, y, self.sprite)
        z.put("number", 0)
        self.start()

    def run(self):
        while True:
            print("ran move")
            clock = time.time()
            while abs(clock - time.time()) < 0.5:
                sleep(50)
            print("finished waiting")
            self.move()
            print("moving")

    def move(self):
        print("entered move")
        dirs = ["F", "R", "D", "L"]
        vects = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        refreshGrid()
        r = randint(1, 2)
        print("Random 1,2:", r)
        if r == 1:
            for a in range(16):
                dire = randint(0, 3)
                print("checking")
                if check(self.x, self.y, vects[dire][0], vects[dire][1]):
                    for step in range(1, 5):
                        self.sprite = "C_01/" + str(dirs[dire]) + "/" + str(step) + ".png"
                        self.x += vects[dire][0] * 0.25
                        self.y += vects[dire][0] * 0.25
                        z.put("npc" + str(self.id), (self.x, self.y, self.sprite))
                        sleep(32)
                        z.put("number", z.get("number") + 1)
                    print("movied")
                    return None
        self.sprite = "C_01/" + dirs[randint(0, 3)] + "/1.png"
        z.put("npc" + str(self.id), (self.x, self.y, self.sprite))
        print("turned", self.x, self.y, self.sprite)


data = {"players": 0, "limit": 2}
server = CC(CC.createSock(serverIp), data)

print(server.ip, server.port)
z = XT(serverIp, server.port)
time.sleep(0.3)
z.put("npcs", [])
z.put("wait", True)
z.put("init", True)
s, xd, yd = getEmpty()
# npc(xd,yd,"Hello",0)
z.put("npcs", 1)

while True:
    cur = z.get("players")
    while cur - z.get("players") == 0:
        sleep(100)
        print(z.get("players"))
    print("got")
    z.put("player" + str(cur), getEmpty())
    z.put("wait", False)

print("Ended\nLet the games commence")
