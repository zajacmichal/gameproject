import os

import pygame

import game_module_1 as gm


# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.movement_x = 0
        self.movement_y = 0
        self.state = 'start'
        self.step = 0
        self.level = None
        self.movement_direction = 'right'

        self.board_x = 0
        self.board_y = 0
        self.next_step = 0
        self.step_value = 2
        self.possible_steps = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reveal_board(self): #
        pos = [(self.rect.x + 60, self.rect.y), (self.rect.x, self.rect.y + 60),
               (self.rect.x - 60, self.rect.y), (self.rect.x, self.rect.y - 60),
               (self.rect.x, self.rect.y)]

        for bp in pos:
            for b in self.level.set_of_blocks:
                if b.rect.x == bp[0] and b.rect.y == bp[1]:
                    self.level.set_of_blocks.remove(b)
                    break

    def collision_detection(self):
        colliding_walls = pygame.sprite.spritecollide(self, self.level.set_of_walls, False)
        for w in colliding_walls:
            if self.movement_x < 0:
                self.rect.left = w.rect.right
                self.state = 'stop'
                self.movement_x = 0
            elif self.movement_x > 0:
                self.rect.right = w.rect.left
                self.state = 'stop'
                self.movement_x = 0
            elif self.movement_y < 0:
                self.rect.top = w.rect.bottom
                self.state = 'stop'
                self.movement_y = 0
            elif self.movement_y > 0:
                self.rect.bottom = w.rect.top
                self.state = 'stop'
                self.movement_y = 0

    def next_step_detection(self):
        self.board_x = (self.rect.x - self.level.map_position[0]) // 60
        self.board_y = (self.rect.y - self.level.map_position[1]) // 60

        board_pos = [(self.board_x + 1, self.board_y), (self.board_x, self.board_y + 1),
                     (self.board_x - 1, self.board_y), (self.board_x, self.board_y - 1)]

        # checking possible next step
        self.possible_steps = []
        for bp in board_pos:
            if bp[0] in range(0, self.level.map_size[0]) and bp[1] in range(0, self.level.map_size[1]):
                if self.level.board[bp[1]][bp[0]] != 1:
                    self.possible_steps.append([bp[0], bp[1], self.level.board[bp[1]][bp[0]]])
        # removing previous position from possible next steps
        if len(self.possible_steps) >= 2:
            for ps in self.possible_steps:
                if self.movement_direction == 'right' and ps[0] == self.board_x - 1:
                    self.possible_steps.remove(ps)
                if self.movement_direction == 'down' and ps[1] == self.board_y - 1:
                    self.possible_steps.remove(ps)
                if self.movement_direction == 'left' and ps[0] == self.board_x + 1:
                    self.possible_steps.remove(ps)
                if self.movement_direction == 'up' and ps[1] == self.board_y + 1:
                    self.possible_steps.remove(ps)
        # checking crossroads
        if len(self.possible_steps) >= 2 and self.level.board[self.board_y][self.board_x] == 0:
            self.step_value += 1
        if self.level.board[self.board_y][self.board_x] == 0:
            self.level.board[self.board_y][self.board_x] = self.step_value

        if len(self.possible_steps) == 1:
            self.next_step = (self.possible_steps[0][0], self.possible_steps[0][1])
        else:
            step_min = self.possible_steps[0]
            for m in self.possible_steps[1:]:
                if m[2] < step_min[2]:
                    step_min = m
            self.next_step = (step_min[0], step_min[1])

    def update(self):
        if self.state == 'start':
            # revealing board at start state
            self.reveal_board()
            self.next_step_detection()
            self.state = 'stop'

        if self.state == 'moving':
            # move all directions
            self.rect.x += self.movement_x
            self.rect.y += self.movement_y

            # detecting collision
            self.collision_detection()

            # checking steps
            self.step += self.movement_x + self.movement_y

            # moving by step - state before stop
            if self.step == 60 or self.step == -60:
                self.step = 0
                self.state = 'stop'
                self.movement_x = 0
                self.movement_y = 0

                self.reveal_board()

                self.board_x = (self.rect.x - self.level.map_position[0]) // 60
                self.board_y = (self.rect.y - self.level.map_position[1]) // 60
                curr_step = (self.board_x, self.board_y)

                if curr_step == self.level.end_position:
                    self.state = 'completed'
                elif curr_step != self.next_step:
                    self.rect.x = self.level.player_start_position[0]
                    self.rect.y = self.level.player_start_position[1]

                    self.state = 'start'

                    # reset board
                    self.step_value = 2
                    for y in range(0, len(self.level.board)):
                        for x in range(0, len(self.level.board[0])):
                            if self.level.board[y][x] != 1:
                                self.level.board[y][x] = 0
                else:
                    self.next_step_detection()
    #keys movement
    def get_event(self, event):
        speed = 10

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.state != 'moving':
                    self.state = 'moving'
                    self.movement_direction = 'left'
                    self.image = gm.MY_PLAYER_L
                    self.movement_x = speed * -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.state != 'moving':
                    self.state = 'moving'
                    self.movement_direction = 'right'
                    self.image = gm.MY_PLAYER_R
                    self.movement_x = speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.state != 'moving':
                    self.state = 'moving'
                    self.movement_direction = 'up'
                    self.image = gm.MY_PLAYER_UP
                    self.movement_y = speed * -1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.state != 'moving':
                    self.state = 'moving'
                    self.movement_direction = 'down'
                    self.image = gm.MY_PLAYER_DOWN
                    self.movement_y = speed

