# Определение персонажей игры.
define e = Character('Незнакомка', color="#291246")

# Игра начинается здесь:
label start:

# Флаги 

    $ flag_for_pic = 1
    $ sum_in_wardrobe = 1
    $ flag_for_key = 1
    $ flag_for_game_in_kitchen = 1

# Все функции которые будут использоваться в игре:

    python:
        def show_image(x):
            image_map = {
                0: "tabs0.png",
                1: "tabs1.png",
                2: "tabs2.png",
                3: "tabs3.png",
                4: "tabs4.png",
                5: "tabs5.png",
                6: "tabs6.png"
            }
            
            return image_map.get(x, None)

    jump act1

#Все локации которые будут использоваться в игре:

screen bedroom_map():
    imagemap:
        idle "bedroom"
        hover "bedroom2"


        hotspot (191, 191, 250, 400) action If(flag_for_pic == 0, Notify("Не могу больше смотреть на эти лица."), Jump("pic_in_bed"))

        hotspot (90, 620, 830, 320) action If(flag_for_key == 0, Notify("Я не устал."), Jump("key"))
# шкаф        hotspot (191, 191, 250, 400) action If(sum_in_wardrobe == 0, Notify("Не могу больше смотреть на эти лица."), Jump("wardrobe"))
#        hotspot (191, 191, 250, 400) action Jump("titles") alt "Swimming"
#        hotspot (191, 191, 250, 400) action Jump("titles") alt "Swimming"
#        hotspot (1390, 988, 530, 92) action If(flag_for_key == 1, Notify("Дверь заперта."), Jump("basement"))
        hotspot (1390, 988, 530, 92) action Jump("hallway")

label pic_in_bed:
    scene bedroom
    show pic:
        xalign 0.45
        yalign 0.5
    "Это… кто эти люди? Почему фотография здесь? Они имеют ко мне отношение?"
    "Дети… Они вызывают тревогу. Почему?"
    hide pic
    $ flag_for_pic = 0
    jump bedroom

label wardrode:

label key:
    scene bedroom
    show key
    play sound "key.mp3"
    "Ключ… Он от чего‑то важного"
    hide key    
    $ flag_for_key = 0
    jump bedroom

screen hallway_map():
    imagemap:
        idle "hallway"
        hover "hallway2"


        hotspot (640, 280, 300, 600) action Jump("bedroom")
        hotspot (1450, 50, 470, 1020) action If(flag_for_key == 1, Notify("Дверь заперта."), Jump("basement"))
        hotspot (1, 1, 400, 1080) action Jump("kitchen")

screen kitchen_map():
    imagemap:
        idle "kitchen"
        hover "kitchen2"

        hotspot (1, 900, 400, 180) action Jump("hallway")
        hotspot (1350, 300, 1500, 600) action Jump("game_in_kitchen")
#        If(flag_for_game_in_kitchen == 1, hotspot (1350, 300, 1500, 600) action Jump("game_in_kitchen"))

screen plates():
    imagemap:
        idle "ware"
        hover "ware2"

        hotspot (300, 300, 900, 500) action Jump("game")
        hotspot (1, 750, 500, 330) action Jump("kitchen")

label game_in_kitchen:
    scene ware
    "За тарелками лежит что-то. Не могу достать."
    "Эти тарелки... они... они мне очень дороги."
    call screen plates 

# Инициализация переменных
init python:
    import random

    # Список книг и правильный порядок
    books = ["book_a", "book_b", "book_c"]
    target_order = ["book_a", "book_b", "book_c"]  # нужный порядок слева направо


    # Начальные позиции книг (случайные)
    book_positions = {}
    for book in books:
        book_positions[book] = {
            "x": random.randint(200, 1600),  # случайная x в пределах экрана
            "y": random.randint(200, 500),   # случайная y вверху экрана
            "dragging": False,
            "in_zone": False
        }

    # Координаты зон на полке (3 места, выровнены по центру)
    shelf_zones = [
        (600, 750),  # зона 1 (левая)
        (960, 750),  # зона 2 (центральная)
        (1320, 750)  # зона 3 (правая)
    ]

    # Флаг победы
    game_won = False

