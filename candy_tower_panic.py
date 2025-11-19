import pygame
import random
import sys

ROWS = 20
COLS = 10
CELL_SIZE = 48  

BOARD_WIDTH = COLS * CELL_SIZE      
BOARD_HEIGHT = ROWS * CELL_SIZE      

INFO_PANEL_WIDTH = 600
TOTAL_GAME_WIDTH = BOARD_WIDTH + INFO_PANEL_WIDTH

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

FPS = 60

EMPTY = 0
NUM_TYPES = 5  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (80, 80, 80)
GREEN = (80, 255, 80)
RED = (255, 80, 80)
YELLOW = (255, 255, 80)

CANDY_COLORS = {
    1: (255, 80, 80),   # red
    2: (80, 80, 255),   # blue
    3: (80, 255, 80),   # green
    4: (255, 255, 80),  # yellow
    5: (200, 80, 255),  # purple
}

# Game states
STATE_RUNNING = 0
STATE_WON = 1
STATE_LOST = 2

# Scenes
SCENE_MAIN_MENU = "main_menu"
SCENE_MODE_SELECT = "mode_select"
SCENE_DIFFICULTY = "difficulty"
SCENE_OPTIONS = "options"
SCENE_AUDIO = "audio"
SCENE_CONTROLS = "controls"
SCENE_CREDITS = "credits"
SCENE_GAME = "game"

# Modes
MODE_SCORE = "score"  # Sweet Target
MODE_TIME = "time"    # Sugar Rush

# Audio
BGM_MENU_FILE = "sounds/bgm_menu.ogg"
BGM_GAME_FILE = "sounds/bgm_game.ogg"
SFX_CLICK_FILE = "sounds/sfx_click.wav"
SFX_CLEAR_FILE = "sounds/sfx_clear.wav"
SFX_GAMEOVER_FILE = "sounds/sfx_gameover.wav"
SFX_WIN_FILE = "sounds/sfx_win.wav"
SFX_HOVER_FILE = "sounds/sfx_hover.wav"

GAME_OFFSET_X = (WINDOW_WIDTH - TOTAL_GAME_WIDTH) // 2
GAME_OFFSET_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2
BOARD_ORIGIN_X = GAME_OFFSET_X
BOARD_ORIGIN_Y = GAME_OFFSET_Y
PANEL_ORIGIN_X = GAME_OFFSET_X + BOARD_WIDTH
PANEL_ORIGIN_Y = GAME_OFFSET_Y

TEXTS = {
    "TITLE": "Candy Tower Panic",
    "BTN_PLAY": "Play",
    "BTN_CHOOSE_DIFFICULTY": "Choose Difficulty",
    "BTN_OPTIONS": "Options",
    "BTN_AUDIO": "Audio",
    "BTN_BACK": "Back",
    "BTN_EASY": "Easy",
    "BTN_MEDIUM": "Medium",
    "BTN_HARD": "Hard",
    "BTN_MODE_SCORE": "Sweet Target (Score Mode)",
    "BTN_MODE_TIME": "Sugar Rush (Time Mode)",
    "BTN_CREDITS": "Credits",
    "BTN_CONTROLS": "Controls",
    "BTN_YES": "Yes",
    "BTN_NO": "No",

    "MODE_SCORE": "Sweet Target",
    "MODE_TIME": "Sugar Rush",
    "DIFFICULTY": "Difficulty",
    "SCORE": "Score",
    "GOAL": "Goal",
    "SPAWNS": "Spawns",
    "TIME_LEFT": "Time left",
    "WIN": "WIN",
    "LOSE": "LOSE",
    "WIN_COND": "Win condition:",
    "LOSE_COND": "Lose condition:",

    "WIN_TEXT_SCORE": "Reach the goal score before candies run out or the tower reaches the top.",
    "LOSE_TEXT_SCORE": "Tower reaches the top, or candies run out before you reach the goal.",
    "WIN_TEXT_TIME": "Reach the goal score before time runs out or the tower reaches the top.",
    "LOSE_TEXT_TIME": "Tower reaches the top, or time runs out before you reach the goal.",

    "INSTR_HEADER": "How to play:",
    "INSTR_LINE1": "Click groups of 3+ same color",
    "INSTR_LINE2": "to clear them.",
    "INSTR_LINE3": "Candies above fall down to fill gaps.",

    "PRESS_R_RESTART": "Press R to restart",
    "PRESS_M_MENU": "Press M for main menu",
    "AUDIO_TITLE": "Audio Settings",
    "BGM_VOLUME": "BGM Volume",
    "SFX_VOLUME": "SFX Volume",
    "BTN_BGM_DOWN": "BGM -",
    "BTN_BGM_UP": "BGM +",
    "BTN_SFX_DOWN": "SFX -",
    "BTN_SFX_UP": "SFX +",
    "OPTIONS_TITLE": "Options",
    "MODE_SELECT_TITLE": "Choose Game Mode",
    "DIFFICULTY_TITLE": "Choose Difficulty",
    "CREDITS_TITLE": "Credits",
    "CONTROLS_TITLE": "Controls",

    "CONFIRM_RETRY": "Retry?",
    "CONFIRM_MENU": "Go back to main menu?",
    "PAUSED": "PAUSED",
}

