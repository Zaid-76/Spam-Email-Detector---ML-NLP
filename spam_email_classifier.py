# install the required libraries as mentioned below

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import base64
import joblib

# --- Gmail API Functions (No changes needed) ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # to define the access type(read,write,send,modify emails)


def get_gmail_service():
    """Authenticates and returns the Gmail service object."""
    # Authenticates only once by accepting the email address and consent and saves the credentials in token.pickle file
    # for future use
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: # Tokens change periodically
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def classify_recent_emails(classifier, cv):
    """
    Fetches the first 15 emails from the user's inbox and classifies them
    using a pre-trained model and CountVectorizer from our model_training.py file.
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=15).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found in your inbox.")
            return

        print("--- Classifying your 15 most recent emails ---")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

            email_body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        email_body = part['body']['data']
                        break
            elif 'body' in msg['payload'] and 'data' in msg['payload']['body']:
                email_body = msg['payload']['body']['data']

            if email_body:
                decoded_body = base64.urlsafe_b64decode(email_body).decode('utf-8') #  Used to decode the base64-encoded
                                                                                    # email body content retrieved from
                                                                                    # the Gmail API.
                email_vector = cv.transform([decoded_body]).toarray() # Count vectorizing process
                prediction = classifier.predict(email_vector) # Classification Process

                subject = "No Subject"
                for header in msg['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value'] # for displaying the subject instead of entire email body for formatted
                                                  # output
                        break

                classification = "SPAM" if prediction == 1 else "NOT SPAM" # The classification part
                print(f"Subject: {subject} -> Classification: {classification}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Load the pre trainined models
loaded_classifier = joblib.load('classifier.joblib')
loaded_cv = joblib.load('vectorizer.joblib')
# Now, call the function with the loaded objects
classify_recent_emails(loaded_classifier, loaded_cv)