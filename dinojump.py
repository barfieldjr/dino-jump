#Chris Barfield - cdb8da

import gamebox
import pygame
import time

#Start initalizing variables to be used throughout code

camera = gamebox.Camera(800, 600)
game_on = False
score = 0
base = 0
cloud_pad = -100
cactus_pad = -20
timer = 0
game_on = False
game_over = False

#Creatin images for background and  to be shown throughout game

start = gamebox.from_image(400, 300, 'dinopic.png')
start.scale_by(1)
ground_box = gamebox.from_color(400,  599,"black", 800, 10)
wall = gamebox.from_color(1, 0, "black", 1, 10000)

#Creating cacti from images

cactus1 = gamebox.from_image(700, 565, 'cactus.png')
cactus1.scale_by(.1)
cactus2 = gamebox.from_image(1200, 565, 'cactus.png')
cactus2.scale_by(.12)

#Creating clouds from images

cloud1 = gamebox.from_image(200, 100, 'clouds.png')
cloud1.scale_by(.09)
cloud2 = gamebox.from_image(510, 270, 'clouds.png')
cloud2.scale_by(.09)
cloud3 = gamebox.from_image(740, 50, 'clouds.png')
cloud3.scale_by(.1)


#Creating spritesheet for moving dino

sheet = gamebox.load_sprite_sheet("Dino sprite.png", 1, 6)
frame = 0
player_box = gamebox.from_image(100, 100, sheet[frame])  # gamebox image is first pic in sprite sheet
player_box.scale_by(.9)

def tick(keys):

    #Initializing global variables

    global timer
    global game_on
    global score
    global game_over
    global frame
    global base
    global cloud_pad

    #Initializing spritebox image

    frame += 1
    if frame == 6:
        frame = 0
    player_box.image = sheet[frame]

    #Starting game

    if pygame.K_SPACE in keys:
        if game_on == False:
            score = 0
            base = 0
        game_on = True

    if game_on:
        timer += 1
        if timer % 50 == 0:
            score += 10
        if timer % 200 == 0 and base > -15:
            base -= 1
        score_box = gamebox.from_text(700, 25, "Score " + str(score), 50, "black", italic=True)
        camera.clear("white")

        #Setting speed for cacti and clouds

        player_box.speedy += 2
        cactus1.speedx = base -10
        cactus2.speedx = base -10
        cloud1.speedx = base -6
        cloud2.speedx = base -6
        cloud3.speedx = base -6

        #Collision detection for cacti and dino

        if player_box.touches(cactus1, cactus_pad) or player_box.touches(cactus2, cactus_pad):
            camera.draw("Game Over", 36, "blue", [400, 200])
            game_over = True

        #Creating gravity

        if player_box.bottom_touches(ground_box):
            player_box.speedy = 0
            if pygame.K_SPACE in keys:
                player_box.speedy = -24

        #Respawns cacti at the right of the screen once it reaches the left side

        if cactus1.touches(wall):
            cactus1.x = 1000
            score += 10
        if cactus2.touches(wall):
            cactus2.x = 1000
            cactus2.speedx += -1
            score += 10
        if cloud1.touches(wall, cloud_pad):
            cloud1.x = 1000
            cloud1.speedx += -2
        if cloud2.touches(wall, cloud_pad):
            cloud2.x = 1000
            cloud2.speedx += -2
        if cloud3.touches(wall, cloud_pad):
            cloud3.x = 1000
            cloud3.speedx += -2

        #Move functions

        player_box.move_speed()
        cactus1.move_speed()
        cactus2.move_speed()
        cloud1.move_speed()
        cloud2.move_speed()
        cloud3.move_speed()
        player_box.move_to_stop_overlapping(ground_box)

        #Draw functions

        camera.draw(player_box)
        camera.draw(ground_box)
        camera.draw(cactus1)
        camera.draw(cactus2)
        camera.draw(cloud1)
        camera.draw(cloud2)
        camera.draw(cloud3)
        camera.draw(wall)
        camera.draw(score_box)
        camera.display()
    else:

        #Start and respawn screen

        camera.clear('white')
        camera.draw(start)
        if timer > 0:
            camera.draw("Your last score was " + str(score) + ".", 50, "black", [400, 500])
        camera.draw("DINO JUMP!", 100, "black", [400, 70])
        camera.draw("Press space to play", 30, "red", [400, 550])
        camera.display()
    if game_over:

        #Ends game when cacti is hit

        cactus1.x = 700
        cactus2.x = 1200
        camera.clear('white')
        gamebox.pause()
        time.sleep(1)
        game_on = False
        game_over = False
        gamebox.unpause()


ticks_per_second = 30
gamebox.timer_loop(30, tick)
