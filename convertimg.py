from multiprocessing import Pool
import os
import subprocess
import sys


def get_files(source, exts):
    result = []
    for name in os.listdir(source):
        for ext in exts:
            if name.endswith("." + ext):
                result.append(os.path.join(source, name))
                break
    return result


def get_files_with_settings():
    exts = ["jpg"]
    if len(sys.argv) != 4:
        print("Необходимо ввести 2 параметра через пробел: каталог-источник, каталог-приемник и ширину")
        exit(1)
    source = sys.argv[1]
    destination = sys.argv[2]
    size = sys.argv[3]
    if not os.path.exists(source):
        print("Каталога-источника не существует")
        exit(2)
    files = get_files(source, exts)
    if len(files) == 0:
        print("Не найдено файлов с расширениями", exts)
        exit(3)
    if not os.path.exists(destination):
        os.mkdir(destination)
    result = []
    for file in files:
        result.append({"file": file, "dest": destination, "size": size})
    return result


def convert(settings):
    file = settings["file"]
    dest = settings["dest"]
    size = settings["size"]
    print("Начата обработка файла:", file)
    cmd_line = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "convert.exe") + " " + file + " -resize " + size
    cmd_line += " " + os.path.join(dest, os.path.basename(file))
    subprocess.run(cmd_line)
    print("Обработка файла:", file, "- закончена")


if __name__ == '__main__':
    settings = get_files_with_settings()
    thread_number = 4
    with Pool(thread_number) as p:
        p.map(convert, settings)
    print("Конвертация завершена")
