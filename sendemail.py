import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import whatsthetea

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

urls = {"Tech": ["https://www.youtube.com/watch?v=ytdIjfGuHZQ"], "AI": [], "Politics": []}

def send_email(name, email, topics):
    youtube_url_list = []
    for topic in topics:
        print(urls.get(topic))
        for url in urls.get(topic):
            youtube_url_list.append(url)

    # youtube_url_list = ["https://www.youtube.com/watch?v=ytdIjfGuHZQ"]
    body, topic = whatsthetea.generate_summary(youtube_url_list)
    message = MIMEText(body)
    message['to'] = email
    message['subject'] = topic
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None
