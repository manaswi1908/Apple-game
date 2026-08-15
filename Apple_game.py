import pygame
import random
import math

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Catcher")

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

SKY_TOP = (70, 165, 235)
SKY_BOTTOM = (205, 235, 255)

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)

GRASS = (76, 165, 65)
DARK_GRASS = (45, 120, 45)
LIGHT_GRASS = (110, 190, 75)

BROWN = (135, 78, 32)
DARK_BROWN = (78, 42, 20)
LIGHT_BROWN = (190, 125, 62)

RED = (210, 35, 35)
DARK_RED = (145, 18, 18)
LIGHT_RED = (255, 95, 80)

GREEN = (45, 135, 50)
DARK_GREEN = (30, 100, 35)

YELLOW = (255, 215, 70)
ORANGE = (240, 150, 45)

PANEL = (255, 248, 225)


# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(None, 82)
large_font = pygame.font.Font(None, 58)
medium_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)


# =========================================================
# GAME STATES
# =========================================================

MENU = "menu"
INSTRUCTIONS = "instructions"
PLAYING = "playing"
GAME_OVER = "game_over"

game_state = MENU


# =========================================================
# GAME DATA
# =========================================================

score = 0
lives = 3
high_score = 0

# Current apple speed
apple_speed = 2.0

# Maximum possible speed
MAX_SPEED = 6.0

# Speed at different life stages
THREE_LIVES_SPEED = 2.0
TWO_LIVES_SPEED = 3.0
ONE_LIFE_SPEED = 4.2

# How much catching apples increases difficulty
CATCH_SPEED_INCREASE = 0.12

# Number of catches before speed increase
CATCHES_PER_SPEED_UP = 4

catch_count = 0


# =========================================================
# BASKET
# =========================================================

basket_width = 130
basket_height = 48

basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - 115

basket_speed = 3


# =========================================================
# APPLE
# =========================================================

apple_size = 36

apple_x = random.randint(
    60,
    WIDTH - 60
)

apple_y = -50


# =========================================================
# CLOUDS
# =========================================================

clouds = [
    [100, 100, 1.0, 0.25],
    [450, 145, 0.8, 0.18],
    [760, 90, 0.7, 0.22],
    [250, 210, 0.55, 0.15]
]


# =========================================================
# FLOWERS
# =========================================================

flowers = [
    (90, 535),
    (150, 555),
    (220, 525),
    (620, 550),
    (690, 530),
    (770, 560),
    (830, 525)
]


# =========================================================
# SKY
# =========================================================

def draw_sky():

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        r = int(
            SKY_TOP[0] * (1 - ratio)
            + SKY_BOTTOM[0] * ratio
        )

        g = int(
            SKY_TOP[1] * (1 - ratio)
            + SKY_BOTTOM[1] * ratio
        )

        b = int(
            SKY_TOP[2] * (1 - ratio)
            + SKY_BOTTOM[2] * ratio
        )

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )


# =========================================================
# CLOUD
# =========================================================

def draw_cloud(x, y, scale):

    x = int(x)
    y = int(y)

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        int(27 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            x + int(32 * scale),
            y - int(12 * scale)
        ),
        int(34 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            x + int(67 * scale),
            y
        ),
        int(27 * scale)
    )

    pygame.draw.ellipse(
        screen,
        WHITE,
        (
            x - int(12 * scale),
            y,
            int(92 * scale),
            int(32 * scale)
        )
    )


def update_clouds():

    for cloud in clouds:

        cloud[0] += cloud[3]

        if cloud[0] > WIDTH + 100:
            cloud[0] = -120


# =========================================================
# TREE
# =========================================================

def draw_tree(x, y):

    pygame.draw.polygon(
        screen,
        DARK_BROWN,
        [
            (x - 22, y),
            (x + 22, y),
            (x + 30, y + 155),
            (x - 30, y + 155)
        ]
    )

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y + 55),
        (x - 65, y + 5),
        17
    )

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x + 5, y + 60),
        (x + 65, y + 8),
        17
    )

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (x - 60, y - 5),
        58
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (x, y - 35),
        70
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (x + 62, y - 5),
        58
    )

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (x, y + 15),
        60
    )


