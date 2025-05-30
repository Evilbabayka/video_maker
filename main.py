#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой видеоредактор
Главный файл для запуска программы

Автор: [@EvilBabayka]
Дата: 2025
"""

import os
import sys
from pathlib import Path
import logging

# Импортируем наши модули (пока они не созданы, но будут)
try:
    from video_composer import VideoComposer
    from config import VIDEO_CONFIG
    from utils import setup_folders, validate_input_files, cleanup_temp_files
except ImportError as e:
    print(f"Ошибка импорта модулей: {e}")
    print("Убедитесь, что все файлы проекта находятся в одной папке")
    sys.exit(1)


def setup_logging():
    """Настройка системы логирования для отслеживания работы программы"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/video_maker.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def print_welcome():
    """Выводит приветственное сообщение"""
    print("=" * 60)
    print("🎬 ПРОСТОЙ ВИДЕОРЕДАКТОР 🎬")
    print("=" * 60)
    print("Программа создает видео из изображений с аудио и субтитрами")
    print()


def get_user_input():
    """
    Получает от пользователя пути к файлам
    Возвращает словарь с путями к файлам
    """
    print("📁 Укажите файлы для создания видео:")
    print()

    # Папка с изображениями
    while True:
        images_folder = input(
            "Папка с изображениями (или Enter для input/images/): "
        ).strip()
        if not images_folder:
            images_folder = "input/images/"

        if os.path.exists(images_folder):
            break
        else:
            print(f"❌ Папка '{images_folder}' не найдена. Попробуйте еще раз.")

    # Аудиофайл
    while True:
        audio_file = input("Аудиофайл (или Enter для поиска в input/audio/): ").strip()
        if not audio_file:
            # Ищем первый аудиофайл в папке input/audio/
            audio_folder = Path("input/audio/")
            if audio_folder.exists():
                audio_files = list(audio_folder.glob("*.mp3")) + list(
                    audio_folder.glob("*.wav")
                )
                if audio_files:
                    audio_file = str(audio_files[0])
                    print(f"📻 Найден аудиофайл: {audio_file}")
                    break
                else:
                    print("❌ Аудиофайлы не найдены в input/audio/")
                    continue
            else:
                print("❌ Папка input/audio/ не найдена")
                continue

        if os.path.exists(audio_file):
            break
        else:
            print(f"❌ Файл '{audio_file}' не найден. Попробуйте еще раз.")

    # Файл субтитров (необязательный)
    subtitles_file = input("Файл субтитров (Enter для пропуска): ").strip()
    if subtitles_file and not os.path.exists(subtitles_file):
        print(
            f"⚠️ Файл субтитров '{subtitles_file}' не найден. Продолжаем без субтитров."
        )
        subtitles_file = None

    # Имя выходного файла
    output_file = input("Имя выходного файла (Enter для 'output/result.mp4'): ").strip()
    if not output_file:
        output_file = "output/result.mp4"

    return {
        "images_folder": images_folder,
        "audio_file": audio_file,
        "subtitles_file": subtitles_file,
        "output_file": output_file,
    }


def main():
    """Главная функция программы"""

    # Настройка логирования
    setup_logging()
    logging.info("Запуск программы видеоредактора")

    # Приветствие
    print_welcome()

    try:
        # Создание необходимых папок
        print("📂 Подготовка рабочих папок...")
        setup_folders()

        # Получение данных от пользователя
        file_paths = get_user_input()

        # Валидация входных файлов
        print("\n🔍 Проверка файлов...")
        if not validate_input_files(file_paths):
            print("❌ Ошибка в файлах. Программа завершена.")
            return

        print("✅ Все файлы найдены и готовы к обработке")

        # Создание объекта видеоредактора
        print("\n🎬 Инициализация видеоредактора...")
        composer = VideoComposer(VIDEO_CONFIG)

        # Создание видео
        print("\n🔄 Создание видео... Это может занять несколько минут.")
        print("⏳ Пожалуйста, подождите...")

        success = composer.create_video(
            images_folder=file_paths["images_folder"],
            audio_file=file_paths["audio_file"],
            subtitles_file=file_paths["subtitles_file"],
            output_file=file_paths["output_file"],
        )

        if success:
            print(f"\n🎉 ГОТОВО! Видео сохранено: {file_paths['output_file']}")
            print(
                f"📁 Размер файла: {os.path.getsize(file_paths['output_file']) / (1024*1024):.1f} МБ"
            )
            logging.info(f"Видео успешно создано: {file_paths['output_file']}")
        else:
            print("\n❌ Произошла ошибка при создании видео")
            logging.error("Ошибка при создании видео")

    except KeyboardInterrupt:
        print("\n\n⚠️ Программа прервана пользователем")
        logging.info("Программа прервана пользователем")

    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")
        logging.error(f"Непредвиденная ошибка: {e}", exc_info=True)

    finally:
        # Очистка временных файлов
        print("\n🧹 Очистка временных файлов...")
        cleanup_temp_files()
        print("✅ Программа завершена")


def show_help():
    """Показывает справку по использованию программы"""
    help_text = """
    🆘 СПРАВКА ПО ИСПОЛЬЗОВАНИЮ
    
    Подготовка файлов:
    1. Поместите изображения в папку input/images/ (форматы: jpg, png)
    2. Поместите аудиофайл в папку input/audio/ (форматы: mp3, wav)
    3. (Опционально) Поместите субтитры в папку input/subtitles/ (формат: srt)
    
    Запуск программы:
    python main.py        - обычный запуск с интерактивным меню
    python main.py --help - показать эту справку
    
    Результат:
    Готовое видео будет сохранено в папку output/
    
    Требования к файлам:
    - Изображения: любой размер, будут автоматически подогнаны
    - Аудио: любой формат, поддерживаемый FFmpeg
    - Субтитры: формат SRT с UTF-8 кодировкой
    """
    print(help_text)


if __name__ == "__main__":
    # Проверка аргументов командной строки
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
    else:
        main()
