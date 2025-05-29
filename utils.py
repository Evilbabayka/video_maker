import os
import json
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoInfo:
    """Класс для хранения информации о видео"""
    def __init__(self, width: int, height: int, fps: float, duration: float, 
                 codec: str = "", bitrate: int = 0):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.codec = codec
        self.bitrate = bitrate
    
    def __str__(self):
        return f"VideoInfo(size={self.width}x{self.height}, fps={self.fps}, duration={self.duration:.2f}s)"

def format_time(seconds: float) -> str:
    """
    Форматирует время в секундах в формат HH:MM:SS.mmm
    
    Args:
        seconds: Время в секундах
        
    Returns:
        Отформатированная строка времени
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    else:
        return f"{minutes:02d}:{secs:06.3f}"

def parse_time(time_str: str) -> float:
    """
    Парсит строку времени в секунды
    Поддерживает форматы: MM:SS, HH:MM:SS, SS.mmm
    
    Args:
        time_str: Строка времени
        
    Returns:
        Время в секундах
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 1:
            # Формат: SS.mmm
            return float(parts[0])
        elif len(parts) == 2:
            # Формат: MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            # Формат: HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        else:
            raise ValueError("Неверный формат времени")
    except (ValueError, IndexError) as e:
        logger.error(f"Ошибка парсинга времени '{time_str}': {e}")
        return 0.0

def get_video_info(file_path: str) -> Optional[VideoInfo]:
    """
    Получает информацию о видеофайле с помощью ffprobe
    
    Args:
        file_path: Путь к видеофайлу
        
    Returns:
        Объект VideoInfo или None при ошибке
    """
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return None
    
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Ищем видеопоток
        video_stream = None
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            logger.error("Видеопоток не найден")
            return None
        
        width = int(video_stream.get('width', 0))
        height = int(video_stream.get('height', 0))
        
        # Получаем FPS
        fps_str = video_stream.get('r_frame_rate', '0/1')
        if '/' in fps_str:
            num, den = map(int, fps_str.split('/'))
            fps = num / den if den != 0 else 0
        else:
            fps = float(fps_str)
        
        # Получаем длительность
        duration = float(video_stream.get('duration', 0))
        if duration == 0:
            duration = float(data.get('format', {}).get('duration', 0))
        
        codec = video_stream.get('codec_name', '')
        bitrate = int(video_stream.get('bit_rate', 0))
        
        return VideoInfo(width, height, fps, duration, codec, bitrate)
        
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as e:
        logger.error(f"Ошибка получения информации о видео: {e}")
        return None

def validate_video_file(file_path: str) -> bool:
    """
    Проверяет, является ли файл валидным видеофайлом
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        True если файл валиден, False иначе
    """
    if not os.path.exists(file_path):
        return False
    
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext not in video_extensions:
        return False
    
    # Дополнительная проверка с помощью ffprobe
    info = get_video_info(file_path)
    return info is not None

def generate_output_filename(input_path: str, suffix: str = "_edited", 
                           extension: str = None) -> str:
    """
    Генерирует имя выходного файла на основе входного
    
    Args:
        input_path: Путь к входному файлу
        suffix: Суффикс для добавления к имени
        extension: Новое расширение (если нужно изменить)
        
    Returns:
        Путь к выходному файлу
    """
    path = Path(input_path)
    stem = path.stem
    ext = extension if extension else path.suffix
    
    if not ext.startswith('.'):
        ext = '.' + ext
    
    output_name = f"{stem}{suffix}{ext}"
    return str(path.parent / output_name)

def ensure_directory(file_path: str) -> bool:
    """
    Создает директорию для файла, если она не существует
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        True если директория создана или существует, False при ошибке
    """
    try:
        directory = Path(file_path).parent
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as e:
        logger.error(f"Ошибка создания директории: {e}")
        return False

def get_file_size(file_path: str) -> int:
    """
    Получает размер файла в байтах
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        Размер файла в байтах, 0 при ошибке
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def format_file_size(size_bytes: int) -> str:
    """
    Форматирует размер файла в человекочитаемый вид
    
    Args:
        size_bytes: Размер в байтах
        
    Returns:
        Отформатированная строка размера
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def calculate_bitrate(file_size: int, duration: float) -> int:
    """
    Рассчитывает битрейт файла
    
    Args:
        file_size: Размер файла в байтах
        duration: Длительность в секундах
        
    Returns:
        Битрейт в бит/сек
    """
    if duration <= 0:
        return 0
    return int((file_size * 8) / duration)

def clean_temp_files(temp_dir: str = "temp") -> None:
    """
    Очищает временные файлы
    
    Args:
        temp_dir: Директория с временными файлами
    """
    try:
        temp_path = Path(temp_dir)
        if temp_path.exists():
            for file in temp_path.glob("*"):
                if file.is_file():
                    file.unlink()
                    logger.info(f"Удален временный файл: {file}")
    except OSError as e:
        logger.error(f"Ошибка очистки временных файлов: {e}")

def progress_callback(current: int, total: int, operation: str = "Обработка") -> None:
    """
    Функция обратного вызова для отображения прогресса
    
    Args:
        current: Текущий прогресс
        total: Общий объем работы
        operation: Название операции
    """
    if total > 0:
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\r{operation}: |{bar}| {percentage:.1f}% ({current}/{total})', end='')
        if current == total:
            print()

def check_ffmpeg_installation() -> bool:
    """
    Проверяет, установлен ли FFmpeg
    
    Returns:
        True если FFmpeg доступен, False иначе
    """
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_supported_formats() -> Dict[str, List[str]]:
    """
    Возвращает поддерживаемые форматы файлов
    
    Returns:
        Словарь с типами файлов и их расширениями
    """
    return {
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a'],
        'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    }

def create_backup(file_path: str) -> Optional[str]:
    """
    Создает резервную копию файла
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        Путь к резервной копии или None при ошибке
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        timestamp = int(time.time())
        path = Path(file_path)
        backup_name = f"{path.stem}_backup_{timestamp}{path.suffix}"
        backup_path = path.parent / backup_name
        
        import shutil
        shutil.copy2(file_path, backup_path)
        logger.info(f"Создана резервная копия: {backup_path}")
        return str(backup_path)
        
    except OSError as e:
        logger.error(f"Ошибка создания резервной копии: {e}")
        return None

def validate_time_range(start_time: float, end_time: float, 
                       duration: float) -> Tuple[bool, str]:
    """
    Проверяет корректность временного диапазона
    
    Args:
        start_time: Время начала
        end_time: Время окончания
        duration: Общая длительность видео
        
    Returns:
        Кортеж (валиден ли диапазон, сообщение об ошибке)
    """
    if start_time < 0:
        return False, "Время начала не может быть отрицательным"
    
    if end_time <= start_time:
        return False, "Время окончания должно быть больше времени начала"
    
    if start_time >= duration:
        return False, "Время начала превышает длительность видео"
    
    if end_time > duration:
        return False, "Время окончания превышает длительность видео"
    
    return True, ""

# Константы для качества видео
VIDEO_QUALITY_PRESETS = {
    'low': {'crf': 28, 'preset': 'fast'},
    'medium': {'crf': 23, 'preset': 'medium'},
    'high': {'crf': 18, 'preset': 'slow'},
    'ultra': {'crf': 15, 'preset': 'veryslow'}
}

# Константы для разрешений
RESOLUTION_PRESETS = {
    '480p': (854, 480),
    '720p': (1280, 720),
    '1080p': (1920, 1080),
    '1440p': (2560, 1440),
    '4K': (3840, 2160)
}