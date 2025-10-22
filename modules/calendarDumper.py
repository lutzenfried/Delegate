#!/usr/bin/env python

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from pprint import pprint

# Scopes required for Calendar and for searching recordings in Drive
SCOPES = [
    # Changed to read/write to allow event creation
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def get_service(service_name, version, service_account_key, impersonate):
    """
    Creates a Google API service object with domain-wide delegation.
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            service_account_key, scopes=SCOPES
        )
        delegated_creds = creds.with_subject(impersonate)
        service = build(service_name, version, credentials=delegated_creds)
        return service
    except Exception as e:
        print(f"[!] Error creating {service_name} service: {e}")
        return None

def listCalendars(service_account_key, impersonate):
    """
    Lists all calendars the impersonated user has access to.
    """
    print(f"[*] Listing calendars for {impersonate}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return

    try:
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        if not calendars:
            print("[*] No calendars found.")
            return

        print(f"\n[+] Found {len(calendars)} calendars:\n")
        for calendar in calendars:
            summary = calendar.get('summary', 'No Title')
            cal_id = calendar.get('id')
            role = calendar.get('accessRole')
            print(f"  Summary: {summary}")
            print(f"    ID: {cal_id}")
            print(f"    Access Role: {role}")
            print("-" * 40)

    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def listEvents(service_account_key, impersonate, calendar_id='primary', max_results=100):
    """
    Lists upcoming events from a specific calendar.
    """
    print(f"[*] Listing UPCOMING events from calendar: {calendar_id}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return
        
    try:
        # Get events from now onwards
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print(f"[*] No upcoming events found in calendar '{calendar_id}'.")
            return

        print(f"\n[+] Found {len(events)} upcoming events:\n")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No Title')
            event_id = event.get('id')
            
            print(f"  Event: {summary}")
            print(f"    ID: {event_id}")
            print(f"    Start: {start}")
            print(f"    End: {end}")
            if 'hangoutLink' in event:
                print(f"    Meet Link: {event['hangoutLink']}")
            print("-" * 40)

    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def listPastEvents(service_account_key, impersonate, time_ago, calendar_id='primary', max_results=100):
    """
    Lists past events from a specific calendar within a given timeframe.
    time_ago format: "30d" for 30 days, "4w" for 4 weeks, "2m" for 2 months.
    """
    print(f"[*] Listing PAST events from the last {time_ago} in calendar: {calendar_id}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return

    try:
        # Calculate the start time based on the time_ago string
        now = datetime.utcnow()
        time_max_str = now.isoformat() + 'Z'

        unit = time_ago[-1].lower()
        value = int(time_ago[:-1])
        
        if unit == 'd':
            delta = timedelta(days=value)
        elif unit == 'w':
            delta = timedelta(weeks=value)
        elif unit == 'm':
            # A month is approximated to 30 days for simplicity with timedelta
            delta = timedelta(days=value * 30)
        else:
            print(f"[!] Invalid time unit '{unit}'. Please use 'd' (days), 'w' (weeks), or 'm' (months).")
            return
            
        start_time = now - delta
        time_min_str = start_time.isoformat() + 'Z'

        print(f"[*] Searching for events between {start_time.strftime('%Y-%m-%d')} and now.")

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min_str,
            timeMax=time_max_str,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print(f"[*] No past events found in the last {time_ago}.")
            return

        print(f"\n[+] Found {len(events)} past events:\n")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            event_id = event.get('id')
            
            print(f"  Event: {summary}")
            print(f"    ID: {event_id}")
            print(f"    Start: {start}")
            print("-" * 40)

    except ValueError:
        print(f"[!] Invalid time format '{time_ago}'. Please use the format like '30d', '4w', etc.")
    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def getEventDetails(service_account_key, impersonate, calendar_id, event_id):
    """
    Gets detailed information for a specific event.
    """
    print(f"[*] Getting details for event {event_id} in calendar {calendar_id}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        print("\n" + "="*50)
        print(f"  Event Details for: {event.get('summary', 'No Title')}")
        print("="*50)
        
        print(f"  ID: {event.get('id')}")
        print(f"  Status: {event.get('status')}")
        print(f"  Created: {event.get('created')}")
        print(f"  Updated: {event.get('updated')}")

        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(f"  Start: {start}")
        print(f"  End: {end}")
        
        if 'description' in event:
            print(f"\n  Description:\n{event['description']}")
        
        if 'location' in event:
            print(f"\n  Location: {event['location']}")

        if 'hangoutLink' in event:
            print(f"\n  Meet Link: {event['hangoutLink']}")

        if 'attendees' in event:
            print("\n  Attendees:")
            for attendee in event['attendees']:
                email = attendee.get('email')
                response = attendee.get('responseStatus')
                print(f"    - {email} ({response})")
        print("="*50 + "\n")

    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def getAttendees(service_account_key, impersonate, calendar_id, event_id):
    """
    Lists attendees for a specific event.
    """
    print(f"[*] Getting attendees for event {event_id}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        if 'attendees' not in event:
            print("[*] No attendees found for this event.")
            return

        print(f"\n[+] Attendees for '{event.get('summary', 'No Title')}':\n")
        for attendee in event['attendees']:
            email = attendee.get('email')
            name = attendee.get('displayName', 'N/A')
            response = attendee.get('responseStatus')
            print(f"  Email: {email}")
            print(f"    Name: {name}")
            print(f"    Response: {response}")
            print("-" * 30)

    except HttpError as error:
        print(f"[!] An error occurred: {error}")


def createEvent(service_account_key, impersonate, calendar_id, summary, description, start_time, end_time, location, attendees):
    """
    Creates a new event in the specified calendar.
    """
    print(f"[*] Creating new event in calendar: {calendar_id}")
    service = get_service('calendar', 'v3', service_account_key, impersonate)
    if not service:
        return

    # Format attendees list
    attendee_list = [{'email': email.strip()} for email in attendees]

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York', # You may want to make this configurable
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York', # You may want to make this configurable
        },
        'attendees': attendee_list,
        'reminders': {
            'useDefault': True,
        },
        # Add Google Meet conference data
        'conferenceData': {
            'createRequest': {
                'requestId': f"{datetime.now().timestamp()}",
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }

    try:
        created_event = service.events().insert(
            calendarId=calendar_id, 
            body=event,
            sendUpdates='all',
            conferenceDataVersion=1
        ).execute()
        
        print("\n[+] Event created successfully!")
        print(f"    Summary: {created_event.get('summary')}")
        print(f"    ID: {created_event.get('id')}")
        print(f"    Link: {created_event.get('htmlLink')}")
        if 'hangoutLink' in created_event:
            print(f"    Meet Link: {created_event.get('hangoutLink')}")

    except HttpError as error:
        print(f"[!] An error occurred: {error}")

def listMeetingRecordings(service_account_key, impersonate, calendar_id='primary', max_results=20):
    """
    Finds potential meeting recordings by searching Drive for videos matching event titles.
    """
    print("[*] Searching for meeting recordings...")
    
    cal_service = get_service('calendar', 'v3', service_account_key, impersonate)
    drive_service = get_service('drive', 'v3', service_account_key, impersonate)
    
    if not cal_service or not drive_service:
        print("[!] Could not create required API services.")
        return

    try:
        # Get past events from the last 30 days
        time_delta = datetime.utcnow() - timedelta(days=30)
        past_time = time_delta.isoformat() + 'Z'

        events_result = cal_service.events().list(
            calendarId=calendar_id,
            timeMin=past_time,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print("[*] No recent events found to check for recordings.")
            return

        print(f"\n[*] Checking {len(events)} recent events for linked recordings...")
        found_recordings = 0

        for event in events:
            summary = event.get('summary')
            if not summary:
                continue

            # Search Drive for video files with a title matching the event summary
            escaped_summary = summary.replace("'", "\\'")
            query = f"mimeType contains 'video/' and name contains '{escaped_summary}'"
            
            drive_results = drive_service.files().list(
                q=query,
                fields="files(id, name, webViewLink, createdTime)"
            ).execute()
            
            files = drive_results.get('files', [])

            if files:
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                print("\n" + "-"*50)
                print(f"  Event: {summary} ({start_time})")
                print("  [+] Found potential recording(s) in Google Drive:")
                for f in files:
                    print(f"    - Name: {f.get('name')}")
                    print(f"      Link: {f.get('webViewLink')}")
                    print(f"      Created: {f.get('createdTime')}")
                found_recordings += len(files)
        
        print("\n" + "="*50)
        if found_recordings == 0:
            print("[*] No matching recordings found in Google Drive for recent events.")
        else:
            print(f"[+] Scan complete. Found {found_recordings} potential recording(s).")

    except HttpError as error:
        print(f"[!] An error occurred: {error}")