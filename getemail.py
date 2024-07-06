import imaplib
import email
from email.header import decode_header
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    token_path = 'token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            print("Loaded credentials from token.pickle")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing credentials...")
            creds.refresh(Request())
        else:
            print("Fetching new credentials...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            print("Saved new credentials to token.pickle")
    print("Credentials:", creds)
    return creds

def generate_oauth2_string(username, access_token):
    auth_string = f'user={username}\1auth=Bearer {access_token}\1\1'
    return auth_string

def fetch_emails():
    creds = authenticate_gmail()
    imap_host = 'imap.gmail.com'
    imap_user = 'michael@xorgonix.com'
    
    # Connect to the server
    print("Connecting to IMAP server...")
    mail = imaplib.IMAP4_SSL(imap_host)

    # Use the OAuth2 token for authentication
    auth_string = generate_oauth2_string(imap_user, creds.token)
    print("Auth String:", auth_string)  # Debug information
    try:
        print("Authenticating with XOAUTH2...")
        result, data = mail.authenticate('XOAUTH2', lambda x: auth_string.encode('utf-8'))
        print("IMAP authentication result:", result)
    except imaplib.IMAP4.error as e:
        print("IMAP4 authentication error:", e)
        return

    # Select the mailbox you want to use (e.g., inbox)
    print("Selecting mailbox...")
    mail.select("inbox")

    # Search for all emails in the mailbox
    print("Searching for emails...")
    status, messages = mail.search(None, "ALL")

    if status != 'OK':
        print("Failed to search emails")
        return

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()
    print("Email IDs:", email_ids)

    # Get the last 20 email IDs
    latest_email_ids = email_ids[-20:]

    # Print the subjects of the last 20 emails
    for email_id in latest_email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        print(f"Fetching email ID {email_id}: status {status}")

        if status != 'OK':
            print(f"Failed to fetch email ID {email_id}")
            continue
        
        # Get the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                
                # Decode the subject if necessary
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                print("Subject:", subject)

    # Logout and close the connection
    mail.logout()
    print("Logged out from IMAP server")

def send_email():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText("This is a test email")
    message['to'] = 'recipient@example.com'
    message['from'] = 'michael@xorgonix.com'
    message['subject'] = 'Test Email'

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        print("Sending email...")
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Message Id: {message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__
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