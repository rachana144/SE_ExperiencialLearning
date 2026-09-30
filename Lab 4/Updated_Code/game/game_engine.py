import pygame
from .snake import Snake
from .food import Food
from .sound import SoundEffects

# Game Engine

WHITE = (255, 255, 255)
GREY = (180, 180, 180)
GREEN = (0, 200, 0)
RED = (220, 60, 60)

# Ignore key presses for a moment after dying so a direction key the player
# was still hammering does not instantly dismiss the Game Over screen.
GAME_OVER_INPUT_DELAY_MS = 700

# Difficulty -> moves per second (all divide 60 evenly so the speeds are exact).
DIFFICULTIES = {
    pygame.K_1: ("Easy", 6),
    pygame.K_2: ("Medium", 10),
    pygame.K_3: ("Hard", 15),
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.sounds = SoundEffects()

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)

        self.moves_per_second = 8
        self._frame_counter = 0

        self.game_over = False
        self._game_over_time = 0

    def _end_game(self):
        self.game_over = True
        self._game_over_time = pygame.time.get_ticks()
        self.sounds.play_game_over()

    def restart(self, moves_per_second):
        # Start a fresh round at the chosen speed, reusing the existing
        # font/food objects. Food is re-spawned clear of the new snake.
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food.respawn(self.snake.body)
        self.score = 0
        self.moves_per_second = moves_per_second
        self._frame_counter = 0
        self.game_over = False
        self._game_over_time = 0

    def handle_keydown(self, key):
        # On the Game Over screen only 1/2/3 (restart) and Esc/Q (exit) do
        # anything. Arrow/WASD keys are ignored, and nothing is accepted for
        # a short delay after death, so a key still being pressed at the
        # moment of death can never skip the screen.
        if self.game_over:
            if pygame.time.get_ticks() - self._game_over_time < GAME_OVER_INPUT_DELAY_MS:
                return
            if key in DIFFICULTIES:
                self.restart(DIFFICULTIES[key][1])
            elif key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Direction changes are applied immediately on key press.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self._end_game()
            return

        if self.snake.collides_with_self():
            self._end_game()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self.sounds.play_eat()
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        # Dim the frozen final board, then draw the Game Over text on top.
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        cx = self.width // 2
        cy = self.height // 2

        title = self.title_font.render("GAME OVER", True, RED)
        score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        play = self.font.render("Play again:", True, GREY)
        choices = self.font.render("1 Easy    2 Medium    3 Hard", True, WHITE)
        quit_hint = self.font.render("Esc / Q to exit", True, GREY)

        screen.blit(title, title.get_rect(center=(cx, cy - 90)))
        screen.blit(score, score.get_rect(center=(cx, cy - 25)))
        screen.blit(play, play.get_rect(center=(cx, cy + 40)))
        screen.blit(choices, choices.get_rect(center=(cx, cy + 80)))
        screen.blit(quit_hint, quit_hint.get_rect(center=(cx, cy + 135)))