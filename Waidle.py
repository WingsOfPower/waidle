import pygame
t = 0
import string
def ListToString(list):
    str = ""

    for element in list:
        if str != "":
            str = str + "," + element
        else:
            str = str + element
    
    return str
pygame.init()
def saveTimer():
    global t
    if t != 2000:
        t +=1
    else:
        t = 0
        saveGame()

# color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)
width = 1600
height = 800
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
pygame.display.set_caption("Waidle, Water idle game")
background = black
framerate = 60
font = pygame.font.Font("assets/fonts/pixel.ttf", 16)
timer = pygame.time.Clock()

# game variables
green_value = 1
red_value = 2
orange_value = 3
white_value = 4
purple_value = 5
# drawing values
draw_green = False
draw_red = False
draw_orange = False
draw_white = False
draw_purple = False
# lengths of loading bars
green_length = 0
red_length = 0
orange_length = 0
white_length = 0
purple_length = 0
# speed of loading bars
green_speed = .5
red_speed = 1
orange_speed = 1.5
white_speed = 2
purple_speed = 2.5
#is the generator unlocked?
#upgraded # of tmes
upgrades = [1, 1, 1, 1, 1]
#cost
green_cost = 0
red_cost = 5
orange_cost = 10
white_cost = 15
purple_cost = 20
#images
lockImg = pygame.image.load("assets/lock.png")
score_barImg = pygame.image.load("assets/Score_Info_Bar.png")
#read save file
with open("game.sav", "r") as save:
    content = save.readlines()
rebirthValue = int(content[0])
l = content[1].rstrip("\n")
locked = l.split(",")

score = int(content[2])
def openOptions():
    print("options")
    print(locked)
def saveGame():
    content[0] = str(rebirthValue) + "\n"
    content[1] = ListToString(locked) + "\n"
    content[2] = str(score) + "\n"
    with open("game.sav", "w") as save:
        save.writelines(content)
def buttonExe(btnId, genId=0):
    global running
    if btnId == 0:
        saveGame()
        running = False
    elif btnId == 1:
        openOptions()
    elif btnId == 2:
        print("upgrade")

def drawImg(img, x ,y):
    screen.blit(img, (x, y))

def draw_task(color, y_coord, value, draw, length, speed, mouseX, mouseY, click, isLocked, cost, img):
    global score
    income = upgrades[value-1] * rebirthValue + value
    if mouseX >= 15 and mouseX <= 60 and mouseY >= y_coord - 25 and mouseY <= y_coord + 15 and click == True and isLocked == "False":
        draw = True
    if mouseX >= 15 and mouseX <= 60 and mouseY >= y_coord - 20 and mouseY <= y_coord + 15 and click == True and isLocked == "True" and score >= cost:
        score = score - cost
        locked[value-1] = "False"
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        score += income
    currentImg = pygame.image.load(img)
    drawImg(pygame.transform.scale(currentImg, (50, 50)), 5, y_coord - 25)
    task = pygame.draw.circle(screen, color, (30, y_coord), 30, 5)
    currentImg = pygame.image.load(img)
    if isLocked == "True":
        drawImg(pygame.transform.scale(lockImg, (60, 60)), 0, y_coord - 30)
    pygame.draw.rect(screen, color, [70, y_coord - 15, 200, 30])
    pygame.draw.rect(screen, black, [75, y_coord - 10, 190, 20])
    pygame.draw.rect(screen, color, [70, y_coord - 15, length, 30])
    drawButton(270, y_coord-15, 30, 30, mouseX, mouseY, 2, click)
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_coord - 10))
    return task, length, draw



def drawButton(px, py, sx, sy, mx, my, buttonId, click):
    btnImg = "assets/ui/button_" + str(buttonId) + ".png"
    if mx >= px and mx <= px + sx and my >= py and my <= py + sy and click == True:
        buttonExe(buttonId)
    drawImg(pygame.transform.scale(pygame.image.load(btnImg), (sx, sy)), px, py)
running = True
while running:
    green_locked = locked[0]
    red_locked = locked[1]
    orange_locked = locked[2]
    white_locked = locked[3]
    purple_locked = locked[4]
    mouse = pygame.mouse.get_pos()
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saveGame()
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        else:
            mouseDown = False

    
    screen.fill(background)
    drawButton(width-100, 0, 100, 32, mouse[0], mouse[1], 0, mouseDown)
    drawButton(width-250, 0, 50, 32, mouse[0], mouse[1], 1, mouseDown)
    drawImg(pygame.transform.scale(score_barImg, (150, 32)), 0, 0)
    scoreText = font.render("Score:   " + str(score), True, (252, 205, 119))
    screen.blit(scoreText, (10, 0))
    task1, green_length, draw_green = draw_task(green, 80, green_value, draw_green, green_length, green_speed, mouse[0], mouse[1], mouseDown, green_locked, green_cost, "assets/green_icon.png")
    task2, red_length, draw_red = draw_task(red, 140, red_value, draw_red, red_length, red_speed, mouse[0], mouse[1], mouseDown, red_locked, red_cost, "assets/red_icon.png")
    task3, orange_length, draw_orange = draw_task(orange, 200, orange_value, draw_orange, orange_length, orange_speed, mouse[0], mouse[1], mouseDown, orange_locked, orange_cost, "assets/green_icon.png")
    task4, white_length, draw_white = draw_task(white, 260, white_value, draw_white, white_length, white_speed, mouse[0], mouse[1], mouseDown, white_locked, white_cost, "assets/green_icon.png")
    task5, purple_length, draw_purple = draw_task(purple, 320, purple_value, draw_purple, purple_length, purple_speed, mouse[0], mouse[1], mouseDown, purple_locked, purple_cost, "assets/green_icon.png")
    pygame.display.flip()
    saveTimer()
pygame.quit()
        