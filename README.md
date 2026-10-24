# YouTube Auto Uploader

A small desktop app that uploads a batch of videos to your YouTube channel in one go. Pick your Google OAuth client file, pick the videos, set a title, description, tags and privacy, and click upload. The URLs of the uploaded videos are saved to `video_urls.xlsx`.

<img width="795" alt="The uploader window" src="https://github.com/user-attachments/assets/3980aac1-c982-4a23-82ca-f3711339f1b7" />

## Features

- **OAuth 2.0 sign-in** through the browser. No passwords stored.
- **Batch uploads.** Select many files at once; each is uploaded in resumable chunks.
- **Titles from filenames** or one fixed title for the whole batch.
- **Shared metadata.** Description, tags and privacy (public, unlisted, private) apply to every video in the batch.
- **Spreadsheet of results.** Every upload appends a row with the video URL.

## Setup

1. In [Google Cloud Console](https://console.cloud.google.com/), create a project, enable the **YouTube Data API v3**, and create an **OAuth client ID** of type Desktop app. Download its JSON.
2. Install and run:

```bash
pip install -r requirements.txt
python run.py
```

3. In the window, choose the JSON you downloaded, choose the videos, fill in the fields and click upload. A browser tab opens for you to approve the YouTube permission.

The interface is in Portuguese.

## Quota

The YouTube API gives each project 10,000 units per day and an upload costs about 1,600, so expect around six uploads a day unless you request a higher quota.

## Build a standalone app

```bash
pyinstaller run.spec
```

The executable lands in `dist/`.

## License

MIT.