# =========================================================
# GROUND
# =========================================================

def draw_ground():

    ground_y = HEIGHT - 130

    pygame.draw.rect(
        screen,
        GRASS,
        (0, ground_y, WIDTH, 130)
    )

    for x in range(0, WIDTH, 20):

        pygame.draw.line(
            screen,
            DARK_GRASS,
            (x, ground_y + 20),
            (x + 5, ground_y + 8),
            2
        )

    for x in range(10, WIDTH, 32):

        pygame.draw.line(
            screen,
            LIGHT_GRASS,
            (x, ground_y + 45),
            (x + 5, ground_y + 32),
            2
        )


# =========================================================
# FLOWER
# =========================================================

def draw_flower(x, y):

    pygame.draw.line(
        screen,
        DARK_GREEN,
        (x, y),
        (x, y + 25),
        3
    )

    pygame.draw.circle(
        screen,
        (255, 105, 130),
        (x - 6, y),
        6
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 6, y),
        6
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (x, y),
        5
    )


# =========================================================
# APPLE
# =========================================================

def draw_apple(x, y):

    x = int(x)
    y = int(y)

    pygame.draw.circle(
        screen,
        DARK_RED,
        (x - 9, y),
        20
    )

    pygame.draw.circle(
        screen,
        RED,
        (x + 9, y),
        20
    )

    pygame.draw.circle(
        screen,
        RED,
        (x, y + 8),
        22
    )

    pygame.draw.ellipse(
        screen,
        LIGHT_RED,
        (
            x - 13,
            y - 10,
            9,
            14
        )
    )

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y - 15),
        (x + 4, y - 31),
        5
    )

    pygame.draw.ellipse(
        screen,
        GREEN,
        (
            x + 3,
            y - 33,
            24,
            11
        )
    )


# =========================================================
# BASKET
# =========================================================

def draw_basket(x, y):

    pygame.draw.arc(
        screen,
        DARK_BROWN,
        (
            x + 18,
            y - 55,
            basket_width - 36,
            75
        ),
        math.pi,
        math.pi * 2,
        8
    )

    points = [
        (x + 7, y),
        (x + basket_width - 7, y),
        (x + basket_width - 23, y + basket_height),
        (x + 23, y + basket_height)
    ]

    pygame.draw.polygon(
        screen,
        BROWN,
        points
    )

    pygame.draw.ellipse(
        screen,
        LIGHT_BROWN,
        (
            x,
            y - 9,
            basket_width,
            25
        )
    )

    pygame.draw.ellipse(
        screen,
        DARK_BROWN,
        (
            x + 10,
            y - 3,
            basket_width - 20,
            11
        )
    )

    for line_y in range(
        y + 10,
        y + basket_height,
        9
    ):

        pygame.draw.line(
            screen,
            LIGHT_BROWN,
            (x + 16, line_y),
            (x + basket_width - 16, line_y),
            3
        )

    for line_x in range(
        x + 22,
        x + basket_width,
        15
    ):

        pygame.draw.line(
            screen,
            DARK_BROWN,
            (line_x, y + 5),
            (line_x - 5, y + basket_height - 3),
            2
        )


# =========================================================
# BUTTON
# =========================================================

def draw_button(rect, text, mouse_pos):

    hovered = rect.collidepoint(mouse_pos)

    if hovered:

        pygame.draw.rect(
            screen,
            ORANGE,
            rect,
            border_radius=15
        )

    else:

        pygame.draw.rect(
            screen,
            LIGHT_BROWN,
            rect,
            border_radius=15
        )

    pygame.draw.rect(
        screen,
        DARK_BROWN,
        rect,
        3,
        border_radius=15
    )

    text_surface = medium_font.render(
        text,
        True,
        WHITE
    )

    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        )
    )


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global score
    global lives
    global apple_x
    global apple_y
    global basket_x
    global apple_speed
    global catch_count

    score = 0

    lives = 3

    # Start at a reasonable beginner speed
    apple_speed = THREE_LIVES_SPEED

    catch_count = 0

    basket_x = (
        WIDTH - basket_width
    ) // 2

    apple_x = random.randint(
        60,
        WIDTH - 60
    )

    apple_y = -50


