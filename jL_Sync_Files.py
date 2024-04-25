#!/usr/bin/python

import datetime
import os
import pathlib

import requests
import json
import base64
from requests.auth import HTTPBasicAuth

import tkinter as tk
from tkinter import ttk, filedialog

from datetime import datetime
from dateutil import tz
import re

import customtkinter

# TODO: Checkbutton ob Ordnerstruktur der Akte auf dem Server übernommen werden soll
# python 3 -m venv venv
# source venv/bin/activate
# pip3 install customtkinter requests dateutil


#customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Gibt den Pfad zum aktuellen Skript zurück
# current_script_path = os.path.dirname(os.path.realpath(__file__))

home = os.path.expanduser("~")
settings_path = os.path.join(home, ".jL_Sync_Files/")
if not os.path.exists(settings_path):
    # Erstellen des Ordners, falls er nicht existiert
    os.makedirs(settings_path)
print("Einstellungen geladen aus: " + settings_path)

def settings_speichern():
    """Einstellungen für LogIn Daten werden gespeichert
    """

    data = {'user': entry_user.get(), 'password': entry_passwort.get(), 'server_adresse': entry_server.get(),
            'port': entry_port.get()}
    try:
        with open(f"{settings_path}/jL_Sync_Files_Settings.json", "w") as write_file:
            json.dump(data, write_file)
    except:
        status_text.insert(tk.END, '\nFehler, Datei/Ordner nicht gefunden\n')
        status_text.see(tk.END)
    # settings_laden()
    status_text.insert(tk.END, '\nLogin Daten gespeichert (unsicher!)\n')
    status_text.see(tk.END)


def settings_laden():
    """Einstellungen für LogIn Daten werden geladen und die Felder befüllt"""

    try:
        with open(f"{settings_path}/jL_Sync_Files_Settings.json", "r") as read_file:
            settings = json.load(read_file)

        entry_user.delete(0, tk.END)
        entry_user.insert(0, settings['user'])
        entry_passwort.delete(0, tk.END)
        entry_passwort.insert(0, settings['password'])
        entry_server.delete(0, tk.END)
        entry_server.insert(0, settings['server_adresse'])
        entry_port.delete(0, tk.END)
        entry_port.insert(0, settings['port'])
        status_text.insert(tk.END, '\nLogin Daten geladen\n')
        status_text.see(tk.END)
    except FileNotFoundError:
        status_text.insert(tk.END, '\nKeine Login Daten gespeichert\n')
        status_text.see(tk.END)


def load_sync_folder():
    try:
        with open(f"{settings_path}/jL_Sync_Files_Path_Settings.json", "r") as read_file:
            sync_path = json.load(read_file)['sync_path']
            status_text.insert(tk.END, f'\nSync Ordner {sync_path} geladen\n')
            status_text.see(tk.END)
        return sync_path
    except FileNotFoundError:
        status_text.insert(tk.END, '\nKein Sync Ordner gespeichert\n')
        status_text.see(tk.END)


def get_and_save_sync_folder():
    # Nutzer wird nach dem Sync Ordner gefragt
    # Ordner wird gespeichert, wenn eine Speicherung erfolgt ist, soll die App
    # beim nächsten Start denselben Ordner wie beim letzten Mal verwenden

    sync_path = filedialog.askdirectory(title="Aktenordner wählen")

    data = {'sync_path': sync_path}
    try:
        with open(f"{settings_path}/jL_Sync_Files_Path_Settings.json", "w") as write_file:
            json.dump(data, write_file)
    except FileNotFoundError:
        status_text.insert('\nFehler beim Laden und Speichern des Sync-Ordners\n')
        status_text.see(tk.END)
    # settings_laden()
    status_text.insert(tk.END, f'\nSync Ordner {sync_path} gespeichert\n')
    status_text.see(tk.END)
    return sync_path


