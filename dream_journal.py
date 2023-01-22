# dream journal project
import smtplib
from smtplib import SMTP
with SMTP("smtp.gmail.com", 587) as smtp:
    smtp.noop()
import email
from email.message import EmailMessage
import base64
import datetime
from datetime import date, time
import random
import sys
import json



# enable Gmail API
# create credentials--> OAuth client ID --> desktop app
# download .json file with client ID and secret
# rename as credentials.json


import os.path
import pickle
# Gmail API utils
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# binary to text encoding/decoding
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for applicable MIME types
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
# from email.mime.base import MIMEBase
# from mimetypes import guess_type as guess_mime_type


verbose = False

# all-access request
SCOPES = ['https://mail.google.com/']

data = {}
with open("secrets.json", "r") as secrets_file:
    data = json.load(secrets_file)


# dream journal email server information
user = data["user"]
password = data["password"]
app_pw_gmail = data["app_pw_gmail"]


# Dreamer information
dreamer_contact =  data["dreamer_contact"]


def log(message):
    if verbose:
        print(message)


# load user API credentials
def authenticate_gmail():
    log("autenticate gmail")
    creds = None
    # token.pickle stores user access, refresh tokens
    # auto-created when auth flow completes first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if no valid credentials, user can log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # credentials are saved for future
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


service = authenticate_gmail()


subject = "Gm"
body = "Did you have a dream last night?"
to = dreamer_contact


# Did you have a dream last night?

def dream_alert(subject, body, to):
    log("dream alert")
    dream_msg = EmailMessage()
    dream_msg.set_content(body)
    dream_msg['subject'] = subject
    dream_msg['to'] = to
    dream_msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, app_pw_gmail)
    server.send_message(dream_msg)

    server.quit()


def search_messages(service, search_string):
    log("search messages")
    search_string = f"from:{dreamer_contact}, is:unread"

    try:
        search_id = service.users().messages().list(userId=user, q=search_string).execute()
        number_results = search_id['resultSizeEstimate']
        final_list = []
        if number_results>0:
            message_ids = search_id['messages']

            for ids in message_ids:
                final_list.append(ids['id'])

            return final_list

        else:
            log("returns nothing")
            return ""  # do nothing

    except errors.HttpError as error:
        print("An error occured: %s") % error


def get_message(service, user, msg_id):
    log("get message")

    try:
        message = service.users().messages().get(userId=user, id=msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)
        content_types = msg_str.get_content_maintype()

        if content_types == 'multipart':
            # part 1 is plaintext, part 2 is html
            part1, part2 = msg_str.get_payload()
            log(part1.get_payload())
            return part1.get_payload()

        else:
            log(msg_str.get_payload())
            return msg_str.get_payload()

        # split message on "-----Original Message-----" & only return first half

    except errors.HttpError as error:
        print("An error occured: %s") % error

def mark_as_read(service, search_string):
    log("mark as read")
    search_string = f"from:{dreamer_contact}, is:unread"
    messages_to_mark = search_messages(service, search_string)

    return service.users().messages().batchModify(
      userId=user,
      body={
          'ids': [messages_to_mark],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()


date = datetime.datetime.now()
date = date.strftime("%m-%d-%Y")

def write_to_journal(msg_id):
    log("write to journal")
    message = get_message(service, user, msg_id)

    if os.path.isfile('dream_journal.txt') == True:
        with open('dream_journal.txt', 'a') as journal:
            message = message.split("-----Original Message-----")
            journal.write(f"entry: {date} \n\n{message[0]} \n\n")

    else:
        with open('dream_journal.txt', 'w') as journal:
            message = message.split("-----Original Message-----")
            journal.write(f"entry: {date} \n\n{message[0]} \n\n")



# def time function for dream_alert() ??
# at random time between 5:30 and 7:30 AM
# use with ??



# def time function for search_messages()
# if time == noon:


if __name__ == '__main__':

    command = sys.argv[-1]
    if command == "alert":
        dream_alert(subject, body, to)

    elif command == "write":
        msg_ids = search_messages(service, f"from: {dreamer_contact}, is:unread")
        log(msg_ids)

        for msg_id in msg_ids:
            write_to_journal(msg_id)
            mark_as_read(service, f"from: {dreamer_contact}, is:unread")



"""

once a day, at a random time between 5 and 8 am,

bot emails the alert -- did you have a dream last night?

dreamer can text back the dream they had

at noon, the bot searches the messages aka search_messages()

        which involves authenticating gmail, opening unread messages from dreamer,

        getting message ids, storing message ids in a list that gets created new each day

in a function called get_messages()

    the bot uses the message ids to read the messages, and decodes them into text

    and writes to journal



create a shell script which calls program
script is native

"""























# filters results from specific person aka dreamer
# results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=f"from:{dreamer_contact}, is:unread").execute()

