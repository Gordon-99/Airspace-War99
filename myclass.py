import pygame
from random import *

# 小型敌机
class SmallEnemy(pygame.sprite.Sprite):      #基于动画精灵创建子类
    def __init__(self, screen_size):         #
        pygame.sprite.Sprite.__init__(self)  #初始化动画精灵

        self.image = pygame.image.load("images/2.png").convert_alpha()  #加载飞机图片
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()      #获取图片的rect
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 2   #敌机下落的速度
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5*self.height,0)
        self.mask = pygame.mask.from_surface(self.image)  #获取小敌机的轮廓

        self.down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
        self.down_sound.set_volume(0.3)

    def move(self):    #定义飞机移动的方法
        if self.rect.top < self.height - 60: 
            self.rect.top +=  self.speed   
        else:
            self.reset()
    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5*self.height,0)    
    def play_sound(self):
        self.down_sound.play()

# 中型敌机
class MidEnemy(pygame.sprite.Sprite):
    ENERGY = 10
    def __init__(self,screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/3.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy2_down1.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 1
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10*self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)

        self.down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
        self.down_sound.set_volume(0.3)

    def move(self):
        if self.rect.top < self.height - 60:
            self.rect.top +=  self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10*self.height,0)

    def play_sound(self):
        self.down_sound.play()


#我的飞机
class myPlane(pygame.sprite.Sprite):
    def __init__(self,screen,screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('./images/1.png').convert_alpha()
        self.image2 = pygame.image.load('./images/1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.width,self.height = screen_size[0],screen_size[1]
        self.rect.left,self.rect.bottom = (self.width-self.rect.width)//2, self.height-10
 
        self.screen = screen
        self.speed = 10
        self.switch_image = True
        self.delay = 100
 
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('./images/me_destroy_1.png').convert_alpha(),
            pygame.image.load('./images/me_destroy_2.png').convert_alpha(),
            pygame.image.load('./images/me_destroy_3.png').convert_alpha(),
            pygame.image.load('./images/me_destroy_4.png').convert_alpha()])
        self.active = True
        self.down_sound = pygame.mixer.Sound("sound/me_down.wav")    # 添加音效
        self.down_sound.set_volume(0.2)
 
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
 
    def moveDown(self):
        if self.rect.bottom < self.height-10:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height-10
 
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
 
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
 
    def animation(self):
        if self.switch_image:
            self.screen.blit(self.image1, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)
        if self.delay % 5 == 0:
            self.switch_image = not self.switch_image
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100
 
    def time_delay(self):    # 作为整个游戏动态切换的时钟
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100
 
    def reset(self):    # 添加重生的方法
        self.active = True
        self.rect.left, self.rect.bottom = (self.width - self.rect.left) // 2, self.height - 10
 
    def play_sound(self):    # 播放坠毁音效
        self.down_sound.play()
#子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(
            "./images/bullet2.png").convert_alpha()    # 加载子弹的图片
        self.rect = self.image.get_rect()            # 获取子弹的rect对象
        self.rect.left, self.rect.top = position     # 设置子弹的初始位置
        self.speed = 12        # 设置子弹移动的速度
        self.active = True     # 表示子弹是否超出窗体
        self.mask = pygame.sprite.from_surface(self.image)    # 获取子弹的轮廓
        self.direction = direction    # 子弹的方向

    def move(self):
        if self.direction:    # 如果子弹的方向是向上的，direction为True
            self.rect.top -= self.speed    # 移动子弹
            if self.rect.top < 0:          # 判断子弹有没有超出边界
                self.active = False        # 超出边界及修改标志位
        else:
            self.rect.top += self.speed
            if self.rect.top > 700:
                self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position    # 子弹重生
        self.active = True                          # 修改标志位
