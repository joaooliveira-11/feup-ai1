import sys
import pygame

from src.menu import Menu
from src.level import Level
import settings

settings.init()

def main():

    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    pygame.display.set_caption('ChessKoban')
    level = Level(screen)
    menu = Menu(screen, level)
        
    clock = pygame.time.Clock()

    while menu.current_state != "exit":
        pygame.display.set_caption("Running at " + str(int(clock.get_fps())) + " fps")
        if menu.current_state != "game":
            menu.update()
        else:
            level.update()

            if level.player.leave == True:
                menu.current_state = "menu"
                level.player.leave = False
            
            if level.gamewin:
                menu.current_state = "nextLevel"
                level.gamewin = False
                

        pygame.display.update()
        clock.tick(settings.MAX_FRAME_RATE)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()