import os
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

import openpyxl
from openpyxl import Workbook

CATEGORIA_PADRAO = 22 # Categoria "Pessoas e blogs"

def upload_video(youtube, video_file_path, title, description, tags, privacy_status):

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            "tags": tags,
            'categoryId': CATEGORIA_PADRAO,
        },
        "status": {
            'privacyStatus': privacy_status
        }
    }

    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {int(status.progress() * 100)}%")
        
        # Define the file name
        file_name = "video_urls.xlsx"

        # Try to load an existing workbook, or create a new one
        try:
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active
        except FileNotFoundError:
            wb = Workbook()
            ws = wb.active
            ws.append(["Video URLs"])  # Add a header row

        # Append the new URL
        url = f"https://www.youtube.com/watch?v={response['id']}"
        ws.append([url])

        # Save the workbook
        wb.save(file_name)

        print(f"Video {title} Uploaded, URL: https://www.youtube.com/watch?v={response['id']}")


def upload_multiple_videos(youtube, video_paths, is_title_filename ,title, description, tags, privacy_status):
    
    video_names = [os.path.basename(video) for video in video_paths]

    for i, video in enumerate(video_names):
        upload_video(
            youtube,
            video_file_path=video_paths[i],
            title=video if is_title_filename else title + f" {i+1}",
            description=description,
            tags=tags,
            privacy_status=privacy_status
        )

        print(text=f"{i+1}/{len(video_names)} vídeos publicados")