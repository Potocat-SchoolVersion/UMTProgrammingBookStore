# tools/file_handler.py
import csv
import os

# data folder path
def getDataFolderPath():
    cd = os.getcwd()
    print(cd)
    splitted_path = cd.split("\\")#[:-1] #debug console comment it, ui keep
    splitted_path.append("data")
    return "\\".join(splitted_path)

# retrieve specified absolute path
def getAbsolutePath(filename, file_type):
    data_file_path = getDataFolderPath()
    file_name = rf"{filename}.{file_type}"
    return rf"{data_file_path}\{file_name}"

def save_file(filename, file_type, fieldnames, datas):
    absolute_path = getAbsolutePath(filename, file_type)
    with open(absolute_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in datas:
            writer.writerow(data.to_dict())

def read_file(filename, file_type):
    absolute_path = getAbsolutePath(filename, file_type)
    with open(absolute_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        return list(reader)

def export_data():
    pass

def append_save_file(filename, file_type, fieldnames, datas):
    """
    Append rows to an existing CSV file.
    If file does not exist, it will be created and header written.
    """
    absolute_path = getAbsolutePath(filename, file_type)
    file_exists = os.path.exists(absolute_path)

    with open(absolute_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        for data in datas:
            writer.writerow(data.to_dict())

def get_encryption_key():
    pass

def encrypt(file):
    pass

def decrypt(file):
    pass
