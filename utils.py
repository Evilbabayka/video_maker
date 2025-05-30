import os
import shutil

def setup_folders():
    """Создаёт необходимые папки для работы программы"""
    folders = [
        "input/images",
        "input/audio",
        "input/subtitles",
        "output",
        "temp",
        "logs"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def validate_input_files(file_paths):
    """
    Проверяет существование всех нужных файлов и папок.
    file_paths: dict с ключами images_folder, audio_file, subtitles_file, output_file
    """
    ok = True
    if not os.path.isdir(file_paths["images_folder"]):
        print(f"❌ Папка с изображениями не найдена: {file_paths['images_folder']}")
        ok = False
    if not os.path.isfile(file_paths["audio_file"]):
        print(f"❌ Аудиофайл не найден: {file_paths['audio_file']}")
        ok = False
    if file_paths.get("subtitles_file"):
        if not os.path.isfile(file_paths["subtitles_file"]):
            print(f"⚠️ Файл субтитров не найден: {file_paths['subtitles_file']}")
            # Не критично, продолжаем без субтитров
    return ok

def cleanup_temp_files():
    """Удаляет все временные файлы из папки temp/"""
    temp_folder = "temp"
    if os.path.isdir(temp_folder):
        for filename in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ Не удалось удалить {file_path}: {e}")