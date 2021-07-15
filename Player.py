from xenotables import XenoTable as XenoTable
import time
import pygame
from threading import Thread

serverIp = "192.168.0.102"

rows = []
rows.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
rows.append([0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0])
rows.append([0,2,1,1,1,1,2,2,2,2,1,1,1,1,1,1,1,1,2,0])
rows.append([0,2,1,2,2,1,2,2,1,1,1,1,1,1,1,2,2,1,1,0])
rows.append([0,2,1,2,2,1,1,2,1,1,1,2,2,1,2,2,1,1,1,0])
rows.append([0,2,1,1,2,1,1,1,1,2,1,1,2,2,2,1,1,1,1,0])
rows.append([0,2,1,2,2,1,2,1,2,2,1,1,1,2,1,1,2,2,1,0])
rows.append([0,1,1,1,1,1,2,2,2,1,1,2,1,2,1,2,2,1,1,0])
rows.append([0,2,2,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0])
rows.append([0,1,1,1,1,1,2,2,2,2,2,2,1,1,1,2,2,2,2,0])
rows.append([0,2,2,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,0])
rows.append([0,2,2,1,1,1,1,1,2,2,1,1,1,1,2,1,2,2,1,0])
rows.append([0,2,2,1,1,1,2,1,1,2,2,2,1,1,2,1,2,2,1,0])
rows.append([0,1,1,1,2,2,2,1,1,1,1,1,1,2,2,1,1,1,1,0])
rows.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

pygame.mixer.init()
pygame.mixer.music.load('Sounds/Bump.mp3')
def bump():
    pygame.mixer.music.play()
    sleep(200)
def sleep(mil):
    time.sleep(mil/1000.0)
def getGrid(x,y):
    global rows
    return rows[y][x]
def cord(l,m):
    return ((l * 48) - 48, (m * 48) - 48)
def check(x,y,nx,ny):
    if getGrid(x+nx,y+ny) == 1:
        return True
    else:
        return False
players_who_have_left = []
def getOpps():
    global players_who_have_left
    num = z.get("players")
    oppon = []
    lol = True
    while lol:
        for count in range(num):
            if count in players_who_have_left:
                pass
            else:
                while True:
                    try:
                        info = z.get("player" + str(count))
                        break
                    except KeyError:
                        pass
                lol = True
                if info == 0:
                    players_who_have_left.append(count)
                    lol = False
                else:
                    try:
                        int(info[0])
                    except ValueError:
                        lol = False
                        oppon.append((info[0],float(info[1]),float(info[2])))
    return oppon
def display():
    global x
    global y
    global sprite
    global screen
    global z
    global ID
    screen.fill((0,0,0))
    z.put("player" + str(ID -1), (sprite,x,y))
    (mx,my) = cord(x,y)
    mx -= 416
    my -= 288
    mx = -mx
    my = -my
    screen.blit(maze,(mx,my))
    opps = getOpps()
    for j in range(len(rows)):
        for k in range(len(rows[j])):
            if rows[j][k] == 3:
                rows[j][k] = 1
    for o in opps:
        rows[round(o[2])][round(o[1])] = 3
        (a,b) = cord(o[1],o[2])
        screen.blit(pygame.image.load(o[0]),(a + mx + 8, b + my))
    pygame.display.update()


z = XenoTable(serverIp,int(input("Enter port: ")))
ID = z.get("players") + 1
z.put("players", ID)
while z.get("wait"):
    pass
initial_info = z.get("player" + str(ID-1))
z.put("wait",True)
direct = "C_0" + str(int(initial_info[0])) + "/"
sprite = direct + "273/1.png"
direction = 273
maze = pygame.image.load("Mazes/01.png")
x = int(initial_info[1])
y = int(initial_info[2])
Ht = 864
Wt = 624
screen = pygame.display.set_mode((Ht,Wt))
pause_time = 0
opps = []
vectors = [(0,-0.25),(0,0.25),(0.25,0),(-0.25,0)]
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key in range(273,277):
                if direction == event.key:
                    vector = vectors[event.key - 273]
                    sprite = direct + str(event.key) + "/1.png"
                    display()
                    if check(int(x),int(y),int(vector[0]*4),int(vector[1]*4)):
                        for step in range(1,5):
                            sprite = direct + str(event.key) + "/" + str((step%4)+1) + ".png"
                            x += vector[0]
                            y += vector[1]
                            display()
                            sleep(24)
                    else:
                        bump()
                else:
                    sprite = direct + str(event.key) + "/1.png"
                direction = event.key
    x = int(x)
    y = int(y)
    sprite = direct + str(direction) + "/1.png"
    display()

pygame.quit()
print("quit")
z.put("player" + str(ID-1),0)
