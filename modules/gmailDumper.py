import json
from google.oauth2 import service_account
from googleapiclient import discovery
from pprint import pprint
from bs4 import BeautifulSoup 
import base64

### This can be any Gooogle service scope the domain wide delegation have been granted for.
SCOPES = ["https://mail.google.com/"]

def get_gmail_service(service_account_key, impersonate):

    ### Reading Google service account credentials from the JSON key file
    service_creds = None
    with open(service_account_key, "r") as f:
        service_creds = json.load(f)

    ### Configure credentials by assigning the specific GSuite scope
    credentials = service_account.Credentials.from_service_account_info(service_creds, scopes=SCOPES)

    ### Performing delegation and retrieving credentials of the delegated or targeted user
    delegated_credentials = None
    if credentials:
        delegated_credentials = credentials.with_subject(impersonate)

    ### Creating Google service interface with delegated user credentials to impersonate the targeted user
    service = None
    if delegated_credentials:
        try:
            service = discovery.build("gmail", "v1", credentials=delegated_credentials)
        except Exception:
            print("Error testing API access using delegated credentials " 'for "%s"', email)
    return service

def readEmails(service_account_key, impersonate):
    # Read user email within Gmail with 200 max results. This can be modified
    gmail_service = get_gmail_service(service_account_key, impersonate)

    ### Get user's GMAIL Messages list: 
    result = gmail_service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    ### Get user's GMAIL Messages content and formatting:
    for msg in messages:
        # Get the message from its id
        print("\n======================= Message : " + str(msg['id']) + "  =======================")
        txt = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()

        # Get value of 'payload' from dictionary 'txt'
        payload = txt['payload']
        headers = payload['headers']
    
        # Look for Subject and Sender Email in the headers
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
    
        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)
        
        # Now, the data obtained is in lxml. So, we will parse
        # it with BeautifulSoup library
        soup = BeautifulSoup(decoded_data , "lxml")
        body = soup.body()
        
        # Printing the subject, sender's email and message
        print("Subject: ", subject)
        print("From: ", sender)
        print("Message: ", body)
        print('\n')   

def listEmails(service_account_key, impersonate):
    print("++++++++++++++++ Listing Gmails emails ++++++++++++++++")
    gmail_service = get_gmail_service(service_account_key, impersonate)
    result = gmail_service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    for msg in messages:
        # Get the message from its id
        print("\n======================= Gmail Message id: " + str(msg['id']) + "  =======================")
        txt = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
        
        payload = txt['payload']
        headers = payload['headers']
        # Look for Subject and Sender Email in the headers
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        
        # Printing the subject, sender's email and message
        print("Subject: ", subject)
        print("From: ", sender)

def listFolders(service_account_key, impersonate):
    gmail_service = get_gmail_service(service_account_key, impersonate)
    results = gmail_service.users().labels().list(userId='me').execute()

    labels = results.get('labels', [])

    if not labels:
        print("No labels (folders) found in Gmail.")
    else:
        print("Labels (folders) in Gmail:")
        for label in labels:
            print(f"Label Name: {label['name']}")

def save_attachment(filename, file_data):
    with open(filename, 'wb') as f:
        f.write(file_data)
        print(f"===> Downloaded attachment : {filename}")

def downloadAttachments(service_account_key, impersonate):
    # This will download all attachments from the last 200 Gmail emails
    gmail_service = get_gmail_service(service_account_key, impersonate) 
    results = gmail_service.users().messages().list(userId='me', maxResults=200).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found in Gmail.")
    else:
        for message in messages:
            message_data = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
            if 'parts' in message_data['payload']:
                for part in message_data['payload']['parts']:
                    if 'filename' in part:
                        filename = part['filename']
                        attachment_id = part['body'].get('attachmentId', None)  # Handle emails without attachmentId
                        if attachment_id:
                            attachment = gmail_service.users().messages().attachments().get(
                            userId='me', messageId=message_data['id'], id=attachment_id).execute()
                            file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                            print(f"+++ Found attachment : {filename}")
                            save_attachment(filename, file_data)