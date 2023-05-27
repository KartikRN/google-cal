from django.shortcuts import render,HttpResponse,redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import Calender
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from .serializers import GoogleSocialAuthSerializer,Calender

# Create your views here.
SCOPES = ['https://www.googleapis.com/auth/calendar']

global creds
def GoogleCalendarInitView(request):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    pickle.dump(creds,open('token.pkl','wb'))
    return HttpResponse(creds,"login successful")


'''class GoogleCalendarRedirectView(GenericAPIView):
    serializer_class = Calender
    def get(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)'''

def GoogleCalendarRedirectView(request):
    creds=pickle.load(open('token.pkl','rb'))
    service = build('calendar', 'v3', credentials=creds)
    result = service.calendarList().list().execute()
    return HttpResponse(result['items'])