# =========================================================
# UPDATE DIFFICULTY
# =========================================================

def update_difficulty():

    global apple_speed

    # Base speed depending on remaining lives

    if lives == 3:

        base_speed = THREE_LIVES_SPEED

    elif lives == 2:

        base_speed = TWO_LIVES_SPEED

    else:

        base_speed = ONE_LIFE_SPEED

    # Extra difficulty based on score
    score_bonus = (
        score // CATCHES_PER_SPEED_UP
    ) * CATCH_SPEED_INCREASE

    target_speed = (
        base_speed + score_bonus
    )

    # Never exceed maximum speed
    target_speed = min(
        target_speed,
        MAX_SPEED
    )

    # Smoothly move toward target speed
    if apple_speed < target_speed:

        apple_speed += 0.04

        if apple_speed > target_speed:
            apple_speed = target_speed

    elif apple_speed > target_speed:

        apple_speed -= 0.04

        if apple_speed < target_speed:
            apple_speed = target_speed


# =========================================================
# MENU
# =========================================================

def draw_menu():

    draw_sky()

    update_clouds()

    for cloud in clouds:

        draw_cloud(
            cloud[0],
            cloud[1],
            cloud[2]
        )

    draw_ground()

    draw_tree(
        760,
        360
    )

    for flower in flowers:

        draw_flower(
            flower[0],
            flower[1]
        )

    title = title_font.render(
        "APPLE CATCHER",
        True,
        DARK_BROWN
    )

    screen.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            95
        )
    )

    subtitle = medium_font.render(
        "Catch the apples before they fall!",
        True,
        DARK_BROWN
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2
            - subtitle.get_width() // 2,
            175
        )
    )

    draw_apple(
        WIDTH // 2,
        255
    )

    mouse_pos = pygame.mouse.get_pos()

    start_button = pygame.Rect(
        WIDTH // 2 - 130,
        320,
        260,
        60
    )

    instructions_button = pygame.Rect(
        WIDTH // 2 - 130,
        400,
        260,
        60
    )

    quit_button = pygame.Rect(
        WIDTH // 2 - 130,
        480,
        260,
        60
    )

    draw_button(
        start_button,
        "START GAME",
        mouse_pos
    )

    draw_button(
        instructions_button,
        "HOW TO PLAY",
        mouse_pos
    )

    draw_button(
        quit_button,
        "QUIT",
        mouse_pos
    )


# =========================================================
# INSTRUCTIONS
# =========================================================

def draw_instructions():

    draw_sky()

    update_clouds()

    for cloud in clouds:

        draw_cloud(
            cloud[0],
            cloud[1],
            cloud[2]
        )

    draw_ground()

    panel = pygame.Rect(
        120,
        70,
        WIDTH - 240,
        480
    )

    pygame.draw.rect(
        screen,
        PANEL,
        panel,
        border_radius=25
    )

    pygame.draw.rect(
        screen,
        DARK_BROWN,
        panel,
        4,
        border_radius=25
    )

    title = large_font.render(
        "HOW TO PLAY",
        True,
        DARK_BROWN
    )

    screen.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            105
        )
    )

    instructions = [
        "LEFT / RIGHT  -  Move the basket",
        "Catch an apple  =  +1 point",
        "Miss an apple  =  lose 1 life",
        "3 lives  =  Easy speed",
        "2 lives  =  Medium speed",
        "1 life  =  Hard speed",
        "SPACE  =  Play Again",
        "ESC  =  Main Menu"
    ]

    y = 175

    for instruction in instructions:

        text = small_font.render(
            instruction,
            True,
            DARK_BROWN
        )

        screen.blit(
            text,
            (
                WIDTH // 2
                - text.get_width() // 2,
                y
            )
        )

        y += 40

    back_button = pygame.Rect(
        WIDTH // 2 - 120,
        485,
        240,
        55
    )

    draw_button(
        back_button,
        "BACK TO MENU",
        pygame.mouse.get_pos()
    )