def switch_sync_on(file_number):
    """die gewählte Akte wird synchronsiert"""

    gefundene_akte = list(filter(lambda x: x['fileNumber'] == file_number.strip(), cases_loaded))

    # gefundene_akte_nach_name = list(filter(lambda x: x['name'] in file_number, cases_loaded))

    print(gefundene_akte)

    try:
        case_id = gefundene_akte[0]['id']
    except UnboundLocalError:
        status_text.insert(tk.END, f"\nAktenzeichen ungültig\n")
        status_text.see(tk.END)
        return
    except IndexError:
        status_text.insert(tk.END, f"\nAktenzeichen ungültig\n")
        status_text.see(tk.END)
        return

    # status_text.insert(tk.END, f"Gefundene Akten {gefundene_akte_nach_az[0]['fileNumber']}")

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v5/cases/syncsettings")

    upload_data = {'caseId': case_id, 'principalId': user, 'sync': True}

    try:
        r = requests.put(url, auth=HTTPBasicAuth(user, password), json=upload_data, timeout=20)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
        status_text.see(tk.END)


    #print(f"Status code: {r.status_code}")
    status_text.insert(tk.END,
                       f'\nDie Akte {gefundene_akte[0]["name"]} - {gefundene_akte[0]["fileNumber"]} wird nun synchronisiert\n')
    status_text.see(tk.END)


def switch_sync_off(file_number):
    """die gewählte Akte wird nicht mehr synchronisiert"""

    gefundene_akte = list(filter(lambda x: x['fileNumber'] == file_number.strip(), cases_loaded))

    print(gefundene_akte)

    try:
        case_id = gefundene_akte[0]['id']
    except UnboundLocalError:
        status_text.insert(tk.END, f"\nAktenzeichen ungültig\n")
        status_text.see(tk.END)
        return
    except IndexError:
        status_text.insert(tk.END, f"\nAktenzeichen ungültig\n")
        status_text.see(tk.END)
        return

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v5/cases/syncsettings")

    upload_data = {'caseId': case_id, 'principalId': user, 'sync': False}

    try:
        r = requests.put(url, auth=HTTPBasicAuth(user, password), json=upload_data, timeout=20)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")

    # print(f"Status code: {r.status_code}")
    status_text.insert(tk.END,
                       f'\nDie Akte {gefundene_akte[0]["name"]} - {gefundene_akte[0]["fileNumber"]} wird nun nicht mehr synchronisiert\n')
    status_text.see(tk.END)


def convert_utc_to_local_time(time_to_convert):
    """ die UTC Zeit wird in die lokale Zeit konvertiert"""

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()

    # time_to_convert = "2022-05-16T22:00:00Z[UTC]"
    numeric_filter = re.sub("T|Z|U|C", " ", time_to_convert).replace("[", "").replace("]", "")
    time_to_convert = str(numeric_filter.rstrip())
    # print(time_to_convert)
    utc = datetime.strptime(time_to_convert, '%Y-%m-%d %H:%M:%S')

    # tell datetime object that it is in UTC time zone since
    # datetime objects are "naive" by default

    utc = utc.replace(tzinfo=from_zone)

    # convert time zone
    central = utc.astimezone(to_zone)

    lokale_zeit = str(central).removesuffix("+02:00")

    # print(str(central))
    return lokale_zeit


def contactsList():
    """Listet alle Kontakte auf dem Server auf"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/contacts/list")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")

    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    contacts = r.json()
    global contacts_loaded
    try:
        with open(f"{settings_path}/jL_Sync_Files_Contacts.json", "w") as write_file:
            json.dump(contacts, write_file)
    except FileNotFoundError:
        status_text.insert(tk.END, '\nFehler\n')
        status_text.see(tk.END)
    try:
        with open(f"{settings_path}/jL_Sync_Files_Contacts.json", "r") as read_file:
            contacts_loaded = json.load(read_file)
    except FileNotFoundError:
        status_text.insert(tk.END, '\nFehler\n')
        status_text.see(tk.END)

    # Verarbeitet die Ergebnisse
    print(f"Zahl der Adressen: {len(contacts)}")
    status_text.insert(tk.END, f"\n{len(contacts)} Adressen vom Server geladen\n")
    status_text.see(tk.END)


def casesList():
    """Listet alle Cases auf dem Server auf"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/list")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    cases = r.json()
    global cases_loaded
    try:
        with open(f"{settings_path}/jL_Sync_Files_Cases.json", "w") as write_file:
            json.dump(cases, write_file)
    except FileNotFoundError:
        status_text.insert(tk.END, '\nFehler\n')
        status_text.see(tk.END)

    try:
        with open(f"{settings_path}/jL_Sync_Files_Cases.json", "r") as read_file:
            cases_loaded = json.load(read_file)
    except FileNotFoundError:
        status_text.insert(tk.END, '\nFehler\n')
        status_text.see(tk.END)
    # Verarbeitet die Ergebnisse
    print(f"Zahl der Akten: {len(cases)}")
    status_text.insert(tk.END, f"\n{len(cases)} Akten vom Server geladen\n")
    status_text.see(tk.END)


