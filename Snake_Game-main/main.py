'''https://hubberboss.github.io/cobra/'''
import pygame
import random
import time
import sys

# 游戏窗口尺寸
width = 640
height = 480

# 初始化Pygame
pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# 定义贪吃蛇初始位置和大小
snake_pos = [width // 2 - 10, height // 2 + 10]
snake_body = [[width // 2 - 10, height // 2 + 10]]

# 定义食物初始位置
food_pos = [random.randrange(1, width // 10) * 10,
            random.randrange(1, height // 10) * 10]
food_spawn = True

# 初始化移动方向、速度
direction = "RIGHT"
change_to = direction
speed = 15
long_hold = 1

# 定义游戏状态
game_over = False

# 初始化分数
score = 0

# 读取最高分数
with open('data/Highest_Score.dat', 'r', encoding='utf-8') as file:
    file.seek(0)
    Highest_Score = float(file.read())

# 设置字体样式
font_style = pygame.font.SysFont(None, 30)

# 设置分数显示位置和颜色
score_pos = (10, 10)
score_color = (0, 0, 0)

# 渐变色起始颜色和结束颜色
start_color = (0, 255, 0)
end_color = (0, 127, 0)

# 设置游戏结束文本显示位置和颜色
game_over_pos = (width // 2, height // 2)
game_over_color = (255, 0, 0)

# 游戏循环
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # 获取键盘输入
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            elif event.key == pygame.K_DOWN:
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT:
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    # 根据输入更新移动方向
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    elif change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    elif change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    elif change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # 根据移动方向更新蛇的位置
    if direction == "UP":
        snake_pos[1] -= 10
    elif direction == "DOWN":
        snake_pos[1] += 10
    elif direction == "LEFT":
        snake_pos[0] -= 10
    elif direction == "RIGHT":
        snake_pos[0] += 10

    Long = len(snake_body)

    # 更新贪吃蛇的身体
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
        score += 0.5*random.randint(1, 4)*Long
    else:
        snake_body.pop()

    #计算速度
    if Long - long_hold >= 5:
        speed += 1
        long_hold = Long

    # 生成新的食物
    if not food_spawn:
        food_pos = [random.randrange(
            1, width // 10) * 10, random.randrange(1, height // 10) * 10]
    food_spawn = True

    # 计算渐变色步长
    step_r = (end_color[0] - start_color[0]) / Long
    step_g = (end_color[1] - start_color[1]) / Long
    step_b = (end_color[2] - start_color[2]) / Long

    # 绘制游戏窗口
    window.fill((255, 255, 200))
    for i, pos in enumerate(snake_body):
        # 计算当前矩形的渐变色
        color_r = int(start_color[0] + step_r * i)
        color_g = int(start_color[1] + step_g * i)
        color_b = int(start_color[2] + step_b * i)
        color = (color_r, color_g, color_b)

        pygame.draw.rect(window, color, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(window, (128, 128, 128), pygame.Rect(
            pos[0], pos[1], 10, 10), 1)  # 添加灰色边框

    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(
        food_pos[0], food_pos[1], 10, 10))
    pygame.draw.rect(window, (128, 128, 128), pygame.Rect(
        food_pos[0], food_pos[1], 10, 10), 1)  # 添加灰色边框

    # 绘制分数
    score_text = font_style.render("Score: " + str(score), True, score_color)
    window.blit(score_text, score_pos)

    # 判断游戏结束条件
    if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
        game_over = True
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over = True

    if game_over:
        if score > Highest_Score:
            with open('data/data.dat', 'w', encoding='utf-8') as file:
                file.write(str(score))
                Highest_Score = score
        # 绘制游戏结束文本
        game_over_text = font_style.render("Game Over", True, game_over_color)
        game_over_text_pos = game_over_text.get_rect(center=game_over_pos)
        window.blit(game_over_text, game_over_text_pos)
        # 更新游戏窗口显示
        pygame.display.update()
        # 控制游戏速度
        pygame.time.Clock().tick(0)
        # 检测空格以决定是否重新开始，5秒没有反馈自动退出
        times = 0
        while times < 501 and game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        snake_pos = [width // 2 - 10, height // 2 + 10]
                        snake_body = [[width // 2 - 10, height // 2 + 10]]
                        food_pos = [random.randrange(
                            1, width // 10) * 10, random.randrange(1, height // 10) * 10]
                        food_spawn = True
                        direction = "RIGHT"
                        change_to = direction
                        speed = 15
                        game_over = False
                        score = 0
                        times = 0
            times += 1
            time.sleep(0.01)

    # 更新游戏窗口显示
    pygame.display.update()

    # 控制游戏速度
    pygame.time.Clock().tick(speed)

sys.exit()