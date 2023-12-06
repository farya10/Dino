import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run, Dino!')

loss_sound = pygame.mixer.Sound('loss.mp3')
heart_plus_sound = pygame.mixer.Sound('hp+.mp3')
button_sound = pygame.mixer.Sound('button.mp3')
bullet_sound = pygame.mixer.Sound('shot.mp3')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load('Cactus0.png'), pygame.image.load('Cactus1.png'), pygame.image.load('Cactus2.png')]
cactus_options = [51, 431, 70, 410, 50, 420]

stone_img = [pygame.image.load('Stone0.png'), pygame.image.load('Stone1.png')]
cloud_img = [pygame.image.load('Cloud0.png'), pygame.image.load('Cloud1.png')]

dino_img = [pygame.image.load('Dino0.png'), pygame.image.load('Dino1.png'), pygame.image.load('Dino2.png'),
            pygame.image.load('Dino3.png'), pygame.image.load('Dino4.png')]

health_img = pygame.image.load('heart.png')

bullet_img = pygame.image.load('shot.png')
bullet_img = pygame.transform.scale(bullet_img, (30, 9))

img_counter = 0
health = 3


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (17, 100, 180)
        self.active_clr = (62, 95, 138)

    def draw(self, x, y, message, action=None, font_size=40):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 8
        self.speed_y = 0
        self.dest_x = 0
        self.dest_y = 0

    def move(self):
        self.x += self.speed_x
        if self.x <= display_width:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False

    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

        delta_x = dest_x - self.x
        count_up = delta_x // self.speed_x
        if self.y >= dest_y:
            delta_y = self.y - dest_y
            self.speed_y = delta_y / count_up
        else:
            delta_y = dest_y - self.y
            self.speed_y = -(delta_y / count_up)

    def move_to(self):
        self.x += self.speed_x
        self.y -= self.speed_y

        if self.x <= display_width and self.y >= 0:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False


class GameVariables:
    def __init__(self):
        self.make_jump = False
        self.jump_counter = 30
        self.scores = 0
        self.max_scores = 0
        self.max_above = 0
        self.cooldown = 0
        self.usr_width = 60
        self.usr_height = 100
        self.usr_x = display_width // 3
        self.usr_y = display_height - self.usr_height - 100
        self.cactus_width = 20
        self.cactus_height = 70
        self.cactus_x = display_width - 50
        self.cactus_y = display_height - self.cactus_height - 100
        self.img_counter = 0
        self.health = 3
        self.display_width = 800
        self.display_height = 600


game_vars = GameVariables()

usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

cooldown = 0


def show_menu():
    menu_bckgr = pygame.image.load('menu.jpg')

    pygame.mixer.music.load('menu_music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    start_btn = Button(230, 70)
    quit_btn = Button(120, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(menu_bckgr, (0, 0))
        start_btn.draw(270, 200, 'Start game', start_game, 50)
        quit_btn.draw(330, 300, 'Quit', quit, 55)

        pygame.display.update()
        clock.tick(60)


def start_game():
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while game_cycle():
        game_vars.scores = 0
        game_vars.make_jump = False
        game_vars.jump_counter = 30
        game_vars.usr_y = display_height - usr_height - 100
        game_vars.health = 2
        game_vars.cooldown = 0


def game_cycle():
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load('land.png')

    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 50, health_img, 4)

    all_btn_bullets = []
    all_ms_bullets = []

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            game_vars.make_jump = True

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Scores: ' + str(scores), 630, 10)

        draw_array(cactus_arr)
        move_objects(stone, cloud)

        draw_dino()

        if keys[pygame.K_ESCAPE]:
            pause()

        if not game_vars.cooldown:
            if keys[pygame.K_x]:
                pygame.mixer.Sound.play(bullet_sound)
                all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y + 28))
                game_vars.cooldown = 50
            elif click[0]:
                pygame.mixer.Sound.play(bullet_sound)
                add_bullet = Bullet(usr_x + usr_width, usr_y + 28)
                add_bullet.find_path(mouse[0], mouse[1])
                all_ms_bullets.append(add_bullet)
                game_vars.cooldown = 50
        else:
            print_text('Cooldown time: ' + str(game_vars.cooldown // 10), 540, 40)
            game_vars.cooldown -= 1

        for bullet in all_btn_bullets:
            if not bullet.move():
                all_btn_bullets.remove(bullet)

        for bullet in all_ms_bullets:
            if not bullet.move_to():
                all_ms_bullets.remove(bullet)

        heart.move()
        hearts_plus(heart)

        if game_vars.make_jump:
            jump()

        if check_collision(cactus_arr):
            pygame.mixer.music.stop()
            game = False

        show_health()

        pygame.display.update()
        clock.tick(70)
    return game_over()


def jump():
    if game_vars.jump_counter >= -30:
        game_vars.usr_y -= game_vars.jump_counter / 2.5
        game_vars.jump_counter -= 1
    else:
        game_vars.jump_counter = 30
        game_vars.make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)


def draw_dino():
    if game_vars.img_counter == 25:
        game_vars.img_counter = 0

    display.blit(dino_img[game_vars.img_counter // 5], (usr_x, usr_y))
    game_vars.img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='DoorsDefinitiveRegularr.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 431 or barrier.y == 410 or barrier.y == 420:  # маленький кактус
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 40 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 20 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 40 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True

    return False


def count_scores(barriers):
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    above_cactus += 1

        game_vars.max_above = max(game_vars.max_above, above_cactus)
    else:
        if jump_counter == -30:
            game_vars.scores += game_vars.max_above
            game_vars.max_above = 0


def game_over():
    if game_vars.scores > game_vars.max_scores:
        game_vars.max_scores = game_vars.scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press enter to play again, Esc to exit', 40, 300)
        print_text('Max scores: ' + str(game_vars.max_scores), 300, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def show_health():
    show = 0
    x = 20
    while show != game_vars.health:
        display.blit(health_img, (x, 20))
        x += 60
        show += 1


def check_health():
    game_vars.health -= 1
    if game_vars.health == 0:
        pygame.mixer.Sound.play(loss_sound)
        return False
    else:
        return True


def hearts_plus(heart):
    if heart.x <= -heart.width:
        radius = display_width + random.randrange(500, 1700)
        heart.return_self(radius, heart.y, heart.width, heart.image)

    if game_vars.usr_x <= heart.x <= game_vars.usr_x + game_vars.usr_width:
        if game_vars.usr_y <= heart.y <= game_vars.usr_y + game_vars.usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if game_vars.health < 5:
                game_vars.health += 1

            radius = display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, heart.image)


show_menu()
pygame.quit()
quit()
