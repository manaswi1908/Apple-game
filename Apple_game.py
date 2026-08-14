import pygame
import random

pygame.init()

# ==================== WINDOW ====================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Catcher 🍎")

clock = pygame.time.Clock()


# ==================== COLORS ====================

SKY_TOP = (80, 180, 245)
SKY_BOTTOM = (190, 230, 255)

GRASS = (80, 170, 65)
DARK_GRASS = (45, 130, 45)

BROWN = (130, 75, 30)
DARK_BROWN = (90, 45, 20)
LIGHT_BROWN = (190, 120, 55)

RED = (220, 35, 35)
DARK_RED = (150, 20, 20)
LIGHT_RED = (255, 90, 80)

GREEN = (45, 140, 45)

WHITE = (255, 255, 255)
YELLOW = (255, 220, 70)


# ==================== BASKET ====================

basket_width = 120
basket_height = 45

basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - 100

basket_speed = 3


# ==================== APPLE ====================

apple_size = 34

apple_x = random.randint(40, WIDTH - 40)
apple_y = 0

apple_speed = 3


# ==================== GAME DATA ====================

score = 0
lives = 3

game_over = False


# ==================== FONTS ====================

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)


# =========================================================
# SKY
# =========================================================

def draw_sky():

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        r = int(SKY_TOP[0] * (1 - ratio) + SKY_BOTTOM[0] * ratio)
        g = int(SKY_TOP[1] * (1 - ratio) + SKY_BOTTOM[1] * ratio)
        b = int(SKY_TOP[2] * (1 - ratio) + SKY_BOTTOM[2] * ratio)

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )


# =========================================================
# CLOUD
# =========================================================

def draw_cloud(x, y, scale=1):

    pygame.draw.circle(
        screen,
        WHITE,
        (int(x), int(y)),
        int(25 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (int(x + 30 * scale), int(y - 10 * scale)),
        int(32 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (int(x + 65 * scale), int(y)),
        int(25 * scale)
    )

    pygame.draw.ellipse(
        screen,
        WHITE,
        (
            int(x - 10 * scale),
            int(y),
            int(90 * scale),
            int(30 * scale)
        )
    )


# =========================================================
# TREE
# =========================================================

def draw_tree(x, y):

    # Trunk
    pygame.draw.rect(
        screen,
        DARK_BROWN,
        (x - 20, y, 40, 150)
    )

    # Branches
    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y + 40),
        (x - 50, y),
        15
    )

    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y + 45),
        (x + 55, y - 5),
        15
    )

    # Leaves
    pygame.draw.circle(
        screen,
        DARK_GRASS,
        (x - 55, y - 10),
        55
    )

    pygame.draw.circle(
        screen,
        GRASS,
        (x, y - 35),
        65
    )

    pygame.draw.circle(
        screen,
        GRASS,
        (x + 55, y - 10),
        55
    )

    pygame.draw.circle(
        screen,
        DARK_GRASS,
        (x, y + 10),
        60
    )


# =========================================================
# GROUND
# =========================================================

def draw_ground():

    pygame.draw.rect(
        screen,
        GRASS,
        (0, HEIGHT - 120, WIDTH, 120)
    )

    for x in range(0, WIDTH, 25):

        pygame.draw.line(
            screen,
            DARK_GRASS,
            (x, HEIGHT - 20),
            (x + 5, HEIGHT - 35),
            3
        )


# =========================================================
# FLOWER
# =========================================================

def draw_flower(x, y):

    pygame.draw.line(
        screen,
        DARK_GRASS,
        (x, y),
        (x, y + 25),
        2
    )

    pygame.draw.circle(
        screen,
        (255, 100, 120),
        (x, y),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + 6, y),
        5
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (x + 3, y + 3),
        3
    )


# =========================================================
# APPLE
# =========================================================

def draw_apple(x, y):

    # Apple body
    pygame.draw.circle(
        screen,
        DARK_RED,
        (x - 7, y + 2),
        18
    )

    pygame.draw.circle(
        screen,
        RED,
        (x + 7, y + 2),
        18
    )

    pygame.draw.circle(
        screen,
        RED,
        (x, y + 8),
        20
    )

    # Highlight
    pygame.draw.circle(
        screen,
        LIGHT_RED,
        (x - 8, y - 5),
        5
    )

    # Stem
    pygame.draw.line(
        screen,
        DARK_BROWN,
        (x, y - 10),
        (x + 3, y - 25),
        5
    )

    # Leaf
    pygame.draw.ellipse(
        screen,
        GREEN,
        (x + 2, y - 27, 18, 9)
    )


