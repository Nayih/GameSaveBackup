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

#Setup Settings for a New Game
def setupSettings():
    n_cls()
    print("=== ADD NEW GAME ===")
    
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

    config = configparser.ConfigParser()
    if os.path.isfile("Settings.ini"):
        try:
            config.read("Settings.ini")
        except:
            pass

    if not config.has_section(game_title):
        config.add_section(game_title)
    
    config.set(game_title, "game_save_location", game_save_location)
    config.set(game_title, "backup_save_time_minutes", str(backup_save_time_minutes))
    config.set(game_title, "delete_old", str(delete_old))
    config.set(game_title, "max_files_by_folder", str(max_files_by_folder))

    try:
        with open("Settings.ini", "w") as configfile:
            config.write(configfile)
        print(f"\n[INFO] Game '{game_title}' successfully saved to Settings.ini!")
    except:
        print("\n[INFO] Failed To Generate Settings.ini.")
    
    input("\nPress (Enter) To Return to Menu...")

#Load Games List
def getGamesList():
    if not os.path.isfile("Settings.ini"):
        return []
    try:
        config = configparser.ConfigParser()
        config.read("Settings.ini")
        return config.sections()
    except:
        return []

#Load Specific Game Configs
def loadGameConfig(game_title):
    config = configparser.ConfigParser()
    config.read("Settings.ini")
    
    game_save_location = config.get(game_title, "game_save_location")
    backup_save_time_minutes = config.getint(game_title, "backup_save_time_minutes")
    delete_old_str = config.get(game_title, "delete_old")
    max_files_by_folder = config.getint(game_title, "max_files_by_folder")

    delete_old = True if delete_old_str == "True" else False
    game_save_location = game_save_location.replace("\\", "\\\\")
    backup_save_time_minutes = backup_save_time_minutes * 60

    return game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder

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
                    print("[INFO] Error Trying To Remove Files Older Than Today's And Yesterday's Date.")

#Manage Old File Versions
def manageOldFileVersions(game_title, date_today, max_files_by_folder):
    if max_files_by_folder != 0:
        directory_list = os.listdir("NayohSaveLog/" + game_title + "/" + date_today)
        dir_len = len(directory_list)

        if dir_len > max_files_by_folder:
            try:
                shutil.rmtree("NayohSaveLog/" + game_title + "/" + date_today + "/" + directory_list[0])
            except:
                print("[INFO] Error Trying To Remove Old Files From Today's Date.")

#Backup Files
def backupSave(game_title, date_today, game_save_location, max_files_by_folder):
    currentTime = now()
    reformatedCurrentTime = currentTime.replace("-", ":")

    if os.path.isdir(game_save_location):
        dir_files = checkDirectoryFiles(game_save_location)
        if dir_files > 0:
            destination = "NayohSaveLog/" + game_title + "/" + date_today + "/" + currentTime
            try:
                shutil.copytree(game_save_location, destination)
                print("[" + reformatedCurrentTime + "] Backup Performed To " + game_title + ".")
                manageOldFileVersions(game_title, date_today, max_files_by_folder)
            except PermissionError:
                print("[" + reformatedCurrentTime + "] Backup Failed: A file was locked by the game. Retrying in next cycle.")
            except shutil.Error:
                print("[" + reformatedCurrentTime + "] Backup Failed: File in use by another process. Retrying in next cycle.")
            except Exception as e:
                print("[" + reformatedCurrentTime + "] Backup Failed: " + str(e))
        else:
            print("[" + reformatedCurrentTime + "] Backup Not Performed, The Directory for " + game_title + " Is Empty.")
    else:
        print("[" + reformatedCurrentTime + "] Backup Not Performed, The Directory For " + game_title + " Doesn't Exist.")

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

#Run Backup Loop for Selected Game
def runBackup(game_title):
    try:
        game_save_location, backup_save_time_minutes, delete_old, max_files_by_folder = loadGameConfig(game_title)
    except Exception as e:
        print(f"[INFO] Error loading configuration for {game_title}: {str(e)}")
        input("Press (Enter) to return to menu...")
        return

    currentTime = now()
    currentTime = currentTime.replace("-", ":")
    n_cls()
    print("====================================================")
    print(f"[{currentTime}] Backup System Started for: {game_title}")
    print("Press Ctrl+C to stop the backup loop and return to menu.")
    print("====================================================\n")
    
    try:
        while True:
            date_today, date_yesterday = getDate()
            createDirectory(game_title, date_today)
            manageOldFiles(game_title, date_yesterday, date_today, delete_old)
            backupSave(game_title, date_today, game_save_location, max_files_by_folder)
            time.sleep(backup_save_time_minutes)
            
    except KeyboardInterrupt:
        print("\n[INFO] Backup loop stopped by user.")
        input("Press (Enter) to return to main menu...")

#Main Menu
def menu():
    while True:
        n_cls()
        print("========================================")
        print("          GAME SAVE BACKUP MENU         ")
        print("========================================")
        print("1. Add New Game")
        print("2. Run Configured Backup")
        print("3. Exit")
        print("========================================")
        option = input("Select an option (1-3): ").strip()

        if option == "1":
            setupSettings()
        elif option == "2":
            games = getGamesList()
            if not games:
                print("\n[INFO] No games configured yet. Please add a game first.")
                input("Press (Enter) to continue...")
                continue
            
            n_cls()
            print("=== SELECT A GAME TO BACKUP ===")
            for idx, game in enumerate(games, start=1):
                print(f"{idx}. {game}")
            print(f"{len(games) + 1}. Cancel")
            print("===============================")
            
            choice = input(f"Select a game (1-{len(games) + 1}): ").strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(games):
                    runBackup(games[choice_idx])
                elif choice_idx == len(games):
                    continue
                else:
                    print("[INFO] Invalid choice.")
                    input("Press (Enter) to continue...")
            except ValueError:
                print("[INFO] Please enter a valid number.")
                input("Press (Enter) to continue...")
        elif option == "3":
            print("\nExiting program...")
            break
        else:
            print("\n[INFO] Invalid option, try again.")
            time.sleep(1)

if __name__ == "__main__":
    menu()
