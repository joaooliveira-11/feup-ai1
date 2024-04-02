import os
import pygame
import sys

from src.level import Level

class Menu:
    def __init__(self, screen, level: Level):
        self.screen = screen

        self.isInRules = False

        self.option = ["start", "choosingPlayer", "choosingLevel", "inRules", "inExit"]
        self.current_option = 0

        self.state = ["menu", "inRules", "game", "exit", "finish"]
        self.current_state = "menu"

        self.players = ["Human", "Bfs", "Dfs", "IDDfs", "A*", "Uniform", "Greedy", "Weighted A*", "IDA*"]
        self.selected_player = 0

        self.level = level
        self.selected_level = 0
        self.current_level = self.selected_level 
        self.next_level_selected = True
        
        # Read directory and get the number of levels
        DIR = './levels'
        self.nr_levels = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        self.font = pygame.font.Font("./font/NotJamChunky8.ttf", 22)

        self.pawnSprite = pygame.image.load('./sprites/pawn.png')
        self.whiteKnightSprite = pygame.image.load('./sprites/knight-white.png')

    def update(self):

        """
            Update the menu screen
        """
        
        self.checkInputs()
        
        if self.current_state == "inRules":
            self.drawRules()
        elif self.current_state == "nextLevel":
            if self.current_level == self.nr_levels -1:
                self.current_state = "finish"
            else: self.drawNextLevelMenu()
        elif self.current_state == "finish":
            self.drawFinishMenu()
        else:
            self.drawMenu()

    def checkInputs(self):

        """
            Check the inputs of the user and updates the current state
        """

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN: # if a key is pressed

                if event.key == pygame.K_ESCAPE:
                    if self.current_state == "inRules":
                        self.current_option = 0
                        self.selected_player = 0
                        self.selected_player = 0
                        self.selected_level = 0
                        self.current_level = self.selected_level 
                        self.next_level_selected = True
                        self.current_state = "menu"
                    else:
                        pygame.quit()
                        sys.exit()

                if event.key == pygame.K_DOWN:
                    self.current_option += 1
                    self.current_option %= len(self.option)

                if event.key == pygame.K_UP:
                    self.current_option -= 1
                    self.current_option %= len(self.option)

                if event.key == pygame.K_RETURN:
                    if self.current_state == "nextLevel":
                        if self.next_level_selected:
                            self.current_state = "game"
                            self.level.loadNextLevel(self.current_level +1, self.players[self.selected_player])
                            self.current_level += 1
                        else:
                            self.current_state = "menu"
                        break
                    if self.current_state == "finish":
                        if self.next_level_selected:
                            self.current_state = "menu"
                        else:
                            self.current_state = "exit"
                        break

                    if self.option[self.current_option] == "start":
                        self.level.loadLevel(self.selected_level +1, self.players[self.selected_player])
                        self.current_state = "game"
                    if self.option[self.current_option] == "inRules":
                        self.current_state = "inRules"
                    if self.option[self.current_option] == "inExit":
                        self.current_state = "exit"


                if event.key == pygame.K_LEFT:
                    if self.current_state == "nextLevel":
                        self.next_level_selected = not self.next_level_selected
                        break
                    if self.current_state == "finish":
                        self.next_level_selected = not self.next_level_selected
                        break

                    if self.option[self.current_option] == "choosingPlayer":
                        self.selected_player -= 1
                        self.selected_player %= len(self.players)

                    if self.option[self.current_option] == "choosingLevel":
                        self.selected_level -= 1
                        self.selected_level %= self.nr_levels
                        self.current_level = self.selected_level
                
                if event.key == pygame.K_RIGHT:
                    if self.current_state == "nextLevel":
                        self.next_level_selected = not self.next_level_selected
                        break
                    if self.current_state == "finish":
                        self.next_level_selected = not self.next_level_selected
                        break

                    if self.option[self.current_option] == "choosingPlayer":
                        self.selected_player += 1
                        self.selected_player %= len(self.players)

                    if self.option[self.current_option] == "choosingLevel":
                        self.selected_level += 1
                        self.selected_level %= self.nr_levels
                        self.current_level = self.selected_level


        
    def drawMenu(self):

        """
            Draw the menu screen
        """

        self.screen.fill((59, 61, 122))

        text = self.font.render("ChessKoban", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))

        for i in range(len(self.option)):
            if i == self.current_option:
                color = (117, 122, 255)
            else:
                color = (255, 255, 255)
            self.drawOption(self.option[i], color, i)

        resized_sprite = pygame.transform.scale(self.whiteKnightSprite, (250, 250))
        self.screen.blit(resized_sprite, (410, 160))

        resized_sprite = pygame.transform.scale(self.pawnSprite, (250, 250))
        self.screen.blit(resized_sprite, (490, 230))

        pygame.display.update()

    def drawOption(self, option, color, i):

        """
            Draw the options of the menu screen
        """

        if option == "start":
            text = self.font.render("Start", True, color)
            self.screen.blit(text, (100, 200 + i*50))
        if option == "choosingPlayer":
            leftarrow = self.font.render("<", True, color)
            self.screen.blit(leftarrow, (80, 200 + i*50))
            text = self.font.render(self.players[self.selected_player], True, color)
            self.screen.blit(text, (100, 200 + i*50))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (text.get_rect().size[0] + 105, 200 + i*50))
        if option == "choosingLevel":
            leftarrow = self.font.render("<", True, color)
            self.screen.blit(leftarrow, (80, 200 + i*50))
            text = self.font.render("Level " + str(self.selected_level +1), True, color)
            self.screen.blit(text, (100, 200 + i*50))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (text.get_rect().size[0] + 105, 200 + i*50))
        if option == "inRules":
            text = self.font.render("Rules", True, color)
            self.screen.blit(text, (100, 200 + i*50))
        if option == "inExit":
            text = self.font.render("Exit", True, color)
            self.screen.blit(text, (100, 200 + i*50))

    def drawRules(self):

        """
            Draw the rules screen
        """

        self.screen.fill((59, 61, 122))

        rules = self.font.render("Rules", True, (255,255,255))
        self.screen.blit(rules, (20, 30))

        subtitle_font = pygame.font.Font("./font/NotJamChunky8.ttf", 14)
        text_font = pygame.font.Font(None, 22)

        rules_goal = [
            "ChessKoban is a chess variant that combines elements of Chess and Sokoban.",
            "The goal is to move the white knights to positions where they can capture the black knights.",
            "Each white knight can only capture a single black knight.",
            "For this, the movement of the white pawn needs to be used.",
            "The game is won when all black knights are being captured at the same time",
            "by the white knights.",
        ]
        
        rules_gamemodes = [
            "Chesskoban has two main gamemodes: Human and AI.",
            "In the Human gamemode, the player can control the white pawn.",
            "In the AI gamemode, the player can choose between different algorithms to solve the game."
        ]

        rules_controls = [
            "In the Human gamemode, the player can use the Arrow keys to move the white pawn.",
            "In the AI game mode, the player can use the Enter key to move the white pawn along the calculated path."
        ]

        rules_extra = [
            "In the human gamemode, the player can press the Z key to undo the last move.",
            "In the human gamemode, the player can press the Space key to ask for a hint."
        ]

        sections = [
            ("Goal", rules_goal),
            ("Gamemodes", rules_gamemodes),
            ("Controls", rules_controls),
            ("Extra", rules_extra)
        ]

        y = 50 
        for title, rules in sections:
            y += 30 
            subtitle = subtitle_font.render(title, True, (255,255,255))
            self.screen.blit(subtitle, (20, y))

            for rule in rules:
                y += 20
                rule_text = text_font.render(rule, True, (255,255,255))
                self.screen.blit(rule_text, (20, y))

            y += 8

        pygame.display.update()
    
    def drawNextLevelMenu(self):

        """
            Draw the next level screen
        """

        self.screen.fill((59, 61, 122))
        text = self.font.render("Do you want to play the next level?", True, (255,255,255))
        self.screen.blit(text, (170, 100))

        if self.next_level_selected:
            color = (117, 122, 255)
            leftarrow = self.font.render("<", True, color)
            self.screen.blit(leftarrow, (400, 200))
            text = self.font.render("Yes", True, color)
            self.screen.blit(text, (420, 200))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (480, 200))
            text = self.font.render("No", True, (255,255,255))
            self.screen.blit(text, (520, 200))
        else:
            color = (117, 122, 255)
            text = self.font.render("Yes", True, (255,255,255))
            self.screen.blit(text, (420, 200))
            leftarrow = self.font.render("<", True, color)
            self.screen.blit(leftarrow, (500, 200))
            text = self.font.render("No", True, color)
            self.screen.blit(text, (520, 200))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (570, 200))

        pygame.display.update()

    def drawFinishMenu(self):

        """
            Draw the finish screen after the user wins all levels
        """

        self.screen.fill((59, 61, 122))
        text = self.font.render("Congratulations! You won the game!", True, (255,255,255))
        self.screen.blit(text, (170, 100))

        if self.next_level_selected:
            color = (117, 122, 255)
            leftarrow = self.font.render("<", True, color)
            text = self.font.render("Retry", True, color)
            self.screen.blit(leftarrow, (480 - text.get_rect().size[0] - 20, 200))
            self.screen.blit(text, (480 - text.get_rect().size[0], 200))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (480, 200))
            text = self.font.render("Exit", True, (255,255,255))
            self.screen.blit(text, (520, 200))
        else:
            color = (117, 122, 255)
            text = self.font.render("Retry", True, (255,255,255))
            self.screen.blit(text, (480 - text.get_rect().size[0], 200))
            leftarrow = self.font.render("<", True, color)
            self.screen.blit(leftarrow, (500, 200))
            text = self.font.render("Exit", True, color)
            self.screen.blit(text, (520, 200))
            rightarrow = self.font.render(">", True, color)
            self.screen.blit(rightarrow, (500 + text.get_rect().size[0] + 20, 200))

        pygame.display.update()