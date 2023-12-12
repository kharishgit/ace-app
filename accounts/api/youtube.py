from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth import exceptions
import os

def upload_video_to_youtube(file_path, video_title, video_description):
    # Set up the YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"  # Path to your client secrets JSON file
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    try:
        # Build the YouTube API client
        youtube = build(api_service_name, api_version, credentials=None)

        # Get the credentials from the client secrets file
        credentials = youtube.client_secrets.from_client_secrets_file(client_secrets_file, scopes=scopes)

        # Check if the credentials are expired and refresh if necessary
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except exceptions.RefreshError:
                pass

        # Set the access token for the YouTube API client
        youtube = build(api_service_name, api_version, credentials=credentials)

        # Upload the video
        request_body = {
            "snippet": {
                "title": video_title,
                "description": video_description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        media_file = MediaFileUpload(file_path)

        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()

        # Return the video URL
        video_url = f"https://www.youtube.com/watch?v={response['id']}"
        return {
            "message": "Video upload complete",
            "link": video_url
        }
    except Exception as e:
        return {"error": str(e)}
