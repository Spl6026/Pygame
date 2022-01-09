import pygame
import random
import os

FPS = 60
WIDTH = 1920
HEIGHT = 1020

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("華華不要")
clock = pygame.time.Clock()

# 圖片
background = pygame.image.load(os.path.join("image", "background.png")).convert()
background0 = pygame.image.load(os.path.join("image", "background0.jpg")).convert()
background1 = pygame.image.load(os.path.join("image", "background1.jpg")).convert()
icon = pygame.image.load(os.path.join("image", "icon.png")).convert_alpha()
pygame.display.set_icon(icon)
player_image = pygame.image.load(os.path.join("image", "player.png")).convert_alpha()
player_mask_image = pygame.image.load(os.path.join("image", "water.png")).convert_alpha()
player_hide_image = pygame.image.load(os.path.join("image", "player_hide.png")).convert_alpha()
bullet_image = pygame.image.load(os.path.join("image", "bullet.png")).convert_alpha()
wave_image = pygame.image.load(os.path.join("image", "wave.png")).convert_alpha()
heart_image = pygame.image.load(os.path.join("image", "heart.png")).convert_alpha()
heart_image = pygame.transform.scale(heart_image, (50, 50))
rock_image = []
expl_anim = {'lg': [], 'sm': [], 'player': []}
power_images = {'mic': pygame.image.load(os.path.join("image", "mic.png")).convert_alpha(),
                'dio': pygame.image.load(os.path.join("image", "dio.png")).convert_alpha()}
for i in range(7):
    rock_image.append(pygame.image.load(os.path.join("image", f"rock{i}.png")).convert_alpha())
for i in range(9):
    expl_image = (pygame.image.load(os.path.join("image", f"expl{i}.png")).convert_alpha())
    player_expl_image = (pygame.image.load(os.path.join("image", f"player_expl{i}.png")).convert_alpha())
    expl_anim['lg'].append(pygame.transform.scale(expl_image, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_image, (30, 30)))
    expl_anim['player'].append(pygame.transform.scale(player_expl_image, (250, 250)))

# 音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
dog_sound = pygame.mixer.Sound(os.path.join("sound", "dog.wav"))
ahoy_sound = pygame.mixer.Sound(os.path.join("sound", "ahoy.wav"))
hong_sound = pygame.mixer.Sound(os.path.join("sound", "hong.wav"))
toyz_sound = pygame.mixer.Sound(os.path.join("sound", "toyz.wav"))
cry_sound = pygame.mixer.Sound(os.path.join("sound", "cry.wav"))
din_sound = pygame.mixer.Sound(os.path.join("sound", "dinter.wav"))
go_sound = pygame.mixer.Sound(os.path.join("sound", "go.wav"))
leave_sound = pygame.mixer.Sound(os.path.join("sound", "leave.wav"))
water_sound = pygame.mixer.Sound(os.path.join("sound", "water.wav"))
dio_sound = pygame.mixer.Sound(os.path.join("sound", "dio.wav"))
pygame.mixer.music.load(os.path.join("sound", "bgm.wav"))

font_name = os.path.join("font.ttf")
# 宣告全域變數
change = False  # 判斷是否換背景，即判斷變身是否結束
unlimited = False  # 是否掃射子彈，即判斷道具時間是否結束


def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


def draw_text(surf, text, size, x, y, color, center):  # center是指此文字是否置中對齊
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    font_base = pygame.font.Font(font_name, size + 1)  # 加_base之變數是為文字底色
    text_surface_base = font_base.render(text, True, BLACK)
    text_rect_base = text_surface_base.get_rect()
    if center:
        text_rect.centerx = x
    else:
        text_rect.x = x
    text_rect.top = y
    text_rect_base.centerx = text_rect.centerx
    text_rect_base.top = text_rect.top
    surf.blit(text_surface_base, text_rect_base)
    surf.blit(text_surface, text_rect)


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 25
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_menu(surf, img, x, y):  # 此函式用來顯示加分機制於開始畫面
    for i in range(7):
        img_rect = img[i].get_rect()
        img_rect.x = x
        img_rect.y = y + 125 * i
        surf.blit(img[i], img_rect)
        xt = x + 100
        yt = y + 125 * i
        if i == 0:
            draw_text(screen, '打到+100分', 50, xt, yt, (72, 72, 147), False)
        if i == 1:
            draw_text(screen, '+7414啦', 50, xt, yt, (82, 82, 163), False)
        if i == 2:
            draw_text(screen, '+555555', 50, xt, yt, (91, 91, 174), False)
        if i == 3:
            draw_text(screen, '+150萬交保', 50, xt, yt, (116, 116, 185), False)
        if i == 4:
            draw_text(screen, '-1千萬在天堂M', 50, xt, yt, (129, 129, 193), False)
        if i == 5:
            draw_text(screen, '+1萬名觀眾', 50, xt, yt, (153, 153, 204), False)
        if i == 6:
            draw_text(screen, '大牌不潔+300', 50, xt, yt, (167, 167, 211), False)


def draw_item(surf, img, x, y):  # 此函式用來顯示寶物之功能於開始畫面
    count = 0
    for i in img:
        img_rect = img[i].get_rect()
        img_rect.x = x
        img_rect.y = y + 125 * count
        image = pygame.transform.scale(img[i], (100, 110))
        surf.blit(image, img_rect)
        xt = x - 450
        yt = y + 125 * count
        if count == 0:
            draw_text(screen, '吃到華華就能變身', 50, xt, yt, (180, 217, 217), False)
            draw_text(screen, '吃越多變身越久', 30, xt + 200, yt + 60, (180, 217, 217), False)
        if count == 1:
            draw_text(screen, '吃到子彈會變多哦', 50, xt, yt, (180, 217, 217), False)
        count += 1


