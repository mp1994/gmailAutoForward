#!/usr/local/bin/python3

import poplib
import smtplib
import string, random
from io import StringIO
import email
import logging
from email.mime.text import MIMEText

# POP3 Server (default: gmail)
SERVER_POP3 = "pop.gmail.com"
# SMTP Server
SERVER_SMTP = "smtp.gmail.com"
# USERNAME 
USER  = ""
# PASSWORD
PASSWORD = ""

if USER and PASSWORD:
    runFlag = 1
else:
    print("Username and password required. Exiting...")
    exit()

while runFlag:
    
    # connect to server
    logging.debug('connecting to ' + SERVER_POP3)
    server = poplib.POP3_SSL(SERVER_POP3)

    # log in
    logging.debug('log in')
    server.user(USER)
    server.pass_(PASSWORD)

    # list items on server
    # for gmail: it should list only unread messages once
    logging.debug('listing emails')
    resp, items, octets = server.list()
    index = len(items)
        
    # Check if there are unread messages
    if index:
        runFlag = 0
    else:
        continue
    
    # Latest e-mail
    raw_email  = b"\n".join(server.retr(index)[1])
    parsed_email = email.message_from_bytes(raw_email)

    # e-mail data
    oggetto = parsed_email['Subject']
    contenuto = parsed_email.get_payload()

    server.quit()
    logging.debug('connection closed')

# Set a filter on the e-mail subject (optional)
if oggetto != '[My Filter]':
    exit()    

# Set a filter on the sender (optional)
#if parsed_email['From'] != 'foo.bar@test.com':
#  exit()

# Forward the (right) e-mail!
# SMTP connection
server = smtplib.SMTP_SSL(SERVER_SMTP, 465)
server.login(USER,PASSWORD)
server.set_debuglevel(1)

# SEND TO
# Uncomment only one of the following options
# Send to a single recepient...
#TO = "dest1@example.com"
# ... or send to a list
TO = ['dest2@example.com', 
'dest3@example.com', 
'dest4@example.com'] 

# Prepare the content
msg = MIMEText(contenuto)

# Add the subject
msg['Subject'] = oggetto
msg['To'] = ", ".join(TO)

# Send the e-mail
server.sendmail(USER, TO, msg.as_string())

# Close connection
server.quit()