CREDITS_LINES = [
    "Developed by 66050541 Kongpak Phatthanasiri",
    "",
    "Audio used:",
    "",
    "Menu Music For Video Games That Don't Exist",
    "https://youtu.be/qwKDp4n6Udc?si=3p0oOv3TjQMSL-RL",
    "",
    "Free Game SFX Pack",
    "https://youtu.be/d9sQvn0pYts?si=Qy82IVaOdq9dAaXt",
    "",
    "Sounds of Button Selection in the Game Menu",
    "https://youtu.be/YNSbL-Cek1c?si=bgHUU9R0UgnzLWlw",
    "",
    "Cute Pop Sound Effects",
    "https://youtu.be/QvghQOO3K-I?si=Ewk91Rkz5tMF60dm",
    "",
    "Victory Sound Effect",
    "https://youtu.be/rA41FPAhiEI?si=K4eSKgBu36zuar8-",
    "",
    "Game Over Sound Effects",
    "https://youtu.be/bug1b0fQS8Y?si=PdqbZsUC24Uu13Q6",
]

CONTROLS_LINES = [
    "Mouse Left Click : Clear a group of 3+ connected candies.",
    "R : Retry current game.",
    "M : Return to main menu.",
    "P : Pause / Resume the game.",
    "ESC : Quit game.",
]

# Difficulty configuration
DIFFICULTY_CONFIG = {
    "easy":   {"goal_score": 400, "time_limit": 350, "max_spawns": 240, "drop_interval": 0.10},
    "medium": {"goal_score": 700, "time_limit": 480, "max_spawns": 220, "drop_interval": 0.10},
    "hard":   {"goal_score": 1000, "time_limit": 690, "max_spawns": 200, "drop_interval": 0.10},
}

def create_empty_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def flood_fill(board, start_r, start_c, target_type):
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(start_r, start_c)]
    visited[start_r][start_c] = True
    group = []

    while stack:
        r, c = stack.pop()
        group.append((r, c))
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc) and not visited[nr][nc]:
                if board[nr][nc] == target_type:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
    return group


def apply_gravity(board):
    """Make candies fall straight down in each column to fill gaps."""
    for col in range(COLS):
        write_row = ROWS - 1
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] != EMPTY:
                board[write_row][col] = board[row][col]
                if write_row != row:
                    board[row][col] = EMPTY
                write_row -= 1
        for row in range(write_row, -1, -1):
            board[row][col] = EMPTY

class Button:
    def __init__(self, rect, text_key):
        self.rect = pygame.Rect(rect)
        self.text_key = text_key

    def draw(self, surface, font, is_selected=False):
        label = TEXTS.get(self.text_key, self.text_key)
        color_bg = LIGHT_GRAY if is_selected else GRAY
        pygame.draw.rect(surface, color_bg, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)
        text_surf = font.render(label, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def contains(self, pos):
        return self.rect.collidepoint(pos)

class AudioManager:
    def __init__(self):
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5

        self.sfx_click = self.load_sound(SFX_CLICK_FILE)
        self.sfx_clear = self.load_sound(SFX_CLEAR_FILE)
        self.sfx_gameover = self.load_sound(SFX_GAMEOVER_FILE)
        self.sfx_win = self.load_sound(SFX_WIN_FILE)
        self.sfx_hover = self.load_sound(SFX_HOVER_FILE)

        self.apply_sfx_volume()
        self.current_bgm = None

    def load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            return None

    def apply_sfx_volume(self):
        for s in [self.sfx_click, self.sfx_clear,
                  self.sfx_gameover, self.sfx_win, self.sfx_hover]:
            if s is not None:
                s.set_volume(self.sfx_volume)

    def set_bgm_volume(self, v):
        self.bgm_volume = max(0.0, min(1.0, v))
        pygame.mixer.music.set_volume(self.bgm_volume)

    def set_sfx_volume(self, v):
        self.sfx_volume = max(0.0, min(1.0, v))
        self.apply_sfx_volume()

    def play_menu_bgm(self):
        if self.current_bgm == "menu":
            return
        try:
            pygame.mixer.music.load(BGM_MENU_FILE)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1)
            self.current_bgm = "menu"
        except Exception:
            self.current_bgm = None

    def play_game_bgm(self):
        if self.current_bgm == "game":
            return
        try:
            pygame.mixer.music.load(BGM_GAME_FILE)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1)
            self.current_bgm = "game"
        except Exception:
            self.current_bgm = None

    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

    def play_click(self):
        if self.sfx_click is not None:
            self.sfx_click.play()

    def play_clear(self):
        if self.sfx_clear is not None:
            self.sfx_clear.play()

    def play_gameover(self):
        if self.sfx_gameover is not None:
            self.sfx_gameover.play()

    def play_win(self):
        if self.sfx_win is not None:
            self.sfx_win.play()

    def play_hover(self):
        if self.sfx_hover is not None:
            self.sfx_hover.play()