def draw_init():
    screen.blit(background, (0, 0))
    draw_text(screen, '我叫華華', 115, WIDTH / 2, HEIGHT / 4, WHITE, True)
    draw_text(screen, 'W A S D 移動', 44, WIDTH / 2, HEIGHT / 2, (255, 214, 235), True)
    draw_text(screen, '空白鍵發射', 40, WIDTH / 2, HEIGHT / 2 + 100, (255, 214, 235), True)
    draw_text(screen, '按任意鍵開始', 30, WIDTH / 2, HEIGHT * 3 / 4, (255, 168, 212), True)
    draw_menu(screen, rock_image, 50, 100)
    draw_item(screen, power_images, WIDTH - 150, HEIGHT / 2 - 100)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYUP:
                waiting = False
                return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (108, 192))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.speedy = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.change_time = 0
        self.count_time = 0  # 計算增加多久變身時間
        self.d_music = False  # 判斷是否換背景音樂
        self.bullet_change = False  # 判斷是否換子彈
        self.first = True  # 判斷是否為第一次進入change函式，以避免重複更換bgm

    def update(self):
        now = pygame.time.get_ticks()
        global change
        global unlimited
        if now - self.change_time > 10000 + self.count_time:  # 判斷變身時間
            change = False  # 將各數值回歸
            self.first = True
            self.bullet_change = False
            self.change_time = now
            self.count_time = 0
            self.image = pygame.transform.scale(player_image, (108, 192))
            Player.change_music(self)

        if self.gun > 1 and now - self.gun_time > 3000:  # 僅讓子彈掃射時間限制為三秒
            unlimited = False
            if now - self.gun_time > 10000:  # 讓子彈能射出兩發限制為十秒
                self.gun -= 1
                self.gun_time = now
        elif unlimited:
            player.shoot()

        if self.hidden and now - self.hide_time > 2000:  # 還原死亡之圖片
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.image = pygame.transform.scale(player_image, (108, 192))

        key_pressed = pygame.key.get_pressed()  # Player之移動
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        if not (self.hidden):  # 判斷是否死亡
            if self.gun == 1:  # 判斷子彈數目
                bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_change)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, self.bullet_change)
                bullet2 = Bullet(self.rect.right, self.rect.centery, self.bullet_change)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):  # 死亡後，將圖片換為透明之圖片
        global change
        change = False
        self.first = True
        self.bullet_change = False
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.image = pygame.transform.scale(player_hide_image, (10, 10))
        Player.change_music(self)

    def change(self):  # 變身之函式
        self.image = player_mask_image  # 更換圖片
        self.change_time = pygame.time.get_ticks()
        self.bullet_change = True
        self.count_time += 3000
        water_sound.play()
        if self.first:  # 若為第一次進入此函式，則更換bgm及background之image
            global change
            change = True
            self.d_music = True
            self.first = False
            pygame.mixer.music.load(os.path.join("sound", "melody.wav"))
            pygame.mixer.music.play(-1)

    def gunup(self):  # 增加子彈數目
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

    def change_music(self):  # 判斷是否已更換bgm
        if self.d_music:
            self.d_music = False
            pygame.mixer.music.load(os.path.join("sound", "bgm.wav"))
            pygame.mixer.music.play(-1)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_image)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - self.rect.width / 15)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -150)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, change):  # change為判斷子彈是否有更換
        pygame.sprite.Sprite.__init__(self)
        if change:
            self.image = wave_image
        else:
            self.image = pygame.transform.scale(bullet_image, (26, 94))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['mic', 'dio'])
        self.image = power_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


R0 = int(rock_image[0].get_width() / 2 - rock_image[0].get_width() / 15)  # R0~R6為每顆石頭之邊界
R1 = int(rock_image[1].get_width() / 2 - rock_image[1].get_width() / 15)
R2 = int(rock_image[2].get_width() / 2 - rock_image[2].get_width() / 15)
R3 = int(rock_image[3].get_width() / 2 - rock_image[3].get_width() / 15)
R4 = int(rock_image[4].get_width() / 2 - rock_image[4].get_width() / 15)
R5 = int(rock_image[5].get_width() / 2 - rock_image[5].get_width() / 15)
R6 = int(rock_image[6].get_width() / 2 - rock_image[6].get_width() / 15)
pygame.mixer.music.play(-1)

show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
    clock.tick(FPS)
    # 輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新
    all_sprites.update()

    # Bullets&Rocks
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        if hit.radius == R0:  # 每顆石頭分開計分
            dog_sound.play()
            score += 100
        if hit.radius == R1:
            ahoy_sound.play()
            score += 7414
        if hit.radius == R2:
            hong_sound.play()
            score += 555555
        if hit.radius == R3:
            toyz_sound.play()
            score += 1500000
        if hit.radius == R4:
            din_sound.play()
            score -= 10000000
        if hit.radius == R5:
            cry_sound.play()
            score += 10000
        if hit.radius == R6:
            go_sound.play()
            score += 300
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # Rocks&Player
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_rock()
        player.health -= hit.radius
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            leave_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    # Powers&Player
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'mic':  # 變身
            player.change()
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif hit.type == 'dio':  # 掃射
            dio_sound.play()
            player.gunup()
            unlimited = True

    if player.lives == 0 and not (die.alive()):
        show_init = True

    # 畫面
    if change:  # 切背景
        screen.blit(background1, (0, 0))
    else:
        screen.blit(background0, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 36, WIDTH / 2, 10, BLACK, True)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, heart_image, WIDTH - 200, 15)

    pygame.display.update()

pygame.quit()