# =========================================================
# GAME SCREEN
# =========================================================

def draw_game():

    draw_sky()

    update_clouds()

    for cloud in clouds:

        draw_cloud(
            cloud[0],
            cloud[1],
            cloud[2]
        )

    draw_ground()

    draw_tree(
        760,
        360
    )

    for flower in flowers:

        draw_flower(
            flower[0],
            flower[1]
        )

    draw_apple(
        apple_x,
        apple_y
    )

    draw_basket(
        basket_x,
        basket_y
    )

    # Score panel

    score_panel = pygame.Rect(
        20,
        20,
        180,
        55
    )

    pygame.draw.rect(
        screen,
        PANEL,
        score_panel,
        border_radius=15
    )

    score_text = medium_font.render(
        f"Score: {score}",
        True,
        DARK_BROWN
    )

    screen.blit(
        score_text,
        (
            score_panel.centerx
            - score_text.get_width() // 2,
            score_panel.centery
            - score_text.get_height() // 2
        )
    )

    # Lives panel

    lives_panel = pygame.Rect(
        WIDTH - 200,
        20,
        180,
        55
    )

    pygame.draw.rect(
        screen,
        PANEL,
        lives_panel,
        border_radius=15
    )

    lives_text = medium_font.render(
        f"Lives: {lives}",
        True,
        DARK_BROWN
    )

    screen.blit(
        lives_text,
        (
            lives_panel.centerx
            - lives_text.get_width() // 2,
            lives_panel.centery
            - lives_text.get_height() // 2
        )
    )

    # Difficulty indicator

    if lives == 3:

        difficulty = "EASY"

    elif lives == 2:

        difficulty = "MEDIUM"

    else:

        difficulty = "HARD"

    difficulty_text = small_font.render(
        f"{difficulty}  |  Speed: {apple_speed:.1f}",
        True,
        DARK_BROWN
    )

    screen.blit(
        difficulty_text,
        (
            WIDTH // 2
            - difficulty_text.get_width() // 2,
            25
        )
    )


# =========================================================
# GAME OVER
# =========================================================