#drawing texture
class Plate(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, texture):
        super().__init__()
        self.width = 60
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.texture = texture

    def draw(self, surface):
        surface.blit(self.texture, self.rect)

    def __repr__(self):
        return f"({self.rect.x} {self.rect.y})"


class Level:
    def __init__(self, player, position, board):
        self.player = player
        self.set_of_walls = set()
        self.set_of_paths = set()
        self.set_of_blocks = []

        self.map_position = position
        self.board = board
        self.player_start_position = 0
        self.end_position = 0
        self.map_size = [len(board[0]), len(board)]

        map_x = position[0]
        map_y = position[1]
        for line in self.board:
            # blocks_in_line = []
            for col in line:
                if col == 1:
                    self.set_of_walls.add(Plate(map_x, map_y, gm.WALL))
                if col == 0:
                    self.set_of_paths.add(Plate(map_x, map_y, gm.PATH))
                self.set_of_blocks.append(Plate(map_x, map_y, gm.BLOCK))
                map_x += 60
            map_x -= 60 * len(self.board[0])
            map_y += 60

    def draw(self, surface):
        for w in self.set_of_walls:
            w.draw(surface)
        for p in self.set_of_paths:
            p.draw(surface)
        for b in self.set_of_blocks:
            b.draw(surface)

    def update(self):
        for b in self.set_of_blocks:
            b.update()


class Level1(Level):
    def __init__(self, player):
        # board position and structure
        position = [360, 120]
        board = [[1] * 18,
                 [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                 [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                 [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
                 [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]]

        super().__init__(player, position, board)
        # player position
        self.player_start_position = (360, 180)
        self.player.rect.x = self.player_start_position[0]
        self.player.rect.y = self.player_start_position[1]
        self.end_position = (14, 9)


class Level2(Level):
    def __init__(self, player):
        # board position and structure
        position = [360, 120]
        board = [[1] * 7,
                 [0, 0, 0, 0, 1, 0, 1],
                 [1, 1, 1, 0, 1, 0, 0],
                 [1, 1, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1],
                 [1, 1, 0, 0, 0, 0, 1],
                 [1] * 7]

        super().__init__(player, position, board)
        # player position
        self.player_start_position = (360, 180)
        self.player.rect.x = self.player_start_position[0]
        self.player.rect.y = self.player_start_position[1]
        self.end_position = (6, 2)


class Text:
    def __init__(self, text, color, size=62):
        self.text = text
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont('Comic Sans MS', self.size)
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Game:
    def __init__(self):
        # objects initialize
        self.player = Player(gm.MY_PLAYER)
        self.currentLevel = Level1(self.player)
        self.player.level = self.currentLevel
        self.wait = 0
        # player.rect.center = screen.get_rect().center

        # window - center
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # setting screen and game
        #self.screen = pygame.display.set_mode(gm.SCREEN_SIZE)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Python mini game - project 1 typ II')
        clock = pygame.time.Clock()

        # font
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 10)

        # game main loop
        window_open = True
        while window_open:
            self.screen.blit(gm.MAZE, [0, 0])

            # loop with actions
            for event in pygame.event.get():
                self.player.get_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        window_open = False
                elif event.type == pygame.QUIT:
                    window_open = False

            # drawing objects and update
            self.draw()
            self.update()

            # info box
            text_surface = my_font.render(f"x:{self.player.rect.x} y:{self.player.rect.y}", False, (0, 0, 0))
            self.screen.blit(text_surface, (20, 10))
            text_surface = my_font.render(
                f"pos: {self.player.board_x} {self.player.board_y}    {self.player.possible_steps}", False, (0, 0, 0))
            self.screen.blit(text_surface, (20, 20))
            text_surface = my_font.render(f"next: {self.player.next_step}", False, (0, 0, 0))
            self.screen.blit(text_surface, (20, 30))
            text_surface = my_font.render(f"lvl val: {self.player.step_value}", False, (0, 0, 0))
            self.screen.blit(text_surface, (20, 40))
            # text_surface = my_font.render(f"board: {self.currentLevel.board}", False, (0, 0, 0))
            # self.screen.blit(text_surface, (20, 50))

            # end level
            if self.player.state == 'completed':
                self.wait += 1
            if self.player.state == 'completed' and self.wait == 10:
                end_text = Text("CONGRATULATIONS YOU COMPLETED GAME", gm.DARKGREEN)
                end_text.rect.center = self.screen.get_rect().center

                pygame.time.delay(500)
                self.screen.fill(gm.LIGHTBLUE)
                end_text.draw(self.screen)
                pygame.display.flip()
                pygame.time.delay(1000)
                break

            # window update
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def draw(self):
        self.currentLevel.draw(self.screen)
        self.player.draw(self.screen)

    def update(self):
        self.player.update()


labyrinth = Game()


