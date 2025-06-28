import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set the scope to access Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

#  Authenticate and return calendar service
def get_calendar_service():
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # Load credentials from token or ask user
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

# Book a new meeting
def book_meeting(summary, start_time_str, duration_minutes=30):
    service = get_calendar_service()

    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return {
        "message": f" Meeting booked!\n[View in Google Calendar]({created_event.get('htmlLink')})"
    }

# Check if time is free before booking
def check_availability(start_time_str, duration_minutes=30):
    service = get_calendar_service()

    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat() + "Z",
        timeMax=end_time.isoformat() + "Z",
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if events:
        return False, events  # Time is busy
    else:
        return True, None     # Time is available
