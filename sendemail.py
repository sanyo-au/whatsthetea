import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from email.mime.multipart import MIMEMultipart
import whatsthetea

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

def send_email(name, email, topics):
    body = ""
    header, newsletter_content_list, footer, topics = whatsthetea.generate_summary(topics)

    body += header + "\n"
    for topic, summary in zip(topics, newsletter_content_list):
        body += """<h3>""" + topic + """ </h3>"""
        body += summary
    body += "\n"
    body += footer
    title="What's the Tea"
    msg = MIMEMultipart()
    msg['to'] = email
    msg['subject'] = "Today's issue of What's the tea!"
    html = """\
    <html>
        <head></head>
        <h1>""" + title + """ </h1>
        <h3>""" + header + """ </h3>
        <body>
        """ + body + """ 
        </body>
    </html>
    """
    message = MIMEText(html, 'html')
    msg.attach(message)
    create_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None
