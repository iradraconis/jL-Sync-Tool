# jL-Sync-Tool
A synchronisation tool for j-Lawyer that syncs cases and its files to local hard drive.

Python 3.10 required, download from python.org

Installation:
open terminal
Linux, Windows: pip install requests
MacOs: pip3 install requests

go to folder where script is located

Start script:
MacOS: python3 jL_Sync_Files.py
Linux/Windows: python jL_Sync_Files.py

How to use: 
- enter Login Data, save Login Data for your convenience
(be careful with the password, password is saved in plain text in local .json file)
- Load data: Aktenbestand, Adressenbestand
- Choose Sync-Folder, will be saved for next time.

Cases and Contacts  will be saved locally in json file, so not necesseray to load every time, unless new case 
needs to be synchronized. 

=> Synchronisation starten
-----------------------------

What the script does:
- new Folder "Akten" is created
- Files from case are downloaded to local folder in "Akten"
- Beteiligte/tags txt file is created
- Kalender txt is created   
- when new files are added to local folder, this file will be uploaded next time, synchronisation starts.
- certain cases can be activated for synchronization by giving its File-Number
