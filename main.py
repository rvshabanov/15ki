import pygame
from pygame.locals import *
from random import randint

# Константы
FPS = 300                     # Кадров в секунду. Есть связь с временем перемешивания версии 2
TILESIZE_X = 40               # Размер плитки по X
TILESIZE_Y = 40               # Размер плитки по Y
SIZE_X = 4 * TILESIZE_X       # Размер экрана по X - 4 * размер плитки по X
SIZE_Y = 4 * TILESIZE_Y       # Размер экрана по Y - 4 * размер плитки по Y
SHUFFLE_VERSION = 1           # Версия перемешивания: 1 - случайное заполнение;
                              # 2 - визуальное случайное перемешивание
                              # (исключает неразрешаемую задачу по перестановке 14 и 15)
SHUFFLE_STEPS = 1500          # Количество шагов по перемешиванию для версии 2

# Описание класса объектов App
# Все свойства и методы (функции) крутятся в нем
class App:
    # Инициализация объекта App
    # Определяем и задаем значения переменных объекта
    def __init__(self):
        self._running = True                # Игра выполняется
        self._display_surf = None           # Объект экран где будут отображаться плитки
        self.size = self.weight, self.height = SIZE_X, SIZE_Y   # Размер экрана
        self.clock = pygame.time.Clock()    # Часы
        self.fps = FPS                      # Кадров в секунду
        self.playtime = 0.0                 # Время игры
        self.shuffling = SHUFFLE_STEPS        # Количество шагов по перемешиванию версии 2

        # Загружаем в список картинки плиток используя функцию pygame.image.load
        # в tile_images[0] храниться пустая плитка, в tile_images[1] - единица, в tile_images[2] - двойка и т.д.
        self.tile_images = [
            pygame.image.load('resources\\16_1.png'),
            pygame.image.load('resources\\1.png'),
            pygame.image.load('resources\\2.png'),
            pygame.image.load('resources\\3.png'),
            pygame.image.load('resources\\4.png'),
            pygame.image.load('resources\\5.png'),
            pygame.image.load('resources\\6.png'),
            pygame.image.load('resources\\7.png'),
            pygame.image.load('resources\\8.png'),
            pygame.image.load('resources\\9.png'),
            pygame.image.load('resources\\10.png'),
            pygame.image.load('resources\\11.png'),
            pygame.image.load('resources\\12.png'),
            pygame.image.load('resources\\13.png'),
            pygame.image.load('resources\\14.png'),
            pygame.image.load('resources\\15.png'),
        ]

        # Создаем список где будем хранить и отслеживать перемещения плиток
        # Одна лишняя в конеце со знажением 99 нужна для алгоритма случайного заполнения
        # В комментариях ниже указан индекс, чтобы было нагляднее/не запутаться
        self.tiles = [          # индекс tiles[]
            1,  2,  3,  4,      # 0  1  2  3
            5,  6,  7,  8,      # 4  5  6  7
            9,  10, 11, 12,     # 8  9  10 11
            13, 14, 15, 0, 99,  # 12 13 14 15 16
        ]

    # Функция инициализации класса App
    # инициализируем то, что нельзя инициализировать выше
    def on_init(self):
        pygame.init()                               # Инициализация модуля pygame
        pygame.display.set_caption('15ки v1.0a')    # Устанавливаем название окна
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)    # Создаем объект экрана
        if SHUFFLE_VERSION == 1: self.shuffle1()    # Если версия перемешивани 1, иначе будет работать версия 2 в главном цикле
        self._running = True                        # Включаем основной цикл игры

    # Функция класса App перемешивает плитки
    # Версия 1
    def shuffle1(self):
        self.shuffling = 0
        # Случайным образом заполняем список с плитками
        # Сначала обнуляем все, кроме последней со значением 99
        for i in range(0, 16): self.tiles[i] = 0
        # Заполняем случаем образом
        # Перебираем в i цифры плиток от 1 до 15 и для каждой определяем место в списке
        # При этом проверяя, что там еще ничего нет, т.е. место в списке = 0
        for i in range(1, 16):
            r = 16                      # Чтобы обеспечить работу цикла ниже, для этого нужна техническая плитка со значением 99
            while self.tiles[r] != 0:   # Пока рандом не выбросит место в списке в котором будет 0, значит пусто и можно занять
                r = randint(0, 15)      # выбрасываем место случайным образом
            self.tiles[r] = i           # Ставим на это место плитку i

    # Функция класса App перемешивает плитки
    # Версия 2
    def shuffle2(self):
        event = pygame.event.Event(pygame.KEYDOWN, {'key' : randint(237, 276)})
        pygame.event.post(event)
        self.shuffling -= 1
        if self.shuffling == 0: print("SHUFFLE TIME: {:02}:{:02}".format(int(self.playtime / 60), int(self.playtime - int(self.playtime / 60) * 60)))


    # Функция класса App которая проверяет собрали ли мы пазл
    def done(self):
        # Если еще перемешиваем, то выходим
        if self.shuffling: return
        # В цикле перебираем все плитки, если позиция не соответствует плитке, то возвращаем Ложь
        # Правильное положение плиток вот такое:
        # 1  2  3  4
        # 5  6  7  8
        # 9  10 11 12
        # 13 14 15 --
        for i in range(15):
            if self.tiles[i] != i + 1: return False
        # Если дошли до сюда, то возвращаем Правда
        # Значит в цикле выше все плитки были на своем месте и 15ки собраны полностью и правильно
        return True

    # Функция класса App по обработке событий в игре
    # Например закрытие окна и нажатие клавиш
    def on_event(self, event):
        # Закрытие окна
        if event.type == pygame.QUIT:
            self._running = False
        # Нажатие клавиш
        if event.type == pygame.KEYDOWN:
            # Обработка клавиш - стрелок для управления головой и ESC дла выхода
            if event.key == K_LEFT:
                if self.tiles.index(0) in [0,1,2,4,5,6,8,9,10,12,13,14]:            # Если пустышка, т.е. 0 в позициях в которых можно сдвинуть его влево
                    zero_at = self.tiles.index(0)                                   # Запоминаем позицию пустышки, т.е. 0
                    k = self.tiles[zero_at + 1]                                     # Берем плитку справа
                    self.tiles[zero_at] = k                                         # Ставим ее на место пустышки
                    self.tiles[zero_at + 1] = 0                                     # Пустышки ставим на место справа
            elif event.key == K_RIGHT:                                              # Тут все тоже самое, но меняемся с плиткой слева
                if self.tiles.index(0) in [1,2,3,5,6,7,9,10,11,13,14,15]:
                    zero_at = self.tiles.index(0)
                    k = self.tiles[zero_at - 1]
                    self.tiles[zero_at] = k
                    self.tiles[zero_at - 1] = 0
            elif event.key == K_UP:
                if self.tiles.index(0) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:   # По вертикали такой же принцип, только плитка сверху и снизу
                    zero_at = self.tiles.index(0)                                   # индексируется как -4 и +4 соответственно
                    k = self.tiles[zero_at + 4]
                    self.tiles[zero_at] = k
                    self.tiles[zero_at + 4] = 0
            elif event.key == K_DOWN:
                if self.tiles.index(0) in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                    zero_at = self.tiles.index(0)
                    k = self.tiles[zero_at - 4]
                    self.tiles[zero_at] = k
                    self.tiles[zero_at - 4] = 0
            elif event.key == K_ESCAPE:                                             # Если нажали ESC, то завершаем игру
                self._running = False

    # Функция класса App работающая в главном цикле
    # Считаем время и проверяем собрали ли мы 15ки
    def on_loop(self):
        milliseconds = self.clock.tick(self.fps)                                    # Берем кол-во мс с прошедших последнего такта
        self.playtime += milliseconds / 1000.0                                      # Увеличиваем время игры на кол-во секунд (мс / 1000)
        if self.done():                                                             # Проверяем если собрали 15ки, то завершаем игру
            self._running = False

    # Функция класса App по отрисовке экрана игры
    # Очищаем экран (заполняем белым) и выводим плитки согласно их позициям в tiles
    def on_render(self):
        self._display_surf.fill((225, 225, 225))                                    # Заполняем экран белым
        for y in range(4):                                                          # Цикл по y от 0 до 3
            for x in range(4):                                                      # Вложенный цикл по x jn 0 до 3
                self._display_surf.blit(self.tile_images[self.tiles[y * 4 + x]], (x * TILESIZE_X, y * TILESIZE_Y)) # Выводим картинку плитки, которая стоит в позици y * 4 + x
        pygame.display.update()                                                     # По завершению цикла обновляем весь экран 1 раз

    # Функция класса App по завершению игры
    # Выводим время игры, очишаем память, разрушаем объекты и т.п.
    def on_cleanup(self):
        # Выводим в консоль прошедшее время игры
        print("PLAYTIME: {:02}:{:02}".format(int(self.playtime / 60), int(self.playtime - int(self.playtime / 60) * 60)))
        pygame.quit()                                       # Завершаем работу модуля pygame

    # Функция класса App работающая при начале игры
    # Инициализирум все, запускаем главный цикл в котором
    # обрабатываем события, вызываем on_loop и функцию по отрисовук on_render
    #
    def on_execute(self):
        if self.on_init() == False:                         # Инициализиркм все, вызывая on_init, если не успешно, то завершаем программу
            self._running = False

        while (self._running):                              # Главный цикл игры, пока running = True
            if self.shuffling:
                self.shuffle2()
            for event in pygame.event.get():                # Получаем событие от pygame
                self.on_event(event)                        # Обрабатываем событие
            self.on_loop()                                  # Обрабатываем время и проверяем собрали ли мы 15ки в методе on_loop
            self.on_render()                                # Отрисовываем все
        self.on_cleanup()                                   # По завершении цикла вызываем метод on_cleanup()


# Точка входа в программу, куда попадаем при запуске
# В ней создаем объект класса App и выполняем его метод on_execute()
if __name__ == "__main__":
    theApp = App()                                          # Создаем объект theApp типа App()
    theApp.on_execute()                                     # Вызываем метод on_execute объекта theApp
