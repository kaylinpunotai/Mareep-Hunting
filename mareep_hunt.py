# This script is scheduled to run on my RaspberryPi twice a day at 6am and 6pm CT. It uses 
# SerpAPI's Google Shopping search to check if the 45in Mareep plush is in stock at the Pokemon 
# Center website. If it's in stock, it will send me an email alert along with the link to the
# product page. Otherwise, it will only send me out of stock alerts on Sundays so that I can 
# monitor that it is still running correctly.


debug = False

from serpapi import GoogleSearch
import json, os, sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Send gmail alert to myself
def send_email(subject, body, sender, recipient, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipient, msg.as_string())
    smtp_server.quit()

# Request Google Shopping search for 'mareep' with seller filter 'pokemoncenter.com'
## url='https://www.google.com/search?tbm=shop&q=mareep&tbs=merchagg:m102878435'
today = datetime.now().weekday()
shopping_results = []
products = []
params = {
    'q': 'mareep',
    'tbm': 'shop',
    'location': 'Chicago',
    'hl': 'en',
    'gl': 'us',
    'tbs': 'merchagg:m102878435',
    'api_key': os.environ['serpapi_key'],
}

if debug:
    f = open('results_example.json')
    shopping_results = json.load(f)

else:
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results['shopping_results']

# Check if the desired product is available
for entry in shopping_results:
    product = entry['title']
    products.append(product)
    if '45' in product:
        # If in stock, send out an email alert with link and exit script
        link = entry['link']
        subject = 'Mareep alert!!'
        body = 'Mareep is in stock now!\n\n%s' % link
        send_email(subject, body, os.environ['sender'], os.environ['recipient'], os.environ['password'])
        sys.exit()
if today == 6: # send out out of stock notices on Sundays
    subject = 'Not in stock 😔'
    body = '\n'.join(products)
    send_email(subject, body, os.environ['sender'], os.environ['recipient'], os.environ['password'])
sys.exit()