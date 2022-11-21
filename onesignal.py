import requests
import os

def send_email(email_address, text):

    url = "https://onesignal.com/api/v1/notifications"

    payload = {
        "include_email_tokens":[email_address],
        "email_subject": "Your daily boost",
        "email_body": text,
         "app_id": "b5b11918-7ef8-45e9-9d6e-c0b6b0110d33",
        "name": "INTERNAL_CAMPAIGN_NAME"
        }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic " + os.getenv("ONESIGNAL_API_KEY"),
        "content-type": "application/json"
        }

    requests.post(url, json=payload, headers=headers)

   

