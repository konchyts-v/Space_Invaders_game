# -*- coding: utf-8 -*-
# Space Invaders
# Гра
from livewires import games, color
import random

# initialization a screen
games.init(screen_width = 640, screen_height = 480, fps = 50)
#gradient_image = games.load_image("Space_Invaders_background.jpg", transparent = False)
#games.screen.background = gradient_image

# create a class of "Warrior"
class Warrior(games.Sprite):
    image = games.load_image("Warrior_sprites/starship.bmp")

    MISSILE_DELAY = 120
    LIFE = 4
    def __init__(self, game):
        """ Initialization the warrior. """
        super(Warrior, self).__init__(image = Warrior.image,
                                  x = games.screen.width/2,
                                  y = games.screen.height - 25)
        self.missile_wait = 0
        self.game = game

    def update(self):
        """ move and strike. """
        # рух воїна
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 5
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 5
        # заборона на вихід за межі
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        # перевірка на дозвіл запуску ракети
        if self.missile_wait > 0:
            self.missile_wait -= 1
        # якщо відбулась перезарядка та натискули пробіл - постріл
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile_of_warrior(x = self.x + 1, y = self.y - 20)
            games.screen.add(new_missile)
            self.missile_wait = Warrior.MISSILE_DELAY

    def die(self):
        #self.destroy()
        self.missile_wait = 0
        if Warrior.LIFE > 0:
            Warrior.LIFE -= 1
        if Warrior.LIFE <= 0:
            self.game.end()
        self.game.lifes.value = "Life: " + str(Warrior.LIFE)

# create a missile of warrior
class Missile(games.Animation):
    """ Базовий клас для всіх ракет. """
    images = ["Alien_sprites/missile_of_weak_alien01.bmp", "Alien_sprites/missile_of_weak_alien02.bmp", "Alien_sprites/missile_of_weak_alien03.bmp", "Alien_sprites/missile_of_weak_alien02.bmp"]
  
    def update(self):
        """ """
        if self.top < 0:
            self.destroy()
        # перевірка на перекриття
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        self.destroy()

class Missile_of_warrior(Missile):
    """ Ракета воїна. """
    images = ["Warrior_sprites/missile_of_warrior01.bmp","Warrior_sprites/missile_of_warrior02.bmp"]
    sound = games.load_sound("Sound/GUN.wav")
    def __init__(self, x, y):
        """ Initialization the missile bomb."""
        super(Missile_of_warrior, self).__init__(images = Missile_of_warrior.images,
                                      x = x, y = y,
                                      dy = -2, repeat_interval = 20)
        Missile_of_warrior.sound.play()

class Missile_of_alien(Missile):
    """ Ракета чужинця. """
    def __init__(self, x, y):
        """ Initialization the missile bomb."""
        super(Missile_of_alien, self).__init__(images = Missile.images,
                                      x = x, y = y,
                                      dy = 2, repeat_interval = 50)

class Missile_of_alien_strong(Missile):
    """ Ракета чужинця. """
    images = ["Alien_sprites/missile_of_strong_alien.bmp","Alien_sprites/missile_of_strong_alien_next.bmp"]
    def __init__(self, x, y):
        """ Initialization the missile bomb."""
        super(Missile_of_alien_strong, self).__init__(images = Missile_of_alien_strong.images,
                                      x = x, y = y,
                                      dy = 2, repeat_interval = 5)

class Missile_of_alien_average(Missile):
    """ Ракета чужинця. """
    images = ["Alien_sprites/missile_of_average_alien01.bmp","Alien_sprites/missile_of_average_alien02.bmp"]
    def __init__(self, x, y):
        """ Initialization the missile bomb."""
        super(Missile_of_alien_average, self).__init__(images = Missile_of_alien_average.images,
                                      x = x, y = y,
                                      dy = 2, repeat_interval = 5)
    


# create a defense for warrior
class Defense(games.Sprite):
    """ ssss. """
    IMAGES = (games.load_image("Defense/defense01.bmp"), games.load_image("Defense/defense02.bmp"), games.load_image("Defense/defense03.bmp"), games.load_image("Defense/defense04.bmp"),
              games.load_image("Defense/defense05.bmp"), games.load_image("Defense/defense06.bmp"), games.load_image("Defense/defense07.bmp"), games.load_image("Defense/defense08.bmp"))
    image = IMAGES[0]
    def __init__(self, x, y):
        """ Initialization the defense for warrior. """
        super(Defense, self).__init__(image = Defense.image,
                                     x = x, y = y)
        self.health = 0
        
    def die(self):
        self.health += 1
        
        if self.health == 8:
            self.destroy()
        else:
            self.set_image(Defense.IMAGES[self.health])


