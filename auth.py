import os
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

def authenticate_youtube(client_json_path):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if client_json_path:
        client = client_json_path 
    else:
        try:
            client = os.path.join(os.path.dirname(__file__), 'client.json')
        except:
            print("client.json not found")
            return


    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client,
        ['https://www.googleapis.com/auth/youtube.upload']
    )

    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', credentials=credentials
    )

    return youtube