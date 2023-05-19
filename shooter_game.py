from pygame import (
    font,
    mixer,
    sprite,
    display,
    transform,
    image,
    event,
    QUIT,
    KEYDOWN,
    key,
    K_LEFT,
    K_RIGHT,
    time,
    K_SPACE,
)
from random import randint


# Определяем шрифты
font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2 = font.SysFont("Arial", 36)

# Определяем картинки для разных элементов

img_back = "galaxy.jpg" # Основной фон
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # противник


# Определяем фоновую музыку
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


# Определяем переменные игры

score = 0 # количество сбитых кораблей
goal = 20 # сколько надо сбить для победы
lost = 0 # количество пропущенных кораблей

# при достижении этого числа пропущенных кораблей объявляется поражение
max_lost = 5


class GameSprite(sprite.Sprite):
    """
    Класс-родитель спрайтов
    """
    def __init__(self, 
                player_image, 
                player_x: int, 
                player_y: int, 
                size_x: int, 
                size_y: int, 
                player_speed: int
                ):
        sprite.Sprite.__init__(self)


        # определяем поле image - изображение спрайта
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed  

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        """
        Метод для отрисовки спрайта
        """
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):

    """
    Класс для главного спрайта
    """

    def update(self):
        """ Метод для управления спрайтом """
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        """ Метод для выстрела """
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Enemy(GameSprite):
    """ Класс для врага """

    def update(self):
        """ Метод для передвижения спрайта """
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    """ Класс для пули """

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


# Создание рабочего окна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# Создание главного спрайта
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Создание группы монстров
monsters = sprite.Group()

for _ in range(5):
   monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)))

bullets = sprite.Group()

# Флаг для финиша
finish = False

# Флаг открытого окна
run = True

while run:

    # Обработчик нажатий на кнопки
    for e in event.get():
        if e.type == QUIT:  # Если нажата кнопка Закрыть
            run = False  # выход из игры
        elif e.type == KEYDOWN:  # Если пробел - выстрел
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:

        window.blit(background,(0,0))

        # Обновление спрайтов
        ship.update()
        monsters.update()
        bullets.update()


        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Столкновение пули и монстра 

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        # Варианты проигрыша
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        # Проверка набранных очков
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        # Вывод статистики
        text = font2.render(f"Счет: {str(score)}", 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()

    # Перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()


        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
    time.delay(50)