# create an Alien
class Alien(games.Animation):
    """ Створення ворогів. """
    WEAK = 3
    AVERAGE = 2
    STRONG = 1
    POINTS = 60
    images = ["Alien_sprites/alien_weak01.bmp",
             "Alien_sprites/alien_weak02.bmp"]
    total = 0

    def die(self):
        """ Смерть чужого. """
        Army.soldier_count -= 1
        self.destroy()
        for column in self.army.ARMY:
            if self in column:
                column.remove(self)
        for column in self.army.ARMY:
            if column == []:
                self.army.ARMY.remove(column)
        
        Alien.total -= 1
        self.game.score.value += int(Alien.POINTS/self.power)
        self.game.score.right = games.screen.width - 10
        
# create a Weak_Alien
class Alien_Weak(Alien):
    """ Створення слабких ворогів. """
    images = ["Alien_sprites/alien_weak01.bmp",
             "Alien_sprites/alien_weak02.bmp"]

    def __init__(self, x, y, game, army):
        """ Ініціалізація чужого. """
        Alien.total += 1
        self.army = army
        self.game = game
        super(Alien_Weak, self).__init__(images = Alien_Weak.images,
                                    x = x,
                                    y = y,
                                    repeat_interval = 20,
                                    dx = 0.5)
        self.power = 3
        
    def check_shot(self):
        """ Зменшує інтервал очікування та робить постріл. """
        new_missilee = Missile_of_alien(x = self.x, y = self.y + 25)
        games.screen.add(new_missilee)
        
# create an Average Alien
class Alien_Average(Alien):
    """ Створення слабких ворогів. """
    images = ["Alien_sprites/alien_average01.bmp",
             "Alien_sprites/alien_average02.bmp"]

    def __init__(self, x, y, game, army):
        """ Ініціалізація чужого. """
        Alien.total += 1
        self.army = army
        self.game = game
        super(Alien_Average, self).__init__(images = Alien_Average.images,
                                    x = x,
                                    y = y,
                                    repeat_interval = 20,
                                    dx = 0.5)
        self.power = 2
        
    def check_shot(self):
        """ Зменшує інтервал очікування та робить постріл. """
        new_missilee = Missile_of_alien_average(x = self.x, y = self.y + 25)
        games.screen.add(new_missilee)

# create a Strong Alien
class Alien_Strong(Alien):
    """ Створення слабких ворогів. """
    images = ["Alien_sprites/alien_strong01.bmp",
             "Alien_sprites/alien_strong02.bmp"]

    def __init__(self, x, y, game, army):
        """ Ініціалізація чужого. """
        Alien.total += 1
        self.army = army
        self.game = game
        super(Alien_Strong, self).__init__(images = Alien_Strong.images,
                                    x = x,
                                    y = y,
                                    repeat_interval = 20,
                                    dx = 0.5)
        self.power = 1
        
    def check_shot(self):
        """ Зменшує інтервал очікування та робить постріл. """
        new_missilee = Missile_of_alien_strong(x = self.x, y = self.y + 25)
        games.screen.add(new_missilee)

        
