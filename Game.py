import pygame
from Chaser import Chaser
from player import Player
from utils import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Abarosh")
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.splash_screen = True
        self.chaser_score = 0
        self.chased_score = 0
        self.splash_animation_frames = []
        self.__load_splash_animation_frames()  # Load animation frames
        # Menu variables
        self.main_menu = True
        self.pause_menu = False
        self.selected_menu_index = 0

        # creating the players
        self.CHASER = Chaser(game=self, color=RED, speed=CHASER_SPEED)
        self.CHASED = Player(game=self, position=CHASED_INITIAL_POSITION, color=BLUE, speed=CHASED_SPEED)

        # play game_music
        game_music.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            # just starting and in main menu state
            if self.main_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_menu_index = (self.selected_menu_index - 1) % MAIN_MENU_COUNT
                    elif event.key == pygame.K_DOWN:
                        self.selected_menu_index = (self.selected_menu_index + 1) % MAIN_MENU_COUNT
                    elif event.key == pygame.K_RETURN:
                        self.__handle_menu_selection()

            # in paused state
            elif self.pause_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_menu_index = (self.selected_menu_index - 1) % PAUSE_MENU_COUNT
                    elif event.key == pygame.K_DOWN:
                        self.selected_menu_index = (self.selected_menu_index + 1) % PAUSE_MENU_COUNT
                    elif event.key == pygame.K_RETURN:
                        self.__handle_menu_selection()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        self.pause_menu = False

            else:
                if event.type == pygame.KEYDOWN:
                    # enter paused state
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        self.pause_menu = True
                        self.main_menu = False

        if not self.main_menu and not self.pause_menu:
            keys_pressed = pygame.key.get_pressed()  # for continuously pressed keys
            if keys_pressed[pygame.K_w]: self.CHASED.move(UP)
            if keys_pressed[pygame.K_s]: self.CHASED.move(DOWN)
            if keys_pressed[pygame.K_a]: self.CHASED.move(LEFT)
            if keys_pressed[pygame.K_d]: self.CHASED.move(RIGHT)
            if keys_pressed[pygame.K_UP]: self.CHASER.move(UP) 
            if keys_pressed[pygame.K_DOWN]: self.CHASER.move(DOWN)
            if keys_pressed[pygame.K_LEFT]: self.CHASER.move(LEFT)
            if keys_pressed[pygame.K_RIGHT]: self.CHASER.move(RIGHT)


    def check_game_over(self):
        chaser_rect = self.CHASER.get_rect()
        chased_rect = self.CHASED.get_rect()

        # chaser wins
        if chaser_rect.colliderect(chased_rect):
            self.chaser_score += 1
            self.CHASER.reset_position()
            self.CHASED.reset_position()
            self.load_winner(chaser_won=True)
        
        if chased_rect.colliderect(goal_zone):
            self.chased_score += 1
            self.CHASED.reset_position()
            self.load_winner(chaser_won=False)

    def __load_splash_animation_frames(self):
        # play music
        loading_sound.play()

        for i in range(0, 14):
            if i < 10:
                i = f"0{i}"

            frame = pygame.transform.scale(pygame.image.load(f"./images/splash_images/splash{i}.png").convert_alpha(),(800, 600))
            self.splash_animation_frames.append(frame)

    def show_splash_screen(self):
        frame_index = 0
        animation_delay = 125  # Delay between animation frames (in milliseconds)
        animation_timer = 0

        while self.splash_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Display animation frame
            self.screen.blit(self.splash_animation_frames[frame_index], (0, 0))

            pygame.display.flip()

            # Update animation frame
            animation_timer += self.clock.get_time()
            if animation_timer >= animation_delay:
                frame_index += 1
                animation_timer = 0

            # Break out of splash screen after all frames have been displayed
            if frame_index >= len(self.splash_animation_frames):
                break

            self.clock.tick(60)  # Limit frame rate
        pygame.time.wait(1800)  # Wait for 2 seconds after animation
        self.splash_screen = False

    def run(self):
        self.show_splash_screen()

        while self.is_running:
            self.handle_events()

            if self.main_menu:
                self.__show_main_menu()
                pygame.display.flip()

            elif self.pause_menu:
                # a blurry animation to make the selection menu looking good and lively
                blurred_bg = pygame.Surface(self.screen.get_size())
                blurred_bg.blit(self.screen, (0, 0))
                blurred_bg = blurred_bg.convert_alpha()
                blurred_bg.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(blurred_bg, (0, 0))

                self.__show_pause_menu()
                pygame.display.flip()

            else:
                self.check_game_over()
                self.draw_game_board()
                pygame.display.flip()

            # Limit frame rate
            self.clock.tick(10)


    def load_winner(self, chaser_won=True):
        # Display winner text
        font = pygame.font.SysFont("comic", 72)
        text = "Chaser Wins!" if chaser_won else "Chased Wins!"
        text_surf = font.render(text, True, pygame.Color("white"))
        text_rect = text_surf.get_rect(center=self.screen.get_rect().center)

        # Create a blurred background surface
        blurred_bg = pygame.Surface(self.screen.get_size())
        blurred_bg.blit(self.screen, (0, 0))
        blurred_bg = blurred_bg.convert_alpha()
        blurred_bg.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(blurred_bg, (0, 0))

        # Display winner text at the center of the screen
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()

        # Calculate the dimensions of the loading screen line
        line_length = self.screen.get_width() - 40
        line_height = 10
        line_color = pygame.Color("green")
        line_start_pos = (20, self.screen.get_height() // 20 * 19)

        # Draw the initial loading screen line
        pygame.draw.rect(self.screen, line_color, (line_start_pos, (0, line_height)))
        pygame.display.flip()

        game_music.stop()
        winning_sound.play()

        # Start the timer for 4 seconds
        timer = pygame.time.get_ticks()
        while pygame.time.get_ticks() - timer < 4000:
            progress = (pygame.time.get_ticks() - timer) / 4000
            progress_length = int(line_length * progress)

            # Update the loading screen line progress
            pygame.draw.rect(self.screen, line_color, (line_start_pos, (progress_length, line_height)))
            pygame.display.flip()

        winning_sound.stop()
        game_music.play()


    def draw_game_board(self):
        self.screen.fill((0, 0, 0)) # a fallback color

        self.screen.blit(pygame.transform.scale(field, (800, 600)),(0, 0)) # background field image
        self.__draw_top_fence()
        self.__draw_safe_zones()
        self.__draw_side_fence()


        self.__draw_tree_shadows()
        self.__draw_player_shadow(self.CHASER)
        self.CHASER.draw(self.screen)
        self.__draw_player_shadow(self.CHASED)
        self.CHASED.draw(self.screen)

        # show trees / obstacles
        self.__draw_obstacles()
        self.__draw_bottom_fence()
        self.__dispay_panel()

        pygame.display.flip()


    def new_game(self):
        self.chaser_score = 0
        self.chased_score = 0
        self.CHASER = Chaser(game=self, color=RED, speed=CHASER_SPEED)
        self.CHASED = Player(game=self, position=CHASED_INITIAL_POSITION, color=BLUE, speed=CHASED_SPEED)
        self.main_menu = False
        self.pause_menu = False


    def __draw_safe_zones(self):
        for index in range(len(safe_zones)-1):
            safe_zone = safe_zones[index]
            # shrink the safe zone by 5 pixels on each side
            safe_zone = safe_zone.inflate(-25, -25)
            pygame.draw.rect(self.screen, BROWN, safe_zone)    # brown background
            pygame.draw.rect(self.screen, BLUE, safe_zone, 5)  # blue border
            self.screen.blit(pygame.transform.scale( house, (100, 100))
                             ,(safe_zone.x, safe_zone.y)) # house
        
        # for the bottom right corner show the goal
        self.screen.blit(pygame.transform.scale( goal, (50, 50)),(700, 500))
        # show text in blue saying "GOAL" on top of the goal
        font = pygame.font.SysFont("comic", 24)
        text = "GOAL"
        text_rect = font.render(text, True, BLUE)
        text_rect_rectangle = pygame.Rect(0, 0, 0, 0)
        text_rect_rectangle.center = (705, 525)
        self.screen.blit(text_rect, text_rect_rectangle)


    def __draw_top_fence(self):
        # around the top and bottom
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 0))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            # rotate the shadow 45 degrees
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (i, 0))


    def __draw_side_fence(self):
        # aroung the sides
        for i in range(0, 600, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(0, i))
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(750, i))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (0, i))
            self.screen.blit(shadow, (750, i))


    def __handle_menu_selection(self):
        # in side main menu
        if self.main_menu:
            if self.selected_menu_index == 0:
                self.new_game() # start new game

            elif self.selected_menu_index == 1:
                pygame.quit()
        
        # in side pause menu
        elif self.pause_menu:
            if self.selected_menu_index == 0:
                self.pause_menu = False

            elif self.selected_menu_index == 1:
                self.new_game()

            elif self.selected_menu_index == 2:
                pygame.quit()


    def __draw_bottom_fence(self):
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 550))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (i, 550))


    def __dispay_panel(self):
        # Display scores
        font = pygame.font.SysFont("Comic Sans", 30)
        chaser_score_text = font.render(f"Chaser Score: {self.chaser_score}", True, WHITE)
        chased_score_text = font.render(f"Chased Score: {self.chased_score}", True, WHITE)
        self.screen.blit(chaser_score_text, (10, 5))
        self.screen.blit(chased_score_text, (10, 50))

        # display controls
        font = pygame.font.SysFont("Comic Sans", 15)
        controls_text = font.render("Chaser Controls: WASD, Chased Controls: Arrow Keys, ESC to quit", True, WHITE)
        controls_text_area = controls_text.get_rect()
        controls_text_area.center = ( self.screen.get_rect().width //2 + 85, 15)
        self.screen.blit(controls_text, controls_text_area)


    def __show_pause_menu(self):
        # Display pause menu options
        font = pygame.font.SysFont("Comic Sans", 40)
        play_text = font.render("> Play"  if self.selected_menu_index == 0 else "Play", True, WHITE if self.selected_menu_index == 0 else GRAY)
        new_game_text = font.render("> New Game" if self.selected_menu_index == 1 else "New Game", True, WHITE if self.selected_menu_index == 1 else GRAY)
        quit_text = font.render("> Quit" if self.selected_menu_index == 2  else "Quit", True, WHITE if self.selected_menu_index == 2 else GRAY)

        # Calculate option positions
        play_pos = (self.WIDTH // 2 - play_text.get_width() // 2, self.HEIGHT // 2 - play_text.get_height())
        new_game_pos = (self.WIDTH // 2 - new_game_text.get_width() // 2, self.HEIGHT // 2)
        quit_pos = (self.WIDTH // 2 - quit_text.get_width() // 2, self.HEIGHT // 2 + quit_text.get_height())

        # Display options on the screen
        self.screen.blit(play_text, play_pos)
        self.screen.blit(new_game_text, new_game_pos)
        self.screen.blit(quit_text, quit_pos)


    def __draw_obstacles(self):
        for circular_obstacle in obstacles:
            self.screen.blit(pygame.transform.scale(tree, (60, 80)), (circular_obstacle.centerx - 35, circular_obstacle.centery - 60))


    def __draw_tree_shadows(self):
        for circular_obstacle in obstacles:
            shadow_radius = 25
            shadow = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (0, 0, 0, 100), (shadow_radius, shadow_radius), shadow_radius)
            self.screen.blit(shadow, (circular_obstacle.centerx - shadow_radius, circular_obstacle.centery - shadow_radius))


    def __draw_player_shadow(self, player: Player):
        shadow_radius = 12
        shadow = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 100), (shadow_radius, shadow_radius), shadow_radius)
        self.screen.blit(shadow, (player.position[0] - shadow_radius, player.position[1] - shadow_radius))


    def __show_main_menu(self):
        # clearing screen
        self.screen.fill(BLACK)
        # Display main menu options
        font = pygame.font.SysFont("Comic Sans", 40)
        new_game_text = font.render("> New Game" if self.selected_menu_index == 0 else "New Game" , True, WHITE if self.selected_menu_index == 0 else GRAY)
        quit_text = font.render("> Quit" if self.selected_menu_index == 1 else "Quit", True, WHITE if self.selected_menu_index == 1 else GRAY)

        # Calculate option positions
        new_game_pos = (self.WIDTH // 2 - new_game_text.get_width() // 2, self.HEIGHT // 2 - new_game_text.get_height())
        quit_pos = (self.WIDTH // 2 - quit_text.get_width() // 2, self.HEIGHT // 2)

        # Display options on the screen
        self.screen.blit(new_game_text, new_game_pos)
        self.screen.blit(quit_text, quit_pos)
