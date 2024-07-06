import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """Authenticate and return the credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def list_gmail_labels(service):
    """List the user's Gmail labels using the Gmail API."""
    try:
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        print(f"An error occurred: {error}")

def fetch_emails(service):
    """Fetch the latest 20 emails using the Gmail API."""
    try:
        # Call the Gmail API to fetch the latest 20 emails
        results = service.users().messages().list(userId='me', maxResults=20).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        print("Messages:")
        for msg in messages:
            msg_id = msg['id']
            msg = service.users().messages().get(userId='me', id=msg_id).execute()
            print(f"Message snippet: {msg['snippet']}")

    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    """Main function to list Gmail labels and fetch emails."""
    creds = authenticate_gmail()
    try:
        service = build("gmail", "v1", credentials=creds)
        list_gmail_labels(service)
        fetch_emails(service)
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