# Экран игры
screen sort_books:
    # Фон — полка (центрируется)
    add "2.png" xalign 0.5 yalign 0.5


    # Подсветка зон (если хотите видеть места)
    for i, (zx, zy) in enumerate(shelf_zones):
        if not game_won:
            add "back.png" xpos zx ypos zy anchor (0.5, 0.5)


    # Книги — перетаскиваемые объекты
    for book in books:
        $ pos = book_positions[book]
        draggable:
            id book
            xpos pos["x"]
            ypos pos["y"]
            draggable True
            drag_offset (0, 0)
            drag_transform True

            image book + ".png"


            # События перетаскивания
            event "dragstart":
                python:
                    pos["dragging"] = True
            event "dragend":
                python:
                    pos["dragging"] = False
                    # Проверяем, попала ли книга в одну из зон
                    closest_zone = None
                    min_dist = 9999
                    for i, (zx, zy) in enumerate(shelf_zones):
                        dist = ((pos["x"] - zx)**2 + (pos["y"] - zy)**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            closest_zone = i

                    if min_dist < 120:  # радиус «прилипания» к зоне
                        pos["x"] = shelf_zones[closest_zone][0]
                        pos["y"] = shelf_zones[closest_zone][1]
                        pos["in_zone"] = True
                    else:
                        # Возвращаем на случайную позицию вверху
                        pos["x"] = random.randint(200, 1600)
                        pos["y"] = random.randint(200, 500)
                        pos["in_zone"] = False


    # Сообщение о победе (появляется, когда все книги на местах)
    if game_won:
        text "Все книги на месте! Отлично!" size 48 color "#fff" xalign 0.5 ypos 200
        text "(Можно продолжить игру или перейти дальше)" size 28 color "#ccc" xalign 0.5 ypos 260


# Логика проверки порядка
label check_order:
    python:
        # Собираем книги, которые стоят в зонах, по порядку зон
        placed = []
        for zx, zy in shelf_zones:
            for book in books:
                pos = book_positions[book]
                if (abs(pos["x"] - zx) < 10 and abs(pos["y"] - zy) < 10
                        and pos["in_zone"]):
                    placed.append(book)
                    break

        # Если все 3 книги в зонах и в нужном порядке — победа
        if len(placed) == 3 and placed == target_order:
            global game_won
            game_won = True

    # Перерисовываем экран
    show screen sort_books
    return

# Основной ярлык запуска
label game:
    $ game_won = False
    show screen sort_books

    # Цикл проверки порядка, пока не выиграем
    while not game_won:
        pause 0.2
        jump check_order

    # Игра завершена
    pause 2.5
    hide screen sort_books
    jump pic_in_kitchen  # переход к следующей сцене



label pic_in_kitchen:
    scene black #shelf_end
    show pic:
        xalign 0.45
        yalign 0.5
    "Ебать... газета.. нихуя себе"
    hide pic
    $ flag_for_game_in_kitchen = 0
    jump kitchen

screen basement_map():
    imagemap:
        idle "basement"
        hover "basement"

        hotspot (1, 900, 400, 180) action Jump("hallway")

#Bedroom — комната, где просыпается герой

label bedroom:
    call screen bedroom_map

label hallway:
    call screen hallway_map

#Если у игрока есть какие-то данные он сможет подойти к девушке
#Откроется новый скрипт а так он может свободно
#Передвигаться по дому

label basement:
    call screen basement_map

label attic:

label study:

label kitchen:

    call screen kitchen_map

label livingroom:

label bathroom:

label kidsbedroom:

#Акт 1. Пробуждение

label act1:

#    scene kill
#    play sound "scream.mp3"
#    "НЕ НАДО! НЕЕТ!"
#    scene black
#    pause (2)

    scene bedroom

    play music "dark.mp3" #loop=True

    #Сцена 1. Первое пробуждение
    #Заброшенный дом в деревне. Полумрак. Герой лежит на кровати, рядом разбросаны медицинские инструменты. В комнате пахнет лекарствами.

    "Где я? Кто я? Почему вокруг столько незнакомых вещей? Я… я даже не помню своего имени."
    "Что это за место? Дом? Больница? Или…"

    show sorry:
        xalign 0.8
        yalign 1.0

    e "Тише, не торопитесь. Выпейте это, вам станет легче."
    
menu:

    "Хорошо.":
        jump choice1_yes

#    "Нет.":
#        jump choice_death

label choice1_yes:

    $ tabs = 6

    jump choice1_done

label choice1_done:

    # ... the game continues here.
 
    # добавление таблеток
    $ image_name = show_image(tabs)
    show image image_name:
        xalign 1.2
        yalign 1.15

    #Герой (недоверчиво): 

    "Кто вы? Где я нахожусь? И… почему я ничего не помню? Даже самого себя."


#menu:
#
#    "Кто вы такая? Где моя семья? Что с ними?":
#        jump choice2_done
#
#    "Это ты убила их!!":
#        jump choice2_yes

#label choice2_yes:

#    $ tabs -= 1

#    jump choice2_done

#label choice2_done:

    #Незнакомка: 
#    $ image_name = show_image(tabs)
#    show image image_name:
#        xalign 1.2
#        yalign 1.15

    e "Я врач. Я нашла вас в лесу и привезла сюда. Вы были без сознания."
    e "..."
    e "Вы не ранены, но ваш разум… он словно закрыт. Это пройдёт. Постепенно."

    "Сколько я был без сознания? Дни? Недели?"

    e "Недолго. Но вам нужно отдохнуть. Ваши воспоминания вернутся — постепенно."
    e "Сейчас главное — спокойствие."

    "Но я должен знать! Что со мной случилось? Почему я здесь?"

    e "Ваш разум защищает вас. Возможно, он прячет то, что пока не готов показать. Давайте не торопиться."

    "А если я не хочу ждать? Если я боюсь, что никогда не вспомню?"

    e "Страх — это часть пути. Но вы сильнее, чем думаете. Даже если сейчас вам кажется иначе."

    jump bedroom



#Здесь будут концовки:

label choice_death:

    scene doctors

    pause (2)

    "Что... происходит..."

    jump titles

#Конец игры!

label titles:

    scene black

    pause (5)

    return