#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основной модуль видеоредактора
Класс VideoComposer отвечает за создание видео из изображений, аудио и субтитров

Автор: [@EvilBabayka]
Дата: 2025
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import random

# Импорт библиотек для работы с видео (MoviePy 2.2.1)
try:
    from moviepy import (
        VideoFileClip,
        ImageClip,
        TextClip,
        AudioFileClip,
        CompositeVideoClip,
    )
    from moviepy import concatenate_videoclips, concatenate_audioclips
    from PIL import Image
    import pysrt
except ImportError as e:
    print(f"Ошибка импорта библиотек: {e}")
    print("Установите библиотеки: pip install moviepy pillow pysrt")
    raise


class VideoComposer:
    """
    Главный класс для создания видео из изображений, аудио и субтитров
    """

    def __init__(self, config: dict):
        """
        Инициализация видеоредактора

        Args:
            config (dict): Словарь с настройками (из config.py)
        """
        self.config = config
        self.fps = config.get("fps", 24)
        self.resolution = config.get("resolution", (1024, 768))
        self.image_duration = config.get("image_duration", 4.0)
        self.zoom_enabled = config.get("zoom_enabled", True)

        # Настройки для субтитров
        self.subtitle_fontsize = config.get("subtitle_fontsize", 50)
        self.subtitle_color = config.get("subtitle_color", "white")
        self.subtitle_position = config.get("subtitle_position", ("center", "bottom"))

        logging.info(f"VideoComposer инициализирован с разрешением {self.resolution}")

    def create_video(
        self,
        images_folder: str,
        audio_file: str,
        subtitles_file: Optional[str] = None,
        output_file: str = "output/result.mp4",
    ) -> bool:
        """
        Главная функция создания видео

        Args:
            images_folder: путь к папке с изображениями
            audio_file: путь к аудиофайлу
            subtitles_file: путь к файлу субтитров (опционально)
            output_file: путь для сохранения готового видео

        Returns:
            bool: True если видео создано успешно, False если ошибка
        """
        try:
            logging.info("Начало создания видео")

            # 1. Загружаем и обрабатываем изображения
            print("📷 Обработка изображений...")
            image_clips = self._process_images(images_folder)
            if not image_clips:
                logging.error("Не найдено изображений для обработки")
                return False

            # 2. Создаем видеопоследовательность из изображений
            print("🎞️ Создание видеопоследовательности...")
            video_clip = concatenate_videoclips(image_clips, method="compose")

            # 3. Загружаем и добавляем аудио
            print("🎵 Добавление аудиодорожки...")
            video_clip = self._add_audio(video_clip, audio_file)

            # 4. Добавляем субтитры (если есть)
            if subtitles_file and os.path.exists(subtitles_file):
                print("📝 Добавление субтитров...")
                video_clip = self._add_subtitles(video_clip, subtitles_file)

            # 5. Сохраняем итоговое видео
            print("💾 Сохранение видео...")
            self._save_video(video_clip, output_file)

            logging.info(f"Видео успешно создано: {output_file}")
            return True

        except Exception as e:
            logging.error(f"Ошибка при создании видео: {e}", exc_info=True)
            print(f"❌ Ошибка: {e}")
            return False

    def _process_images(self, images_folder: str) -> List:
        """
        Обрабатывает все изображения в папке и создает видеоклипы

        Args:
            images_folder: путь к папке с изображениями

        Returns:
            List: список видеоклипов из изображений
        """
        # Поддерживаемые форматы изображений
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

        # Находим все изображения в папке
        image_files = []
        folder_path = Path(images_folder)

        for ext in image_extensions:
            image_files.extend(folder_path.glob(f"*{ext}"))
            image_files.extend(folder_path.glob(f"*{ext.upper()}"))

        # Сортируем файлы по имени
        image_files.sort()

        if not image_files:
            print(f"❌ Изображения не найдены в папке: {images_folder}")
            return []

        print(f"📷 Найдено изображений: {len(image_files)}")

        clips = []
        for i, image_file in enumerate(image_files):
            print(f"   Обработка {i+1}/{len(image_files)}: {image_file.name}")

            try:
                # Создаем клип из изображения
                clip = self._create_image_clip(str(image_file))
                if clip:
                    clips.append(clip)

            except Exception as e:
                logging.warning(f"Ошибка обработки {image_file}: {e}")
                continue

        return clips

    def _create_image_clip(self, image_path: str):
        """
        Создает видеоклип из одного изображения с возможным эффектом зума

        Args:
            image_path: путь к изображению

        Returns:
            ImageClip: готовый видеоклип
        """
        try:
            # Загружаем изображение и подгоняем под нужный размер
            resized_image = self._resize_image(image_path)

            # Создаем базовый клип с указанием длительности
            clip = ImageClip(resized_image, duration=self.image_duration)

            # Устанавливаем FPS через with_fps (новый API MoviePy 2.2.1)
            clip = clip.with_fps(self.fps)

            # Добавляем эффект зума (если включен)
            if self.zoom_enabled:
                clip = self._add_zoom_effect(clip)

            return clip

        except Exception as e:
            logging.error(f"Ошибка создания клипа из {image_path}: {e}")
            return None

    def _resize_image(self, image_path: str) -> str:
        """
        Изменяет размер изображения под заданное разрешение с сохранением пропорций

        Args:
            image_path: путь к исходному изображению

        Returns:
            str: путь к обработанному изображению
        """
        try:
            # Открываем изображение
            with Image.open(image_path) as img:
                # Конвертируем в RGB если необходимо
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Получаем размеры
                original_width, original_height = img.size
                target_width, target_height = self.resolution

                # Вычисляем пропорции
                width_ratio = target_width / original_width
                height_ratio = target_height / original_height

                # Используем меньший коэффициент, чтобы изображение поместилось целиком
                scale_ratio = min(width_ratio, height_ratio)

                # Новые размеры
                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)

                # Изменяем размер (ИСПРАВЛЕНО: resize вместо resized)
                resized_img = img.resize(
                    (new_width, new_height), resample=Image.Resampling.LANCZOS
                )

                # Создаем фон нужного размера
                background = Image.new("RGB", (target_width, target_height), (0, 0, 0))

                # Размещаем изображение по центру
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - new_height) // 2
                background.paste(resized_img, (paste_x, paste_y))

                # Сохраняем во временную папку
                temp_path = f"temp/resized_{Path(image_path).name}"
                os.makedirs("temp", exist_ok=True)
                background.save(temp_path, quality=95)

                return temp_path

        except Exception as e:
            logging.error(f"Ошибка изменения размера изображения {image_path}: {e}")
            # Возвращаем оригинальный путь в случае ошибки
            return image_path

    def _add_zoom_effect(self, clip):
        """
        Добавляет эффект зума (Ken Burns effect) к видеоклипу

        Args:
            clip: исходный видеоклип

        Returns:
            видеоклип с эффектом зума
        """
        try:
            # Параметры зума
            zoom_factor = 1.2  # насколько увеличиваем (1.2 = на 20%)

            # Случайно выбираем направление зума
            zoom_in = random.choice([True, False])

            if zoom_in:
                # Зум внутрь (от большего к меньшему)
                start_scale = zoom_factor
                end_scale = 1.0
            else:
                # Зум наружу (от меньшего к большему)
                start_scale = 1.0
                end_scale = zoom_factor

            # Функция для плавного изменения масштаба
            def resize_func(t):
                progress = t / clip.duration
                current_scale = start_scale + (end_scale - start_scale) * progress
                return current_scale

            # Применяем плавный зум через resize
            return clip.resized(resize_func)

        except Exception as e:
            logging.warning(f"Ошибка добавления эффекта зума: {e}")
            return clip

    def _add_audio(self, video_clip, audio_file: str):
        """
        Добавляет аудиодорожку к видео

        Args:
            video_clip: видеоклип
            audio_file: путь к аудиофайлу

        Returns:
            видеоклип с аудио
        """
        try:
            # Загружаем аудиофайл
            audio_clip = AudioFileClip(audio_file)

            # Подгоняем длительность
            video_duration = video_clip.duration
            audio_duration = audio_clip.duration

            if audio_duration > video_duration:
                # Аудио длиннее видео - обрезаем аудио
                audio_clip = audio_clip.subclipped(0, video_duration)
                print(f"🎵 Аудио обрезано до {video_duration:.1f} секунд")

            elif audio_duration < video_duration:
                # Видео длиннее аудио - зацикливаем аудио или обрезаем видео
                if audio_duration * 2 >= video_duration:
                    # Если аудио можно зациклить не более 2 раз
                    loops_needed = int(video_duration / audio_duration) + 1
                    audio_clips = [audio_clip] * loops_needed
                    audio_clip = concatenate_audioclips(audio_clips).subclipped(
                        0, video_duration
                    )
                    print(f"🎵 Аудио зациклено для соответствия длительности видео")
                else:
                    # Обрезаем видео под аудио
                    video_clip = video_clip.subclipped(0, audio_duration)
                    print(f"🎞️ Видео обрезано до {audio_duration:.1f} секунд")

            # Добавляем аудио к видео с использованием with_audio (MoviePy 2.2.1)
            final_clip = video_clip.with_audio(audio_clip)

            return final_clip

        except Exception as e:
            logging.error(f"Ошибка добавления аудио: {e}")
            print(f"⚠️ Продолжаем без аудио из-за ошибки: {e}")
            return video_clip

    def _add_subtitles(self, video_clip, subtitles_file: str):
        """
        Добавляет субтитры к видео

        Args:
            video_clip: видеоклип
            subtitles_file: путь к файлу субтитров (.srt)

        Returns:
            видеоклип с субтитрами
        """
        try:
            # Загружаем субтитры
            subtitles = pysrt.open(subtitles_file, encoding="utf-8")

            # Создаем список текстовых клипов
            subtitle_clips = []

            for subtitle in subtitles:
                # Конвертируем время из формата SRT в секунды
                start_time = self._srt_time_to_seconds(subtitle.start)
                end_time = self._srt_time_to_seconds(subtitle.end)
                duration = end_time - start_time

                # Создаем текстовый клип
                try:
                    text_clip = (
                        TextClip(
                            subtitle.text,
                            fontsize=self.subtitle_fontsize,
                            color=self.subtitle_color,
                            font="Arial",  # Используем стандартный шрифт
                            method="caption",
                            size=(self.resolution[0] - 100, None),  # Отступы по бокам
                        )
                        .with_duration(duration)
                        .with_start(start_time)
                        .with_position(self.subtitle_position)
                    )

                    subtitle_clips.append(text_clip)

                except Exception as e:
                    logging.warning(f"Ошибка создания субтитра '{subtitle.text}': {e}")
                    continue

            if subtitle_clips:
                # Накладываем субтитры на видео
                final_clip = CompositeVideoClip([video_clip] + subtitle_clips)
                print(f"📝 Добавлено субтитров: {len(subtitle_clips)}")
                return final_clip
            else:
                print("⚠️ Субтитры не добавлены из-за ошибок")
                return video_clip

        except Exception as e:
            logging.error(f"Ошибка добавления субтитров: {e}")
            print(f"⚠️ Продолжаем без субтитров из-за ошибки: {e}")
            return video_clip

    def _srt_time_to_seconds(self, srt_time) -> float:
        """
        Конвертирует время из формата SRT в секунды

        Args:
            srt_time: время в формате pysrt

        Returns:
            float: время в секундах
        """
        return (
            srt_time.hours * 3600
            + srt_time.minutes * 60
            + srt_time.seconds
            + srt_time.milliseconds / 1000.0
        )

    def _save_video(self, video_clip, output_file: str):
        """
        Сохраняет готовое видео в файл

        Args:
            video_clip: готовый видеоклип
            output_file: путь для сохранения
        """
        try:
            # Создаем папку output если её нет
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Настройки кодирования
            codec = self.config.get("video_codec", "libx264")
            audio_codec = self.config.get("audio_codec", "aac")
            bitrate = self.config.get("video_bitrate", "2000k")

            # Сохраняем видео
            video_clip.write_videofile(
                output_file,
                fps=self.fps,
                codec=codec,
                audio_codec=audio_codec,
                bitrate=bitrate,
                # verbose=False,  # Отключаем подробный вывод FFmpeg
                # logger=None,  # Отключаем логи MoviePy
            )

            print(f"✅ Видео сохранено: {output_file}")

        except Exception as e:
            logging.error(f"Ошибка сохранения видео: {e}")
            raise

        finally:
            # Освобождаем ресурсы
            video_clip.close()


# Вспомогательные функции для тестирования
def test_video_composer():
    """Функция для тестирования VideoComposer"""

    # Базовая конфигурация для тестов
    test_config = {
        "fps": 24,
        "resolution": (1024, 768),
        "image_duration": 4.0,
        "zoom_enabled": True,
        "subtitle_fontsize": 50,
        "subtitle_color": "white",
        "subtitle_position": ("center", "bottom"),
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "2000k",
    }

    # Создаем экземпляр
    composer = VideoComposer(test_config)

    # Тестируем создание видео
    success = composer.create_video(
        images_folder="examples/sample_images/",
        audio_file="examples/sample_audio.mp3",
        subtitles_file="examples/sample_subtitles.srt",
        output_file="output/test_video.mp4",
    )

    if success:
        print("🎉 Тест пройден успешно!")
    else:
        print("❌ Тест провален")

    return success


if __name__ == "__main__":
    # Запуск тестов при прямом вызове файла
    test_video_composer()
