import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework import serializers


class Calender(serializers.Serializer):
    creds=pickle.load(open('token.pkl','rb'))
    service = build('calendar', 'v3', credentials=creds)
    result = service.calendarList().list().execute()
    calender_list=result['items']