class CandyTowerGame:
    def __init__(self, mode, difficulty_key, audio_manager):
        self.board = create_empty_board()
        self.current_candy = None

        self.mode = mode
        self.difficulty_key = difficulty_key
        cfg = DIFFICULTY_CONFIG[difficulty_key]

        self.goal_score = cfg["goal_score"]
        self.max_spawns = cfg["max_spawns"]
        self.time_limit = cfg["time_limit"] if mode == MODE_TIME else None
        self.time_left = self.time_limit

        self.score = 0
        self.spawned_count = 0
        self.game_state = STATE_RUNNING

        self.drop_interval = cfg.get("drop_interval", 0.2)
        self.drop_timer = 0.0

        self.paused = False

        self.audio = audio_manager

        self.spawn_new_candy()

    def spawn_new_candy(self):
        if self.mode == MODE_SCORE:
            if self.spawned_count >= self.max_spawns:
                if self.score >= self.goal_score:
                    self.game_state = STATE_WON
                    self.audio.play_win()
                else:
                    self.game_state = STATE_LOST
                    self.audio.play_gameover()
                self.current_candy = None
                return

        col = random.randint(0, COLS - 1)
        if self.board[0][col] != EMPTY:
            self.game_state = STATE_LOST
            self.audio.play_gameover()
            self.current_candy = None
            return

        candy_type = random.randint(1, NUM_TYPES)
        self.current_candy = {"row": 0, "col": col, "type": candy_type}
        self.spawned_count += 1

    def try_move_candy_down(self):
        if self.current_candy is None or self.game_state != STATE_RUNNING:
            return

        r = self.current_candy["row"]
        c = self.current_candy["col"]
        next_r = r + 1

        if next_r >= ROWS or self.board[next_r][c] != EMPTY:
            # Lock candy
            self.board[r][c] = self.current_candy["type"]
            self.current_candy = None

            # Check win by score
            if self.score >= self.goal_score:
                self.game_state = STATE_WON
                self.audio.play_win()

            if self.game_state == STATE_RUNNING:
                self.spawn_new_candy()
        else:
            self.current_candy["row"] = next_r

    def handle_click(self, mouse_pos):
        if self.game_state != STATE_RUNNING or self.paused:
            return

        x, y = mouse_pos

        if not (BOARD_ORIGIN_X <= x < BOARD_ORIGIN_X + BOARD_WIDTH and
                BOARD_ORIGIN_Y <= y < BOARD_ORIGIN_Y + BOARD_HEIGHT):
            return

        col = (x - BOARD_ORIGIN_X) // CELL_SIZE
        row = (y - BOARD_ORIGIN_Y) // CELL_SIZE

        if not in_bounds(row, col):
            return

        if self.current_candy is not None:
            if row == self.current_candy["row"] and col == self.current_candy["col"]:
                return

        cell_type = self.board[row][col]
        if cell_type == EMPTY:
            return

        group = flood_fill(self.board, row, col, cell_type)
        if len(group) >= 3:
            # Remove group
            for (r, c) in group:
                self.board[r][c] = EMPTY

            self.score += 10 * len(group)
            self.audio.play_clear()

            # Candies above fall down to fill gaps
            apply_gravity(self.board)

            # Check win by score
            if self.score >= self.goal_score:
                self.game_state = STATE_WON
                self.audio.play_win()

    def update(self, dt):
        if self.game_state != STATE_RUNNING or self.paused:
            return

        if self.mode == MODE_TIME and self.time_left is not None:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                if self.score >= self.goal_score:
                    self.game_state = STATE_WON
                    self.audio.play_win()
                else:
                    self.game_state = STATE_LOST
                    self.audio.play_gameover()
                return

        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer -= self.drop_interval
            self.try_move_candy_down()

    def draw_board(self, surface):
        pygame.draw.rect(surface, BLACK, (BOARD_ORIGIN_X, BOARD_ORIGIN_Y, BOARD_WIDTH, BOARD_HEIGHT))

        for row in range(ROWS):
            for col in range(COLS):
                cell_rect = pygame.Rect(
                    BOARD_ORIGIN_X + col * CELL_SIZE,
                    BOARD_ORIGIN_Y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(surface, GRAY, cell_rect)

        for row in range(ROWS):
            for col in range(COLS):
                t = self.board[row][col]
                if t != EMPTY:
                    color = CANDY_COLORS.get(t, LIGHT_GRAY)
                    cell_rect = pygame.Rect(
                        BOARD_ORIGIN_X + col * CELL_SIZE + 2,
                        BOARD_ORIGIN_Y + row * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4,
                    )
                    pygame.draw.rect(surface, color, cell_rect, border_radius=8)

        if self.current_candy is not None:
            r = self.current_candy["row"]
            c = self.current_candy["col"]
            t = self.current_candy["type"]
            color = CANDY_COLORS.get(t, WHITE)
            cell_rect = pygame.Rect(
                BOARD_ORIGIN_X + c * CELL_SIZE + 2,
                BOARD_ORIGIN_Y + r * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            )
            pygame.draw.rect(surface, color, cell_rect, border_radius=8)

        for x in range(COLS + 1):
            px = BOARD_ORIGIN_X + x * CELL_SIZE
            pygame.draw.line(surface, LIGHT_GRAY, (px, BOARD_ORIGIN_Y), (px, BOARD_ORIGIN_Y + BOARD_HEIGHT))
        for y in range(ROWS + 1):
            py = BOARD_ORIGIN_Y + y * CELL_SIZE
            pygame.draw.line(surface, LIGHT_GRAY, (BOARD_ORIGIN_X, py), (BOARD_ORIGIN_X + BOARD_WIDTH, py))

    def draw_info_panel(self, surface, font, big_font):
        panel_rect = pygame.Rect(PANEL_ORIGIN_X, PANEL_ORIGIN_Y, INFO_PANEL_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(surface, (20, 20, 20), panel_rect, border_radius=16)

        x0 = PANEL_ORIGIN_X + 20
        y = PANEL_ORIGIN_Y + 20

        title_surf = big_font.render(TEXTS["TITLE"], True, YELLOW)
        surface.blit(title_surf, (x0, y))
        y += 40

        difficulty_label = TEXTS["DIFFICULTY"]
        mode_label = TEXTS["MODE_SCORE"] if self.mode == MODE_SCORE else TEXTS["MODE_TIME"]

        for line in [
            f"{difficulty_label}: {self.difficulty_key.title()}",
            f"Mode: {mode_label}",
        ]:
            surface.blit(font.render(line, True, WHITE), (x0, y))
            y += 24

        y += 8

        score_line = f'{TEXTS["SCORE"]}: {self.score}'
        goal_line = f'{TEXTS["GOAL"]}: {self.goal_score}'
        surface.blit(font.render(score_line, True, WHITE), (x0, y))
        y += 24
        surface.blit(font.render(goal_line, True, WHITE), (x0, y))
        y += 24

        if self.mode == MODE_SCORE:
            spawns_line = f'{TEXTS["SPAWNS"]}: {self.spawned_count}/{self.max_spawns}'
            surface.blit(font.render(spawns_line, True, WHITE), (x0, y))
            y += 24
        else:
            time_line = f'{TEXTS["TIME_LEFT"]}: {int(self.time_left)} s'
            surface.blit(font.render(time_line, True, WHITE), (x0, y))
            y += 24

        y += 8

        if self.mode == MODE_SCORE:
            win_body = TEXTS["WIN_TEXT_SCORE"]
            lose_body = TEXTS["LOSE_TEXT_SCORE"]
        else:
            win_body = TEXTS["WIN_TEXT_TIME"]
            lose_body = TEXTS["LOSE_TEXT_TIME"]

        surface.blit(font.render(TEXTS["WIN_COND"], True, GREEN), (x0, y))
        y += 22
        surface.blit(font.render(win_body, True, WHITE), (x0 + 10, y))
        y += 24

        surface.blit(font.render(TEXTS["LOSE_COND"], True, RED), (x0, y))
        y += 22
        surface.blit(font.render(lose_body, True, WHITE), (x0 + 10, y))
        y += 30

        header = TEXTS["INSTR_HEADER"]
        instr_lines = [TEXTS["INSTR_LINE1"], TEXTS["INSTR_LINE2"], TEXTS["INSTR_LINE3"]]
        surface.blit(font.render(header, True, YELLOW), (x0, y))
        y += 24
        for line in instr_lines:
            surface.blit(font.render(line, True, WHITE), (x0, y))
            y += 22

        # Game state banner / restart hints
        if self.game_state == STATE_WON:
            msg = TEXTS["WIN"]; color = GREEN
        elif self.game_state == STATE_LOST:
            msg = TEXTS["LOSE"]; color = RED
        else:
            msg = ""; color = WHITE

        if msg:
            text_surf = big_font.render(msg, True, color)
            rect = text_surf.get_rect()
            rect.center = (PANEL_ORIGIN_X + INFO_PANEL_WIDTH // 2, PANEL_ORIGIN_Y + BOARD_HEIGHT - 120)
            surface.blit(text_surf, rect)

            hint_r = TEXTS["PRESS_R_RESTART"]
            hint_m = TEXTS["PRESS_M_MENU"]
            hint_r_surf = font.render(hint_r, True, WHITE)
            hint_m_surf = font.render(hint_m, True, WHITE)
            rect_r = hint_r_surf.get_rect(center=(PANEL_ORIGIN_X + INFO_PANEL_WIDTH // 2,
                                                  PANEL_ORIGIN_Y + BOARD_HEIGHT - 70))
            rect_m = hint_m_surf.get_rect(center=(PANEL_ORIGIN_X + INFO_PANEL_WIDTH // 2,
                                                  PANEL_ORIGIN_Y + BOARD_HEIGHT - 40))
            surface.blit(hint_r_surf, rect_r)
            surface.blit(hint_m_surf, rect_m)

    def restart(self):
        self.__init__(self.mode, self.difficulty_key, self.audio)

class CandyApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Tower Panic - Falling Objects Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 40, bold=True)

        self.audio = AudioManager()

        self.scene = SCENE_MAIN_MENU
        self.scene_stack = []

        self.buttons = []
        self.selected_difficulty = "easy"
        self.selected_mode = MODE_SCORE

        self.game = None
        self.last_hovered_button = None

        self.confirm_active = False
        self.confirm_type = None  
        self.confirm_buttons = [] 

        self.build_main_menu()
        self.audio.play_menu_bgm()

    def push_scene(self, new_scene):
        self.scene_stack.append(self.scene)
        self.scene = new_scene
        self.build_scene_buttons()

    def pop_scene(self):
        if self.scene_stack:
            self.scene = self.scene_stack.pop()
        else:
            self.scene = SCENE_MAIN_MENU
        self.build_scene_buttons()

    def build_scene_buttons(self):
        if self.scene == SCENE_MAIN_MENU:
            self.build_main_menu()
        elif self.scene == SCENE_MODE_SELECT:
            self.build_mode_menu()
        elif self.scene == SCENE_DIFFICULTY:
            self.build_difficulty_menu()
        elif self.scene == SCENE_OPTIONS:
            self.build_options_menu()
        elif self.scene == SCENE_AUDIO:
            self.build_audio_menu()
        elif self.scene == SCENE_CREDITS:
            self.build_credits_menu()
        elif self.scene == SCENE_CONTROLS:
            self.build_controls_menu()
        else:
            self.buttons = []

    def build_main_menu(self):
        self.buttons = []
        w = 500
        h = 80
        spacing = 40
        x = (WINDOW_WIDTH - w) // 2
        n = 5
        total_height = n * h + (n - 1) * spacing
        start_y = (WINDOW_HEIGHT - total_height) // 2

        self.buttons.append(Button((x, start_y, w, h), "BTN_PLAY"))
        self.buttons.append(Button((x, start_y + (h + spacing), w, h), "BTN_CHOOSE_DIFFICULTY"))
        self.buttons.append(Button((x, start_y + 2 * (h + spacing), w, h), "BTN_OPTIONS"))
        self.buttons.append(Button((x, start_y + 3 * (h + spacing), w, h), "BTN_CONTROLS"))
        self.buttons.append(Button((x, start_y + 4 * (h + spacing), w, h), "BTN_CREDITS"))

    def build_mode_menu(self):
        self.buttons = []
        w = 600
        h = 80
        spacing = 40
        x = (WINDOW_WIDTH - w) // 2
        n = 3
        total_height = n * h + (n - 1) * spacing
        start_y = (WINDOW_HEIGHT - total_height) // 2

        self.buttons.append(Button((x, start_y, w, h), "BTN_MODE_SCORE"))
        self.buttons.append(Button((x, start_y + h + spacing, w, h), "BTN_MODE_TIME"))
        self.buttons.append(Button((x, start_y + 2 * (h + spacing), w, h), "BTN_BACK"))

    def build_difficulty_menu(self):
        self.buttons = []
        w = 400
        h = 70
        spacing = 30
        x = (WINDOW_WIDTH - w) // 2
        n = 4
        total_height = n * h + (n - 1) * spacing
        start_y = (WINDOW_HEIGHT - total_height) // 2

        self.buttons.append(Button((x, start_y, w, h), "BTN_EASY"))
        self.buttons.append(Button((x, start_y + h + spacing, w, h), "BTN_MEDIUM"))
        self.buttons.append(Button((x, start_y + 2 * (h + spacing), w, h), "BTN_HARD"))
        self.buttons.append(Button((x, start_y + 3 * (h + spacing), w, h), "BTN_BACK"))

    def build_options_menu(self):
        self.buttons = []
        w = 400
        h = 80
        spacing = 40
        x = (WINDOW_WIDTH - w) // 2
        n = 2
        total_height = n * h + (n - 1) * spacing
        start_y = (WINDOW_HEIGHT - total_height) // 2

        self.buttons.append(Button((x, start_y, w, h), "BTN_AUDIO"))
        self.buttons.append(Button((x, start_y + h + spacing, w, h), "BTN_BACK"))

    def build_audio_menu(self):
        self.buttons = []
        w = 150
        h = 60
        center_x = WINDOW_WIDTH // 2
        y_start = WINDOW_HEIGHT // 2 - 80
        gap_x = 200
        spacing_y = 120

        self.buttons.append(Button((center_x - gap_x - w//2, y_start, w, h), "BTN_BGM_DOWN"))
        self.buttons.append(Button((center_x + gap_x - w//2, y_start, w, h), "BTN_BGM_UP"))
        self.buttons.append(Button((center_x - gap_x - w//2, y_start + spacing_y, w, h), "BTN_SFX_DOWN"))
        self.buttons.append(Button((center_x + gap_x - w//2, y_start + spacing_y, w, h), "BTN_SFX_UP"))
        self.buttons.append(Button((center_x - 200, y_start + 2 * spacing_y, 400, h), "BTN_BACK"))

    def build_credits_menu(self):
        self.buttons = []
        w = 300
        h = 70
        x = (WINDOW_WIDTH - w) // 2
        y = WINDOW_HEIGHT - 150
        self.buttons.append(Button((x, y, w, h), "BTN_BACK"))

    def build_controls_menu(self):
        self.buttons = []
        w = 300
        h = 70
        x = (WINDOW_WIDTH - w) // 2
        y = WINDOW_HEIGHT - 150
        self.buttons.append(Button((x, y, w, h), "BTN_BACK"))

    def open_confirm(self, action_type):
        """action_type: 'restart' or 'main_menu'."""
        self.confirm_active = True
        self.confirm_type = action_type
        self.confirm_buttons = []

        w = 180
        h = 60
        spacing = 40
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 + 40

        yes_rect = (center_x - w - spacing//2, center_y, w, h)
        no_rect = (center_x + spacing//2, center_y, w, h)

        self.confirm_buttons.append(Button(yes_rect, "BTN_YES"))
        self.confirm_buttons.append(Button(no_rect, "BTN_NO"))

    def close_confirm(self):
        self.confirm_active = False
        self.confirm_type = None
        self.confirm_buttons = []

    def handle_confirm_click(self, pos):
        for btn in self.confirm_buttons:
            if btn.contains(pos):
                self.audio.play_click()
                if btn.text_key == "BTN_YES":
                    if self.confirm_type == "restart" and self.game is not None:
                        self.game.restart()
                    elif self.confirm_type == "main_menu":
                        self.return_to_main_menu()
                self.close_confirm()
                break

    def handle_menu_click(self, pos):
        if self.scene not in [
            SCENE_MAIN_MENU,
            SCENE_MODE_SELECT,
            SCENE_DIFFICULTY,
            SCENE_OPTIONS,
            SCENE_AUDIO,
            SCENE_CREDITS,
            SCENE_CONTROLS,
        ]:
            return

        for btn in self.buttons:
            if btn.contains(pos):
                self.audio.play_click()
                self.handle_button_action(btn.text_key)
                break

    def handle_button_action(self, key):
        if self.scene == SCENE_MAIN_MENU:
            if key == "BTN_PLAY":
                self.push_scene(SCENE_MODE_SELECT)
            elif key == "BTN_CHOOSE_DIFFICULTY":
                self.push_scene(SCENE_DIFFICULTY)
            elif key == "BTN_OPTIONS":
                self.push_scene(SCENE_OPTIONS)
            elif key == "BTN_CONTROLS":
                self.push_scene(SCENE_CONTROLS)
            elif key == "BTN_CREDITS":
                self.push_scene(SCENE_CREDITS)

        elif self.scene == SCENE_MODE_SELECT:
            if key == "BTN_MODE_SCORE":
                self.selected_mode = MODE_SCORE
                self.start_game()
            elif key == "BTN_MODE_TIME":
                self.selected_mode = MODE_TIME
                self.start_game()
            elif key == "BTN_BACK":
                self.pop_scene()

        elif self.scene == SCENE_DIFFICULTY:
            if key == "BTN_EASY":
                self.selected_difficulty = "easy"
            elif key == "BTN_MEDIUM":
                self.selected_difficulty = "medium"
            elif key == "BTN_HARD":
                self.selected_difficulty = "hard"
            elif key == "BTN_BACK":
                self.pop_scene()

        elif self.scene == SCENE_OPTIONS:
            if key == "BTN_AUDIO":
                self.push_scene(SCENE_AUDIO)
            elif key == "BTN_BACK":
                self.pop_scene()

        elif self.scene == SCENE_AUDIO:
            step = 0.1
            if key == "BTN_BGM_DOWN":
                self.audio.set_bgm_volume(self.audio.bgm_volume - step)
            elif key == "BTN_BGM_UP":
                self.audio.set_bgm_volume(self.audio.bgm_volume + step)
            elif key == "BTN_SFX_DOWN":
                self.audio.set_sfx_volume(self.audio.sfx_volume - step)
            elif key == "BTN_SFX_UP":
                self.audio.set_sfx_volume(self.audio.sfx_volume + step)
            elif key == "BTN_BACK":
                self.pop_scene()

        elif self.scene == SCENE_CREDITS:
            if key == "BTN_BACK":
                self.pop_scene()

        elif self.scene == SCENE_CONTROLS:
            if key == "BTN_BACK":
                self.pop_scene()

    def start_game(self):
        self.game = CandyTowerGame(self.selected_mode, self.selected_difficulty, self.audio)
        self.scene_stack = []
        self.scene = SCENE_GAME
        self.buttons = []
        self.close_confirm()
        self.audio.play_game_bgm()

    def return_to_main_menu(self):
        self.scene = SCENE_MAIN_MENU
        self.scene_stack = []
        self.game = None
        self.close_confirm()
        self.build_main_menu()
        self.audio.play_menu_bgm()

    def update_hover_sound(self):
        if self.confirm_active:
            self.last_hovered_button = None
            return

        if self.scene not in [
            SCENE_MAIN_MENU,
            SCENE_MODE_SELECT,
            SCENE_DIFFICULTY,
            SCENE_OPTIONS,
            SCENE_AUDIO,
            SCENE_CREDITS,
            SCENE_CONTROLS,
        ]:
            self.last_hovered_button = None
            return

        mouse_pos = pygame.mouse.get_pos()
        hovered = None
        for btn in self.buttons:
            if btn.contains(mouse_pos):
                hovered = btn
                break

        if hovered is not None and hovered is not self.last_hovered_button:
            self.audio.play_hover()
        self.last_hovered_button = hovered

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.scene == SCENE_GAME and self.game is not None:
                        if self.confirm_active:
                            self.handle_confirm_click(event.pos)
                        else:
                            self.game.handle_click(event.pos)
                    else:
                        self.handle_menu_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if self.scene == SCENE_GAME and self.game is not None:
                        if self.confirm_active:
                            pass
                        else:
                            if event.key == pygame.K_p:
                                self.game.paused = not self.game.paused
                            elif event.key == pygame.K_r:
                                self.open_confirm("restart")
                            elif event.key == pygame.K_m:
                                self.open_confirm("main_menu")

            self.update_hover_sound()

            if self.scene == SCENE_GAME and self.game is not None and not self.confirm_active:
                self.game.update(dt)

            if self.scene == SCENE_GAME and self.game is not None:
                self.draw_game()
            else:
                self.draw_menu()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_menu(self):
        self.screen.fill((15, 15, 25))

        title_surf = self.big_font.render(TEXTS["TITLE"], True, YELLOW)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_surf, title_rect)

        if self.scene == SCENE_MAIN_MENU:
            diff_text = f'{TEXTS["DIFFICULTY"]}: {self.selected_difficulty.title()}'
            diff_surf = self.font.render(diff_text, True, WHITE)
            diff_rect = diff_surf.get_rect(center=(WINDOW_WIDTH // 2, 170))
            self.screen.blit(diff_surf, diff_rect)

        if self.scene == SCENE_MAIN_MENU:
            subtitle = TEXTS["TITLE"]
        elif self.scene == SCENE_MODE_SELECT:
            subtitle = TEXTS["MODE_SELECT_TITLE"]
        elif self.scene == SCENE_DIFFICULTY:
            subtitle = TEXTS["DIFFICULTY_TITLE"]
        elif self.scene == SCENE_OPTIONS:
            subtitle = TEXTS["OPTIONS_TITLE"]
        elif self.scene == SCENE_AUDIO:
            subtitle = TEXTS["AUDIO_TITLE"]
        elif self.scene == SCENE_CREDITS:
            subtitle = TEXTS["CREDITS_TITLE"]
        elif self.scene == SCENE_CONTROLS:
            subtitle = TEXTS["CONTROLS_TITLE"]
        else:
            subtitle = ""

        if subtitle:
            sub_surf = self.font.render(subtitle, True, WHITE)
            sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, 220))
            self.screen.blit(sub_surf, sub_rect)

        if self.scene == SCENE_AUDIO:
            bgm_label = TEXTS["BGM_VOLUME"] + f": {int(self.audio.bgm_volume * 100)}%"
            sfx_label = TEXTS["SFX_VOLUME"] + f": {int(self.audio.sfx_volume * 100)}%"
            bgm_surf = self.font.render(bgm_label, True, WHITE)
            sfx_surf = self.font.render(sfx_label, True, WHITE)
            self.screen.blit(bgm_surf, (WINDOW_WIDTH // 2 - 260, WINDOW_HEIGHT // 2 - 140))
            self.screen.blit(sfx_surf, (WINDOW_WIDTH // 2 - 260, WINDOW_HEIGHT // 2 - 20))

        if self.scene == SCENE_CREDITS:
            start_y = 260
            x = WINDOW_WIDTH // 2
            for line in CREDITS_LINES:
                text_surf = self.font.render(line, True, WHITE)
                rect = text_surf.get_rect(center=(x, start_y))
                self.screen.blit(text_surf, rect)
                start_y += 28

        if self.scene == SCENE_CONTROLS:
            start_y = 260
            x = WINDOW_WIDTH // 2
            for line in CONTROLS_LINES:
                text_surf = self.font.render(line, True, WHITE)
                rect = text_surf.get_rect(center=(x, start_y))
                self.screen.blit(text_surf, rect)
                start_y += 32

        for btn in self.buttons:
            is_selected = False
            if self.scene == SCENE_DIFFICULTY:
                if btn.text_key == "BTN_EASY" and self.selected_difficulty == "easy":
                    is_selected = True
                if btn.text_key == "BTN_MEDIUM" and self.selected_difficulty == "medium":
                    is_selected = True
                if btn.text_key == "BTN_HARD" and self.selected_difficulty == "hard":
                    is_selected = True

            btn.draw(self.screen, self.font, is_selected=is_selected)

    def draw_game(self):
        self.screen.fill((10, 10, 20))
        if self.game is not None:
            self.game.draw_board(self.screen)
            self.game.draw_info_panel(self.screen, self.font, self.big_font)

            if self.game.paused and self.game.game_state == STATE_RUNNING and not self.confirm_active:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                self.screen.blit(overlay, (0, 0))
                paused_surf = self.big_font.render(TEXTS["PAUSED"], True, YELLOW)
                paused_rect = paused_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(paused_surf, paused_rect)

            if self.confirm_active:
                self.draw_confirm_dialog()

    def draw_confirm_dialog(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        box_w, box_h = 600, 260
        box_x = (WINDOW_WIDTH - box_w) // 2
        box_y = (WINDOW_HEIGHT - box_h) // 2
        pygame.draw.rect(self.screen, (30, 30, 40), (box_x, box_y, box_w, box_h), border_radius=16)
        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_w, box_h), 2, border_radius=16)

        if self.confirm_type == "restart":
            msg = TEXTS["CONFIRM_RETRY"]
        else:
            msg = TEXTS["CONFIRM_MENU"]

        msg_surf = self.big_font.render(msg, True, YELLOW)
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, box_y + 80))
        self.screen.blit(msg_surf, msg_rect)

        for btn in self.confirm_buttons:
            btn.draw(self.screen, self.font, is_selected=False)

def main():
    app = CandyApp()
    app.run()

if __name__ == "__main__":
    main()
