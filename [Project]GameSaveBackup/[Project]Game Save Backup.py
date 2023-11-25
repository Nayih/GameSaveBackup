#Imports
from datetime import datetime, date, timedelta
import configparser
import shutil
import os
import time

#Validate Folder Name
def validateFolder(content):
    try:
        if content != "NayohSaveLog":
            if os.path.exists(content):
                shutil.rmtree(content)

            os.makedirs(content)
            shutil.rmtree(content)
        return True
    except:
        return False

#Validate Bool
def validateBool(content):
    if content.lower() == "n":
        content = False
    elif content.lower() == "y":
        content = True
    else:
        content = 5

    return content

#Validate Number
def validateNumber(content, stats):
    try:
        content = int(content)

        if content > 0 and stats == False:
            content = True
        elif content >= 0 and stats == True:
            content = True
        else:
            content = False
    except:
        content = False
    
    return content

#cls
def n_cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Get Current Time
def now():
    now = datetime.now()
    currentTime = now.strftime("%H-%M-%S")
    return currentTime

#Setup Settings
def setupSettings():
    if os.path.isfile("Settings.ini"):
        try:
            os.remove("Settings.ini")
        except:
            print("[INFO]Failed To Remove Settings.ini, Closing Program...")
            input("Press (Enter) To Continue...")
            exit()

    i = False
    while not i:
        game_title = input("Game Title: ")
        i = validateFolder(game_title)

    i = False
    while not i:
        game_save_location = input("Game Save Location: ")
        i = os.path.isdir(game_save_location)

    i = False
    while not i:
        backup_save_time_minutes = input("The Save Backup Will Be Performed Every X Minutes: ")
        i = validateNumber(backup_save_time_minutes, False)

    backup_save_time_minutes = int(backup_save_time_minutes)

    i = 5
    while i == 5:
        delete_old = input("Delete All Files From Previous Days. (y/n): ")
        i = validateBool(delete_old)

    delete_old = i

    i = False
    while not i:
        max_files_by_folder = input("Maximum Files By Folder At Once Before Starting To Delete Old Files. (Use 0 To Not Delete Files): ")
        i = validateNumber(max_files_by_folder, True)

    max_files_by_folder = int(max_files_by_folder)

    try:
        settings = open("Settings.ini", "w")
        settings.write("[game_informations]\n")
        settings.write("game_title = " + game_title + "\n")
        settings.write("game_save_location = " + game_save_location + "\n")
        settings.write("backup_save_time_minutes = " + str(backup_save_time_minutes) + "\n")
        settings.write("delete_old = " + str(delete_old) + "\n")
        settings.write("max_files_by_folder = " + str(max_files_by_folder))
        settings.close()
    except:
        print("[INFO]Failed To Generate Settings.ini, Closing Program...")
        input("Press (Enter) To Continue...")
        exit()

    game_save_location = game_save_location.replace("\\", "\\\\")
    backup_save_time_minutes = backup_save_time_minutes * 60
    input("Press (Enter) To Start...")
    n_cls

    return game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder


#Check Settings File
def checkSettings():
    if os.path.isfile("Settings.ini"):
        try:
            settings = configparser.ConfigParser()
            with open("Settings.ini","r") as file_object:
                settings.read_file(file_object)
                game_title = settings.get("game_informations", "game_title")
                game_save_location = settings.get("game_informations", "game_save_location")
                backup_save_time_minutes = settings.getint("game_informations", "backup_save_time_minutes")
                delete_old = settings.get("game_informations", "delete_old")
                max_files_by_folder = settings.getint("game_informations", "max_files_by_folder")

            validateTitle = validateFolder(game_title)
            validateSave = os.path.isdir(game_save_location)
            game_save_location = game_save_location.replace("\\", "\\\\")
            validateTime = validateNumber(backup_save_time_minutes, False)
            backup_save_time_minutes = backup_save_time_minutes * 60

            if delete_old == "True":
                validateDelete = True
                delete_old = True
            elif delete_old == "False":
                validateDelete = True
                delete_old = False
            else:
                validateDelete = False

            validateLimit = validateNumber(max_files_by_folder, True)

            if validateTitle and validateSave and validateTime and validateDelete and validateLimit:
                return game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder
            else:
                print("[INFO]Unknown Parameters In Settings.ini, Let's Reconfigure It.")
                input("Press (Enter) To Continue...")
                n_cls()
                game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder = setupSettings()
                return game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder
        except:
            print("[INFO]Unknown Parameters In Settings.ini, Let's Reconfigure It.")
            input("Press (Enter) To Continue...")
            n_cls()
            game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder = setupSettings()
            return game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder
    else:
        print("[INFO]It Looks Like You Don't Have A Settings.ini File, Let's Configure It.")
        game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder = setupSettings()
        return game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder

