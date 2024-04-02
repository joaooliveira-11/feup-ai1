import pygame
import time
import settings

class Dashboard:
    def __init__(self, screen):
        self.font = pygame.font.Font("./font/NotJamChunky8.ttf", 22)
        self.screen = screen
        self.nrMoves = 0
        self.time = 0
        self.ticks = 0
        
    def drawText(self, text, x, y):

        """
            Draw text on the screen
        """
        self.screen.blit(self.font.render(text, 1, (255, 255, 255)), (x, y))


class HumanDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        # Load the arrow images
        self.keys = {
            'up': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/arrow_up.png'), (50, 50)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/arrow_up_w.png'), (50, 50))
            },
            'down': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/arrow_down.png'), (50, 50)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/arrow_down_w.png'), (50, 50))
            },
            'left': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/arrow_left.png'), (50, 50)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/arrow_left_w.png'), (50, 50))
            },
            'right': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/arrow_right.png'), (50, 50)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/arrow_right_w.png'), (50, 50))
            },
            'space': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/space-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/space-w.png'), (70, 70))
            },
            'z': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/letter-z-p.png'), (60, 60)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/letter-z-w.png'), (60, 60))
            }
        }

        self.key_states = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'space': False,
            'z': False
        }
    
    def update(self):

        """
            Update the dashboard
        """

        self.ticks += 1
        if self.ticks % settings.MAX_FRAME_RATE == 0 :
            self.time += 1
        self.draw()

    def draw(self):

        """
            Draw the human dashboard
        """

        self.drawText("Player: Human", 30, 30)
        self.drawText(f"Moves: {self.nrMoves}", 30, 60)
        self.drawText(f"Time: {self.time}", 30, 90)

        key_size = self.keys['up']['black'].get_size()
        key_y = 600 - key_size[1] - 10
        key_x = 10

        key_positions = {
            'up': (key_x + key_size[0], key_y - key_size[1]),
            'down': (key_x + key_size[0], key_y),
            'left': (key_x, key_y),
            'right': (key_x + key_size[0] * 2, key_y),
            'space': (30, 180),
            'z': (30, 280) 
        }
        
        for key in ['up', 'down', 'left', 'right', 'space', 'z']:
            color = 'white' if self.key_states[key] else 'black'
            self.screen.blit(self.keys[key][color], key_positions[key])
        
        self.drawText("Hints", key_positions['space'][0], key_positions['space'][1] - 15)
        self.drawText("Undo", key_positions['z'][0], key_positions['z'][1] - 20)



class BfsDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }
        

    def update(self):

        """
            Update the dashboard
        """
        self.draw()

    def draw(self):

        """
            Draw the BFS dashboard
        """

        self.drawText("Player: Bfs", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90) 

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])

class DfsDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }

    def update(self):

        """
            Update the dashboard
        """
        self.draw()

    def draw(self):

        """
            Draw the DFS dashboard
        """

        self.drawText("Player: Dfs", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90)

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])

class IDDfsDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }

    def update(self):

        """
            Update the dashboard
        """

        self.draw()

    def draw(self):

        """
            Draw the IDDFS dashboard
        """
        self.drawText("Player: IDDfs", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90)

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])

class AStarDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }

    def update(self):

        """
            Update the dashboard
        """

        self.draw()

    def draw(self):

        """
            Draw the A* dashboard
        """

        self.drawText("Player: A*", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90)

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])

class IDAStarDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }

    def update(self):
        """
            Update the dashboard
        """
        self.draw()

    def draw(self):
        """
            Draw the IDA* dashboard
        """        
        self.drawText("Player: IDA*", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90)

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])

class MonteCarloDashboard(Dashboard):
    def __init__(self, screen):
        super().__init__(screen)

        self.keys = {
            'enter': {
                'black': pygame.transform.scale(pygame.image.load('./sprites/enter-p.png'), (70, 70)),
                'white': pygame.transform.scale(pygame.image.load('./sprites/enter-w.png'), (70, 70))
            }
        }

        self.key_states = {
            'enter': False
        }

    def update(self):
        """
            Update the dashboard
        """
        self.draw()

    def draw(self):
        """
            Draw the Monte Carlo dashboard
        """
        self.drawText("Player: MonteCarlo", 30, 30) 
        self.drawText(f"Moves: {self.nrMoves}", 30, 60) 
        self.drawText(f"Time: {self.time}", 30, 90)

        key_positions = {
            'enter': (30, 180)
        }

        self.drawText("Move", key_positions['enter'][0], key_positions['enter'][1] - 15)
        color = 'white' if self.key_states['enter'] else 'black'
        self.screen.blit(self.keys['enter'][color], key_positions['enter'])
