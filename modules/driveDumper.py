import json
from google.oauth2 import service_account
from googleapiclient import discovery
from pprint import pprint

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_gdrive_service(service_account_key, impersonate):

    ### 1. Read Google service account credentials from the file
    service_creds = None
    with open(service_account_key, "r") as f:
        service_creds = json.load(f)

    ### 2. Setup those credentials by assigning the specific GSuite scope
    credentials = service_account.Credentials.from_service_account_info(service_creds, scopes=SCOPES)

    ### 3. Perform delegation and retrieve credentials of the delegated user
    delegated_credentials = None
    if credentials:
        delegated_credentials = credentials.with_subject(impersonate)

    ### 4. Configure Google service interface with delegated user credentials to operate on the delegated user behalf
    service = None
    if delegated_credentials:
        try:
            service = discovery.build("drive", "v3", credentials=delegated_credentials)
        except Exception:
            print("Error testing API access using delegated credentials " 'for "%s"', email)
    return service

def listFiles(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)

    ### Get user's gdrive files: 
    results = gdrive_service.files().list(
        q="trashed=false",
        fields="files(name, mimeType)",
    ).execute()

    items = results.get('files', [])

    if not items:
        print("No files or folders found.")
    else:
        print("======================= Files and folders in Google Drive =======================")
        for item in items:
            print(f"Title: {item['name']}, Type: {item['mimeType']}")

def readFiles(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    
def downloadFiles(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
    
def uploadFiles(service_account_key, impersonate):
    gdrive_service = get_gdrive_service(service_account_key, impersonate)
