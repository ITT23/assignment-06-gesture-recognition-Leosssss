# application for task 3
# mp3 from: https://www.youtube.com/watch?v=mRD0-GxqHVo&t=1s

import pygame

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
CANVAS_WIDTH = 350
CANVAS_HEIGHT = 350
MP3_PATH = "Glass_Animals_Heat_Waves.mp3"

current_position = 0

# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.mixer.music.load(MP3_PATH)

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill((255, 255, 255)) 

def play_music(current_position):
    pygame.mixer.music.play(start=current_position/1000)

def pause_music():
    global current_position
    current_position = pygame.mixer.music.get_pos()
    pygame.mixer.music.pause()

def restart_music():
    global current_position
    current_position = 0
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_music()
                print("stop: "+str(current_position))
            elif event.key == pygame.K_s:
                play_music(current_position)
                print("start: "+str(current_position))
            elif event.key == pygame.K_r: 
                restart_music()
                
    window.fill("#Ffa500")
    window.blit(canvas, ((WINDOW_WIDTH - CANVAS_WIDTH)/2, (WINDOW_HEIGHT - CANVAS_HEIGHT)/2 - 60))
    

    button_font = pygame.font.Font(None, 24)
    play_button = button_font.render("Press 's' or draw 's' to start", True, (250, 250, 250))
    pause_button = button_font.render("Press 'p' or draw 'o' to pause", True, (250, 250, 250))
    restart_button = button_font.render("Press 'r' or draw 'v' to restart", True, (250, 250, 250))
    window.blit(play_button, (WINDOW_WIDTH/2 - 60, 380))
    window.blit(pause_button, (WINDOW_WIDTH/2 - 60, 410))
    window.blit(restart_button, (WINDOW_WIDTH/2 - 60, 440))

    pygame.display.flip()
