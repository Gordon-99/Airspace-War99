import pygame
import sys
from pygame.locals import *
import myclass



pygame.init()
screen_size = width, height = 480, 700                 #窗体尺寸
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('AA')                       #设置标题
bg = pygame.image.load('./images/4.jpeg').convert()    #加载背景图片
                                                       #convert的作用是将图片转化为像素格式，在进行图片刷新时，程序效率会更高

 
pygame.mixer.music.load('./sound/game_music.ogg')      #加载背景音乐
pygame.mixer.music.set_volume(0.2)                     #设置音量
pygame.mixer.music.play(-1)                            #播放背景音乐-1 循环播放
 


# 生成中敌机的方法
def add_mid_enemies(group1, group2, num):
    for mid_enemy_num in range(num):   # 这里的num是指飞机的数量
        each_mid_enemy = myclass.MidEnemy(screen_size)   #创建中敌机
        group1.add(each_mid_enemy)                       #将中敌机添加到组
        group2.add(each_mid_enemy)

# 生成小敌机的方法 
def add_small_enemies(group1, group2, num):
    for small_enemy_num in range(num):
        each_small_enemy = myclass.SmallEnemy(screen_size)
        group1.add(each_small_enemy)
        group2.add(each_small_enemy)
 

 
def main():
    clock = pygame.time.Clock()                  #创建一个clock对象，用来控制游戏每秒的帧数
 
    heroPlane = myclass.myPlane(screen, screen_size)   # 生成己方飞机
 
    enemies = pygame.sprite.Group()               # 创建全部敌机的组
 
    #中敌机
    mid_enemies = pygame.sprite.Group()           # 创建中敌机的组
    add_mid_enemies(mid_enemies, enemies, 4)      # 生成中敌机及数量

    #小敌机
    small_enemies = pygame.sprite.Group()           # 创建小敌机的组
    add_small_enemies(small_enemies, enemies, 15)   # 生成小敌机出现及数量


    #子弹
    bullet1 = []          # 生成己方飞机的子弹序列
    bullet1_index = 0     #子弹的序号
    BULLET1_NUM = 5       #表示五颗子弹连发
    for i in range(BULLET1_NUM):       # 序列生成子弹
        bullet1.append(myclass.Bullet(heroPlane.rect.midtop, True))   #子弹在飞机中上方生成，方向向上
 
    small_destroy_index = 0   #用来存储动画播放的下标
    mid_destroy_index = 0    
    hero_destroy_index = 0    # 击毁后己方飞机动画的序号
 
    life_image = pygame.image.load("images/life.png").convert_alpha()    #加载右下角我方飞机生命数-几条命 / 血量图
    life_rect = life_image.get_rect()    # 获取血量的rect
    life_NUM = 3     #我方飞机生命值-几条命 / 设置血量为3
 
    score = 0      #得分
    score_font = pygame.font.Font("font/font.ttf", 30)       #得分版字体及大小
    WhiteFont = (255, 255, 255)                              #白色字体
    gameover_font = pygame.font.Font("font/font.ttf", 48)    #游戏结束得分版字体及大小
    again_image = pygame.image.load("images/again.png").convert_alpha()         #加载again图片
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()   #加载gameover图片





    # Game Loop 游戏循环
    while True:                                      #死循环，让程序一直执行下去
        for event in pygame.event.get():         
            if event.type == QUIT:                   #如果事件的类型是退出
                pygame.quit()                        #先将pygame退出
                sys.exit()                           #系统关闭

 
        key_pressed = pygame.key.get_pressed()       # 获取按键信息，使操作更加平滑
        
        if key_pressed[K_UP]:                        # 如果方向上键按下
            heroPlane.moveUp()                       # 让飞机向上移动
        if key_pressed[K_DOWN]:
            heroPlane.moveDown()
        if key_pressed[K_LEFT]:
            heroPlane.moveLeft()
        if key_pressed[K_RIGHT]:
            heroPlane.moveRight()
 
        screen.blit(bg, (0, 0))         # 绘制背景图片-背景图片在屏幕中的位置
        heroPlane.time_delay()          # 显示飞机
 
        if life_NUM > 0:


            #绘制中敌机
            for each in mid_enemies:       # 遍历类，将每个中敌机都显示出来
                if each.active == True:    # 如果飞机是活着的
                    each.move()            # 改变飞机位置/移动并检测边界
                    screen.blit(each.image, each.rect)  #在窗体上绘制飞机
                else:    #飞机坠毁了
                    if not (heroPlane.delay % 3):   # 切换图片稍微延时一会儿
                        screen.blit(each.destroy_images[mid_destroy_index], each.rect)  # 绘制坠毁图片
                        mid_destroy_index = (mid_destroy_index + 1) % 4      #坠毁图片一共有4张
                        if mid_destroy_index == 0:  # 如果是最后一张
                            each.play_sound()       # 播放音效
                            score += 200      # 摧毁敌机 得分加200
                            each.reset()      # 重生中敌机
 
            #绘制小敌机
            for each in small_enemies:
                if each.active == True:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (heroPlane.delay % 3):
                        screen.blit(each.destroy_images[small_destroy_index], each.rect)
                        small_destroy_index = (small_destroy_index + 1) % 4
                        if small_destroy_index == 0:
                            each.play_sound()
                            score += 100      #碰撞小敌机 得分加100
                            each.reset()
 
            if heroPlane.active == True:      # 判断己方飞机的状态
                heroPlane.animation()         # 如果没有被击毁就正常移动
            else:
                if not (heroPlane.delay % 3):   # 做一定延迟
                    screen.blit(heroPlane.destroy_images[hero_destroy_index], heroPlane.rect)   # 绘制坠毁的图片
                    hero_destroy_index = (hero_destroy_index + 1) % 4    # 更改图片的序号
                    if hero_destroy_index == 0:
                        life_NUM -= 1
                        heroPlane.play_sound()
                        heroPlane.reset()
 
            if life_NUM > 0:   #生命值大于0时
                for i in range(life_NUM):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))
 
            if not (heroPlane.delay % 10): # 每十个指令周期发射一枚子弹
                bullet1[bullet1_index].reset(heroPlane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM
 

            # 绘制子弹
            for each in bullet1:              
                if each.active == True:       # 如果子弹没有飞出界面及击中飞机
                    each.move()
                    screen.blit(each.image, each.rect)    # 绘制子弹
                    enemies_hit = pygame.sprite.spritecollide(each, enemies, False,pygame.sprite.collide_mask)  #检测子弹是否与敌机发生碰撞 即为击中
                    if enemies_hit:           #如果发生击中，enemies就是True
                        each.active = False   #更改子弹状态
                        for e in enemies_hit:
                            if e in mid_enemies:   #如果击中敌机，那么就扣血
                                e.energy -= 1
                                if e.energy == 0:  #如果血扣完了，中敌机摧毁
                                    e.active = False
                            else:
                                e.active = False   #子弹重生
                else:
                    each.reset(heroPlane.rect.midtop)   #子弹在我方飞机中上方重生 
 
            enemies_collided = pygame.sprite.spritecollide(heroPlane, enemies, False, pygame.sprite.collide_mask)
 
            if enemies_collided:         # 如果与敌机碰撞，就被击毁
                heroPlane.active = False    # 更改己方飞机的状态
                for each in enemies_collided:
                    each.active = False     # 碰撞后，将敌机状态设置为False
 
            score_surface = score_font.render("Score : %s" % str(score), True, WhiteFont)
            screen.blit(score_surface, (10, 5))   #得分版在屏幕上的位置
        else:
            pygame.mixer.music.stop()   #背景音乐结束

            #游戏结束页面设置
            gameover_score = gameover_font.render("Score : %s" % str(score), True, WhiteFont)
            screen.blit(gameover_score,(100,200))    #得分版图片位置
            screen.blit(again_image, (90,350))       #again图片位置
            screen.blit(gameover_image, (90,450))    #gameover图片位置
 
            mouse_down = pygame.mouse.get_pressed()   #鼠标点击
            if mouse_down[0]:
                pos = pygame.mouse.get_pos()
                if 90 < pos[0] < 390 and 350 < pos[1] < 390:
                    main()
                elif 90 < pos[0] < 390 and 450 < pos[1] < 490:     
                    pygame.quit()
                    sys.exit()
 
        pygame.display.flip()           #刷新屏幕/游戏界面
        clock.tick(60)                  #设置游戏每秒60帧
 
if __name__ == '__main__':
    main()
