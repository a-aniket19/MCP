from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import os
from email.mime.text import MIMEText

mcp = FastMCP("Gmail")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_gmail_service():
    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

@mcp.tool()
def read_emails(max_results: int = 5) -> str:
    """Read the latest emails from the Gmail inbox. Use this when the user wants to check, read or see their emails."""
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        labelIds=["INBOX"]
    ).execute()
    
    messages = results.get("messages", [])
    if not messages:
        return "No emails found."
    
    output = []
    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()
        
        headers = {h["name"]: h["value"] for h in full_msg["payload"]["headers"]}
        output.append(
            f"From: {headers.get('From', 'Unknown')}\n"
            f"Subject: {headers.get('Subject', 'No Subject')}\n"
            f"Date: {headers.get('Date', 'Unknown')}\n"
        )
    
    return "\n---\n".join(output)

@mcp.tool()
def search_emails(query: str, max_results: int = 5) -> str:
    """Search Gmail emails using a query string. Supports standard Gmail search operators like from:, subject:, after:. Use this when the user wants to find specific emails."""
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get("messages", [])
    if not messages:
        return f"No emails found for query: {query}"
    
    output = []
    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()
        
        headers = {h["name"]: h["value"] for h in full_msg["payload"]["headers"]}
        output.append(
            f"From: {headers.get('From', 'Unknown')}\n"
            f"Subject: {headers.get('Subject', 'No Subject')}\n"
            f"Date: {headers.get('Date', 'Unknown')}\n"
        )
    
    return "\n---\n".join(output)

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient. Use this when the user wants to send, compose or write an email."""
    service = get_gmail_service()
    
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    service.users().messages().send(
        userId="me",
        body={"raw": encoded}
    ).execute()
    
    return f"Email sent to {to} successfully."

if __name__ == "__main__":
    mcp.run()