# =========================================================
# BASKET
# =========================================================

def draw_basket(x, y):

    # Handles
    pygame.draw.arc(
        screen,
        DARK_BROWN,
        (x + 5, y - 25, 35, 40),
        0,
        3.14,
        6
    )

    pygame.draw.arc(
        screen,
        DARK_BROWN,
        (
            x + basket_width - 40,
            y - 25,
            35,
            40
        ),
        0,
        3.14,
        6
    )

    # Basket body
    basket_points = [
        (x + 5, y),
        (x + basket_width - 5, y),
        (x + basket_width - 18, y + basket_height),
        (x + 18, y + basket_height)
    ]

    pygame.draw.polygon(
        screen,
        BROWN,
        basket_points
    )

    # Basket rim
    pygame.draw.ellipse(
        screen,
        LIGHT_BROWN,
        (
            x,
            y - 8,
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
            12
        )
    )

    # Horizontal woven lines
    for line_y in range(
        y + 10,
        y + basket_height,
        10
    ):

        pygame.draw.line(
            screen,
            LIGHT_BROWN,
            (x + 15, line_y),
            (x + basket_width - 15, line_y),
            3
        )

    # Vertical woven lines
    for line_x in range(
        x + 20,
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
# RESET GAME
# =========================================================

def reset_game():

    global score
    global lives
    global basket_x
    global apple_x
    global apple_y
    global game_over

    score = 0
    lives = 3

    basket_x = (WIDTH - basket_width) // 2

    apple_x = random.randint(
        40,
        WIDTH - 40
    )

    apple_y = 0

    game_over = False


# =========================================================
# GAME LOOP
# =========================================================

running = True

while running:

    # ==================== EVENTS ====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Play Again
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_over:
                reset_game()


    # ==================== MOVEMENT ====================

    keys = pygame.key.get_pressed()

    if not game_over:

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


    # ==================== APPLE ====================

    if not game_over:

        apple_y += apple_speed


    # Apple collision rectangle

    apple_rect = pygame.Rect(
        apple_x - apple_size // 2,
        apple_y - apple_size // 2,
        apple_size,
        apple_size
    )


    # Basket collision rectangle

    basket_rect = pygame.Rect(
        basket_x,
        basket_y,
        basket_width,
        basket_height
    )


    # ==================== CATCH ====================

    if (
        apple_rect.colliderect(basket_rect)
        and not game_over
    ):

        score += 1

        apple_y = -30

        apple_x = random.randint(
            40,
            WIDTH - 40
        )


    # ==================== MISS ====================

    if apple_y > HEIGHT and not game_over:

        lives -= 1

        apple_y = -30

        apple_x = random.randint(
            40,
            WIDTH - 40
        )

        # Game Over
        if lives <= 0:

            lives = 0
            game_over = True


    # =====================================================
    # DRAW
    # =====================================================

    draw_sky()

    # Clouds
    draw_cloud(100, 100, 1)
    draw_cloud(500, 150, 0.8)
    draw_cloud(680, 80, 0.7)

    # Tree
    draw_tree(700, 350)

    # Ground
    draw_ground()

    # Flowers
    draw_flower(100, 510)
    draw_flower(180, 530)
    draw_flower(600, 520)
    draw_flower(650, 500)

    # Apple
    if not game_over:
        draw_apple(
            apple_x,
            apple_y
        )

    # Basket
    draw_basket(
        basket_x,
        basket_y
    )


    # =====================================================
    # UI
    # =====================================================

    score_text = font.render(
        f"Score: {score}",
        True,
        DARK_BROWN
    )

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        DARK_BROWN
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        lives_text,
        (650, 20)
    )


    # =====================================================
    # GAME OVER SCREEN
    # =====================================================

    if game_over:

        # Dark overlay
        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))

        screen.blit(
            overlay,
            (0, 0)
        )


        # Game Over
        game_over_text = big_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2
                - game_over_text.get_width() // 2,
                200
            )
        )


        # Final Score
        final_score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            final_score_text,
            (
                WIDTH // 2
                - final_score_text.get_width() // 2,
                285
            )
        )


        # Play Again
        play_again_text = font.render(
            "Press SPACE to Play Again",
            True,
            YELLOW
        )

        screen.blit(
            play_again_text,
            (
                WIDTH // 2
                - play_again_text.get_width() // 2,
                350
            )
        )


    # Update display
    pygame.display.update()

    clock.tick(60)


pygame.quit()