def contactAbrufen(contact_id):
    """Listet alle Daten eines Kontakts nach dessen ID (Param) auf"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v2/contacts/" + contact_id)

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    response_dict = r.json()
    return response_dict


def beteiligte_abrufen(case_id):
    """Listet alle Beteiligte einer Akte auf"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/" + case_id + "/parties")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    response_dict = r.json()
    return response_dict


def etiketten_abrufen(case_id):
    """Listet alle Etiketten einer Akte auf"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/" + case_id + "/tags")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    response_dict = r.json()
    return response_dict


def dateiSenden(datei_local_name, case_id):
    """lokale Datei wird auf Server in die Akte geladen"""

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/document/create")

    file_to_upload = pathlib.Path('.', datei_local_name)
    print("Datei zum hochladen: ")
    print(file_to_upload)

    with open(file_to_upload, 'r') as f:
        base64content = file_to_upload.read_bytes()
        base64string = base64.b64encode(base64content).decode("utf-8")

    data = {"base64content": base64string, "caseId": case_id, "fileName": datei_local_name}

    try:
        r = requests.put(url, auth=HTTPBasicAuth(user, password), json=data, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")

    # print(f"Status code: {r.status_code}")
    status_text.insert(tk.END, f"\n{file_to_upload} auf den Server geladen\n")
    status_text.see(tk.END)


def dateiListeEmpfangen(case_id):
    """lädt eine Liste von Dateien einer Akte herunter und gibt eine Liste zurück,
    /v1/cases/{id}/documents
    """

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/" + case_id + "/documents")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")

    # Speichert die Api Antwort in einer Variablen
    response_dict = r.json()
    zahl_der_dateien = len(response_dict)

    # return datei_liste_ids, datei_liste_name
    return response_dict


def getDueDates(case_id):
    # Returns all due dates for a given case - /v1/cases/{id}/duedates

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v1/cases/" + case_id + "/duedates")

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")
    # print(f"Status code: {r.status_code}")
    response_dict = r.json()
    return response_dict


# new implementation with downloading in chunks
def dateiEmpfangen(document_id):
    """Lädt Datei einer Akte herunter und speichert sie auf der Festplatte."""

    # Verbindungsparameter holen
    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    # Erzeugen Sie die URL mit f-string anstelle von +
    url = f"http://{server_adresse}:{port}/j-lawyer-io/rest/v1/cases/document/{document_id}/content"

    try:
        # Download der Datei. Der Parameter stream=True ermöglicht das Herunterladen großer Dateien.
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=120, stream=True)
        r.raise_for_status()  # überprüft, ob der Request erfolgreich war
    except requests.exceptions.HTTPError as errh:
        print("Http Fehler:", errh)
        status_text.insert(tk.END, f"\nHTTP Fehler: {errh}\n")
        return
    except requests.exceptions.ConnectionError as errc:
        print("Verbindungsfehler:", errc)
        status_text.insert(tk.END, f"\nVerbindungsfehler: {errc}\n")
        return
    except requests.exceptions.Timeout as errt:
        print("Timeout Fehler:", errt)
        status_text.insert(tk.END, f"\nTimeout Fehler: {errt}\n")
        return
    except requests.exceptions.RequestException as err:
        print("Fehler:", err)
        status_text.insert(tk.END, f"\nFehler: {err}\n")
        return

    # Die Antwort als JSON interpretieren
    response_dict = r.json()
    file_name = response_dict['fileName']
    file_name = file_name.replace('/', '-')
    base64_string = response_dict['base64content']

    # Datei speichern, wenn sie noch nicht existiert
    if not os.path.isfile(file_name):
        print("PDF Datei wird heruntergeladen... ")
        status_text.insert(tk.END, f"Lade {file_name}...\n")
        status_text.see(tk.END)
        window.update()
        base64_file_bytes = base64_string.encode('utf-8')
        with open(file_name, 'wb') as file_to_save:
            decoded_data = base64.decodebytes(base64_file_bytes)
            file_to_save.write(decoded_data)
    else:
        print("Datei existiert bereits")
        status_text.insert(tk.END, f"{file_name} existiert bereits\n")
        status_text.see(tk.END)
        window.update()


def getSyncedCases(principal_id):
    """
    listet die Anzahl der und die synchr. Akten auf.
    Erstellt den Unterordner Akten und je Akte einen Ordner mit dem Kurzrubrum als Namen
    """


    status_text.insert(tk.END, f"\nAkten werden synchronisiert...\n")
    status_text.see(tk.END)

    user = entry_user.get()
    password = entry_passwort.get()
    server_adresse = entry_server.get()
    port = entry_port.get()

    url = ("http://" + server_adresse + ":" + port + "/j-lawyer-io/rest/v5/cases/list/synced/" + principal_id)

    headers = {"accept: application/json"}

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=20)
    except requests.exceptions.ConnectionError:
        print("Verbindungsfehler")
        status_text.insert(tk.END, f"\nKeine Verbindung zum Server \n")

    # Speichert die Api Antwort in einer Variablen
    response_dict = r.json()
    #print(f"Status code: {r.status_code}")
    print("-----------------------------------")

    #global zahl_der_akten_to_sync
    zahl_der_akten_to_sync = len(response_dict)

    progress_bar.configure(maximum=zahl_der_akten_to_sync)

    print(f"\nFür {principal_id} sind {zahl_der_akten_to_sync} Akten zu synchronisieren: ")
    status_text.insert(tk.END, f"\nFür {user} sind {zahl_der_akten_to_sync} Akten zu synchronisieren: \n")
    status_text.see(tk.END)
    print("-----------------------------------")
    status_text.insert(tk.END, "-----------------------------------\n")

    index = 0

    # cwd = gibt aktuellen Ordner zurück
    cwd = os.getcwd()
    # der gespeicherte Sync Ordner wird geladen
    sync_path = load_sync_folder()
    if os.path.isdir(sync_path):
        os.chdir(sync_path)
    else:
        os.mkdir(sync_path)
        os.chdir(sync_path)
    if os.path.isdir('./Akten'):
        os.chdir("Akten")
    else:
        os.mkdir("Akten")
        os.chdir("Akten")
    # für die Zahl der zu synchr. Akten wird über den Index ein Ordner angelegt, umbenannt und in den Ordner gewechselt
    while index < zahl_der_akten_to_sync:

        if os.path.isdir(
                response_dict[index]['name'].replace('/', '-') + " - " + response_dict[index]['fileNumber'].replace('/',
                                                                                                                    '-')):
            os.chdir(
                response_dict[index]['name'].replace('/', '-') + " - " + response_dict[index]['fileNumber'].replace('/',
                                                                                                                    '-'))
        else:
            os.mkdir(
                response_dict[index]['name'].replace('/', '-') + " - " + response_dict[index]['fileNumber'].replace('/',
                                                                                                                    '-'))
            os.chdir(
                response_dict[index]['name'].replace('/', '-') + " - " + response_dict[index]['fileNumber'].replace('/',
                                                                                                                    '-'))

        # über die Funktion dateiListeEmpfangen werden alle Pdf Dateien zurückgegeben zu der angefragten Akten ID
        print("\nSynchronisiere die Akte: " + response_dict[index]['name'] + " - " + response_dict[index]['fileNumber'])
        status_text.insert(tk.END,
                           f'\nSynchronisiere die Akte: {response_dict[index]["name"]} - {response_dict[index]["fileNumber"]}\n')
        status_text.see(tk.END)
        progress_var.set(index)
        window.update()
        # 2 Listen, id und name werden erstellt und mit den Dateien Remote verglichen
        datei_liste_response = dateiListeEmpfangen(response_dict[index]['id'])
        # print(datei_liste_response)

        # die Liste der lokal vorhandenen Dateien
        datei_liste_local_name = [f for f in os.listdir('.') if os.path.isfile(f)]
        if ".DS_Store" in datei_liste_local_name:
            datei_liste_local_name.remove(".DS_Store")
        print("Dateien lokal")
        print(datei_liste_local_name)
        print("Dateien remote")
        print(datei_liste_response)
        print("Case-ID: " + response_dict[index]['id'])

        # die Liste mit den PDF Dateien wird iteriert und die jeweilige Datei heruntergeladen
        print("---------------------------------------------------------------------------")

        datei_liste_remote = []

        # jede Datei auf dem Server (PDF, html) wird heruntergeladen und der Name in datei_liste_remote aufgenommen
        # damit beim Upload von Dateien ein Vergleich vorgenommen werden kann mit den lokal und remote vorh. Dateien
        for count, value in enumerate(datei_liste_response):
            #print(count, "Dokument-Id: ", value['id'])
            print(count, "Dokumenten-Name: ", value['name'])

            datei_liste_remote.append(value['name'])

            if sync_pdf_html_only.get() == True:  # nur PDF und HTML Dateien werden synchronisiert
                if ((".pdf" in str({value['name']})) | (".html" in str({value['name']}))) & (
                        ".eml" not in str({value['name']})):
                    if not value['name'] in datei_liste_local_name:
                        dateiEmpfangen(value['id'])

                    else:
                        pass  # Datei existiert bereits lokal
            else:  # alle Dateien werden synchronisiert
                if not value['name'] in datei_liste_local_name:
                    dateiEmpfangen(value['id'])

                else:
                    pass

        for datei in datei_liste_local_name:
            if (datei not in datei_liste_remote):
                window.update()
                dateiSenden(datei_local_name=datei, case_id=response_dict[index]['id'])

            else:
                pass  # Datei existiert bereits remote

        # schreibt alle WV/Termine/Fristen in eine html/text Datei
        dueDates = getDueDates(case_id=response_dict[index]['id'])

        # Sortiere die dueDates Liste in absteigender Reihenfolge
        dueDates.sort(key=lambda x: x['dueDate'], reverse=True)


        ############### Erstellt eine Datei mit Wiedervorlagen, Terminen etc. ##################

        with open('_KALENDER.txt', 'w') as file:
            for count, value in enumerate(dueDates):
                if not value['done']:
                    file.write("\n############# Wiedervorlagen - Termine - Fristen #############\n\n")
                    file.write("Datum: " + convert_utc_to_local_time(value['dueDate']) + " - ")
                    if value['type'] == "FOLLOWUP":
                        file.write("Wiedervorlage - ")
                    elif value['type'] == "EVENT":
                        file.write("Termin - ")
                    elif value['type'] == "RESPITE":
                        file.write("Frist - ")

                    if value['done']:
                        file.write("Status: erledigt\n")
                    else:
                        file.write("Status: offen\n")
                    file.write("Grund: " + value['reason'] + "\n")
                    file.write("für: " + value['assignee'] + "\n")
            for count, value in enumerate(dueDates):
                if value['done']:
                    file.write("\n############# Wiedervorlagen - Termine - Fristen #############\n\n")
                    file.write("Datum: " + convert_utc_to_local_time(value['dueDate']) + " - ")
                    if value['type'] == "FOLLOWUP":
                        file.write("Wiedervorlage - ")
                    elif value['type'] == "EVENT":
                        file.write("Termin - ")
                    elif value['type'] == "RESPITE":
                        file.write("Frist - ")

                    if value['done']:
                        file.write("Status: erledigt\n")
                    else:
                        file.write("Status: offen\n")
                    file.write("Grund: " + value['reason'] + "\n")
                    file.write("für: " + value['assignee'] + "\n")

        ############### Beteiligte der Akte werden in Datei geschrieben ###############

        beteiligte_in_akte = beteiligte_abrufen(response_dict[index]['id'])
        # print(beteiligte_in_akte)

        etiketten_in_akte = etiketten_abrufen(response_dict[index]['id'])

        try:
            with open('_BETEILIGTE.txt', 'w') as file:
                for count, value in enumerate(reversed(beteiligte_in_akte)):
                    beteiligte_details = contactAbrufen(value['addressId'])

                    file.write("\n###################### Beteiligte ######################\n\n")
                    file.write("Name: " + beteiligte_details['firstName'] + " " + beteiligte_details['name']+" "+ beteiligte_details['company'] + f" ({value['involvementType']})")
                    file.write(
                        "\nAnschrift: " + beteiligte_details['street'] + " " + beteiligte_details['streetNumber'] + ", " +
                        beteiligte_details['zipCode'] + " " + beteiligte_details['city'])
                    file.write("\nTelefon: " + beteiligte_details['phone'])
                    file.write("\nMobil: " + beteiligte_details['mobile'])
                    file.write("\neMail: " + beteiligte_details['email'])
                    file.write("\nZeichen: " + value['reference'] + "\n")
                file.write("\n###################### Etiketten ######################\n\n")
                for count, value in enumerate(etiketten_in_akte):
                    file.write(value['name'] + ", ")
        except Exception as e:
            print("Ein Fehler ist aufgetreten beim Schreiben der Datei BETEILIGTE.txt")
            print(e)
            status_text.insert(tk.END, f"\nEin Fehler ist aufgetreten beim Schreiben der Datei BETEILIGTE.txt\n")
        progress_var.set(index+1)
        window.update()

        os.chdir("..")

        index += 1

        print()
    status_text.insert(tk.END, f"\nFür {user} wurden {zahl_der_akten_to_sync} Akten synchronisiert \n")
    status_text.see(tk.END)
    print(f"\nFür {user} wurden {zahl_der_akten_to_sync} Akten synchronisiert \n")
    os.chdir(cwd)


def main():
    print("jL-Sync-Files gestartet...")


############################# GUI ##########################
window = customtkinter.CTk()
window.geometry("685x730+550+150")
window.eval('tk::PlaceWindow . center')
window.title("j-Lawyer-Tools --- jL-Sync-Files")
window.columnconfigure(0, weight=1)
window.rowconfigure(99, weight=1)

sync_pdf_html_only = tk.BooleanVar(window, True)
status = tk.StringVar(window, "Status...")
progress_var = tk.IntVar(window)



# label frame SETTINGS und LOGIN laden und speichern Buttons
lf = customtkinter.CTkFrame(window, corner_radius=15)
lf.grid(column=0, row=0, padx=15, pady=15)

lb_user_input = customtkinter.CTkLabel(lf, text="Benutzer:")
lb_user_input.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
entry_user = customtkinter.CTkEntry(lf, width=150)
entry_user.grid(column=1, row=0, padx=15, pady=10, sticky=tk.E)

lb_pw_input = customtkinter.CTkLabel(lf, text="Passwort:")
lb_pw_input.grid(column=0, row=1, padx=5, pady=10, sticky=tk.W)
entry_passwort = customtkinter.CTkEntry(lf, show='*', width=150)
entry_passwort.grid(column=1, row=1, padx=15, pady=10, sticky=tk.E)

lb_server_input = customtkinter.CTkLabel(lf, text="Server:")
lb_server_input.grid(column=2, row=0, padx=5, pady=10, sticky=tk.W)
entry_server = customtkinter.CTkEntry(lf, width=150)
entry_server.grid(column=3, row=0, padx=15, pady=10, sticky=tk.E)

lb_port_input = customtkinter.CTkLabel(lf, text="Port:")
lb_port_input.grid(column=2, row=1, padx=5, pady=10, sticky=tk.W)
entry_port = customtkinter.CTkEntry(lf, width=150)
entry_port.grid(column=3, row=1, padx=15, pady=10, sticky=tk.E)

bt_load_settings = customtkinter.CTkButton(lf, text="Login laden", command=settings_laden)
bt_load_settings.grid(column=0, row=2, columnspan=2, padx=15, pady=10, sticky=(tk.W + tk.E))

bt_save_settings = customtkinter.CTkButton(lf, text="Login speichern", command=settings_speichern)
bt_save_settings.grid(column=2, row=2, columnspan=3, padx=15, pady=10, sticky=(tk.W + tk.E))

bt_sync_akten_laden = customtkinter.CTkButton(lf, text="Aktenbestand laden / aktualisieren", command=casesList)
bt_sync_akten_laden.grid(column=0, row=3, columnspan=2, padx=15, pady=10, sticky=(tk.W + tk.E))

bt_sync_adressen_laden = customtkinter.CTkButton(lf, text="Adressenbestand laden / aktualisieren", command=contactsList)
bt_sync_adressen_laden.grid(column=2, row=3, columnspan=2, padx=15, pady=10, sticky=(tk.W + tk.E))

bt_sync_ordner_waehlen = customtkinter.CTkButton(lf, text="Sync Ordner wählen",
                                    command=get_and_save_sync_folder)
bt_sync_ordner_waehlen.grid(column=0, row=4, columnspan=4, padx=15, pady=10, sticky=(tk.W + tk.E))

# Frame Button Sync
lf_bt_sync = customtkinter.CTkFrame(window, corner_radius=15)
lf_bt_sync.grid(column=0, row=1, padx=10, pady=20)

lb_akte_to_sync_input = customtkinter.CTkLabel(lf_bt_sync, text="Aktenzeichen: ")
lb_akte_to_sync_input.grid(column=0, row=1, padx=10, sticky=(tk.W + tk.E))
entry_akte_to_sync_input = customtkinter.CTkEntry(lf_bt_sync)
entry_akte_to_sync_input.grid(column=1, row=1, padx=10, pady=10, sticky=(tk.W + tk.E))

bt_sync_aktivieren = customtkinter.CTkButton(lf_bt_sync, text="Sync an",
                                command=lambda: switch_sync_on(entry_akte_to_sync_input.get()))
bt_sync_aktivieren.grid(column=3, row=1, padx=10, pady=10)

bt_sync_deaktivieren = customtkinter.CTkButton(lf_bt_sync, text="Sync aus",
                                  command=lambda: switch_sync_off(entry_akte_to_sync_input.get()))
bt_sync_deaktivieren.grid(column=4, row=1, padx=10, pady=10)

# Checkbutton: nur PDF/HTML Dateien synchronisieren
chk_sync_pdf_html_only = customtkinter.CTkCheckBox(lf, text="Nur PDF/HTML Dateien synchronisieren", variable=sync_pdf_html_only)
chk_sync_pdf_html_only.grid(column=0, row=5, columnspan=4, padx=15, pady=10, sticky=(tk.W + tk.E))

# BUTTON Sync Starten FRAME
lf_bt_sync_starten = customtkinter.CTkFrame(window, corner_radius=15)
lf_bt_sync_starten.grid(column=0, row=2, padx=15, pady=20)


bt_sync_starten = customtkinter.CTkButton(lf_bt_sync_starten, text="Synchronisation starten",
                             command=lambda: getSyncedCases(entry_user.get()))
bt_sync_starten.pack(side=tk.TOP, padx=15, pady=10)

progress_bar = ttk.Progressbar(lf_bt_sync_starten, orient=tk.HORIZONTAL, variable=progress_var, length=300, mode="determinate")
progress_bar.pack(side=tk.BOTTOM, padx=10, pady=10)


########################## STATUS TEXT FELD ###########################

status_text = tk.Text(width=75, height=12)
status_text.configure(font=("Courier", 11))
status_text.grid(row=99, padx=15, pady=15, columnspan=4, sticky=(tk.W + tk.E + tk.S))

################### General loading of Data ##########################

if os.path.exists(settings_path + "jL_Sync_Files_Settings.json"):
    settings_laden()
else:
    status_text.insert(tk.END, "\nBitte Login Daten für den Server eingeben.\n")
    status_text.see(tk.END)

# Cases werden geprüft und ggfs. geladen
if os.path.exists(settings_path + "jL_Sync_Files_Cases.json"):
    with open(settings_path + "jL_Sync_Files_Cases.json", "r") as read_file:
        global cases_load
        cases_loaded = json.load(read_file)
        status_text.insert(tk.END, "\nLetzten Aktenbestand geladen.\n")
        status_text.see(tk.END)
else:
    status_text.insert(tk.END, "\nBitte zuerst den Aktenbestand vom Server laden!\n")
    status_text.see(tk.END)

# Contacts werden geladen, falls gespeichert, ansonsten Hinweis beim 1. Start
if os.path.exists(settings_path + "jL_Sync_Files_Contacts.json"):
    with open(settings_path + "jL_Sync_Files_Contacts.json", "r") as read_file:

        contacts_loaded = json.load(read_file)
        status_text.insert(tk.END, "\nLetzten Adressenbestand geladen.\n")
        status_text.see(tk.END)
else:
    status_text.insert(tk.END, "\nBitte zuerst den Adressenbestand vom Server laden!\n")
    status_text.see(tk.END)

# Sync Ordner wird geladen, falls einer gespeichert ist
if os.path.exists(settings_path + "jL_Sync_Files_Path_Settings.json"):
    with open(settings_path + "jL_Sync_Files_Path_Settings.json", "r") as read_file:
        sync_path = json.load(read_file)['sync_path']
    status_text.insert(tk.END, f'\nSync Ordner {sync_path} geladen\n')
    status_text.see(tk.END)
else:
    status_text.insert(tk.END, f'\nBitte zuerst Sync Ordner auswählen\n')
    status_text.see(tk.END)

if __name__ == "__main__":
    main()  # beim Start werden die Settings geladen, falls die Datei vorhanden ist
    window.mainloop()