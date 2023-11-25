# Game Save Backup

The program will make a backup of the selected folder every X minutes, which can be specified in the settings.

Preview:

![](https://i.imgur.com/obgJb8O.png)

### Setup (How to Use):

Run the program in [Project]Run.bat or run the python file from cmd.
```sh
python "[Project]Game Save Backup.py"
```



When starting the program it will ask for some information, these are:

- Game title: The program will use it to create a folder with the game name to store your backup files.
    >  e.g.: Dark Souls II
- Game save location: The root directory where the game save is stored.
    > e.g.: C:\Users\Nayoh\AppData\Roaming\DarkSoulsII
- Backup save time: The time in minutes that the backup should be performed.
    > e.g.: 15
- Delete old files: By activating this option, the program will delete folders of old files that are not from today or yesterday.
    > e.g.: Y
- Maximum number of saves per day: The maximum number of save files that must be kept before starting to delete old ones, using 0(zero) will never delete save files.
    > e.g.: 50

Optionally, you can create a settings file with the following model and the name "Settings.ini" in the program folder and configure its settings:

 ```ini
[game_informations]
game_title = Dark Souls II
game_save_location = C:\Users\Nayoh\AppData\Roaming\DarkSoulsII
backup_save_time_minutes = 15
delete_old = True
max_files_by_folder = 50
  ```

After configuration, your files will be in a folder called "NayohSaveLog" which will be in the same directory as the program.