#Generate Backups Folder
def createDirectory(game_title, date_today):
    if not os.path.exists("NayohSaveLog"):
        os.makedirs("NayohSaveLog")

    if not os.path.exists("NayohSaveLog/" + game_title):
        os.makedirs("NayohSaveLog/" + game_title)

    if not os.path.exists("NayohSaveLog/" + game_title + "/" + date_today):
        os.makedirs("NayohSaveLog/" + game_title + "/" + date_today)

#Manage Old Files
def manageOldFiles(game_title, date_yesterday, date_today, stats):
    if stats:
        directory_list = os.listdir("NayohSaveLog/" + game_title)

        for folder in directory_list:
            if folder != date_today and folder != date_yesterday:
                try:
                    shutil.rmtree("NayohSaveLog/" + game_title + "/" + folder)
                except:
                    print("[INFO]Error Trying To Remove Files Older Than Today's And Yesterday's Date.")

#Manage Old File Versions
def manageOldFileVersions(game_title, date_today, max_files_by_folder):
    if max_files_by_folder != 0:
        directory_list = os.listdir("NayohSaveLog/" + game_title + "/" + date_today)
        dir_len = len(directory_list)

        if dir_len > max_files_by_folder:
            try:
                shutil.rmtree("NayohSaveLog/" + game_title + "/" + date_today + "/" + directory_list[0])
            except:
                print("[INFO]Error Trying To Remove Old Files From Today's Date.")

#Backup Files
def backupSave(game_title, date_today, game_save_location, max_files_by_folder):
    currentTime = now()
    reformatedCurrentTime = currentTime.replace("-", ":")

    if os.path.isdir(game_save_location):
        dir_files = checkDirectoryFiles(game_save_location)
        if dir_files > 0:
            files = os.listdir(game_save_location)
            shutil.copytree(game_save_location, "NayohSaveLog/" + game_title + "/" + date_today + "/" + currentTime)
            print("[" + reformatedCurrentTime + "]Backup Performed To " + game_title + ".")
            manageOldFileVersions(game_title, date_today, max_files_by_folder)
        else:
            print("[" + reformatedCurrentTime + "]Backup Not Performed, The Directory for " + game_title + " Is Empty.")
    else:
        print("[" + reformatedCurrentTime + "]Backup Not Performed, The Directory For " + game_title + " Doesn't Exist.")

#Check if Directory is Empty
def checkDirectoryFiles(path):
    dir_files = sum([len(files) for r, d, files in os.walk(path)])
    return dir_files

#Variables
def getDate():
    today = date.today()
    date_today = today.strftime("%Y.%m.%d")
    yesterday = today - timedelta(days = 1)
    date_yesterday = yesterday.strftime("%Y.%m.%d")

    return date_today, date_yesterday

#Start
def start():
    date_today, date_yesterday = getDate()
    game_title, game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder = checkSettings()
    createDirectory(game_title, date_today)
    manageOldFiles(game_title, date_yesterday, date_today, delete_old)
    currentTime = now()
    currentTime = currentTime.replace("-", ":")
    n_cls()
    print("[" + currentTime + "]Backup System Started.\n")
    while True:
        time.sleep(backup_save_time_minutes)
        backupSave(game_title, date_today, game_save_location, max_files_by_folder)

start()