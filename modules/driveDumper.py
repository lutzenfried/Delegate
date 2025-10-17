#!/usr/bin/env python

import json
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from pprint import pprint

# Le scope a été élargi pour supporter toutes les fonctionnalités du module (lecture, écriture, permissions)
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_gdrive_service(service_account_key, impersonate):
    """Crée un objet de service Google Drive authentifié."""
    try:
        service_creds = None
        with open(service_account_key, "r") as f:
            service_creds = json.load(f)

        credentials = service_account.Credentials.from_service_account_info(service_creds, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(impersonate)
        service = discovery.build("drive", "v3", credentials=delegated_credentials)
        return service
    except Exception as e:
        print(f"Erreur lors de la création du service Drive : {e}")
        return None

def listFiles(service_account_key, impersonate):
    """Liste tous les fichiers et dossiers dans le Drive de l'utilisateur."""
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    if not gdrive_service: return

    try:
        results = gdrive_service.files().list(
            q="trashed=false",
            fields="files(name, mimeType)"
        ).execute()
        items = results.get('files', [])

        if not items:
            print("Aucun fichier ou dossier trouvé.")
        else:
            print("======================= Fichiers et dossiers dans Google Drive =======================")
            for item in items:
                print(f"Titre: {item['name']}, Type: {item['mimeType']}")
    except Exception as e:
        print(f"Une erreur est survenue lors du listage des fichiers : {e}")
            
def listFolders(service_account_key, impersonate):
    """Liste les dossiers et leur contenu."""
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    if not gdrive_service: return

    try:
        results = gdrive_service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name)"
        ).execute()
        folders = results.get('files', [])
        
        if not folders:
            print('----- Aucun dossier trouvé. -----')
        else:
            print('======================= Dossiers identifiés dans Google Drive =======================')
            for folder in folders:
                folder_id = folder["id"]
                folder_name = folder["name"]
                folder_query = f"'{folder_id}' in parents and trashed=false"
                folder_files = gdrive_service.files().list(q=folder_query, fields="files(id, name, mimeType)").execute()
                files = folder_files.get('files', [])
                print(f"\n{folder_name} ({folder_id}) - {len(files)} Fichier(s):")
                for file in files:
                    print(f'  - {file["name"]} (Type MIME: {file["mimeType"]})')
    except Exception as e:
        print(f"Une erreur est survenue lors du listage des dossiers : {e}")

def _find_folder_id_by_name(gdrive_service, foldername):
    """Fonction interne pour trouver l'ID d'un dossier par son nom."""
    folder_query = f"name='{foldername}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = gdrive_service.files().list(q=folder_query, fields="files(id)").execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None

def _find_file_id_by_name(gdrive_service, filename, folder_id=None):
    """Fonction interne pour trouver l'ID d'un fichier par son nom, optionnellement dans un dossier."""
    query = f"name = '{filename}' and trashed=false"
    if folder_id:
        query += f" and '{folder_id}' in parents"
    
    file_list = gdrive_service.files().list(q=query, fields="files(id)").execute()
    files = file_list.get('files', [])
    return files[0]["id"] if files else None

def downloadFiles(service_account_key, impersonate, filename, foldername=None):
    """Télécharge un fichier, en le cherchant optionnellement dans un dossier spécifique."""
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    if not gdrive_service: return

    file_id = None
    try:
        if foldername:
            print(f"[*] Recherche du fichier '{filename}' dans le dossier '{foldername}'...")
            folder_id = _find_folder_id_by_name(gdrive_service, foldername)
            if not folder_id:
                print(f"[!] Dossier '{foldername}' introuvable.")
                return
            file_id = _find_file_id_by_name(gdrive_service, filename, folder_id)
        else:
            print(f"[*] Recherche du fichier '{filename}' dans tout le Drive...")
            file_id = _find_file_id_by_name(gdrive_service, filename)
        
        if not file_id:
            location = f"dans le dossier '{foldername}'" if foldername else "dans le Drive"
            print(f"[!] Fichier '{filename}' introuvable {location}.")
            return

        file_metadata = gdrive_service.files().get(fileId=file_id).execute()
        file_name_to_save = file_metadata.get('name')

        if 'vnd.google-apps' in file_metadata['mimeType']:
            mime_map = {
                'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
                'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
                'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
            }
            if file_metadata['mimeType'] in mime_map:
                export_mime, ext = mime_map[file_metadata['mimeType']]
                print(f"+++ Conversion du document Google au format {ext}")
                file_name_to_save += ext
                request = gdrive_service.files().export_media(fileId=file_id, mimeType=export_mime)
            else:
                print(f"L'exportation n'est pas supportée pour ce type de fichier Google : {file_metadata['mimeType']}")
                return
        else:
            request = gdrive_service.files().get_media(fileId=file_id)

        with open(file_name_to_save, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"+++ Téléchargement {int(status.progress() * 100)}%")
        print(f"====> Fichier téléchargé : '{file_name_to_save}'\n")
    
    except Exception as e:
        print(f"Une erreur est survenue lors du téléchargement : {e}")
    
def uploadFiles(service_account_key, impersonate, filepath, filename, foldername=None):
    """Téléverse un fichier, optionnellement dans un dossier spécifique."""
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    if not gdrive_service: return
    try:
        file_metadata = {'name': filename}
        if foldername:
            parent_folder_id = _find_folder_id_by_name(gdrive_service, foldername)
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            else:
                print(f"[!] Dossier '{foldername}' introuvable. Le fichier sera téléversé à la racine.")

        media_body = MediaFileUpload(filepath, resumable=True)
        uploaded_file = gdrive_service.files().create(body=file_metadata, media_body=media_body, fields='id').execute()
        print(f"Fichier '{filename}' téléversé avec succès. ID : {uploaded_file.get('id')}")
    except Exception as e:
        print(f"Une erreur est survenue lors du téléversement : {e}")

def modifyPermissions(service_account_key, impersonate, externalaccount, filename): 
    """Partage un fichier avec un compte externe en lui donnant les droits d'écriture."""
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    if not gdrive_service: return
    
    file_id = _find_file_id_by_name(gdrive_service, filename)
    if not file_id:
        print(f"[!] Fichier '{filename}' introuvable.")
        return

    try:
        permission = {'type': 'user', 'role': 'writer', 'emailAddress': externalaccount}
        gdrive_service.permissions().create(fileId=file_id, body=permission, sendNotificationEmail=True).execute()
        print(f"+++ Accès complet accordé à {externalaccount} pour le fichier : {filename}\n")
    except Exception as e:
        print(f"--- Une erreur est survenue lors du partage des permissions : {e}")