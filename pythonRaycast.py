import pygame
import math

# Pygame初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Detection")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 形状の設定
circle = pygame.Rect(300, 200, 50, 50)
square = pygame.Rect(400, 300, 100, 100)
triangle = [(600, 250), (550, 400), (650, 400)]
selected_shape = None

# 円と四角の交差判定
def circle_rect_collision(circle, rect):
    circle_center = (circle.x + circle.width // 2, circle.y + circle.height // 2)
    closest_x = max(rect.left, min(circle_center[0], rect.right))
    closest_y = max(rect.top, min(circle_center[1], rect.bottom))
    distance = math.hypot(circle_center[0] - closest_x, circle_center[1] - closest_y)
    return distance < circle.width // 2

# 点と三角形の内外判定
def point_in_triangle(pt, tri):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    b1 = sign(pt, tri[0], tri[1]) < 0.0
    b2 = sign(pt, tri[1], tri[2]) < 0.0
    b3 = sign(pt, tri[2], tri[0]) < 0.0
    
    return (b1 == b2) and (b2 == b3)

# 円と三角形の交差判定
def circle_triangle_collision(circle, tri):
    circle_center = (circle.x + circle.width // 2, circle.y + circle.height // 2)
    if point_in_triangle(circle_center, tri):
        return True
    return False

# 四角と三角の交差判定
def rect_triangle_collision(rect, tri):
    for x in range(rect.left, rect.right + 1, rect.width):
        for y in range(rect.top, rect.bottom + 1, rect.height):
            if point_in_triangle((x, y), tri):
                return True
    return False

# メインループ
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if circle.collidepoint(mx, my):
                selected_shape = "circle"
            elif square.collidepoint(mx, my):
                selected_shape = "square"
            elif point_in_triangle((mx, my), triangle):
                selected_shape = "triangle"
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_shape = None
        elif event.type == pygame.MOUSEMOTION and selected_shape:
            dx, dy = event.rel
            if selected_shape == "circle":
                circle.move_ip(dx, dy)
            elif selected_shape == "square":
                square.move_ip(dx, dy)
            elif selected_shape == "triangle":
                triangle = [(x + dx, y + dy) for x, y in triangle]
    
    # 判定
    circle_hit_square = circle_rect_collision(circle, square)
    circle_hit_triangle = circle_triangle_collision(circle, triangle)
    square_hit_triangle = rect_triangle_collision(square, triangle)
    
    # 描画
    pygame.draw.ellipse(screen, RED if circle_hit_square else BLUE, circle)
    pygame.draw.rect(screen, RED if square_hit_triangle else BLUE, square)
    pygame.draw.polygon(screen, RED if circle_hit_triangle else GREEN, triangle)
    
    pygame.display.flip()
    
pygame.quit()