def draw_game_over():

    draw_game()

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (20, 20, 20, 165)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title = title_font.render(
        "GAME OVER",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            150
        )
    )

    final_score = medium_font.render(
        f"Final Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        final_score,
        (
            WIDTH // 2
            - final_score.get_width() // 2,
            245
        )
    )

    high_score_text = medium_font.render(
        f"High Score: {high_score}",
        True,
        YELLOW
    )

    screen.blit(
        high_score_text,
        (
            WIDTH // 2
            - high_score_text.get_width() // 2,
            290
        )
    )

    play_again = pygame.Rect(
        WIDTH // 2 - 140,
        360,
        280,
        60
    )

    menu_button = pygame.Rect(
        WIDTH // 2 - 140,
        440,
        280,
        60
    )

    mouse_pos = pygame.mouse.get_pos()

    draw_button(
        play_again,
        "PLAY AGAIN",
        mouse_pos
    )

    draw_button(
        menu_button,
        "MAIN MENU",
        mouse_pos
    )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        # =================================================
        # MENU
        # =================================================

        if game_state == MENU:

            if event.type == pygame.MOUSEBUTTONDOWN:

                start_button = pygame.Rect(
                    WIDTH // 2 - 130,
                    320,
                    260,
                    60
                )

                instructions_button = pygame.Rect(
                    WIDTH // 2 - 130,
                    400,
                    260,
                    60
                )

                quit_button = pygame.Rect(
                    WIDTH // 2 - 130,
                    480,
                    260,
                    60
                )

                if start_button.collidepoint(
                    event.pos
                ):

                    reset_game()

                    game_state = PLAYING

                elif instructions_button.collidepoint(
                    event.pos
                ):

                    game_state = INSTRUCTIONS

                elif quit_button.collidepoint(
                    event.pos
                ):

                    running = False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    reset_game()

                    game_state = PLAYING


        # =================================================
        # INSTRUCTIONS
        # =================================================

        elif game_state == INSTRUCTIONS:

            if event.type == pygame.MOUSEBUTTONDOWN:

                back_button = pygame.Rect(
                    WIDTH // 2 - 120,
                    485,
                    240,
                    55
                )

                if back_button.collidepoint(
                    event.pos
                ):

                    game_state = MENU


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = MENU


        # =================================================
        # PLAYING
        # =================================================

        elif game_state == PLAYING:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = MENU


        # =================================================
        # GAME OVER
        # =================================================

        elif game_state == GAME_OVER:

            if event.type == pygame.MOUSEBUTTONDOWN:

                play_again = pygame.Rect(
                    WIDTH // 2 - 140,
                    360,
                    280,
                    60
                )

                menu_button = pygame.Rect(
                    WIDTH // 2 - 140,
                    440,
                    280,
                    60
                )

                if play_again.collidepoint(
                    event.pos
                ):

                    reset_game()

                    game_state = PLAYING

                elif menu_button.collidepoint(
                    event.pos
                ):

                    game_state = MENU


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    reset_game()

                    game_state = PLAYING

                elif event.key == pygame.K_ESCAPE:

                    game_state = MENU


    # =====================================================
    # GAME LOGIC
    # =====================================================

    if game_state == PLAYING:

        keys = pygame.key.get_pressed()

        # Basket movement

        if keys[pygame.K_LEFT]:

            basket_x -= basket_speed

        if keys[pygame.K_RIGHT]:

            basket_x += basket_speed

        # Keep basket inside screen

        basket_x = max(
            0,
            min(
                basket_x,
                WIDTH - basket_width
            )
        )

        # Update difficulty first

        update_difficulty()

        # Apple movement

        apple_y += apple_speed

        # Collision

        apple_rect = pygame.Rect(
            apple_x - apple_size // 2,
            apple_y - apple_size // 2,
            apple_size,
            apple_size
        )

        basket_rect = pygame.Rect(
            basket_x,
            basket_y,
            basket_width,
            basket_height
        )

        # =================================================
        # APPLE CAUGHT
        # =================================================

        if apple_rect.colliderect(
            basket_rect
        ):

            score += 1

            catch_count += 1

            if score > high_score:

                high_score = score

            apple_x = random.randint(
                60,
                WIDTH - 60
            )

            apple_y = -50

            # Every few catches,
            # slightly increase difficulty

            if (
                catch_count
                % CATCHES_PER_SPEED_UP
                == 0
            ):

                apple_speed = min(
                    apple_speed
                    + CATCH_SPEED_INCREASE,
                    MAX_SPEED
                )


        # =================================================
        # APPLE MISSED
        # =================================================

        if apple_y > HEIGHT:

            lives -= 1

            apple_x = random.randint(
                60,
                WIDTH - 60
            )

            apple_y = -50

            # Immediately adjust difficulty
            # after losing a life

            if lives == 2:

                apple_speed = max(
                    apple_speed,
                    TWO_LIVES_SPEED
                )

            elif lives == 1:

                apple_speed = max(
                    apple_speed,
                    ONE_LIFE_SPEED
                )

            # Game over

            if lives <= 0:

                lives = 0

                if score > high_score:

                    high_score = score

                game_state = GAME_OVER


    # =====================================================
    # DRAW
    # =====================================================

    if game_state == MENU:

        draw_menu()

    elif game_state == INSTRUCTIONS:

        draw_instructions()

    elif game_state == PLAYING:

        draw_game()

    elif game_state == GAME_OVER:

        draw_game_over()


    pygame.display.update()

    clock.tick(60)


pygame.quit()
