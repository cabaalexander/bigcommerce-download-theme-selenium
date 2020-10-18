from __future__ import print_function
import pickle
import os.path
import re
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def parse_message_doc(msg):
    body = msg['payload']['body']['data']
    html_doc = base64.urlsafe_b64decode(body.encode("ASCII")).decode("utf-8")
    return BeautifulSoup(html_doc, 'html.parser')

def get_token_from_span(soup):
    spans = soup.find_all(
        'span',
    )
    for span in spans:
        span_text = span.text.strip()
        if re.search(r'^\d{6}$', span_text):
            return span_text
    return ''

def get_bigcommerce_token(service, user_id='me'):
    # get email threads
    threads = service.users().threads().list(
        userId=user_id,
        q="login from new device to bigcommerce"
    ).execute().get('threads', [])
    # get threads data (messages)
    first_thread = threads[0]
    first_thread_data = service.users().threads().get(
        userId=user_id, id=first_thread['id']
    ).execute()
    # get just one message (the last)
    last_message = first_thread_data['messages'][-1]
    # parse doc to python object
    message_soup = parse_message_doc(last_message)
    # return token
    return get_token_from_span(message_soup)

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    token = get_bigcommerce_token(service)
    return token

if __name__ == '__main__':
    main()
