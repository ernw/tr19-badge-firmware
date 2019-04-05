import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((296, 128))
pygame.display.set_caption('Troopers Badge 19')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

screen.blit(background, (0, 0))
pygame.display.flip()

try:
    process = subprocess.Popen(['./micropython', 'test.py'], stdout=subprocess.PIPE)
    display_update = False
    display_line = 0
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = output.strip()
            if line == b'---INIT DISPLAY UPDATE---':
                display_line = 0
                display_update = True
            elif line == b'---DONE DISPLAY UPDATE---':
                display_update = False
                pygame.display.update()
            elif display_update:
                for i, c in enumerate(line.decode('ascii')):
                    #pygame.draw.rect(screen, (255, 255, 255) if c == '1' else (0, 0, 0), (i, display_line, 1, 1), 0)
                    screen.set_at((i, display_line),  (255, 255, 255) if c == '1' else (0, 0, 0))
                display_line += 1
            else:
                print(line.decode('ascii'))
    rc = process.poll()
    print(rc)
except KeyboardInterrupt:
    print("Exiting")
    pygame.display.quit()
    pygame.quit()
