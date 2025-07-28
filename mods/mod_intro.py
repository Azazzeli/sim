# mods/mod_intro.py
import pygame
import os

# Пути к ресурсам
INTRO_BG_PATH = "assets/intro_background.jpg"
INTRO_MUSIC_PATH = "assets/intro_music.mp3"
SFX_TYPE_PATH = "assets/type_sound.wav"


def init(game):
    """Инициализация заставки с эффектом печати и звуком"""
    game.state = "intro"
    game.intro_texts = [
        "Темнота...",
        "Вы чувствуете боль в голове.",
        "Где вы? Что произошло?",
        "Вы медленно открываете глаза.",
        "Разрушенный город. Тишина. Ни души.",
        "Рядом — потрёпанная сумка. Внутри: немного еды, вода, бинт.",
        "На бирке сумки — имя, но оно не ваше.",
        "Вы не помните, кто вы.",
        "Не помните, откуда пришли.",
        "Но помните одно: вы должны выжить.",
        "Зомби повсюду. Радиосигналы молчат.",
        "Ваше сердце бьётся. Вы живы.",
        "Пока."
    ]

    # Состояние
    game.intro_lines = []          # уже напечатанные строки
    game.current_line = ""         # текущий текст
    game.target_line = game.intro_texts[0]  # первая строка
    game.type_speed = 40           # мс на символ
    game.last_type = 0             # таймер для печати
    game.intro_index = 0           # индекс текущего слайда

    # Загрузка фона
    if os.path.exists(INTRO_BG_PATH):
        bg = pygame.image.load(INTRO_BG_PATH)
        game.intro_background = pygame.transform.scale(bg, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    else:
        game.intro_background = None

    # Инициализация звука
    try:
        pygame.mixer.init()
        if os.path.exists(INTRO_MUSIC_PATH):
            pygame.mixer.music.load(INTRO_MUSIC_PATH)
            pygame.mixer.music.play(-1, fade_ms=500)  # бесконечно, с плавным включением
        if os.path.exists(SFX_TYPE_PATH):
            game.type_sound = pygame.mixer.Sound(SFX_TYPE_PATH)
        else:
            game.type_sound = None
    except Exception as e:
        print(f"⚠️ Ошибка звука: {e}")
        game.type_sound = None

    # Сохраняем оригинальные методы
    original_handle = game.handle_events
    original_draw = game.draw

    def enhanced_handle():
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                return

            # Пропуск слайда: Пробел или клик
            if game.state == "intro":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    next_slide(game)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    next_slide(game)
            else:
                original_handle()

        # Автопечать символа
        if game.state == "intro" and game.target_line and len(game.current_line) < len(game.target_line):
            if current_time - game.last_type > game.type_speed:
                game.current_line += game.target_line[len(game.current_line)]
                game.last_type = current_time
                if game.type_sound:
                    game.type_sound.play()

    def enhanced_draw():
        if game.state == "intro":
            draw_intro(game)
        else:
            original_draw()

    game.handle_events = enhanced_handle
    game.draw = enhanced_draw


def next_slide(game):
    """Переход к следующему слайду"""
    if game.target_line and len(game.current_line) < len(game.target_line):
        # Если текст не допечатан — допечатать мгновенно
        game.current_line = game.target_line
    else:
        # Сохраняем текущую строку
        if game.current_line:
            game.intro_lines.append(game.current_line)

        # Следующий слайд
        game.intro_index += 1
        if game.intro_index >= len(game.intro_texts):
            # Все слайды показаны
            game.state = "start"
            pygame.mixer.music.stop()  # ✅ Музыка останавливается!
            game.intro_lines = []      # очищаем
            game.current_line = ""
            game.target_line = ""
        else:
            game.target_line = game.intro_texts[game.intro_index]
            game.current_line = ""


def draw_intro(game):
    """Отрисовка заставки с прокруткой текста"""
    if game.intro_background:
        game.screen.blit(game.intro_background, (0, 0))
    else:
        game.screen.fill((5, 10, 15))

    y_offset = 80

    # Рисуем старые строки
    for line in game.intro_lines:
        text_surf = game.font_medium.render(line, True, (200, 200, 200))
        game.screen.blit(text_surf, (game.SCREEN_WIDTH // 2 - text_surf.get_width() // 2, y_offset))
        y_offset += 40

    # Рисуем текущую строку
    if game.target_line:
        text_surf = game.font_medium.render(game.current_line, True, (220, 220, 220))
        game.screen.blit(text_surf, (game.SCREEN_WIDTH // 2 - text_surf.get_width() // 2, y_offset))

    # Подсказка
    if game.target_line and len(game.current_line) == len(game.target_line):
        hint = game.font_small.render("Нажмите ПРОБЕЛ или кликните, чтобы продолжить", True, (220, 180, 60))
        game.screen.blit(hint, (game.SCREEN_WIDTH // 2 - hint.get_width() // 2, game.SCREEN_HEIGHT - 50))

    pygame.display.flip()