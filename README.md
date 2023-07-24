# jL-Sync-Tool
A synchronisation tool for j-Lawyer that syncs case files to local hard drive.
You need a running j-Lawyer.org installation (server) to sync files. 
Also go to www.j-lawyer.org 

**Python 3.10** or newer required, download from python.org

**Tkinter** required, install via terminal 

    sudo apt install python3-tk 

on Ubuntu or 

    sudo dnf install python3-tkinter 

on Fedora

or 

    brew install tkinter

on MacOS (using Homebrew)

## Installation:
- open terminal
- Linux, Windows: pip install requests python-dateutil customtkinter
- MacOs: pip3 install requests python-dateutil customtkinter


## Start script via terminal:
- Open Terminal in Script folder
- MacOS: python3 jL_Sync_Files.py
- Linux/Windows: python jL_Sync_Files.py


## How to use: 
- enter Login Data; can be saved for your convenience
(be careful with the password, password is saved in plain text in local .json file)
- "Aktenbestand laden / aktualiseren" and "Adressenbestand laden / aktualisieren" (will be saved for next run of the script)
- Choose Sync-Folder (will be saved for next time).

Cases and Contacts  will be saved locally in json file to make the tool aware of your case data. It is not necesseray to load the data every time, unless new cases are added to the serverside database. Cases that the tool does not know wont be synced. 


Run
    "Synchronisation starten"


## Features

What the script does:
- new Folder "Akten" is created
- Files from case are downloaded to local folder in "Akten"
- Beteiligte/tags.txt file is created
- Kalender.txt is created   
- when new files are added to local folder, these files will be uploaded next time, synchronisation starts.
- certain cases can be activated for synchronization by giving its File-Number
- the user can choose if only PDF/HTML files or every file of the case is being downloaded
- script can be used from everywhere, just use a VPN tunnel. The login data stay the same
