#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурационный файл для видеоредактора
Содержит все настройки программы

Автор: [@EvilBabayka]
Дата: 2025
"""

# =============================================================================
# ОСНОВНЫЕ НАСТРОЙКИ ВИДЕО
# =============================================================================

# Разрешение выходного видео (ширина, высота)
# Популярные варианты:
# (1920, 1080) - Full HD
# (1280, 720)  - HD
# (1024, 768)  - XGA (для небольших файлов)
# (854, 480)   - SD (для быстрой обработки)
VIDEO_RESOLUTION = (1024, 768)

# Частота кадров (fps - frames per second)
# 24 - киношный стандарт
# 30 - стандарт для веб-видео
# 60 - для плавного видео (больше размер файла)
VIDEO_FPS = 24

# Длительность показа каждого изображения (в секундах)
# 3.0 - быстрая смена
# 4.0 - стандартная скорость
# 5.0 - медленная смена для детального просмотра
IMAGE_DURATION = 4.0

# =============================================================================
# НАСТРОЙКИ ЭФФЕКТОВ
# =============================================================================

# Включить эффект зума (Ken Burns effect)
ZOOM_ENABLED = True

# Интенсивность зума (1.0 = без зума, 1.3 = сильный зум)
ZOOM_FACTOR = 1.2

# Случайное направление зума для каждого изображения
RANDOM_ZOOM_DIRECTION = True

# Настройки переходов между изображениями
# True - плавные переходы, False - резкая смена
SMOOTH_TRANSITIONS = False

# Длительность перехода (в секундах, если включены плавные переходы)
TRANSITION_DURATION = 0.5

# =============================================================================
# НАСТРОЙКИ СУБТИТРОВ
# =============================================================================

# Размер шрифта субтитров
SUBTITLE_FONTSIZE = 50

# Цвет субтитров
# Можно использовать: 'white', 'black', 'red', 'blue', 'yellow', etc.
# Или RGB: (255, 255, 255) для белого
SUBTITLE_COLOR = 'white'

# Цвет обводки субтитров (для лучшей читаемости)
SUBTITLE_STROKE_COLOR = 'black'
SUBTITLE_STROKE_WIDTH = 2

# Позиция субтитров на экране
# ('center', 'bottom') - по центру внизу
# ('center', 'top') - по центру вверху
# ('left', 'bottom') - слева внизу
# ('right', 'bottom') - справа внизу
SUBTITLE_POSITION = ('center', 'bottom')

# Отступ субтитров от края экрана (в пикселях)
SUBTITLE_MARGIN = 50

# Шрифт для субтитров (должен быть установлен в системе)
# Windows: 'Arial', 'Times-New-Roman', 'Calibri'
# Если шрифт не найден, будет использован системный по умолчанию
SUBTITLE_FONT = 'Arial'

# =============================================================================
# НАСТРОЙКИ АУДИО
# =============================================================================

# Поведение при несовпадении длительности аудио и видео
# 'loop_audio' - зациклить аудио под видео
# 'cut_video' - обрезать видео под аудио
# 'cut_audio' - обрезать аудио под видео
AUDIO_SYNC_MODE = 'loop_audio'

# Максимальное количество циклов аудио (чтобы избежать бесконечного повтора)
MAX_AUDIO_LOOPS = 3

# Громкость аудио (1.0 = оригинальная, 0.5 = тише в 2 раза, 2.0 = громче в 2 раза)
AUDIO_VOLUME = 1.0

# Плавное появление/исчезновение аудио (fade in/out) в секундах
AUDIO_FADEIN = 0.5
AUDIO_FADEOUT = 1.0

# =============================================================================
# НАСТРОЙКИ КОДИРОВАНИЯ И КАЧЕСТВА
# =============================================================================

# Видеокодек для сжатия
# 'libx264' - лучшая совместимость (рекомендуется)
# 'libx265' - лучшее сжатие, но медленнее
VIDEO_CODEC = 'libx264'

# Аудиокодек
# 'aac' - современный стандарт (рекомендуется)
# 'mp3' - универсальная совместимость
AUDIO_CODEC = 'aac'

# Битрейт видео (влияет на качество и размер файла)
# '1000k' - низкое качество, маленький файл
# '2000k' - среднее качество (рекомендуется)
# '4000k' - высокое качество, большой файл
VIDEO_BITRATE = '2000k'

# Битрейт аудио
# '128k' - стандартное качество
# '192k' - высокое качество
# '320k' - максимальное качество
AUDIO_BITRATE = '128k'

# Качество сжатия (0-51, где 0 = без потерь, 23 = по умолчанию, 51 = худшее)
VIDEO_CRF = 23

# =============================================================================
# НАСТРОЙКИ ФАЙЛОВ И ПАПОК
# =============================================================================

# Поддерживаемые форматы изображений
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

# Поддерживаемые форматы аудио
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.aac', '.ogg', '.m4a']

# Поддерживаемые форматы субтитров
SUPPORTED_SUBTITLE_FORMATS = ['.srt', '.vtt']

# Стандартные папки проекта
DEFAULT_INPUT_FOLDER = "input"
DEFAULT_OUTPUT_FOLDER = "output"
DEFAULT_TEMP_FOLDER = "temp"
DEFAULT_EXAMPLES_FOLDER = "examples"

# Максимальный размер файла изображения (в байтах)
# 50 МБ = 50 * 1024 * 1024
MAX_IMAGE_SIZE = 50 * 1024 * 1024

# Максимальная длительность аудио (в секундах)
# 10 минут = 600 секунд
MAX_AUDIO_DURATION = 600

# =============================================================================
# НАСТРОЙКИ ЛОГИРОВАНИЯ
# =============================================================================

# Уровень детализации логов
# 'DEBUG' - все сообщения (для разработки)
# 'INFO' - основные события (рекомендуется)
# 'WARNING' - только предупреждения и ошибки
# 'ERROR' - только ошибки
LOG_LEVEL = 'INFO'

# Имя файла для логов
LOG_FILENAME = 'video_maker.log'

# Максимальный размер файла лога (в байтах)
LOG_MAX_SIZE = 5 * 1024 * 1024  # 5 МБ

# Количество резервных копий лога
LOG_BACKUP_COUNT = 3

# =============================================================================
# ПРЕДУСТАНОВЛЕННЫЕ КОНФИГУРАЦИИ
# =============================================================================

# Быстрая обработка (для тестирования)
FAST_CONFIG = {
    'fps': 24,
    'resolution': (854, 480),
    'image_duration': 3.0,
    'zoom_enabled': False,
    'video_bitrate': '1000k',
    'video_crf': 28
}

# Высокое качество (для финальных версий)
HIGH_QUALITY_CONFIG = {
    'fps': 30,
    'resolution': (1920, 1080),
    'image_duration': 5.0,
    'zoom_enabled': True,
    'video_bitrate': '4000k',
    'video_crf': 18,
    'audio_bitrate': '192k'
}

# Для социальных сетей (квадратный формат)
SOCIAL_MEDIA_CONFIG = {
    'fps': 30,
    'resolution': (1080, 1080),
    'image_duration': 3.0,
    'zoom_enabled': True,
    'video_bitrate': '2000k',
    'subtitle_fontsize': 60,
    'subtitle_position': ('center', 'center')
}

# =============================================================================
# ОСНОВНАЯ КОНФИГУРАЦИЯ
# =============================================================================

# Главный словарь конфигурации, который используется в программе
VIDEO_CONFIG = {
    # Основные параметры видео
    'fps': VIDEO_FPS,
    'resolution': VIDEO_RESOLUTION,
    'image_duration': IMAGE_DURATION,
    
    # Эффекты
    'zoom_enabled': ZOOM_ENABLED,
    'zoom_factor': ZOOM_FACTOR,
    'random_zoom_direction': RANDOM_ZOOM_DIRECTION,
    'smooth_transitions': SMOOTH_TRANSITIONS,
    'transition_duration': TRANSITION_DURATION,
    
    # Субтитры
    'subtitle_fontsize': SUBTITLE_FONTSIZE,
    'subtitle_color': SUBTITLE_COLOR,
    'subtitle_stroke_color': SUBTITLE_STROKE_COLOR,
    'subtitle_stroke_width': SUBTITLE_STROKE_WIDTH,
    'subtitle_position': SUBTITLE_POSITION,
    'subtitle_margin': SUBTITLE_MARGIN,
    'subtitle_font': SUBTITLE_FONT,
    
    # Аудио
    'audio_sync_mode': AUDIO_SYNC_MODE,
    'max_audio_loops': MAX_AUDIO_LOOPS,
    'audio_volume': AUDIO_VOLUME,
    'audio_fadein': AUDIO_FADEIN,
    'audio_fadeout': AUDIO_FADEOUT,
    
    # Кодирование
    'video_codec': VIDEO_CODEC,
    'audio_codec': AUDIO_CODEC,
    'video_bitrate': VIDEO_BITRATE,
    'audio_bitrate': AUDIO_BITRATE,
    'video_crf': VIDEO_CRF,
    
    # Файлы и форматы
    'supported_image_formats': SUPPORTED_IMAGE_FORMATS,
    'supported_audio_formats': SUPPORTED_AUDIO_FORMATS,
    'supported_subtitle_formats': SUPPORTED_SUBTITLE_FORMATS,
    'max_image_size': MAX_IMAGE_SIZE,
    'max_audio_duration': MAX_AUDIO_DURATION,
    
    # Папки
    'default_input_folder': DEFAULT_INPUT_FOLDER,
    'default_output_folder': DEFAULT_OUTPUT_FOLDER,
    'default_temp_folder': DEFAULT_TEMP_FOLDER,
    
    # Логирование
    'log_level': LOG_LEVEL,
    'log_filename': LOG_FILENAME,
    'log_max_size': LOG_MAX_SIZE,
    'log_backup_count': LOG_BACKUP_COUNT
}

# =============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С КОНФИГУРАЦИЕЙ
# =============================================================================

def get_config(config_name='default'):
    """
    Возвращает конфигурацию по имени
    
    Args:
        config_name (str): Имя конфигурации ('default', 'fast', 'high_quality', 'social_media')
        
    Returns:
        dict: Словарь с настройками
    """
    if config_name == 'fast':
        config = VIDEO_CONFIG.copy()
        config.update(FAST_CONFIG)
        return config
    elif config_name == 'high_quality':
        config = VIDEO_CONFIG.copy()
        config.update(HIGH_QUALITY_CONFIG)
        return config
    elif config_name == 'social_media':
        config = VIDEO_CONFIG.copy()
        config.update(SOCIAL_MEDIA_CONFIG)
        return config
    else:
        return VIDEO_CONFIG


def print_config(config_name='default'):
    """
    Выводит текущую конфигурацию в читаемом виде
    
    Args:
        config_name (str): Имя конфигурации для вывода
    """
    config = get_config(config_name)
    
    print(f"\n📋 КОНФИГУРАЦИЯ: {config_name.upper()}")
    print("=" * 50)
    
    print(f"🎬 Видео:")
    print(f"   Разрешение: {config['resolution'][0]}x{config['resolution'][1]}")
    print(f"   FPS: {config['fps']}")
    print(f"   Длительность кадра: {config['image_duration']} сек")
    print(f"   Битрейт: {config['video_bitrate']}")
    
    print(f"\n🎭 Эффекты:")
    print(f"   Зум: {'включен' if config['zoom_enabled'] else 'выключен'}")
    if config['zoom_enabled']:
        print(f"   Интенсивность зума: {config['zoom_factor']}")
    
    print(f"\n📝 Субтитры:")
    print(f"   Размер шрифта: {config['subtitle_fontsize']}")
    print(f"   Цвет: {config['subtitle_color']}")
    print(f"   Позиция: {config['subtitle_position']}")
    
    print(f"\n🎵 Аудио:")
    print(f"   Режим синхронизации: {config['audio_sync_mode']}")
    print(f"   Громкость: {config['audio_volume']}")
    print(f"   Битрейт: {config['audio_bitrate']}")
    
    print("=" * 50)


def validate_config(config):
    """
    Проверяет корректность конфигурации
    
    Args:
        config (dict): Словарь с настройками
        
    Returns:
        tuple: (is_valid, errors) - валидность и список ошибок
    """
    errors = []
    
    # Проверка разрешения
    if not isinstance(config.get('resolution'), tuple) or len(config['resolution']) != 2:
        errors.append("Разрешение должно быть кортежем из двух чисел")
    
    # Проверка FPS
    fps = config.get('fps', 0)
    if not isinstance(fps, (int, float)) or fps <= 0 or fps > 120:
        errors.append("FPS должен быть числом от 1 до 120")
    
    # Проверка длительности кадра
    duration = config.get('image_duration', 0)
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("Длительность кадра должна быть положительным числом")
    
    # Проверка размера шрифта
    fontsize = config.get('subtitle_fontsize', 0)
    if not isinstance(fontsize, (int, float)) or fontsize <= 0:
        errors.append("Размер шрифта должен быть положительным числом")
    
    return len(errors) == 0, errors


# =============================================================================
# ТЕСТИРОВАНИЕ КОНФИГУРАЦИИ
# =============================================================================

if __name__ == "__main__":
    print("🔧 ТЕСТИРОВАНИЕ КОНФИГУРАЦИИ")
    print("=" * 60)
    
    # Выводим все доступные конфигурации
    configs = ['default', 'fast', 'high_quality', 'social_media']
    
    for config_name in configs:
        print_config(config_name)
        
        # Валидация конфигурации
        config = get_config(config_name)
        is_valid, errors = validate_config(config)
        
        if is_valid:
            print(f"✅ Конфигурация '{config_name}' корректна\n")
        else:
            print(f"❌ Ошибки в конфигурации '{config_name}':")
            for error in errors:
                print(f"   - {error}")
            print()
    
    print("🎯 Тестирование завершено!")