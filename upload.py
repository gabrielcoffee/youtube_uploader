import os
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

from googleapiclient.errors import HttpError
import googleapiclient.http
import json

import openpyxl
from openpyxl import Workbook

CATEGORIA_PADRAO = 22 # Categoria "Pessoas e blogs"

def upload_video(youtube, video_file_path, title, description, tags, privacy_status):
    # Vídeo data and information
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

    # Try uploeads
    try:
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=googleapiclient.http.MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        )

        # Upload the video, response is None when it's finished
        response = None
        while response is None:
            status, response = request.next_chunk()

        # Define the file name
        file_name = "video_urls.xlsx"

        try:
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active
        except FileNotFoundError:
            wb = Workbook()
            ws = wb.active
            ws.append(["Titulo do Video", "Video URL"])  # Cabeçalho

        # Append the new URL
        url = f"https://www.youtube.com/watch?v={response['id']}"
        ws.append([title, url])
        wb.save(file_name)

        print(f"Video {title} Publicado, URL: {url}")
        return 'success'

    # Handling errors:
    except HttpError as e:
        error_content = e.content.decode("utf-8")
        error_data = json.loads(error_content)
        reason = error_data['error']['errors'][0]['reason']

        print(f"Erro da API ({reason}): {error_data['error']['message']}")
        return 'quota'

    except Exception as e:
        print("Erro inesperado durante o upload, mostrar erro ao desenvolvedor:", str(e))
        return 'error'


def upload_multiple_videos(youtube, video_paths, is_title_filename, title, description, tags, privacy_status):
    # remove base path and extension from titles and leave only the file name
    video_names = [os.path.splitext(os.path.basename(video_path))[0] for video_path in video_paths]
    published = 0

    for i, video in enumerate(video_names):
        video_title = video if is_title_filename else title + f" {i+1}"

        print(f"Publicando vídeo {i+1}: {video_title}...")
        
        result =  upload_video(
            youtube,
            video_file_path=video_paths[i],
            title=video_title,
            description=description,
            tags=tags,
            privacy_status=privacy_status
        )

        if result == 'success':
            print(f"{i+1}/{len(video_names)} vídeos publicados\n")
            published += 1
        elif result == 'quota':
            print("Limite de cota da API atingido. Encerrando o publicações.")
            break
        elif result == 'error':
            print("Erro inesperado. Continuando com outros uploads.")
    
    print(f"\nPublicações concluídas. Total: {published} vídeos publicados.")