# create an army
class Army(games.Sprite):
    """ Створення армії. """
    image = games.load_image("Alien_sprites/army.bmp")
    ROW = 3
    COLUMN = 6
    
    
    soldier_count = 5
    def __init__(self, game):
        """ Створення армії чужих. """
        self.game = game
        self.ARMY =  [
            [Alien_Weak(x = 145, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 145, y = games.screen.height/2 - 50, game = self.game, army = self), Alien_Strong(x = 145, y = games.screen.height/2 - 100, game = self.game, army = self) ],
            [Alien_Weak(x = 190, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 190, y = games.screen.height/2 - 50, game = self.game, army = self), Alien_Strong(x = 190, y = games.screen.height/2 - 100, game = self.game, army = self) ],
            [Alien_Weak(x = 235, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 235, y = games.screen.height/2 - 50, game = self.game, army = self), Alien_Strong(x = 235, y = games.screen.height/2 - 100, game = self.game, army = self) ],
            [Alien_Weak(x = 280, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 280, y = games.screen.height/2 - 50, game = self.game, army = self), Alien_Strong(x = 280, y = games.screen.height/2 - 100, game = self.game, army = self) ],
            [Alien_Weak(x = 325, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 325, y = games.screen.height/2 - 50, game = self.game, army =  self), Alien_Strong(x = 325, y = games.screen.height/2 - 100, game = self.game, army = self) ],
            [Alien_Weak(x = 370, y = games.screen.height/2, game = self.game, army = self), Alien_Average(x = 370, y = games.screen.height/2 - 50, game = self.game, army = self), Alien_Strong(x = 370, y = games.screen.height/2 - 100, game = self.game, army = self) ]
            ]
        self.time_till_shot = 60
        super(Army, self).__init__(image = Army.image,
                                   x = 20, y = 20,
                                   is_collideable = False)
        for i in range(6):
            for j in range(3):
                games.screen.add(self.ARMY[i][j])
        self.game = game

    def update(self):
        """ Рух армії. """
        if self.ARMY:
            for column in self.ARMY:
                for soldier in column:
                     if soldier.left < 0 or soldier.right > games.screen.width:
                        for column in self.ARMY:
                            for soldier in column:
                                soldier.dx = -soldier.dx
                        break
        """ Постріли армії. """
        if self.ARMY:
            who = random.randrange(len(self.ARMY))
            if self.time_till_shot > 0:
                self.time_till_shot -= 1
            else:
                self.ARMY[who][0].check_shot()
                self.time_till_shot = 60
        # якщо чужих більше не лишилось, переходимо на новий рівень
        if Alien.total == 0:
            self.game.advance()

class Game(object):
    """ Game. """
    # об'єкт для ведення рахунку
    score = games.Text(value = 0,
                       color = color.white,
                       size = 30,
                       top = 5,
                       right = games.screen.width - 10,
                       is_collideable = False)
    lifes = games.Text(value = "Life: 4",
                       color = color.white,
                       size = 30,
                       top = 5,
                       left = 10,
                       is_collideable = False)
    def __init__(self):
        """ Ініціалізація об'єкту Game. """
        # level
        self.level = 0
        # завантаження звуку
        self.sound = games.load_sound("Sound/level.wav")
        # додати рахунок
        games.screen.add(Game.score)
        # додати життя
        games.screen.add(Game.lifes)
        # створення воїна
        self.warrior = Warrior(game = self)
        games.screen.add(self.warrior)
        # створення огорожі
        defense1 = Defense(x = games.screen.width-80, y = games.screen.height-100)
        defense2 = Defense(x = games.screen.width-240, y = games.screen.height-100)
        defense3 = Defense(x = games.screen.width-400, y = games.screen.height-100)
        defense4 = Defense(x = games.screen.width-560, y = games.screen.height-100)
        games.screen.add(defense1)
        games.screen.add(defense2)
        games.screen.add(defense3)
        games.screen.add(defense4)
        
    def play(self):
        """ Починає гру. """
        # запуск музики
        games.music.load("Sound/music_for_game.wav")
        games.music.play(-1)
        # завантаження фону
        main_image = games.load_image("Space_Invaders_background.jpg", transparent = False)
        games.screen.background = main_image
        # перехід на 1 рівень
        self.advance()
        # start the game
        games.screen.mainloop()

    def advance(self):
        """ Переводить гру на черговий рівень. """
        self.level += 1

        # створення армії
        
        army = Army(self)
        games.screen.add(army)

        # відображення номера рівня
        level_message = games.Message(value = "Level " + str(self.level),
                                      size = 40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = 50,
                                      is_collideable = False,
                                      lifetime = 3*games.screen.fps)
        games.screen.add(level_message)
        # звуковий ефект(окрім 1-го рівня)
        if self.level > 1:
            self.sound.play()

    def end(self):
        """ Завершення гри. """
        # 5 секунд Game Over + sound
        games.music.stop()
        end_message = games.Message(value = "Game Over",
                                    color = color.red,
                                    size = 90,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5*games.screen.fps,
                                    after_death = self.game_over,
                                    is_collideable = False)
        games.screen.add(end_message)
        self.sound_end = games.load_sound("Sound/SK3.wav")
        self.sound_end.play()

    def game_over(self):
        """ Статистика до гри. """
        Score_value = self.score.value
        for sprite in games.screen.all_objects:
            sprite.destroy()
        game_over_wall = games.load_image("game_over.jpg")
        games.screen.background = game_over_wall
        Score = games.Message(value = "Score: " + str(Score_value),
                              color = color.red,
                              size = 60,
                              x = games.screen.width/2,
                              y = games.screen.height/2,
                              lifetime = 7*games.screen.fps,
                              after_death = games.screen.quit,
                              is_collideable = False)
        games.screen.add(Score)

def main():
    game = Game()
    game.play()

main()

