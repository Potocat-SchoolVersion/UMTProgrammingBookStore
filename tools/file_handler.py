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

def save_file(filename, file_type):
    absolute_path = getAbsolutePath(filename, file_type)
    print(absolute_path)
    with open(absolute_path, 'w') as file:
        pass

def read_file(filename, file_type):
    absolute_path = getAbsolutePath(filename, file_type)
    print(absolute_path)
    with open(absolute_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)[0].split("\t") # see if want use or no
        data = []
        for row in reader:
            data.append(row[0].split("\t"))
        return header, data

def export_data():
    pass
